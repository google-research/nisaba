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

"""Romanization rules that depend on iso graphemes."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.utils import rewrite as cmp

gr = iso.GRAPHEME_INVENTORY
tr = ltn.TRANSLIT_INVENTORY
ph = psa.PHONEME_INVENTORY

## Rules to apply before txn to ltn mappings

# <v> is "w" after {s}, {ss}, and {sh}.
SIBV_TO_SIBW = rw.rewrite(
    ph.VU,
    tr.W,
    ph.SIBILANT)


# Palatal and velar assimilated anusvara is transliterated as "n".
NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,
    ls.union_opt(ph.NG, ph.NY),
    tr.N)

NYJ_NJ = rw.rewrite(ph.NY, tr.N, following=ph.D_ZH)

GAAV_GAON = rw.merge(
    gr.AA, ph.A + ph.DURH, gr.V, ph.VU, tr.A + tr.O + tr.N,
    gr.G
)
OO_AO_BEFORE_ANUSVARA = rw.reassign(
    gr.OO, ph.O + ph.DURH, tr.A + tr.O, following=gr.ANS
)

AE_A = rw.rewrite(ph.AE, tr.A)
OH_A = rw.reassign(gr.A, ph.OH, tr.A)

AA_AO_CND = rw.reassign(
    gr.AA, ph.A + ph.DURH,
    tr.A + tr.O,
    following=(gr.CND + (al.SKIP + gr.OO).ques + al.SKIP + al.EOW)
)
WF_CND_OO = rw.reassign_word_final(
    gr.OO, ph.O + ph.DURH, tr.DEL, preceding=gr.CND
)

OOYY_W = rw.reassign(gr.OO_I + gr.YY, ph.VU, tr.W)
IYY_I = rw.reassign(gr.YY, ph.Y, tr.DEL, (ph.I | ph.U) + ph.DURH.ques)


def _transliterate_vocalic(
    vcl: pyn.FstLike,
    vcl_l: pyn.FstLike) -> pyn.Fst:
  """Transliterates all vowels in vocalics as vcl_tr."""
  long_syl = rw.rewrite(
      ph.SYL + ph.DURH,
      vcl_l,
      gr.VOCALIC)
  rest = rw.rewrite(
      ls.union_opt(ph.VOWEL, ph.SYL),
      vcl,
      gr.VOCALIC)
  return long_syl @ rest

VOCALIC_TR_I = _transliterate_vocalic(tr.I, tr.S_II)

# Word initial <aa> is "aa".
AA_WI = rw.reassign_word_initial(
    gr.AA_I,
    ph.A + ph.DURH,
    tr.S_AA)

EN_LIKE_LONG = cmp.ComposeFsts(ls.apply_foreach(rw.rewrite, [
    [ph.I + ph.DURH, tr.E + tr.E],
    [ph.U + ph.DURH, tr.O + tr.O],
    ]))

EE_AE = rw.reassign(gr.EE, ph.E + ph.DURH, tr.A + tr.E)
OO_OA = rw.reassign(gr.OO, ph.O + ph.DURH, tr.O + tr.A, (ph.VU | ph.Y))
OO_OA = cmp.ComposeFsts([
    rw.reassign(gr.OO, ph.O + ph.DURH, tr.O + tr.A, ph.APPROXIMANT),
    rw.reassign(gr.OO, ph.O + ph.DURH, tr.O + tr.A, following=ph.APPROXIMANT),
])


TI_TH = cmp.ComposeFsts([
    rw.merge_repeated_alignment(gr.T, ph.TI, tr.T + tr.H),
    rw.reassign(gr.T, ph.TI, tr.T + tr.H),
    rw.reassign(gr.T, ph.DI, tr.T + tr.H),
])

TT_TR = rw.reassign(gr.RR + gr.RR, ph.T + ph.T, tr.T + tr.T + tr.R)
RD_R = rw.reassign(gr.RD, ph.RD, tr.R)

NY_N = rw.rewrite(ph.NY, tr.N, following=ph.CONSONANT)
NY_GN = rw.reassign(gr.NY, ph.NY, tr.G + tr.N, ph.VOWEL, ph.VOWEL)

# Transliterate diphthong graphemes as diphthong instead of long vowel.

DIPHTHONG_GR = cmp.ComposeFsts(ls.apply_foreach(rw.reassign, [
    [gr.AI, ph.EH + ph.DURH, tr.S_AI],
    [gr.AU, ph.OH + ph.DURH, tr.S_AU],
    [gr.AI_I, ph.EH + ph.DURH, tr.S_AI],
    [gr.AU_I, ph.OH + ph.DURH, tr.S_AU],
]))


# Translit options for long phonemes
TRANSLIT_LONG = cmp.ComposeFsts(ls.apply_foreach(
    rw.rewrite,
    [[long.ph + ph.DURH, ltn.double_substring_tr(long.tr_dict['psa'])]
     for long in psa.PH],
))
IGNORE_LONG = rw.delete(ph.DURH)

# Rules for natural translit of two-letter geminates.
# TODO: Revise and generalise all geminate rules.

# <c><c> is "cch"
CC_TO_CCH = rw.merge_repeated_alignment(gr.C, tr.S_CH, tr.C + tr.S_CH)

# <c><ch> is "chh"
CCH_TO_CHH = rw.merge(
    gr.C, tr.S_CH,
    gr.CH, tr.S_CH + tr.H,
    tr.S_CH + tr.H)

# Translit <sh><sh> and <ss><ss> as "ssh"
S_SHSH_TO_SSH = cmp.ComposeFsts(ls.apply_foreach(rw.merge_repeated_alignment, [
    [gr.SS, tr.S_SH, tr.S + tr.S_SH],
    [gr.SH, tr.S_SH, tr.S + tr.S_SH],
]))

TRANSLIT_BY_PSA = phon.ls_translit_by_key(psa.PHONEMES, 'psa')


# Compose common rules for romanization
TXN_TO_PSA_COMMON = (DIPHTHONG_GR @ NON_LABIAL_ANUSVARA)

# Convert txn to PSAF and outputs only translit strings.
TXN_TO_PSAF = (
    TXN_TO_PSA_COMMON @
    TRANSLIT_LONG @
    TRANSLIT_BY_PSA @
    ltn.print_only_ltn()
    ).optimize()

# Remove all repeated translit substrings in PSAC.
# TODO: This should be ph geminate removal + post tr cleanup.
REMOVE_REPEATED_LTN = cmp.ComposeFsts(ls.apply_foreach(
    rw.rewrite_repeated,
    [[char.glyph] for char in ltn.ASCII_LC + ltn.OTHER_SUBSTRING],
))

TXN_TO_PSAC = (
    TXN_TO_PSA_COMMON @
    IGNORE_LONG @
    TRANSLIT_BY_PSA @
    ltn.print_only_ltn() @
    REMOVE_REPEATED_LTN).optimize()
