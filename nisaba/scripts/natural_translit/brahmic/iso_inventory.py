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
"""ISO inventory.

ISO - typ mapping

'a': 'a'           'd': 'd'           'ṉ': 'na'          'z': 'z'
'ā': 'aa'          'ḍ': 'dd'          'p': 'p'           '’': 'avg'
'æ': 'ac'          'f': 'f'           'q': 'q'           'ˑ': 'nkt'
'e': 'e'           'g': 'g'           'r': 'r'           'ḥ': 'vis'
'ē': 'ee'          'ġ': 'gg'          'ṛ': 'rd'          'ṁ': 'ans'
'ê': 'ec'          'h': 'h'           'ṟ': 'rr'          '̐' : 'cnd_dia'
'i': 'i'           'j': 'j'           's': 's'           'ḫ': 'upadh'
'ī': 'ii'          'k': 'k'           'ś': 'sh'          'ẖ': 'jihva'
'o': 'o'           'l': 'l'           'ṣ': 'ss'          'ʰ': 'asp'
'ō': 'oo'          'ḷ': 'll'          't': 't'           '̥' : 'vcl'
'ô': 'oc'          'ḻ': 'lr'          'ṭ': 'tt'          '̄' : 'long'
'õ': 'ot'          'm': 'm'           'ṯ': 'ta'          'ⸯ': 'chl'
'u': 'u'           'n': 'n'           'v': 'v'           '̆' : 'eye'
'ū': 'uu'          'ñ': 'ny'          'x': 'x'           '.': 'ind'
'b': 'b'           'ṅ': 'ng'          'y': 'y'           '+': 'zwj'
'c': 'c'           'ṇ': 'nn'          'ẏ': 'yy'          '|': 'zwn'
'ạ': 'an'

"""

from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import list_op as ls

# Single point characters

INHERENT_VOWEL = [c.make_char('a', 'a', ph.SCHWA)]

SIMPLE_VOWEL_SIGN = ls.apply_foreach(c.make_char, [
    ['aa', 'ā', ph.A_L],
    ['ac', 'æ', ph.AE],
    ['an', 'ạ', ph.A],
    ['e', 'e', ph.E],
    ['ee', 'ē', ph.E_L],
    ['ec', 'ê', ph.AE],
    ['i', 'i', ph.I],
    ['ii', 'ī', ph.I_L],
    ['o', 'o', ph.O],
    ['oo', 'ō', ph.O_L],
    ['oc', 'ô', ph.O_L],
    ['u', 'u', ph.U],
    ['uu', 'ū', ph.U_L],
])

SIMPLE_VOWEL = INHERENT_VOWEL + SIMPLE_VOWEL_SIGN

SIMPLE_CONSONANT = ls.apply_foreach(c.make_char, [
    ['b', 'b', ph.B],
    ['c', 'c', ph.TSH],
    ['d', 'd', ph.DI],
    ['dd', 'ḍ', ph.DD],
    ['f', 'f', ph.F],
    ['g', 'g', ph.G],
    ['gg', 'ġ', ph.GH],
    ['h', 'h', ph.H],
    ['j', 'j', ph.DZH],
    ['k', 'k', ph.K],
    ['l', 'l', ph.L],
    ['ll', 'ḷ', ph.LL],
    ['lr', 'ḻ', ph.RRU],
    ['m', 'm', ph.M],
    ['n', 'n', ph.NI],
    ['ny', 'ñ', ph.NY],
    ['ng', 'ṅ', ph.NG],
    ['nn', 'ṇ', ph.NN],
    ['na', 'ṉ', ph.N],
    ['p', 'p', ph.P],
    ['q', 'q', ph.Q],
    ['r', 'r', ph.RT],
    ['rd', 'ṛ', ph.RRT],
    ['rr', 'ṟ', ph.R],
    ['s', 's', ph.S],
    ['sh', 'ś', ph.SH],
    ['ss', 'ṣ', ph.SS],
    ['t', 't', ph.TI],
    ['tt', 'ṭ', ph.TT],
    ['ta', 'ṯ', ph.T],
    ['v', 'v', ph.VU],
    ['x', 'x', ph.KH],
    ['y', 'y', ph.Y],
    ['yy', 'ẏ', ph.Y + ph.ASP],
    ['z', 'z', ph.Z],
])

SIMPLE_CODA = ls.apply_foreach(c.make_char, [
    ['avg', '’', ph.SIL],
    ['nkt', 'ˑ', ph.SIL],
    ['vis', 'ḥ', ph.H],
    ['ans', 'ṁ', ph.NSL],
    ['cnd_dia', '̐', ph.SIL],
    ['upadh', 'ḫ', ph.H],
    ['jihva', 'ẖ', ph.H],
])

OM_VOWEL = [c.make_char('ot', 'õ', ph.O_L)]

