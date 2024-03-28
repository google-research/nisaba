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

from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.script import char as c

ph = psa.PHONEME_INVENTORY

# Single point characters

INHERENT_VOWEL = [c.make_char('a', 'a', ph.V_TNT)]

SIMPLE_VOWEL_SIGN = [c.make_char(*args) for args in [
    ['aa', 'ā', ph.A + ph.DURH],
    ['ac', 'æ', ph.AE],
    ['an', 'ạ', ph.A],
    ['e', 'e', ph.E],
    ['ee', 'ē', ph.E + ph.DURH],
    ['ec', 'ê', ph.AE],
    ['i', 'i', ph.I],
    ['ii', 'ī', ph.I + ph.DURH],
    ['o', 'o', ph.O],
    ['oo', 'ō', ph.O + ph.DURH],
    ['oc', 'ô', ph.OH],
    ['u', 'u', ph.U],
    ['uu', 'ū', ph.U + ph.DURH],
]]

SIMPLE_VOWEL = INHERENT_VOWEL + SIMPLE_VOWEL_SIGN

SIMPLE_CONSONANT = [c.make_char(*args) for args in [
    ['b', 'b', ph.B],
    ['c', 'c', ph.T_SH],
    ['d', 'd', ph.DI],
    ['dd', 'ḍ', ph.DD],
    ['f', 'f', ph.F],
    ['g', 'g', ph.G],
    ['gg', 'ġ', ph.GH],
    ['h', 'h', ph.H],
    ['j', 'j', ph.D_ZH],
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
    ['rd', 'ṛ', ph.RD],
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
]]

SIMPLE_CODA = [c.make_char(*args) for args in [
    ['avg', '’', ph.SIL],
    ['nkt', 'ˑ', ph.SIL],
    ['vis', 'ḥ', ph.H],
    ['vis_ta', 'ḵ', ph.G],
    ['ans', 'ṁ', ph.NSL],
    ['cnd_dia', '̐', ph.SIL],
    ['upadh', 'ḫ', ph.H],
    ['jihva', 'ẖ', ph.H],
    ['add', '˖', ph.SIL],
    ['tip', 'ṃ', ph.NSL],
]]

OM_VOWEL = [c.make_char('ot', 'õ', ph.O + ph.DURH)]

MODIFIER = [c.make_char(*args) for args in [
    ['asp', 'ʰ', ph.ASP],
    ['vcl', '̥', ph.SYL],
    ['long', '̄', ph.SIL],
    ['chl', 'ⸯ', ph.SIL],
    ['eye', '̆', ph.SIL],
]]

VIRAMA = [c.make_char('vir', '', ph.SIL)]

SYMBOL = [c.make_char(*args) for args in [
    ['ind', '.', ph.SIL],
    ['zwj', '+', ph.SIL],
    ['zwn', '|', ph.SIL],
]]

SINGLE_POINT = (
    SIMPLE_VOWEL + SIMPLE_CONSONANT + SIMPLE_CODA +
    MODIFIER + SYMBOL + OM_VOWEL
)
sp = c.char_inventory(SINGLE_POINT)

# Composite vowels

# Three point vowel sign
LONG_VOCALIC = [c.make_composite_char(*args) for args in [
    [[sp.L, sp.VCL, sp.LONG], 'llv', ph.L + ph.SYL + ph.DURH],
    [[sp.R, sp.VCL, sp.LONG], 'rrv', ph.R + ph.SYL + ph.DURH],
]]

SHORT_VOCALIC = [c.make_composite_char(*args) for args in [
    [[sp.L, sp.VCL], 'lv', ph.L + ph.SYL],
    [[sp.R, sp.VCL], 'rv', ph.R + ph.SYL],
]]

VOCALIC_SIGN = SHORT_VOCALIC + LONG_VOCALIC

DIPHTHONG_SIGN = [c.make_composite_char(*args) for args in [
    [[sp.A, sp.I], 'ai', ph.A_I],
    [[sp.A, sp.U], 'au', ph.A_U],
]]

SANTAL_AAN = [c.make_composite_char([sp.AN, sp.LONG], 'aan', ph.A + ph.DURH)]

TWO_POINT_SIGN = SHORT_VOCALIC + DIPHTHONG_SIGN + SANTAL_AAN

VOWEL_SIGN = SIMPLE_VOWEL + TWO_POINT_SIGN + LONG_VOCALIC
VOWEL_S = c.store_gr_union('VOWEL_S', VOWEL_SIGN)
VOWEL_S_TR = c.store_tr_union('VOWEL_S', VOWEL_SIGN)


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

