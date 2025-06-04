# Copyright 2025 Nisaba Authors.
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

"""Grammar parameters for Gujarati."""

from nisaba.scripts.natural_translit.brahmic import g2p
from nisaba.scripts.natural_translit.brahmic import phoneme_inventory as psa
from nisaba.scripts.natural_translit.brahmic import romanizer
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import transcriptor
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import fst_list as fl


ph = psa.PHONEME_INVENTORY

_ONSET_CL = fl.FstList(
    cc.concat_r(ph.K, ph.SH),
    cc.concat_r(ph.S, (ph.T | ph.RT | ph.NI | ph.Y | ph.VU)),
    cc.concat_r((ph.VU | ph.NI), ph.Y),
    cc.concat_r((ph.K | ph.P | ph.G | ph.DI | ph.SH), ph.RT),
).union_opt()


_CODA_CL = fl.FstList(
    cc.concat_r(ph.CONSONANT, ph.STOP),
    cc.concat_r(ph.VOICED, ph.NASAL),
    cc.concat_r((ph.FRICATIVE - ph.H), (ph.NASAL - ph.M)),
    cc.concat_r(ph.SIBILANT, ph.M),
    cc.concat_r((ph.LIQUID | ph.NASAL), ph.NASAL),
    cc.concat_r(ph.RHOTIC, ph.RHOTIC),
).union_opt()

_PROCESS_SCHWA = g2p.process_schwa(_ONSET_CL, _CODA_CL)


_TXN_OPS = fl.FstList(
    g2p.A_TO_EC,
    g2p.VOCALIC_U,
    g2p.ANUSVARA_ASSIMILATION,
    _PROCESS_SCHWA,
    g2p.SCHWA_EC,
    g2p.DEFAULT_ANUSVARA_DENTAL,
    g2p.JNY_TO_DNY,
    g2p.PH_F,
)

_NAT_OPS = fl.FstList(
    romanizer.SIBV_TO_SIBW,
    romanizer.OO_AO_BEFORE_ANUSVARA,
    romanizer.GAAV_GAON,
    romanizer.TXN_TO_PSA_COMMON,
    romanizer.IGNORE_LONG,
    romanizer.TRANSLIT_BY_PSA,
    romanizer.CC_TO_CCH,
    romanizer.CCH_TO_CHH,
    romanizer.S_SHSH_TO_SSH,
)


def _iso_to_txn() -> fl.FstList:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return fl.FstList(g2p.iso_to_txn(), _TXN_OPS)


def iso_to_psaf() -> fl.FstList:
  """Pan-South Asian fine grained transliteration."""
  return fl.FstList(_iso_to_txn(), romanizer.TXN_TO_PSAF)


def iso_to_psac() -> fl.FstList:
  """Pan-South Asian coarse grained transliteration."""
  return fl.FstList(_iso_to_txn(), romanizer.TXN_TO_PSAC)


def iso_to_ipa() -> fl.FstList:
  """Pronunciation in IPA."""
  return fl.FstList(_iso_to_txn(), transcriptor.txn_to_ipa())


def iso_to_nat() -> fl.FstList:
  """Natural transliteration."""
  return fl.FstList(
      g2p.iso_to_txn(),
      _TXN_OPS,
      _NAT_OPS,
      ltn.print_only_ltn(),
  )
