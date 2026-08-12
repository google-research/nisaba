# Copyright 2026 Nisaba Authors.
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

"""Brahmic romanization rules."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import grapheme_inventory as iso
from nisaba.scripts.natural_translit.brahmic import phoneme_inventory as psa
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

gr = iso.GRAPHEME_INVENTORY
tr = ltn.TRANSLIT_INVENTORY
ph = psa.PHONEME_INVENTORY

## Rules to apply before txn to ltn mappings

# <v> is "w" after {s}, {ss}, and {sh}.
SIBV_TO_SIBW = rw.rewrite(
    ph.VU,  # pyrefly: ignore[missing-attribute]
    tr.W,  # pyrefly: ignore[missing-attribute]
    ph.SIBILANT)  # pyrefly: ignore[missing-attribute]


# Palatal and velar assimilated anusvara is transliterated as "n".
NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,  # pyrefly: ignore[missing-attribute]
    fl.FstList(ph.NG, ph.NY).union_opt(),  # pyrefly: ignore[missing-attribute]
    tr.N)  # pyrefly: ignore[missing-attribute]

NYJ_NJ = rw.rewrite(ph.NY, tr.N, following=ph.D_ZH)  # pyrefly: ignore[missing-attribute]

GAAV_GAON = rw.merge(
    gr.AA, ph.A + ph.DURH, gr.V, ph.VU, tr.A + tr.O + tr.N,  # pyrefly: ignore[missing-attribute]
    gr.G  # pyrefly: ignore[missing-attribute]
)
OO_AO_BEFORE_ANUSVARA = rw.reassign(
    gr.OO, ph.O + ph.DURH, tr.A + tr.O, following=gr.ANS  # pyrefly: ignore[missing-attribute]
)

AE_A = rw.rewrite(ph.AE, tr.A)  # pyrefly: ignore[missing-attribute]
OH_A = rw.reassign(gr.A, ph.OH, tr.A)  # pyrefly: ignore[missing-attribute]

AA_AO_CND = rw.reassign(
    gr.AA, ph.A + ph.DURH,  # pyrefly: ignore[missing-attribute]
    tr.A + tr.O,  # pyrefly: ignore[missing-attribute]
    following=(gr.CND + (al.SKIP + gr.OO).ques + al.SKIP + al.EOW)  # pyrefly: ignore[missing-attribute]
)
WF_CND_OO = rw.reassign_word_final(
    gr.OO, ph.O + ph.DURH, tr.DEL, preceding=gr.CND  # pyrefly: ignore[missing-attribute]
)

OOYY_W = rw.reassign(gr.OO_I + gr.YY, ph.VU, tr.W)  # pyrefly: ignore[missing-attribute]
IYY_I = rw.reassign(gr.YY, ph.Y, tr.DEL, (ph.I | ph.U) + ph.DURH.ques)  # pyrefly: ignore[missing-attribute]


def _transliterate_vocalic(
    vcl: pyn.FstLike,
    vcl_l: pyn.FstLike) -> pyn.Fst:
  """Transliterates all vowels in vocalics as vcl_tr."""
  return fl.FstList.make(
      rw.rewrite,
      (ph.SYL + ph.DURH, vcl_l, gr.VOCALIC),  # pyrefly: ignore[missing-attribute]
      (ph.VOWEL | ph.SYL, vcl, gr.VOCALIC),  # pyrefly: ignore[missing-attribute]
  ).compose()

VOCALIC_TR_I = _transliterate_vocalic(tr.I, tr.S_II)  # pyrefly: ignore[missing-attribute]

# Word initial <aa> is "aa".
AA_WI = rw.reassign_word_initial(
    gr.AA_I,  # pyrefly: ignore[missing-attribute]
    ph.A + ph.DURH,  # pyrefly: ignore[missing-attribute]
    tr.S_AA)  # pyrefly: ignore[missing-attribute]

EN_LIKE_LONG = fl.FstList.make(
    rw.rewrite,
    (ph.I + ph.DURH, tr.E + tr.E),  # pyrefly: ignore[missing-attribute]
    (ph.U + ph.DURH, tr.O + tr.O),  # pyrefly: ignore[missing-attribute]
).compose()

EE_AE = rw.reassign(gr.EE, ph.E + ph.DURH, tr.A + tr.E)  # pyrefly: ignore[missing-attribute]
OO_OA = rw.reassign(gr.OO, ph.O + ph.DURH, tr.O + tr.A, (ph.VU | ph.Y))  # pyrefly: ignore[missing-attribute]
OO_OA = fl.FstList.make(
    rw.reassign,
    (gr.OO, ph.O + ph.DURH, tr.O + tr.A, ph.APPROXIMANT),  # pyrefly: ignore[missing-attribute]
    (gr.OO, ph.O + ph.DURH, tr.O + tr.A, '', ph.APPROXIMANT)  # pyrefly: ignore[missing-attribute]
).compose()

TI_TH = fl.FstList(
    rw.merge_repeated_alignment(gr.T, ph.TI, tr.T + tr.H),  # pyrefly: ignore[missing-attribute]
    rw.reassign(gr.T, ph.TI, tr.T + tr.H),  # pyrefly: ignore[missing-attribute]
    rw.reassign(gr.T, ph.DI, tr.T + tr.H),  # pyrefly: ignore[missing-attribute]
).compose()

TT_TR = rw.reassign(gr.RR + gr.RR, ph.T + ph.T, tr.T + tr.T + tr.R)  # pyrefly: ignore[missing-attribute]
RD_R = rw.reassign(gr.RD, ph.RD, tr.R)  # pyrefly: ignore[missing-attribute]
RDH_DH = rw.reassign(gr.RDH, ph.RD + ph.ASP, tr.D + tr.H)  # pyrefly: ignore[missing-attribute]
RDH_RH = rw.reassign(gr.RDH, ph.RD + ph.ASP, tr.R + tr.H)  # pyrefly: ignore[missing-attribute]

NY_N = rw.rewrite(ph.NY, tr.N, following=ph.CONSONANT)  # pyrefly: ignore[missing-attribute]
NY_GN = rw.reassign(gr.NY, ph.NY, tr.G + tr.N, ph.VOWEL, ph.VOWEL)  # pyrefly: ignore[missing-attribute]

# Transliterate diphthong graphemes as diphthong instead of long vowel.

DIPHTHONG_GR = fl.FstList.make(
    rw.reassign,
    (gr.AI, ph.EH + ph.DURH, tr.S_AI),  # pyrefly: ignore[missing-attribute]
    (gr.AU, ph.OH + ph.DURH, tr.S_AU),  # pyrefly: ignore[missing-attribute]
    (gr.AI_I, ph.EH + ph.DURH, tr.S_AI),  # pyrefly: ignore[missing-attribute]
    (gr.AU_I, ph.OH + ph.DURH, tr.S_AU),  # pyrefly: ignore[missing-attribute]
).compose()


# Translit options for long phonemes
TRANSLIT_LONG = fl.FstList.make(
    rw.rewrite,
    *[
        (long.ph + ph.DURH, ltn.double_substring_tr(long.tr_dict['psa']))  # pyrefly: ignore[missing-attribute]
        for long in psa.PH
    ]
).compose()

IGNORE_LONG = rw.delete(ph.DURH)  # pyrefly: ignore[missing-attribute]

# Rules for natural translit of two-letter geminates.
# TODO: Revise and generalise all geminate rules.

# <c><c> is "cch"
CC_TO_CCH = rw.merge_repeated_alignment(gr.C, tr.S_CH, tr.C + tr.S_CH)  # pyrefly: ignore[missing-attribute]

# <c><ch> is "chh"
CCH_TO_CHH = rw.merge(
    gr.C, tr.S_CH,  # pyrefly: ignore[missing-attribute]
    gr.CH, tr.S_CH + tr.H,  # pyrefly: ignore[missing-attribute]
    tr.S_CH + tr.H)  # pyrefly: ignore[missing-attribute]

# Translit <sh><sh> and <ss><ss> as "ssh"
S_SHSH_TO_SSH = fl.FstList.make(
    rw.merge_repeated_alignment,
    (gr.SS, tr.S_SH, tr.S + tr.S_SH),  # pyrefly: ignore[missing-attribute]
    (gr.SH, tr.S_SH, tr.S + tr.S_SH),  # pyrefly: ignore[missing-attribute]
).compose()

TRANSLIT_BY_PSA = phon.ls_translit_by_key(psa.PHONEMES, 'psa')


# Compose common rules for romanization
TXN_TO_PSA_COMMON = (DIPHTHONG_GR @ NON_LABIAL_ANUSVARA @ RDH_DH)

# Convert txn to PSAF and outputs only translit strings.
TXN_TO_PSAF = (
    TXN_TO_PSA_COMMON @
    TRANSLIT_LONG @
    TRANSLIT_BY_PSA @
    ltn.print_only_ltn()
    ).optimize()

# Remove all repeated translit substrings in PSAC.
# TODO: This should be ph geminate removal + post tr cleanup.
REMOVE_REPEATED_LTN = fl.FstList(
    ltn.DEL_REPEATED_SUBSTRING, ltn.DEL_REPEATED_LOWER
).compose()


TXN_TO_PSAC = (
    TXN_TO_PSA_COMMON @
    IGNORE_LONG @
    TRANSLIT_BY_PSA @
    ltn.print_only_ltn() @
    REMOVE_REPEATED_LTN).optimize()