ASPIRATED_CONSONANT = [_make_aspirated(char) for char in [
    sp.B, sp.C, sp.D, sp.DD, sp.G, sp.J,
    sp.K, sp.P, sp.RD, sp.T, sp.TT,
]]

DEAD_CONSONANT = [c.make_composite_char(*args) for args in [
    [[sp.K, sp.CHL], 'k_chl', sp.K.ph],
    [[sp.L, sp.CHL], 'l_chl', sp.L.ph],
    [[sp.LL, sp.CHL], 'll_chl', sp.LL.ph],
    [[sp.N, sp.CHL], 'n_chl', ph.N],
    [[sp.NN, sp.CHL], 'nn_chl', sp.NN.ph],
    [[sp.RR, sp.CHL], 'rr_chl', sp.RR.ph],
    [[sp.R, sp.CHL], 'reph', ph.RT],
    [[sp.R, sp.EYE], 'r_eye', ph.RT]
]]

SCHWA_BEARING = SIMPLE_CONSONANT + ASPIRATED_CONSONANT
SCHWA_BEARING_GR = c.store_gr_union('SCH_CONS', SCHWA_BEARING)
SCHWA_BEARING_TR = c.store_tr_union('SCH_CONS', SCHWA_BEARING)
DEAD_CONSONANT_TR = c.store_tr_union('DEAD_CONS', DEAD_CONSONANT)
COMPOSITE_CONSONANT = ASPIRATED_CONSONANT + DEAD_CONSONANT
ONSET_CONSONANT = SIMPLE_CONSONANT + COMPOSITE_CONSONANT
ONSET_CONSONANT_TR = c.store_tr_union('ONSET_CONS', ONSET_CONSONANT)

CND = [c.make_composite_char([sp.M, sp.CND_DIA], 'cnd', ph.NSL)]
CODA = c.store_gr_union('CODA', SIMPLE_CODA + CND)

# Om
OM = [c.make_composite_char([sp.OT, sp.M], 'om', ph.O + ph.DURH + ph.M)]

TWO_POINT = TWO_POINT_SIGN + INDEPENDENT_VOWEL + COMPOSITE_CONSONANT + CND + OM

GR_CHAR = SINGLE_POINT + TWO_POINT + LONG_VOCALIC
CHAR = GR_CHAR + VIRAMA
GR_STORES = [VOWEL_S, VOWEL_I, CODA, VOCALIC, SCHWA_BEARING_GR]
TR_STORES = [
    VOWEL_S_TR, SCHWA_BEARING_TR, DEAD_CONSONANT_TR, ONSET_CONSONANT_TR
]

CHAR_INVENTORY = c.char_inventory(CHAR)
GRAPHEME_INVENTORY = c.gr_inventory(CHAR, GR_STORES)
TRANSLIT_INVENTORY = c.tr_inventory(CHAR, TR_STORES)

DEVA = 'deva'
TAML = 'taml'
DEROM_SCRIPTS = [DEVA, TAML]

