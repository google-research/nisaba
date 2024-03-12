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

"""Grammar parameters for Ta."""

from nisaba.scripts.natural_translit.brahmic import derom_inventory as derom
from nisaba.scripts.natural_translit.brahmic import deromanizer
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import txn2ipa
from nisaba.scripts.natural_translit.phonology.operations import voicing
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl

drm = derom.DEROMANIZATION_INVENTORY

deromanize = deromanizer.Deromanizer.params(
    script='taml',
    monophthong=(drm.a, drm.e, drm.i, drm.o, drm.u),
    diphthong=(drm.ai, drm.au, drm.ae_ee, drm.oa_oo),
    drops_aspirated=(
        drm.b_p, drm.ch, drm.d_t, drm.g_k, drm.j, drm.k, drm.p, drm.t
    ),
    no_aspirated=(
        drm.c, drm.h, drm.l, drm.m, drm.n, drm.q, drm.r, drm.s,
        drm.sh, drm.v, drm.w, drm.x, drm.y, drm.zh_lr
    ),
    only_geminated=(drm.tr_rr),
    foreign=(drm.f, drm.z),
)

ph = psa.PHONEME_INVENTORY

_VOICING_OP = [
    voicing.K_G,
    voicing.P_B,
    voicing.T_D,
    voicing.TI_DI,
    voicing.TT_DD,
    voicing.TSH_S,
]
_VOICING_CONTEXT = fl.FstList(
    ph.VOWEL, ph.APPROXIMANT, ph.NASAL, ph.RHOTIC
).union_opt()
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

_TXN_OPS = fl.FstList(
    iso2txn_ops.VOCALIC_EC,
    iso2txn_ops.SCHWA_A,
    iso2txn_ops.ANUSVARA_ASSIMILATION,
    iso2txn_ops.DEFAULT_ANUSVARA_LABIAL,
    iso2txn_ops.RR_TT,
    iso2txn_ops.NR_NDR,
    _NY_TSH,
    _VOICING,
    _C_WI,
    iso2txn_ops.JNY_TO_NY,
)

_NAT_OPS = fl.FstList(
    iso2ltn_ops.EN_LIKE_LONG,
    iso2ltn_ops.EE_AE,
    iso2ltn_ops.OO_OA,
    iso2ltn_ops.TI_TH,
    iso2ltn_ops.TT_TR,
    iso2ltn_ops.CC_TO_CCH,
    iso2ltn_ops.CCH_TO_CHH,
    iso2ltn_ops.S_SHSH_TO_SSH,
    iso2ltn_ops.SIBV_TO_SIBW,
    iso2ltn_ops.NY_N,
    iso2ltn_ops.NY_GN,
)


def iso_to_psaf() -> fl.FstList:
  """Pan-South Asian fine grained transliteration."""
  return fl.FstList(
      iso2txn.iso_to_txn(),
      _TXN_OPS,
      iso2ltn_ops.VOCALIC_TR_I,
      iso2ltn_ops.TXN_TO_PSAF,
  )


def iso_to_psac() -> fl.FstList:
  """Pan-South Asian coarse grained transliteration."""
  return fl.FstList(iso2txn.iso_to_txn(), _TXN_OPS, iso2ltn_ops.TXN_TO_PSAC)


def iso_to_nat() -> fl.FstList:
  """Tamil natural transliteration."""
  return fl.FstList(
      iso2txn.iso_to_txn(),
      _TXN_OPS,
      _NAT_OPS,
      iso2ltn_ops.TXN_TO_PSA_COMMON,
      iso2ltn_ops.TRANSLIT_BY_PSA,
      ltn.print_only_ltn(),
  )


def iso_to_ipa() -> fl.FstList:
  """Pronunciation in IPA."""
  return fl.FstList(iso2txn.iso_to_txn(), _TXN_OPS, txn2ipa.txn_to_ipa())
