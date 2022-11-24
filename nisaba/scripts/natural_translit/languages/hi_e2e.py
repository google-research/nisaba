# Copyright 2022 Nisaba Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""End-to-end natural transliteration for Hindi."""

import pynini as p
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
import nisaba.scripts.natural_translit.common.rewrite_functions as rw
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.phonology import txn2ipa
from nisaba.scripts.natural_translit.phonology import txn2ltn

_ONSET_CL = p.union(
    rw.concat_r(
        ph.K,
        ph.SH),
    rw.concat_r(
        ph.S,
        p.union(ph.T + ph.ASP.ques, ph.RT, ph.NI, ph.Y, ph.VU).optimize()),
    rw.concat_r(
        p.union(ph.VU, ph.NI),
        ph.Y),
    rw.concat_r(
        p.union(ph.K, ph.P, ph.G, ph.DI, ph.SH).optimize(),
        ph.RT)
    ).optimize()


_CODA_CL = p.union(
    rw.concat_r(
        ph.CONSONANT,
        ph.STOP
    ),
    rw.concat_r(ph.VOICED,
                ph.NASAL),
    rw.concat_r(
        p.difference(ph.FRICATIVE, ph.H),
        p.difference(ph.NASAL, ph.M)),
    rw.concat_r(
        ph.SIBILANT,
        ph.M),
    rw.concat_r(
        p.union(ph.LIQUID, ph.NASAL),
        ph.NASAL),
    rw.concat_r(
        ph.RHOTIC,
        ph.RHOTIC)
    ).optimize()

_PROCESS_SCHWA = iso2txn_ops.process_schwa(_ONSET_CL, _CODA_CL)


def _iso_to_txn() -> p.Fst:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return (iso2txn.iso_to_txn() @
          iso2txn_ops.A_TO_EC @
          iso2txn_ops.VOCALIC_I @
          iso2txn_ops.ANUSVARA_ASSIMILATION @
          _PROCESS_SCHWA @
          iso2txn_ops.SCHWA_EC @
          iso2txn_ops.DEFAULT_ANUSVARA_DENTAL @
          iso2txn_ops.FINAL_ANUSVARA_NASALIZATION @
          iso2txn_ops.JNY_TO_GY @
          iso2txn_ops.PHPH_TO_FF).optimize()


def iso_to_psaf() -> p.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAF).optimize()


def iso_to_psac() -> p.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAC).optimize()


def iso_to_ipa() -> p.Fst:
  """Pronunciation in IPA."""
  return (_iso_to_txn() @ txn2ipa.txn_to_ipa()).optimize()


def iso_to_nat() -> p.Fst:
  """Natural transliteration."""
  return (_iso_to_txn() @
          iso2ltn_ops.SIBV_TO_SIBW @
          iso2ltn_ops.AA_WI @
          iso2ltn_ops.TXN_TO_PSA_COMMON @
          txn2ltn.MAP_VOWEL_IGNORE_LENGTH @
          iso2ltn_ops.CC_TO_CCH @
          iso2ltn_ops.CCH_TO_CHH @
          iso2ltn_ops.SSSS_TO_SSH @
          iso2ltn_ops.SHSH_TO_SSH @
          txn2ltn.STRIP).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_IPA'] = iso_to_ipa()
      exporter['ISO_TO_NAT'] = iso_to_nat()


if __name__ == '__main__':
  multi_grm.run(generator_main)
