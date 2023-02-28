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
"""Phoneme inventory.

txn is an internal typable representation for phonemes. txn strings
are enclosed in '{ }'. This library provides the constants for IPA - txn
conversion and the phonological features of phonemes such as class (vowel,
consonant, etc), manner (nasal, stop, etc) and the place of articulation
(labial, dental, etc).

IPA - txn mapping

'ə'   : {ec}       'əː'  : {ec_l}     'a' : {a}          'aː' : {a_l}
'æ'   : {ae}       'æː'  : {ae_l}	    'e' : {e}          'eː' : {e_l}
'ɛ'   : {eh}       'ɛː'  : {eh_l}	    'i' : {i}          'iː' : {i_l}
'o'   : {o}        'oː'  : {o_l}      'ɔ' : {oh}         'ɔː' : {oh_l}
'u'   : {u}        'uː'  : {u_l}

'b'   : {b}        't͡ʃ' : {t}{+}{sh} 'd' : {d}           'ɖ' : {dd}
'd̪'   : {di}       'f'   : {f}        'ɡ' : {g}           'h' : {h}
'd͡ʒ' : {d}{+}{zh} 'k'   : {k}        'l' : {l}           'ɭ' : {ll}
'm'   : {m}        'n'   : {n}        'ŋ' : {ng}          'n̪' : {ni}
'ɳ'   : {nn}       'ɲ'   : {ny}       'p' : {p}           'q' : {q}
'r'   : {r}        'ɽ'   : {rrt}      'ɻ' : {rru}         'ɾ' : {rt}
's'   : {s}        'ʃ'   : {sh}       'ʂ' : {ss}          't' : {t}
't̪'   : {ti}       'ʈ'   : {tt}       'ʋ' : {vu}          'x' : {kh}
'ɣ'   : {gh}       'j'   : {y}        'z' : {z}           'ʒ' : {zh}

'ʰ'   : {H}        '~'   : {N}        '̍ ' : {V}
'͡'   : {+}

"""

import pynini as pyn
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.utils import list_op as ls

tr = ltn.TRANSLIT_INVENTORY

SILENCE = [p.base_phon('sil', ['silent'], '', tr.DEL)]

COMBINER = [p.base_phon('+', ['composite'], '͡', tr.DEL, 'CMB')]

MODIFIER_FEATURE = ls.apply_foreach(p.base_phon, [
    ['_l', ['long'], 'ː', tr.DEL, 'LONG'],
])

STANDALONE_FEATURE = ls.apply_foreach(p.base_phon, [
    ['V', ['syllabic'], '̍', tr.I, 'SYL'],
    ['GLD', ['glide'], '̯', tr.DEL, 'GLD'],
    ['N', ['nasalized'], '~', tr.N, 'NSL'],
    ['H', ['aspirated'], 'ʰ', tr.H, 'ASP'],
])

_MOD = p.phon_inventory(COMBINER + MODIFIER_FEATURE + STANDALONE_FEATURE)

UNASSIGNED_VOWEL = ls.apply_foreach(p.base_phon, [
    ['sch', ['vowel'], '', tr.DEL, 'SCHWA'],
    ['@', ['vowel'], '', tr.DEL, 'VCL_SCHWA'],
])

SHORT_VOWEL = ls.apply_foreach(p.base_phon, [
    ['a', ['vowel'], 'a', tr.A],
    ['ae', ['vowel'], 'æ', tr.A],
    ['e', ['vowel'], 'e', tr.E],
    ['ec', ['vowel'], 'ə', tr.U],
    ['eh', ['vowel'], 'ɛ', tr.E],
    ['i', ['vowel'], 'i', tr.I],
    ['o', ['vowel'], 'o', tr.O],
    ['oh', ['vowel'], 'ɔ', tr.O],
    ['u', ['vowel'], 'u', tr.U],
])

_SV = p.phon_inventory(SHORT_VOWEL)


def long(phon: p.Phon, long_tr: pyn.FstLike = None) -> p.Phon:
  if not long_tr:
    long_tr = phon.tr_dict['base']
  return p.derive_with_suffix(
      phon,
      _MOD.LONG,
      long_tr)

LONG_SYL = [long(_MOD.SYL, tr.S_II)]

LONG_VOWEL = ls.apply_foreach(long, [
    [_SV.A, tr.S_AA],
    [_SV.E, tr.S_EE],
    [_SV.EC, tr.S_UU],
    [_SV.EH, tr.S_EE],
    [_SV.I, tr.S_II],
    [_SV.O, tr.S_OO],
    [_SV.OH, tr.S_OO],
    [_SV.U, tr.S_UU],
])


