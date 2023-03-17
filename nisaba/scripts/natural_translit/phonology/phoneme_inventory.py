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
"""Multilingual phoneme inventory.

This library builds a high coverage Phon inventory. Language specific phoneme
inventories can be built by importing the relevant subset of Phons.
For example: /nisaba/scripts/natural_translit/brahmic/psa_phoneme_inventory.py

The multilingual inventory is used for shared multilingual or
language agnostic modules. For example:
/nisaba/scripts/natural_translit/phonology/operations/voicing.py

TODO: Add test to make sure phon_table is up to date.
"""

from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import feature
from nisaba.scripts.natural_translit.phonology import modify_phon as mod
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.utils import list_op as ls

f = feature.FEATURE_INVENTORY
tr = ltn.TRANSLIT_INVENTORY

SILENCE = [p.base_phon('sil', [f.silent], '', tr.DEL)]

BASE_FEATURE = ls.apply_foreach(p.base_phon, [
    ['S', [f.syllabic], '̍', tr.I, 'SYL'],
    ['Z', [f.nonsyllabic], '̯', tr.DEL, 'NSY'],
    ['N', [f.nasal], '~', tr.N, 'NSL'],
    ['H', [f.aspirated], 'ʰ', tr.H, 'ASP'],
])

_FTR = p.phon_inventory(BASE_FEATURE)

LONG_SYL = [mod.long(_FTR.SYL, tr.S_II)]

STANDALONE_FEATURE = BASE_FEATURE + LONG_SYL

UNASSIGNED_VOWEL = ls.apply_foreach(p.base_phon, [
    ['_', [f.vowel], '', tr.DEL, 'V_TNT'],  # tentative
    ['V', [f.vowel], '', tr.DEL, 'V_PRN'],  # pronounced
])

SHORT_VOWEL = ls.apply_foreach(p.base_phon, [
    ['a', [f.vowel], 'a', tr.A],
    ['ae', [f.vowel], 'æ', tr.A],
    ['e', [f.vowel], 'e', tr.E],
    ['ec', [f.vowel], 'ə', tr.U],
    ['eh', [f.vowel], 'ɛ', tr.E],
    ['i', [f.vowel], 'i', tr.I],
    ['o', [f.vowel], 'o', tr.O],
    ['oh', [f.vowel], 'ɔ', tr.O],
    ['u', [f.vowel], 'u', tr.U],
])

LONG_VOWEL = [mod.long(short) for short in SHORT_VOWEL]

_V = p.phon_inventory(SHORT_VOWEL + LONG_VOWEL)

DIPHTHONG = ls.apply_foreach(mod.diphthong, [
    [[_V.A, _V.I], tr.S_AI],
    [[_V.A, _V.U], tr.S_AU],
])

VOWEL = (UNASSIGNED_VOWEL + SHORT_VOWEL + LONG_VOWEL + DIPHTHONG)

NASAL = ls.apply_foreach(p.base_phon, [
    ['m', [f.bilabial], 'm', tr.M],
    ['n', [f.alveolar], 'n', tr.N],
    ['ng', [f.velar], 'ŋ', tr.S_NG],
    ['ni', [f.dental], 'n̪', tr.N],
    ['nn', [f.retroflex], 'ɳ', tr.N],
    ['ny', [f.palatal], 'ɲ', tr.S_NY],
])

VOICELESS_STOP = ls.apply_foreach(p.base_phon, [
    ['p', [f.bilabial], 'p', tr.P],
    ['q', [f.uvular], 'q', tr.K],
    ['k', [f.velar], 'k', tr.K],
    ['t', [f.alveolar], 't', tr.T],
    ['ti', [f.dental], 't̪', tr.T],
    ['tt', [f.retroflex], 'ʈ', tr.T],
])

VOICED_STOP = ls.apply_foreach(p.base_phon, [
    ['b', [f.bilabial], 'b', tr.B],
    ['d', [f.alveolar], 'd', tr.D],
    ['dd', [f.retroflex], 'ɖ', tr.D],
    ['di', [f.dental], 'd̪', tr.D],
    ['g', [f.velar], 'ɡ', tr.G],

])

STOP = (VOICELESS_STOP + VOICED_STOP)
_ST = p.phon_inventory(VOICELESS_STOP + VOICED_STOP)

VOICELESS_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['f', [f.labiodental], 'f', tr.F],
    ['h', [f.glottal], 'h', tr.H],
    ['kh', [f.uvular], 'x', tr.S_KH],
    ['s', [f.alveolar], 's', tr.S],
    ['sh', [f.postalveolar], 'ʃ', tr.S_SH],
    ['ss', [f.retroflex], 'ʂ', tr.S_SH],
])

VOICED_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['gh', [f.uvular], 'ɣ', tr.G],
    ['z', [f.alveolar], 'z', tr.Z],
    ['zh', [f.postalveolar], 'ʒ', tr.S_ZH],
])

FRICATIVE = (VOICELESS_FRICATIVE + VOICED_FRICATIVE)
_FRIC = p.phon_inventory(FRICATIVE)

VOICELESS_AFFRICATE = ls.apply_foreach(mod.affricate, [
    [[_ST.T, _FRIC.SH], tr.S_CH],
])

VOICED_AFFRICATE = ls.apply_foreach(mod.affricate, [
    [[_ST.D, _FRIC.ZH], tr.J],
])

AFFRICATE = (VOICELESS_AFFRICATE + VOICED_AFFRICATE)

CENTRAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['rru', [f.retroflex], 'ɻ', tr.S_ZH],
    ['vu', [f.labiodental], 'ʋ', tr.V],
    ['y', [f.palatal], 'j', tr.Y],
])

LATERAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['l', [f.alveolar], 'l', tr.L],
    ['ll', [f.retroflex], 'ɭ', tr.L],
])

APPROXIMANT = (CENTRAL_APPROXIMANT + LATERAL_APPROXIMANT)

TAP = ls.apply_foreach(p.base_phon, [
    ['rd', [f.retroflex], 'ɽ', tr.S_RD],
    ['rt', [f.alveolar], 'ɾ', tr.R],
])

TRILL = [p.base_phon('r', [f.alveolar], 'r', tr.R)]

CONSONANT = (
    NASAL + STOP + FRICATIVE + AFFRICATE + APPROXIMANT + TAP + TRILL
)

FEATURE = mod.MODIFIER_FEATURE + STANDALONE_FEATURE

PHONEMES = SILENCE + FEATURE + VOWEL + CONSONANT

PHON_INVENTORY = p.phon_inventory(PHONEMES)

PHONEME_INVENTORY = p.ph_inventory(PHONEMES + mod.COMBINER)
