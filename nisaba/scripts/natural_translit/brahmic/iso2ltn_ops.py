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

"""Romanization rules that depend on iso graphemes."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.utils import rewrite as cmp

gr = iso.GRAPHEME_INVENTORY
tr = ltn.TRANSLIT_INVENTORY
ph = psa.PHONEME_INVENTORY

## Rules to apply before txn to ltn mappings

# <v> is "w" after {s}, {ss}, and {sh}.
SIBV_TO_SIBW = rw.reassign(
    gr.V,
    ph.VU,
    tr.W,
    ph.SIBILANT)


# Palatal and velar assimilated anusvara is transliterated as "n".
_NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,
    ls.union_opt(ph.NG, ph.NY),
    tr.N)


def _transliterate_vocalic(
    vcl: pyn.FstLike,
    vcl_l: pyn.FstLike) -> pyn.Fst:
  """Transliterates all vowels in vocalics as vcl_tr."""
  long_syl = rw.rewrite(
      ph.SYL_L,
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
    ph.A_L,
    tr.S_AA)

# Transliterate diphthong graphemes as diphthong instead of long vowel.

_DIPHTHONG_GR = cmp.ComposeFsts(ls.apply_foreach(rw.reassign, [
    [ls.union_opt(gr.AI, gr.AI_I), ph.EH_L, tr.S_AI],
    [ls.union_opt(gr.AU, gr.AU_I), ph.OH_L, tr.S_AU],
]))

# Rules for natural translit of two-letter geminates.

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

TRANSLIT_BY_PSAF = phon.ls_translit_by_key(psa.PHONEMES, 'psaf')
TRANSLIT_BY_PSAC = phon.ls_translit_by_key(psa.PHONEMES, 'psac')

# Compose common rules for romanization
TXN_TO_PSA_COMMON = (_DIPHTHONG_GR @ _NON_LABIAL_ANUSVARA)

# Convert txn to PSAF and outputs only translit strings.
TXN_TO_PSAF = (
    TXN_TO_PSA_COMMON @
    TRANSLIT_BY_PSAF @
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
    TRANSLIT_BY_PSAC @
    ltn.print_only_ltn() @
    REMOVE_REPEATED_LTN).optimize()