MODIFIER = ls.apply_foreach(c.make_char, [
    ['asp', 'ʰ', ph.ASP],
    ['vcl', '̥', ph.SYL],
    ['long', '̄', ph.SIL],
    ['chl', 'ⸯ', ph.SIL],
    ['eye', '̆', ph.SIL],
])

SYMBOL = ls.apply_foreach(c.make_char, [
    ['ind', '.', ph.SIL],
    ['zwj', '+', ph.SIL],
    ['zwn', '|', ph.SIL],
])

SINGLE_POINT = (
    SIMPLE_VOWEL + SIMPLE_CONSONANT + SIMPLE_CODA +
    MODIFIER + SYMBOL + OM_VOWEL
)
sp = c.char_inventory(SINGLE_POINT)

# Composite vowels

# Three point vowel sign
LONG_VOCALIC = ls.apply_foreach(c.make_composite_char, [
    [[sp.L, sp.VCL, sp.LONG], 'llv', ph.L + ph.SYL_L],
    [[sp.R, sp.VCL, sp.LONG], 'rrv', ph.R + ph.SYL_L],
])

SHORT_VOCALIC = ls.apply_foreach(c.make_composite_char, [
    [[sp.L, sp.VCL], 'lv', ph.L + ph.SYL],
    [[sp.R, sp.VCL], 'rv', ph.R + ph.SYL],
])

VOCALIC_SIGN = SHORT_VOCALIC + LONG_VOCALIC

DIPHTHONG_SIGN = ls.apply_foreach(c.make_composite_char, [
    [[sp.A, sp.I], 'ai', ph.AE],
    [[sp.A, sp.U], 'au', ph.O_L],
])

SANTAL_AAN = [c.make_composite_char([sp.AN, sp.LONG], 'aan', ph.A_L)]

TWO_POINT_SIGN = SHORT_VOCALIC + DIPHTHONG_SIGN + SANTAL_AAN

VOWEL_SIGN = SIMPLE_VOWEL + TWO_POINT_SIGN + LONG_VOCALIC
VOWEL_S = c.store_gr_union('VOWEL_S', VOWEL_SIGN)


def _independent(sign: c.Char):
  return c.make_composite_char(
      [sp.IND, sign],
      sign.typ + '_i',
      sign.ph)

INDEPENDENT_NONVOCALIC = [
    _independent(sign) for sign in SIMPLE_VOWEL_SIGN + DIPHTHONG_SIGN]

INDEPENDENT_VOCALIC = [_independent(sign) for sign in VOCALIC_SIGN]

# Independent A isn't schwa.
INDEPENDENT_A = [c.make_composite_char([sp.IND, sp.A], sp.A.typ + '_i', ph.A)]

INDEPENDENT_VOWEL = INDEPENDENT_NONVOCALIC + INDEPENDENT_VOCALIC + INDEPENDENT_A
VOWEL_I = c.store_gr_union('VOWEL_I', INDEPENDENT_VOWEL)

VOCALIC = c.store_gr_union('VOCALIC', VOCALIC_SIGN + INDEPENDENT_VOCALIC)

#  Composite consonants


def _make_aspirated(char: c.Char) -> c.Char:
  return c.make_composite_char(
      [char, sp.ASP],
      char.typ + 'h',
      char.ph + ph.ASP)

ASPIRATED_CONSONANT = ls.apply_foreach(_make_aspirated, [
    [sp.B], [sp.C], [sp.D], [sp.DD], [sp.G], [sp.J],
    [sp.K], [sp.P], [sp.RD], [sp.T], [sp.TT],
])

DEAD_CONSONANT = ls.apply_foreach(c.make_composite_char, [
    [[sp.K, sp.CHL], 'k_chl', sp.K.ph],
    [[sp.L, sp.CHL], 'l_chl', sp.L.ph],
    [[sp.LL, sp.CHL], 'll_chl', sp.LL.ph],
    [[sp.N, sp.CHL], 'n_chl', ph.N],
    [[sp.NN, sp.CHL], 'nn_chl', sp.NN.ph],
    [[sp.RR, sp.CHL], 'rr_chl', sp.RR.ph],
    [[sp.R, sp.CHL], 'reph', ph.RT],
    [[sp.R, sp.EYE], 'r_eye', ph.RT]
])

COMPOSITE_CONSONANT = ASPIRATED_CONSONANT + DEAD_CONSONANT

CND = [c.make_composite_char([sp.M, sp.CND_DIA], 'cnd', ph.NSL)]
CODA = c.store_gr_union('CODA', SIMPLE_CODA + CND)

# Om
OM = [c.make_composite_char([sp.OT, sp.M], 'om', ph.O_L + ph.M)]

TWO_POINT = TWO_POINT_SIGN + INDEPENDENT_VOWEL + COMPOSITE_CONSONANT + CND + OM

CHAR = (SINGLE_POINT + TWO_POINT + LONG_VOCALIC)
STORES = [VOWEL_S, VOWEL_I, CODA, VOCALIC]

GRAPHEME_INVENTORY = c.gr_inventory(CHAR, STORES)
