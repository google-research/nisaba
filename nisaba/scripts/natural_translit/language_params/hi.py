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

"""Grammar parameters for Hi."""

from nisaba.scripts.natural_translit.brahmic import acronym
from nisaba.scripts.natural_translit.brahmic import derom_inventory as derom
from nisaba.scripts.natural_translit.brahmic import deromanizer
from nisaba.scripts.natural_translit.brahmic import g2p
from nisaba.scripts.natural_translit.brahmic import phoneme_inventory as psa
from nisaba.scripts.natural_translit.brahmic import romanizer
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import transcriptor
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import fst_list as fl


drm = derom.DEROMANIZATION_INVENTORY

deromanize = deromanizer.Deromanizer.params(
    script='deva',
    schwa_deletion=True,
    schwa_deletion_wf=True,
    monophthong=(drm.a, drm.e, drm.i, drm.o, drm.u),
    always_long_vowel=(drm.e, drm.o),
    diphthong=(drm.ai, drm.au),
    has_aspirated=(drm.b, drm.ch, drm.d, drm.g, drm.j, drm.k, drm.p, drm.t),
    no_aspirated=(
        drm.c, drm.h, drm.l, drm.m, drm.n, drm.q,
        drm.r, drm.s, drm.sh, drm.v, drm.w, drm.x, drm.y,
    ),
    foreign=(drm.f, drm.z),
    anusvara_n=True,
    nasal_assimilation=True,
)

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
    g2p.AI_TO_EH_LONG,
    g2p.AU_TO_OH_LONG,
    g2p.A_TO_EC,
    g2p.VOCALIC_I,
    g2p.ANUSVARA_ASSIMILATION,
    _PROCESS_SCHWA,
    g2p.SCHWA_EC,
    g2p.DEFAULT_ANUSVARA_DENTAL,
    g2p.FINAL_ANUSVARA_NASALIZATION,
    g2p.JNY_TO_GY,
    g2p.PHPH_TO_FF,
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
      acronym.HI_ACR_TYP_TO_TR,
      _TXN_OPS,
      romanizer.SIBV_TO_SIBW,
      romanizer.AA_WI,
      romanizer.TXN_TO_PSA_COMMON,
      romanizer.IGNORE_LONG,
      romanizer.TRANSLIT_BY_PSA,
      romanizer.CC_TO_CCH,
      romanizer.CCH_TO_CHH,
      romanizer.S_SHSH_TO_SSH,
      ltn.print_only_ltn(),
  )