def diphthong(
    alias: str, vowels: [p.Phon], diph: pyn.FstLike,
    semi: pyn.FstLike = None, mono: pyn.FstLike = None) -> p.Phon:
  tr_dict = {}
  if semi:
    tr_dict['semi'] = semi
  if mono:
    tr_dict['mono'] = mono
  return p.compose(alias, vowels, _MOD.CMB, 'diph', diph, tr_dict)

DIPHTHONG = ls.apply_foreach(diphthong, [
    ['AI', [_SV.A, _SV.I], tr.S_AI],
    ['AU', [_SV.A, _SV.U], tr.S_AU],
])

VOWEL = (UNASSIGNED_VOWEL + SHORT_VOWEL + LONG_VOWEL + DIPHTHONG)

NASAL = ls.apply_foreach(p.base_phon, [
    ['m', ['bilabial'], 'm', tr.M],
    ['n', ['alveolar'], 'n', tr.N],
    ['ng', ['velar'], 'ŋ', tr.S_NG],
    ['ni', ['dental'], 'n̪', tr.N],
    ['nn', ['retroflex'], 'ɳ', tr.N],
    ['ny', ['palatal'], 'ɲ', tr.S_NY],
])

VOICELESS_STOP = ls.apply_foreach(p.base_phon, [
    ['p', ['bilabial'], 'p', tr.P],
    ['q', ['uvular'], 'q', tr.K],
    ['k', ['velar'], 'k', tr.K],
    ['t', ['alveolar'], 't', tr.T],
    ['ti', ['dental'], 't̪', tr.T],
    ['tt', ['retroflex'], 'ʈ', tr.T],
])

VOICED_STOP = ls.apply_foreach(p.base_phon, [
    ['b', ['bilabial'], 'b', tr.B],
    ['d', ['alveolar'], 'd', tr.D],
    ['dd', ['retroflex'], 'ɖ', tr.D],
    ['di', ['dental'], 'd̪', tr.D],
    ['g', ['velar'], 'ɡ', tr.G],

])

STOP = (VOICELESS_STOP + VOICED_STOP)
_ST = p.phon_inventory(VOICELESS_STOP + VOICED_STOP)

VOICELESS_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['f', ['labiodental'], 'f', tr.F],
    ['h', ['glottal'], 'h', tr.H],
    ['kh', ['uvular'], 'x', tr.S_KH],
    ['s', ['alveolar'], 's', tr.S],
    ['sh', ['postalveolar'], 'ʃ', tr.S_SH],
    ['ss', ['retroflex'], 'ʂ', tr.S_SH],
])

VOICED_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['gh', ['uvular'], 'ɣ', tr.G],
    ['z', ['alveolar'], 'z', tr.Z],
    ['zh', ['postalveolar'], 'ʒ', tr.S_ZH],
])

FRICATIVE = (VOICELESS_FRICATIVE + VOICED_FRICATIVE)
_FRIC = p.phon_inventory(FRICATIVE)


def affricate(
    alias: str, cons: [p.Phon], affr: pyn.FstLike) -> p.Phon:
  return p.compose(alias, cons, _MOD.CMB, 'affr', affr)

VOICELESS_AFFRICATE = ls.apply_foreach(affricate, [
    ['TSH', [_ST.T, _FRIC.SH], tr.S_CH],
])

VOICED_AFFRICATE = ls.apply_foreach(affricate, [
    ['DZH', [_ST.D, _FRIC.ZH], tr.J],
])

AFFRICATE = (VOICELESS_AFFRICATE + VOICED_AFFRICATE)

CENTRAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['rru', ['retroflex'], 'ɻ', tr.S_ZH],
    ['vu', ['labiodental'], 'ʋ', tr.V],
    ['y', ['palatal'], 'j', tr.Y],
])

LATERAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['l', ['alveolar'], 'l', tr.L],
    ['ll', ['retroflex'], 'ɭ', tr.L],
])

APPROXIMANT = (CENTRAL_APPROXIMANT + LATERAL_APPROXIMANT)

TAP = ls.apply_foreach(p.base_phon, [
    ['rrt', ['retroflex'], 'ɽ', tr.S_RD],
    ['rt', ['alveolar'], 'ɾ', tr.R],
])

TRILL = [p.base_phon('r', ['alveolar'], 'r', tr.R)]

CONSONANT = (
    NASAL + STOP + FRICATIVE + AFFRICATE + APPROXIMANT + TAP + TRILL
)

FEATURE = SILENCE + MODIFIER_FEATURE + STANDALONE_FEATURE + LONG_SYL

PHONEMES = FEATURE + VOWEL + CONSONANT

PHON_INVENTORY = p.phon_inventory(PHONEMES)

PHONEME_INVENTORY = p.ph_inventory(PHONEMES + COMBINER)
