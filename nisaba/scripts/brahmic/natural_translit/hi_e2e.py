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
import nisaba.scripts.brahmic.natural_translit.iso2typ as iso
import nisaba.scripts.brahmic.natural_translit.phon_ops as ops
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.txn2ipa as ipa
import nisaba.scripts.brahmic.natural_translit.txn2nat as txn
import nisaba.scripts.brahmic.natural_translit.typ2txn as typ

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

_PROCESS_SCHWA = ops.process_schwa(_ONSET_CL, _CODA_CL)


def _iso_to_txn() -> p.Fst:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return (iso.iso_to_typ() @
          typ.TYP_TO_TXN @
          typ.A_TO_EC @
          ops.VOCALIC_I @
          ops.ANUSVARA_ASSIMILATION @
          _PROCESS_SCHWA @
          ops.SCHWA_EC @
          ops.DEFAULT_ANUSVARA_DENTAL @
          ops.FINAL_ANUSVARA_NASALIZATION @
          ops.JNY_TO_GY).optimize()


def iso_to_psaf() -> p.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (_iso_to_txn() @ txn.TXN_TO_PSAF).optimize()


def iso_to_psac() -> p.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (_iso_to_txn() @ txn.TXN_TO_PSAC).optimize()


def iso_to_ipa() -> p.Fst:
  """Pronunciation in IPA."""
  return (_iso_to_txn() @ ipa.txn_to_ipa()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_IPA'] = iso_to_ipa()


if __name__ == '__main__':
  multi_grm.run(generator_main)
