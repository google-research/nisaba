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

import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
from nisaba.scripts.natural_translit.brahmic.acronym import typ2acr
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.phonology import txn2ipa
from nisaba.scripts.natural_translit.phonology import txn2ltn
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import list_op as ls

_ONSET_CL = ls.union_opt(
    cc.concat_r(ph.K, ph.SH),
    cc.concat_r(ph.S, ls.union_opt(ph.T, ph.RT, ph.NI, ph.Y, ph.VU)),
    cc.concat_r(ls.union_opt(ph.VU, ph.NI), ph.Y),
    cc.concat_r(ls.union_opt(ph.K, ph.P, ph.G, ph.DI, ph.SH), ph.RT)
)


_CODA_CL = ls.union_opt(
    cc.concat_r(ph.CONSONANT, ph.STOP),
    cc.concat_r(ph.VOICED, ph.NASAL),
    cc.concat_r((ph.FRICATIVE - ph.H), (ph.NASAL - ph.M)),
    cc.concat_r(ph.SIBILANT, ph.M),
    cc.concat_r(ls.union_opt(ph.LIQUID, ph.NASAL), ph.NASAL),
    cc.concat_r(ph.RHOTIC, ph.RHOTIC)
)

_PROCESS_SCHWA = iso2txn_ops.process_schwa(_ONSET_CL, _CODA_CL)


_TXN_OPS = (
    iso2txn_ops.AI_TO_EH_L @
    iso2txn_ops.AU_TO_OH_L @
    iso2txn_ops.A_TO_EC @
    iso2txn_ops.VOCALIC_I @
    iso2txn_ops.ANUSVARA_ASSIMILATION @
    _PROCESS_SCHWA @
    iso2txn_ops.SCHWA_EC @
    iso2txn_ops.DEFAULT_ANUSVARA_DENTAL @
    iso2txn_ops.FINAL_ANUSVARA_NASALIZATION @
    iso2txn_ops.JNY_TO_GY @
    iso2txn_ops.PHPH_TO_FF
).optimize()


def _iso_to_txn() -> pyn.Fst:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return (iso2txn.iso_to_txn() @ _TXN_OPS).optimize()


def iso_to_psaf() -> pyn.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAF).optimize()


def iso_to_psac() -> pyn.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAC).optimize()


def iso_to_ipa() -> pyn.Fst:
  """Pronunciation in IPA."""
  return (_iso_to_txn() @ txn2ipa.txn_to_ipa()).optimize()


def iso_to_nat() -> pyn.Fst:
  """Natural transliteration."""
  return (iso2txn.iso_to_txn() @
          typ2acr.HI_ACR_TYP_TO_TR @
          _TXN_OPS @
          iso2ltn_ops.SIBV_TO_SIBW @
          iso2ltn_ops.AA_WI @
          iso2ltn_ops.TXN_TO_PSA_COMMON @
          txn2ltn.MAP_VOWEL_IGNORE_LENGTH @
          iso2ltn_ops.CC_TO_CCH @
          iso2ltn_ops.CCH_TO_CHH @
          iso2ltn_ops.S_SHSH_TO_SSH @
          ltn.print_only_ltn()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_IPA'] = iso_to_ipa()
      exporter['ISO_TO_NAT'] = iso_to_nat()


if __name__ == '__main__':
  multi_grm.run(generator_main)
