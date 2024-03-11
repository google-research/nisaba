# Copyright 2024 Nisaba Authors.
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
"""End-to-end natural transliteration for Malayalam."""

import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import txn2ipa
from nisaba.scripts.natural_translit.phonology.operations import voicing
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

ph = psa.PHONEME_INVENTORY

_VOICING_OP = [
    voicing.K_G,
    voicing.P_B,
    voicing.T_D,
    voicing.TI_DI,
    voicing.TT_DD,
    voicing.TSH_S,
]
_VOICING_CONTEXT = ls.union_opt(ph.VOWEL, ph.APPROXIMANT, ph.NASAL, ph.RHOTIC)
_VOICING = voicing.voicing(
    _VOICING_OP,
    _VOICING_CONTEXT,
    _VOICING_CONTEXT,
)
_C_WI = voicing.voicing(
    [voicing.TSH_S],
    al.BOS,
    _VOICING_CONTEXT,
)
_NY_TSH = voicing.voicing(
    [voicing.TSH_DZH],
    ph.NY,
    _VOICING_CONTEXT,
)

_TXN_OPS = (
    iso2txn_ops.VOCALIC_EC
    @ iso2txn_ops.SCHWA_A
    @ iso2txn_ops.ANUSVARA_ASSIMILATION
    @ iso2txn_ops.DEFAULT_ANUSVARA_LABIAL
    @ iso2txn_ops.RR_TT
    @ iso2txn_ops.NR_NDR
    @ _NY_TSH
    @ _VOICING
    @ _C_WI
    @ iso2txn_ops.JNY_TO_NY
).optimize()

_NAT_OPS = (
    iso2ltn_ops.EN_LIKE_LONG
    @ iso2ltn_ops.EE_AE
    @ iso2ltn_ops.OO_OA
    @ iso2ltn_ops.TI_TH
    @ iso2ltn_ops.TT_TR
    @ iso2ltn_ops.CC_TO_CCH
    @ iso2ltn_ops.CCH_TO_CHH
    @ iso2ltn_ops.S_SHSH_TO_SSH
    @ iso2ltn_ops.SIBV_TO_SIBW
    @ iso2ltn_ops.NY_N
    @ iso2ltn_ops.NY_GN
).optimize()


def iso_to_psaf() -> pyn.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (
      iso2txn.iso_to_txn()
      @ _TXN_OPS
      @ iso2ltn_ops.VOCALIC_TR_I
      @ iso2ltn_ops.TXN_TO_PSAF
  ).optimize()


def iso_to_psac() -> pyn.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (iso2txn.iso_to_txn() @ _TXN_OPS @ iso2ltn_ops.TXN_TO_PSAC).optimize()


def iso_to_nat() -> pyn.Fst:
  """Tamil natural transliteration."""
  return (
      iso2txn.iso_to_txn()
      @ _TXN_OPS
      @ _NAT_OPS
      @ iso2ltn_ops.TXN_TO_PSA_COMMON
      @ iso2ltn_ops.TRANSLIT_BY_PSA
      @ ltn.print_only_ltn()
  ).optimize()


def iso_to_ipa() -> pyn.Fst:
  """Pronunciation in IPA."""
  return (iso2txn.iso_to_txn() @ _TXN_OPS @ txn2ipa.txn_to_ipa()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration for Malayalam."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_NAT'] = iso_to_nat()
      exporter['ISO_TO_IPA'] = iso_to_ipa()


if __name__ == '__main__':
  multi_grm.run(generator_main)