# Only includes the subset of ISO Chars used by deromanizers.
TO_BRAHMIC = {
    CHAR_INVENTORY.VIR.typ: {DEVA: '्', TAML: '்'},
    CHAR_INVENTORY.A.typ: {DEVA: '', TAML: ''},
    CHAR_INVENTORY.A_I.typ: {DEVA: 'अ', TAML: 'அ'},
    CHAR_INVENTORY.AA.typ: {DEVA: 'ा', TAML: 'ா'},
    CHAR_INVENTORY.AA_I.typ: {DEVA: 'आ', TAML: 'ஆ'},
    CHAR_INVENTORY.E.typ: {DEVA: 'ॆ', TAML: 'ெ'},
    CHAR_INVENTORY.E_I.typ: {DEVA: 'ऎ', TAML: 'எ'},
    CHAR_INVENTORY.EE.typ: {DEVA: 'े', TAML: 'ே'},
    CHAR_INVENTORY.EE_I.typ: {DEVA: 'ए', TAML: 'ஏ'},
    CHAR_INVENTORY.I.typ: {DEVA: 'ि', TAML: 'ி'},
    CHAR_INVENTORY.I_I.typ: {DEVA: 'इ', TAML: 'இ'},
    CHAR_INVENTORY.II.typ: {DEVA: 'ी', TAML: 'ீ'},
    CHAR_INVENTORY.II_I.typ: {DEVA: 'ई', TAML: 'ஈ'},
    CHAR_INVENTORY.O.typ: {DEVA: 'ॊ', TAML: 'ொ'},
    CHAR_INVENTORY.O_I.typ: {DEVA: 'ऒ', TAML: 'ஒ'},
    CHAR_INVENTORY.OO.typ: {DEVA: 'ो', TAML: 'ோ'},
    CHAR_INVENTORY.OO_I.typ: {DEVA: 'ओ', TAML: 'ஓ'},
    CHAR_INVENTORY.U.typ: {DEVA: 'ु', TAML: 'ு'},
    CHAR_INVENTORY.U_I.typ: {DEVA: 'उ', TAML: 'உ'},
    CHAR_INVENTORY.UU.typ: {DEVA: 'ू', TAML: 'ூ'},
    CHAR_INVENTORY.UU_I.typ: {DEVA: 'ऊ', TAML: 'ஊ'},
    CHAR_INVENTORY.AI.typ: {DEVA: 'ै', TAML: 'ை'},
    CHAR_INVENTORY.AI_I.typ: {DEVA: 'ऐ', TAML: 'ஐ'},
    CHAR_INVENTORY.AU.typ: {DEVA: 'ौ', TAML: 'ௌ'},
    CHAR_INVENTORY.AU_I.typ: {DEVA: 'औ', TAML: 'ஔ'},
    CHAR_INVENTORY.B.typ: {DEVA: 'ब'},
    CHAR_INVENTORY.BH.typ: {DEVA: 'भ'},
    CHAR_INVENTORY.C.typ: {DEVA: 'च', TAML: 'ச'},
    CHAR_INVENTORY.CH.typ: {DEVA: 'छ'},
    CHAR_INVENTORY.D.typ: {DEVA: 'द'},
    CHAR_INVENTORY.DH.typ: {DEVA: 'ध'},
    CHAR_INVENTORY.G.typ: {DEVA: 'ग'},
    CHAR_INVENTORY.GH.typ: {DEVA: 'घ'},
    CHAR_INVENTORY.H.typ: {DEVA: 'ह', TAML: 'ஹ'},
    CHAR_INVENTORY.J.typ: {DEVA: 'ज', TAML: 'ஜ'},
    CHAR_INVENTORY.Z.typ: {DEVA: 'ज़', TAML: 'ஃஜ'},
    CHAR_INVENTORY.JH.typ: {DEVA: 'झ'},
    CHAR_INVENTORY.K.typ: {DEVA: 'क', TAML: 'க'},
    CHAR_INVENTORY.KH.typ: {DEVA: 'ख'},
    CHAR_INVENTORY.L.typ: {DEVA: 'ल', TAML: 'ல'},
    CHAR_INVENTORY.LR.typ: {TAML: 'ழ'},
    CHAR_INVENTORY.M.typ: {DEVA: 'म', TAML: 'ம'},
    CHAR_INVENTORY.N.typ: {DEVA: 'न', TAML: 'ந'},
    CHAR_INVENTORY.NA.typ: {TAML: 'ன'},
    CHAR_INVENTORY.P.typ: {DEVA: 'प', TAML: 'ப'},
    CHAR_INVENTORY.PH.typ: {DEVA: 'फ'},
    CHAR_INVENTORY.F.typ: {DEVA: 'फ़', TAML: 'ஃப'},
    CHAR_INVENTORY.R.typ: {DEVA: 'र', TAML: 'ர'},
    CHAR_INVENTORY.RR.typ: {TAML: 'ற'},
    CHAR_INVENTORY.S.typ: {DEVA: 'स', TAML: 'ஸ'},
    CHAR_INVENTORY.SH.typ: {DEVA: 'श', TAML: 'ஶ'},
    CHAR_INVENTORY.T.typ: {DEVA: 'त', TAML: 'த'},
    CHAR_INVENTORY.TH.typ: {DEVA: 'थ'},
    CHAR_INVENTORY.V.typ: {DEVA: 'व', TAML: 'வ'},
    CHAR_INVENTORY.Y.typ: {DEVA: 'य', TAML: 'ய'},
    CHAR_INVENTORY.ANS.typ: {DEVA: 'ं', TAML: ''},
}


def get_brh(typ: str, script: str) -> str:
  return TO_BRAHMIC.get(typ, {}).get(script, '')


def ls_tr2brh(script: str) -> list[tuple[str, str]]:
  """List of arguments for rewriting tr field of Char as Brahmic characters.

  Args:
    script: script name, dictionary key for each typ's to_brahmic dictionary.

  Returns:
    List of argument lists for rewrite_ls(), which will in turn generate
    the union of [pcross('`aa_i`', 'आ'), ...] functions.
    In the argument list, the typ string is enclosed in translit
    symbol boundaries `` to match the fst in the tr field of the Char tuple.

  """
  return [('`%s`' % typ, get_brh(typ, script)) for typ in TO_BRAHMIC]
