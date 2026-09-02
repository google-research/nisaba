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

# Lint as: python3
"""Brahmic grapheme inventory.

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
import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import phoneme_inventory as psa
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

ph = psa.PHONEME_INVENTORY

# Single point characters

INHERENT_VOWEL = [c.Char('a', 'a', ph.V_TNT)]  # pyrefly: ignore[missing-attribute]

SIMPLE_VOWEL_SIGN = [c.Char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['aa', 'ā', ph.A + ph.DURH],  # pyrefly: ignore[missing-attribute]
    ['ac', 'æ', ph.AE],  # pyrefly: ignore[missing-attribute]
    ['an', 'ạ', ph.A],  # pyrefly: ignore[missing-attribute]
    ['e', 'e', ph.E],  # pyrefly: ignore[missing-attribute]
    ['ee', 'ē', ph.E + ph.DURH],  # pyrefly: ignore[missing-attribute]
    ['ec', 'ê', ph.AE],  # pyrefly: ignore[missing-attribute]
    ['i', 'i', ph.I],  # pyrefly: ignore[missing-attribute]
    ['ii', 'ī', ph.I + ph.DURH],  # pyrefly: ignore[missing-attribute]
    ['o', 'o', ph.O],  # pyrefly: ignore[missing-attribute]
    ['oo', 'ō', ph.O + ph.DURH],  # pyrefly: ignore[missing-attribute]
    ['oc', 'ô', ph.OH],  # pyrefly: ignore[missing-attribute]
    ['u', 'u', ph.U],  # pyrefly: ignore[missing-attribute]
    ['uu', 'ū', ph.U + ph.DURH],  # pyrefly: ignore[missing-attribute]
]]

SIMPLE_VOWEL = INHERENT_VOWEL + SIMPLE_VOWEL_SIGN

SIMPLE_CONSONANT = [c.Char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['b', 'b', ph.B],  # pyrefly: ignore[missing-attribute]
    ['c', 'c', ph.T_SH],  # pyrefly: ignore[missing-attribute]
    ['d', 'd', ph.DI],  # pyrefly: ignore[missing-attribute]
    ['dd', 'ḍ', ph.DD],  # pyrefly: ignore[missing-attribute]
    ['f', 'f', ph.F],  # pyrefly: ignore[missing-attribute]
    ['g', 'g', ph.G],  # pyrefly: ignore[missing-attribute]
    ['gg', 'ġ', ph.GH],  # pyrefly: ignore[missing-attribute]
    ['h', 'h', ph.H],  # pyrefly: ignore[missing-attribute]
    ['j', 'j', ph.D_ZH],  # pyrefly: ignore[missing-attribute]
    ['k', 'k', ph.K],  # pyrefly: ignore[missing-attribute]
    ['l', 'l', ph.L],  # pyrefly: ignore[missing-attribute]
    ['ll', 'ḷ', ph.LL],  # pyrefly: ignore[missing-attribute]
    ['lr', 'ḻ', ph.RRU],  # pyrefly: ignore[missing-attribute]
    ['m', 'm', ph.M],  # pyrefly: ignore[missing-attribute]
    ['n', 'n', ph.NI],  # pyrefly: ignore[missing-attribute]
    ['ny', 'ñ', ph.NY],  # pyrefly: ignore[missing-attribute]
    ['ng', 'ṅ', ph.NG],  # pyrefly: ignore[missing-attribute]
    ['nn', 'ṇ', ph.NN],  # pyrefly: ignore[missing-attribute]
    ['na', 'ṉ', ph.N],  # pyrefly: ignore[missing-attribute]
    ['p', 'p', ph.P],  # pyrefly: ignore[missing-attribute]
    ['q', 'q', ph.Q],  # pyrefly: ignore[missing-attribute]
    ['r', 'r', ph.RT],  # pyrefly: ignore[missing-attribute]
    ['rd', 'ṛ', ph.RD],  # pyrefly: ignore[missing-attribute]
    ['rr', 'ṟ', ph.R],  # pyrefly: ignore[missing-attribute]
    ['s', 's', ph.S],  # pyrefly: ignore[missing-attribute]
    ['sh', 'ś', ph.SH],  # pyrefly: ignore[missing-attribute]
    ['ss', 'ṣ', ph.SS],  # pyrefly: ignore[missing-attribute]
    ['t', 't', ph.TI],  # pyrefly: ignore[missing-attribute]
    ['tt', 'ṭ', ph.TT],  # pyrefly: ignore[missing-attribute]
    ['ta', 'ṯ', ph.T],  # pyrefly: ignore[missing-attribute]
    ['v', 'v', ph.VU],  # pyrefly: ignore[missing-attribute]
    ['x', 'x', ph.KH],  # pyrefly: ignore[missing-attribute]
    ['y', 'y', ph.Y],  # pyrefly: ignore[missing-attribute]
    ['yy', 'ẏ', ph.Y + ph.ASP],  # pyrefly: ignore[missing-attribute]
    ['z', 'z', ph.Z],  # pyrefly: ignore[missing-attribute]
]]

SIMPLE_CODA = [c.Char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['avg', '’', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['nkt', 'ˑ', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['vis', 'ḥ', ph.H],  # pyrefly: ignore[missing-attribute]
    ['vis_ta', 'ḵ', ph.G],  # pyrefly: ignore[missing-attribute]
    ['ans', 'ṁ', ph.NSL],  # pyrefly: ignore[missing-attribute]
    ['cnd_dia', '̐', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['upadh', 'ḫ', ph.H],  # pyrefly: ignore[missing-attribute]
    ['jihva', 'ẖ', ph.H],  # pyrefly: ignore[missing-attribute]
    ['add', '˖', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['tip', 'ṃ', ph.NSL],  # pyrefly: ignore[missing-attribute]
]]

OM_VOWEL = [c.Char('ot', 'õ', ph.O + ph.DURH)]  # pyrefly: ignore[missing-attribute]

MODIFIER = [c.Char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['asp', 'ʰ', ph.ASP],  # pyrefly: ignore[missing-attribute]
    ['vcl', '̥', ph.SYL],  # pyrefly: ignore[missing-attribute]
    ['long', '̄', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['chl', 'ⸯ', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['eye', '̆', ph.SIL],  # pyrefly: ignore[missing-attribute]
]]

VIRAMA = [c.Char('vir', '', ph.SIL)]  # pyrefly: ignore[missing-attribute]

SYMBOL = [c.Char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['ind', '.', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['sgn', '-', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['zwj', '+', ph.SIL],  # pyrefly: ignore[missing-attribute]
    ['zwn', '|', ph.SIL],  # pyrefly: ignore[missing-attribute]
]]

SINGLE_POINT = (
    SIMPLE_VOWEL + SIMPLE_CONSONANT + SIMPLE_CODA +
    MODIFIER + SYMBOL + OM_VOWEL
)
sp = c.char_inventory(SINGLE_POINT)

# Composite vowels

# Three point vowel sign
LONG_VOCALIC = [c.make_composite_char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [[sp.L, sp.VCL, sp.LONG], 'llv', ph.L + ph.SYL + ph.DURH],  # pyrefly: ignore[missing-attribute]
    [[sp.R, sp.VCL, sp.LONG], 'rrv', ph.R + ph.SYL + ph.DURH],  # pyrefly: ignore[missing-attribute]
]]

SHORT_VOCALIC = [c.make_composite_char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [[sp.L, sp.VCL], 'lv', ph.L + ph.SYL],  # pyrefly: ignore[missing-attribute]
    [[sp.R, sp.VCL], 'rv', ph.R + ph.SYL],  # pyrefly: ignore[missing-attribute]
]]

VOCALIC_SIGN = SHORT_VOCALIC + LONG_VOCALIC

DIPHTHONG_SIGN = [c.make_composite_char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [[sp.A, sp.I], 'ai', ph.A_I],  # pyrefly: ignore[missing-attribute]
    [[sp.A, sp.U], 'au', ph.A_U],  # pyrefly: ignore[missing-attribute]
]]

SANTAL_AAN = [c.make_composite_char([sp.AN, sp.LONG], 'aan', ph.A + ph.DURH)]  # pyrefly: ignore[missing-attribute]

TWO_POINT_SIGN = SHORT_VOCALIC + DIPHTHONG_SIGN + SANTAL_AAN

VOWEL_SIGN = SIMPLE_VOWEL + TWO_POINT_SIGN + LONG_VOCALIC
VOWEL_S = c.thing_gr_union('VOWEL_S', VOWEL_SIGN)
VOWEL_S_TR = c.thing_tr_union('VOWEL_S', VOWEL_SIGN)


def _independent(sign: c.Char):
  return c.make_composite_char(
      [sp.IND, sign],  # pyrefly: ignore[missing-attribute]
      sign.typ + '_i',
      sign.ph)

INDEPENDENT_NONVOCALIC = [
    _independent(sign) for sign in SIMPLE_VOWEL_SIGN + DIPHTHONG_SIGN]

INDEPENDENT_VOCALIC = [_independent(sign) for sign in VOCALIC_SIGN]

# Independent A isn't schwa.
INDEPENDENT_A = [c.make_composite_char([sp.IND, sp.A], sp.A.typ + '_i', ph.A)]  # pyrefly: ignore[missing-attribute]

INDEPENDENT_VOWEL = INDEPENDENT_NONVOCALIC + INDEPENDENT_VOCALIC + INDEPENDENT_A
VOWEL_I = c.thing_gr_union('VOWEL_I', INDEPENDENT_VOWEL)

VOCALIC = c.thing_gr_union('VOCALIC', VOCALIC_SIGN + INDEPENDENT_VOCALIC)

#  Composite consonants


def _make_aspirated(char: c.Char) -> c.Char:
  return c.make_composite_char(
      [char, sp.ASP],  # pyrefly: ignore[missing-attribute]
      char.typ + 'h',
      char.ph + ph.ASP)  # pyrefly: ignore[missing-attribute]

ASPIRATED_CONSONANT = [_make_aspirated(char) for char in [
    sp.B, sp.C, sp.D, sp.DD, sp.G, sp.J,  # pyrefly: ignore[missing-attribute]
    sp.K, sp.P, sp.RD, sp.T, sp.TT,  # pyrefly: ignore[missing-attribute]
]]

DEAD_CONSONANT = [c.make_composite_char(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [[sp.K, sp.CHL], 'k_chl', sp.K.ph],  # pyrefly: ignore[missing-attribute]
    [[sp.L, sp.CHL], 'l_chl', sp.L.ph],  # pyrefly: ignore[missing-attribute]
    [[sp.LL, sp.CHL], 'll_chl', sp.LL.ph],  # pyrefly: ignore[missing-attribute]
    [[sp.N, sp.CHL], 'n_chl', ph.N],  # pyrefly: ignore[missing-attribute]
    [[sp.NN, sp.CHL], 'nn_chl', sp.NN.ph],  # pyrefly: ignore[missing-attribute]
    [[sp.RR, sp.CHL], 'rr_chl', sp.RR.ph],  # pyrefly: ignore[missing-attribute]
    [[sp.R, sp.CHL], 'reph', ph.RT],  # pyrefly: ignore[missing-attribute]
    [[sp.R, sp.EYE], 'r_eye', ph.RT]  # pyrefly: ignore[missing-attribute]
]]

SCHWA_BEARING = SIMPLE_CONSONANT + ASPIRATED_CONSONANT
SCHWA_BEARING_GR = c.thing_gr_union('SCH_CONS', SCHWA_BEARING)
SCHWA_BEARING_TR = c.thing_tr_union('SCH_CONS', SCHWA_BEARING)
DEAD_CONSONANT_TR = c.thing_tr_union('DEAD_CONS', DEAD_CONSONANT)
COMPOSITE_CONSONANT = ASPIRATED_CONSONANT + DEAD_CONSONANT
ONSET_CONSONANT = SIMPLE_CONSONANT + COMPOSITE_CONSONANT
ONSET_CONSONANT_TR = c.thing_tr_union('ONSET_CONS', ONSET_CONSONANT)

CND = [c.make_composite_char([sp.M, sp.CND_DIA], 'cnd', ph.NSL)]  # pyrefly: ignore[missing-attribute]
CODA = c.thing_gr_union('CODA', SIMPLE_CODA + CND)

# Om
OM = [c.make_composite_char([sp.OT, sp.M], 'om', ph.O + ph.DURH + ph.M)]  # pyrefly: ignore[missing-attribute]

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


# TODO: Move into inventory as a class method after symbol conversion.
def iso_to_typ_rules() -> fl.FstList:
  """Makes an FstList of ISO to typ rewrites."""
  return fl.FstList(
      c.read_glyph(SINGLE_POINT),
      ## Compose typ for brahmic characters with multi-point ISO.
      c.compose_from_gr(LONG_VOCALIC),
      c.compose_from_gr(TWO_POINT_SIGN),
      # Word initial vowels are independent but not marked in ISO.
      rw.rewrite_word_initial(
          '',
          GRAPHEME_INVENTORY.IND,  # pyrefly: ignore[missing-attribute]
          GRAPHEME_INVENTORY.VOWEL_S - GRAPHEME_INVENTORY.AAN,  # pyrefly: ignore[missing-attribute]
      ),
      c.compose_from_gr(INDEPENDENT_VOWEL),
      c.compose_from_gr(COMPOSITE_CONSONANT),
      c.compose_from_gr(OM + CND),
      alias='iso_to_typ',
  )


def to_typ(iso: str) -> pyn.Fst:
  """Temporary function for testing purposes."""
  return fl.FstList(iso, iso_to_typ_rules()).compose()


DEVA = 'deva'
TAML = 'taml'
DEROM_SCRIPTS = [DEVA, TAML]

# Only includes the subset of ISO Chars used by deromanizers.
TO_BRAHMIC = {
    CHAR_INVENTORY.VIR.typ: {DEVA: '्', TAML: '்'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.A.typ: {DEVA: '', TAML: ''},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.A_I.typ: {DEVA: 'अ', TAML: 'அ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AA.typ: {DEVA: 'ा', TAML: 'ா'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AA_I.typ: {DEVA: 'आ', TAML: 'ஆ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.E.typ: {DEVA: 'ॆ', TAML: 'ெ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.E_I.typ: {DEVA: 'ऎ', TAML: 'எ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.EE.typ: {DEVA: 'े', TAML: 'ே'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.EE_I.typ: {DEVA: 'ए', TAML: 'ஏ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.I.typ: {DEVA: 'ि', TAML: 'ி'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.I_I.typ: {DEVA: 'इ', TAML: 'இ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.II.typ: {DEVA: 'ी', TAML: 'ீ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.II_I.typ: {DEVA: 'ई', TAML: 'ஈ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.O.typ: {DEVA: 'ॊ', TAML: 'ொ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.O_I.typ: {DEVA: 'ऒ', TAML: 'ஒ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.OO.typ: {DEVA: 'ो', TAML: 'ோ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.OO_I.typ: {DEVA: 'ओ', TAML: 'ஓ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.U.typ: {DEVA: 'ु', TAML: 'ு'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.U_I.typ: {DEVA: 'उ', TAML: 'உ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.UU.typ: {DEVA: 'ू', TAML: 'ூ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.UU_I.typ: {DEVA: 'ऊ', TAML: 'ஊ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AI.typ: {DEVA: 'ै', TAML: 'ை'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AI_I.typ: {DEVA: 'ऐ', TAML: 'ஐ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AU.typ: {DEVA: 'ौ', TAML: 'ௌ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.AU_I.typ: {DEVA: 'औ', TAML: 'ஔ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.B.typ: {DEVA: 'ब'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.BH.typ: {DEVA: 'भ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.C.typ: {DEVA: 'च', TAML: 'ச'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.CH.typ: {DEVA: 'छ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.D.typ: {DEVA: 'द'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.DH.typ: {DEVA: 'ध'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.G.typ: {DEVA: 'ग'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.GH.typ: {DEVA: 'घ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.H.typ: {DEVA: 'ह', TAML: 'ஹ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.J.typ: {DEVA: 'ज', TAML: 'ஜ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.Z.typ: {DEVA: 'ज़', TAML: 'ஃஜ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.JH.typ: {DEVA: 'झ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.K.typ: {DEVA: 'क', TAML: 'க'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.KH.typ: {DEVA: 'ख'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.L.typ: {DEVA: 'ल', TAML: 'ல'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.LR.typ: {TAML: 'ழ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.M.typ: {DEVA: 'म', TAML: 'ம'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.N.typ: {DEVA: 'न', TAML: 'ந'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.NA.typ: {TAML: 'ன'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.P.typ: {DEVA: 'प', TAML: 'ப'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.PH.typ: {DEVA: 'फ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.F.typ: {DEVA: 'फ़', TAML: 'ஃப'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.R.typ: {DEVA: 'र', TAML: 'ர'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.RR.typ: {TAML: 'ற'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.S.typ: {DEVA: 'स', TAML: 'ஸ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.SH.typ: {DEVA: 'श', TAML: 'ஶ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.T.typ: {DEVA: 'त', TAML: 'த'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.TH.typ: {DEVA: 'थ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.V.typ: {DEVA: 'व', TAML: 'வ'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.Y.typ: {DEVA: 'य', TAML: 'ய'},  # pyrefly: ignore[missing-attribute]
    CHAR_INVENTORY.ANS.typ: {DEVA: 'ं', TAML: ''},  # pyrefly: ignore[missing-attribute]
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
