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
"""Multilingual phoneme inventory.

This library builds a high coverage Phon inventory. Language specific phoneme
inventories can be built by importing the relevant subset of Phons.
For example: /nisaba/scripts/natural_translit/brahmic/phoneme_inventory.py

The multilingual inventory is used for shared multilingual or
language agnostic modules. For example:
/nisaba/scripts/natural_translit/phonology/operations/voicing.py

TODO: Add test to make sure phon_table is up to date.
"""

from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import feature
from nisaba.scripts.natural_translit.phonology import modify_phon as mod
from nisaba.scripts.natural_translit.phonology import phon as p

f = feature.FEATURE_INVENTORY
tr = ltn.TRANSLIT_INVENTORY

# Base Phon: Used as building blocks to derive and compose related Phons.
# Simple Phon: Non-composite, i.e. base and derived Phons.

SILENCE = [p.Phon.base('sil', [f.silent], '', tr.DEL)]  # pyrefly: ignore[missing-attribute]

STANDALONE_FEATURE = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['S', [f.syllabic], '̍', tr.U, 'SYL'],  # pyrefly: ignore[missing-attribute]
    ['Z', [f.nonsyllabic], '̯', tr.DEL, 'NSY'],  # pyrefly: ignore[missing-attribute]
    ['N', [f.nasal], '~', tr.N, 'NSL'],  # pyrefly: ignore[missing-attribute]
    ['L', [f.lateral], 'ˡ', tr.L, 'LAT'],  # pyrefly: ignore[missing-attribute]
    ['H', [f.aspirated], 'ʰ', tr.H, 'ASP'],  # pyrefly: ignore[missing-attribute]
    ['W', [f.labial], 'ʷ', tr.W, 'LBL'],  # pyrefly: ignore[missing-attribute]
    ['Y', [f.palatal], 'ʲ', tr.Y, 'PLT'],  # pyrefly: ignore[missing-attribute]
    ['G', [f.velar], 'ˠ', tr.G, 'VLR'],  # pyrefly: ignore[missing-attribute]
    ['C', [f.pharyngeal], 'ˤ', tr.H, 'PHR'],  # pyrefly: ignore[missing-attribute]
    ['X', [f.glottal], 'ˀ', tr.H, 'GLT'],  # pyrefly: ignore[missing-attribute]
    ['R', [f.rhotic], '˞', tr.R, 'RHT'],  # pyrefly: ignore[missing-attribute]
    ['.', [f.interrupt], '.', tr.DEL, 'SYB']  # syllable break  # pyrefly: ignore[missing-attribute]
]]

UNASSIGNED_VOWEL = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['_', [f.vowel], '', tr.DEL, 'V_TNT'],  # tentative  # pyrefly: ignore[missing-attribute]
    ['V', [f.vowel], '', tr.DEL, 'V_PRN'],  # pronounced  # pyrefly: ignore[missing-attribute]
]]

BASE_VOWEL = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['i', f.close_vwl + f.front_unr, 'i', tr.I],  # pyrefly: ignore[missing-attribute]
    ['ui', f.close_vwl + f.front_rnd, 'y', tr.U],  # pyrefly: ignore[missing-attribute]
    ['im', f.close_vwl + f.n_front_unr, 'ï', tr.I],  # pyrefly: ignore[missing-attribute]
    ['um', f.close_vwl + f.n_front_rnd, 'ÿ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['ic', f.close_vwl + f.center_unr, 'ɨ', tr.I],  # pyrefly: ignore[missing-attribute]
    ['uc', f.close_vwl + f.center_rnd, 'ʉ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['in', f.close_vwl + f.n_back_unr, 'ɯ̈', tr.U],  # pyrefly: ignore[missing-attribute]
    ['un', f.close_vwl + f.n_back_rnd, 'ü', tr.U],  # pyrefly: ignore[missing-attribute]
    ['iu', f.close_vwl + f.back_unr, 'ɯ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['u', f.close_vwl + f.back_rnd, 'u', tr.U],  # pyrefly: ignore[missing-attribute]
    ['ie', f.n_close_vwl + f.front_unr, 'i̞', tr.I],  # pyrefly: ignore[missing-attribute]
    ['ue', f.n_close_vwl + f.front_rnd, 'y̞', tr.U],  # pyrefly: ignore[missing-attribute]
    ['iy', f.n_close_vwl + f.n_front_unr, 'ɪ', tr.I],  # pyrefly: ignore[missing-attribute]
    ['uy', f.n_close_vwl + f.n_front_rnd, 'ʏ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['ix', f.n_close_vwl + f.center_unr, 'ɪ̈', tr.U],  # pyrefly: ignore[missing-attribute]
    ['ux', f.n_close_vwl + f.center_rnd, 'ʊ̈', tr.U],  # pyrefly: ignore[missing-attribute]
    ['iv', f.n_close_vwl + f.n_back_unr, 'ɯ̽', tr.U],  # pyrefly: ignore[missing-attribute]
    ['uv', f.n_close_vwl + f.n_back_rnd, 'ʊ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['io', f.n_close_vwl + f.back_unr, 'ɯ̞', tr.U],  # pyrefly: ignore[missing-attribute]
    ['uo', f.n_close_vwl + f.back_rnd, 'u̞', tr.U],  # pyrefly: ignore[missing-attribute]
    ['e', f.c_mid_vwl + f.front_unr, 'e', tr.E],  # pyrefly: ignore[missing-attribute]
    ['oi', f.c_mid_vwl + f.front_rnd, 'ø', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ey', f.c_mid_vwl + f.n_front_unr, 'ë', tr.E],  # pyrefly: ignore[missing-attribute]
    ['oy', f.c_mid_vwl + f.n_front_rnd, 'ø̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['el', f.c_mid_vwl + f.center_unr, 'ɘ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['ol', f.c_mid_vwl + f.center_rnd, 'ɵ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['en', f.c_mid_vwl + f.n_back_unr, 'ɤ̈', tr.U],  # pyrefly: ignore[missing-attribute]
    ['on', f.c_mid_vwl + f.n_back_rnd, 'ö', tr.O],  # pyrefly: ignore[missing-attribute]
    ['eo', f.c_mid_vwl + f.back_unr, 'ɤ', tr.U],  # pyrefly: ignore[missing-attribute]
    ['o', f.c_mid_vwl + f.back_rnd, 'o', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ee', f.mid_vwl + f.front_unr, 'e̞', tr.E],  # pyrefly: ignore[missing-attribute]
    ['oee', f.mid_vwl + f.front_rnd, 'ø̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['eem', f.mid_vwl + f.n_front_unr, 'e̽', tr.E],  # pyrefly: ignore[missing-attribute]
    ['oem', f.mid_vwl + f.n_front_rnd, 'ø̽', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ec', f.mid_vwl + f.center_unr, 'ə', tr.U],  # pyrefly: ignore[missing-attribute]
    ['oc', f.mid_vwl + f.center_rnd, 'ɵ̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['aan', f.mid_vwl + f.n_back_unr, 'ɤ̽', tr.U],  # pyrefly: ignore[missing-attribute]
    ['oon', f.mid_vwl + f.n_back_rnd, 'o̽', tr.O],  # pyrefly: ignore[missing-attribute]
    ['aa', f.mid_vwl + f.back_unr, 'ɤ̞', tr.U],  # pyrefly: ignore[missing-attribute]
    ['oo', f.mid_vwl + f.back_rnd, 'o̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['eh', f.o_mid_vwl + f.front_unr, 'ɛ', tr.E],  # pyrefly: ignore[missing-attribute]
    ['oe', f.o_mid_vwl + f.front_rnd, 'œ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['em', f.o_mid_vwl + f.n_front_unr, 'ɛ̈', tr.E],  # pyrefly: ignore[missing-attribute]
    ['om', f.o_mid_vwl + f.n_front_rnd, 'œ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ex', f.o_mid_vwl + f.center_unr, 'ɜ', tr.E],  # pyrefly: ignore[missing-attribute]
    ['ox', f.o_mid_vwl + f.center_rnd, 'ɞ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ahn', f.o_mid_vwl + f.n_back_unr, 'ʌ̈', tr.A],  # pyrefly: ignore[missing-attribute]
    ['ohn', f.o_mid_vwl + f.n_back_rnd, 'ɔ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ah', f.o_mid_vwl + f.back_unr, 'ʌ', tr.A],  # pyrefly: ignore[missing-attribute]
    ['oh', f.o_mid_vwl + f.back_rnd, 'ɔ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ae', f.n_open_vwl + f.front_unr, 'æ', tr.A],  # pyrefly: ignore[missing-attribute]
    ['oae', f.n_open_vwl + f.front_rnd, 'œ̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['al', f.n_open_vwl + f.n_front_unr, 'a̽', tr.A],  # pyrefly: ignore[missing-attribute]
    ['oal', f.n_open_vwl + f.n_front_rnd, 'ɶ̽', tr.O],  # pyrefly: ignore[missing-attribute]
    ['av', f.n_open_vwl + f.center_unr, 'ɐ', tr.A],  # pyrefly: ignore[missing-attribute]
    ['ov', f.n_open_vwl + f.center_rnd, 'ɞ̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['arn', f.n_open_vwl + f.n_back_unr, 'ɑ̽', tr.A],  # pyrefly: ignore[missing-attribute]
    ['orn', f.n_open_vwl + f.n_back_rnd, 'ɒ̽', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ar', f.n_open_vwl + f.back_unr, 'ʌ̞', tr.A],  # pyrefly: ignore[missing-attribute]
    ['or', f.n_open_vwl + f.back_rnd, 'ɔ̞', tr.O],  # pyrefly: ignore[missing-attribute]
    ['a', f.open_vwl + f.front_unr, 'a', tr.A],  # pyrefly: ignore[missing-attribute]
    ['oa', f.open_vwl + f.front_rnd, 'ɶ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['am', f.open_vwl + f.n_front_unr, 'æ̞', tr.A],  # pyrefly: ignore[missing-attribute]
    ['oam', f.open_vwl + f.n_front_rnd, 'ɶ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['au', f.open_vwl + f.center_unr, 'ä', tr.A],  # pyrefly: ignore[missing-attribute]
    ['ou', f.open_vwl + f.center_rnd, 'ɒ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['awn', f.open_vwl + f.n_back_unr, 'ɑ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['own', f.open_vwl + f.n_back_rnd, 'ɒ̈', tr.O],  # pyrefly: ignore[missing-attribute]
    ['aw', f.open_vwl + f.back_unr, 'ɑ', tr.O],  # pyrefly: ignore[missing-attribute]
    ['ow', f.open_vwl + f.back_rnd, 'ɒ', tr.O],  # pyrefly: ignore[missing-attribute]
]]

SIMPLE_VOWEL = UNASSIGNED_VOWEL + BASE_VOWEL


VOICED_NASAL = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['m', f.vcd_nasal + [f.bilabial], 'm', tr.M],  # pyrefly: ignore[missing-attribute]
    ['mi', f.vcd_nasal + [f.labiodental], 'ɱ', tr.M],  # pyrefly: ignore[missing-attribute]
    ['ni', f.vcd_nasal + [f.dental], 'n̪', tr.N],  # pyrefly: ignore[missing-attribute]
    ['n', f.vcd_nasal + [f.alveolar], 'n', tr.N],  # pyrefly: ignore[missing-attribute]
    ['nx', f.vcd_nasal + [f.postalveolar], 'n̠', tr.N],  # pyrefly: ignore[missing-attribute]
    ['nn', f.vcd_nasal + [f.retroflex], 'ɳ', tr.N],  # pyrefly: ignore[missing-attribute]
    ['ny', f.vcd_nasal + [f.palatal], 'ɲ', tr.S_NY],  # pyrefly: ignore[missing-attribute]
    ['ng', f.vcd_nasal + [f.velar], 'ŋ', tr.S_NG],  # pyrefly: ignore[missing-attribute]
    ['nj', f.vcd_nasal + [f.uvular], 'ɴ', tr.S_NG],  # pyrefly: ignore[missing-attribute]
]]

DEVOICED_NASAL = [mod.devoiced(phon) for phon in VOICED_NASAL]
SHORT_NASAL = VOICED_NASAL + DEVOICED_NASAL
NASAL = SHORT_NASAL

VOICELESS_STOP = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['p', f.vcl_stop + [f.bilabial], 'p', tr.P],  # pyrefly: ignore[missing-attribute]
    ['pi', f.vcl_stop + [f.labiodental], 'p̪', tr.P],  # pyrefly: ignore[missing-attribute]
    ['ti', f.vcl_stop + [f.dental], 't̪', tr.T],  # pyrefly: ignore[missing-attribute]
    ['t', f.vcl_stop + [f.alveolar], 't', tr.T],  # pyrefly: ignore[missing-attribute]
    ['tx', f.vcl_stop + [f.postalveolar], 't̠', tr.T],  # pyrefly: ignore[missing-attribute]
    ['tt', f.vcl_stop + [f.retroflex], 'ʈ', tr.T],  # pyrefly: ignore[missing-attribute]
    ['ky', f.vcl_stop + [f.palatal], 'c', tr.K + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['k', f.vcl_stop + [f.velar], 'k', tr.K],  # pyrefly: ignore[missing-attribute]
    ['q', f.vcl_stop + [f.uvular], 'q', tr.K],  # pyrefly: ignore[missing-attribute]
    ['c', f.vcl_stop + [f.epiglottal], 'ʡ', tr.K],  # pyrefly: ignore[missing-attribute]
    ['x', f.vcl_stop + [f.glottal], 'ʔ', tr.T],  # pyrefly: ignore[missing-attribute]
]]

VOICED_STOP = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['b', f.vcd_stop + [f.bilabial], 'b', tr.B],  # pyrefly: ignore[missing-attribute]
    ['bi', f.vcd_stop + [f.labiodental], 'b̪', tr.B],  # pyrefly: ignore[missing-attribute]
    ['di', f.vcd_stop + [f.dental], 'd̪', tr.D],  # pyrefly: ignore[missing-attribute]
    ['d', f.vcd_stop + [f.alveolar], 'd', tr.D],  # pyrefly: ignore[missing-attribute]
    ['dx', f.vcd_stop + [f.postalveolar], 'd̠', tr.D],  # pyrefly: ignore[missing-attribute]
    ['dd', f.vcd_stop + [f.retroflex], 'ɖ', tr.D],  # pyrefly: ignore[missing-attribute]
    ['gy', f.vcd_stop + [f.palatal], 'ɟ', tr.G + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['g', f.vcd_stop + [f.velar], 'ɡ', tr.G],  # pyrefly: ignore[missing-attribute]
    ['j', f.vcd_stop + [f.uvular], 'ɢ', tr.G],  # pyrefly: ignore[missing-attribute]
]]

EJECTIVE_STOP = [mod.nonpulmonic(phon) for phon in VOICELESS_STOP]
VOICED_IMPLOSIVE = [mod.nonpulmonic(phon) for phon in VOICED_STOP]
DEVOICED_IMPLOSIVE = [mod.devoiced(phon) for phon in VOICED_IMPLOSIVE]
IMPLOSIVE = VOICED_IMPLOSIVE + DEVOICED_IMPLOSIVE
STOP = VOICELESS_STOP + VOICED_STOP + EJECTIVE_STOP + IMPLOSIVE

VOICELESS_FRICATIVE = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['si', f.vcl_sib_fricative + [f.dental], 's̪', tr.S],  # pyrefly: ignore[missing-attribute]
    ['s', f.vcl_sib_fricative + [f.alveolar], 's', tr.S],  # pyrefly: ignore[missing-attribute]
    ['sh', f.vcl_sib_fricative + [f.postalveolar], 'ʃ', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['ss', f.vcl_sib_fricative + [f.retroflex], 'ʂ', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['sy', f.vcl_sib_fricative + [f.palatal], 'ɕ', tr.S_SH + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['ph', f.vcl_nonsib_fricative + [f.bilabial], 'ɸ', tr.F],  # pyrefly: ignore[missing-attribute]
    ['f', f.vcl_nonsib_fricative + [f.labiodental], 'f', tr.F],  # pyrefly: ignore[missing-attribute]
    ['th', f.vcl_nonsib_fricative + [f.dental], 'θ', tr.S_TH],  # pyrefly: ignore[missing-attribute]
    ['sf', f.vcl_nonsib_fricative + [f.alveolar], 'θ̠', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['sx', f.vcl_nonsib_fricative + [f.postalveolar], 'ɹ̠̊˔', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['sr', f.vcl_nonsib_fricative + [f.retroflex], 'ɻ˔̊', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['hy', f.vcl_nonsib_fricative + [f.palatal], 'ç', tr.S_SH + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['kh', f.vcl_nonsib_fricative + [f.velar], 'x', tr.H],  # pyrefly: ignore[missing-attribute]
    ['qh', f.vcl_nonsib_fricative + [f.uvular], 'χ', tr.H],  # pyrefly: ignore[missing-attribute]
    ['ch', f.vcl_nonsib_fricative + [f.pharyngeal], 'ħ', tr.H],  # pyrefly: ignore[missing-attribute]
    ['h', f.vcl_nonsib_fricative + [f.glottal], 'h', tr.H],  # pyrefly: ignore[missing-attribute]
    ['svl', f.vcl_lat_fricative + [f.dental], 'ɬ̪', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['sl', f.vcl_lat_fricative + [f.alveolar], 'ɬ', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['shl', f.vcl_lat_fricative + [f.postalveolar], 'ɬ', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['ssl', f.vcl_lat_fricative + [f.retroflex], 'ꞎ', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['sly', f.vcl_lat_fricative + [f.palatal], '𝼆', tr.S_SH],  # pyrefly: ignore[missing-attribute]
    ['khl', f.vcl_lat_fricative + [f.velar], '𝼄', tr.H],  # pyrefly: ignore[missing-attribute]
    ['qhl', f.vcl_lat_fricative + [f.uvular], '𝼄̠', tr.H],  # pyrefly: ignore[missing-attribute]
    ['fy', f.vcl_nonsib_fricative + [f.palatal, f.labial], 'ɥ̊', tr.F + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['hw', f.vcl_nonsib_fricative + f.vlr_lbl, 'ʍ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['sj', f.vcl_nonsib_fricative + f.vlr_lbl + [f.palatal], 'ɧ', tr.W],  # pyrefly: ignore[missing-attribute]
]]

VOICED_FRICATIVE = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['zi', f.vcd_sib_fricative + [f.dental], 'z̪', tr.Z],  # pyrefly: ignore[missing-attribute]
    ['z', f.vcd_sib_fricative + [f.alveolar], 'z', tr.Z],  # pyrefly: ignore[missing-attribute]
    ['zh', f.vcd_sib_fricative + [f.postalveolar], 'ʒ', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zz', f.vcd_sib_fricative + [f.retroflex], 'ʐ', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zy', f.vcd_sib_fricative + [f.palatal], 'ʑ', tr.S_ZH + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['bh', f.vcd_nonsib_fricative + [f.bilabial], 'β', tr.V],  # pyrefly: ignore[missing-attribute]
    ['v', f.vcd_nonsib_fricative + [f.labiodental], 'v', tr.V],  # pyrefly: ignore[missing-attribute]
    ['dh', f.vcd_nonsib_fricative + [f.dental], 'ð', tr.S_DH],  # pyrefly: ignore[missing-attribute]
    ['zv', f.vcd_nonsib_fricative + [f.alveolar], 'ð̠', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zx', f.vcd_nonsib_fricative + [f.postalveolar], 'ɹ̠˔', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zr', f.vcd_nonsib_fricative + [f.retroflex], 'ɻ˔', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['yy', f.vcd_nonsib_fricative + [f.palatal], 'ʝ', tr.S_ZH + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['gh', f.vcd_nonsib_fricative + [f.velar], 'ɣ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['jh', f.vcd_nonsib_fricative + [f.uvular], 'ʁ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['cha', f.vcd_nonsib_fricative + [f.pharyngeal], 'ʕ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['ha', f.vcd_nonsib_fricative + [f.glottal], 'ɦ', tr.H],  # pyrefly: ignore[missing-attribute]
    ['zvl', f.vcd_lat_fricative + [f.dental], 'ɮ̪', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zl', f.vcd_lat_fricative + [f.alveolar], 'ɮ', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zhl', f.vcd_lat_fricative + [f.postalveolar], 'ɮ', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zzl', f.vcd_lat_fricative + [f.retroflex], 'ɭ˔', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['zly', f.vcd_lat_fricative + [f.palatal], 'ʎ̝', tr.S_ZH],  # pyrefly: ignore[missing-attribute]
    ['ghl', f.vcd_lat_fricative + [f.velar], 'ʟ̝', tr.W],  # pyrefly: ignore[missing-attribute]
    ['jhl', f.vcd_lat_fricative + [f.uvular], 'ʟ̠̝', tr.W],  # pyrefly: ignore[missing-attribute]
]]

EJECTIVE_FRICATIVE = [mod.nonpulmonic(phon) for phon in VOICELESS_FRICATIVE]
FRICATIVE = VOICELESS_FRICATIVE + VOICED_FRICATIVE + EJECTIVE_FRICATIVE

CENTRAL_APPROXIMANT = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['bu', f.central_approximant + [f.bilabial], 'β̞', tr.W],  # pyrefly: ignore[missing-attribute]
    ['vu', f.central_approximant + [f.labiodental], 'ʋ', tr.V],  # pyrefly: ignore[missing-attribute]
    ['du', f.central_approximant + [f.dental], 'ɹ̪', tr.R],  # pyrefly: ignore[missing-attribute]
    ['ru', f.central_approximant + [f.alveolar], 'ɹ', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rxu', f.central_approximant + [f.postalveolar], 'ɹ̠', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rru', f.central_approximant + [f.retroflex], 'ɻ', tr.R],  # pyrefly: ignore[missing-attribute]
    ['y', f.central_approximant + [f.palatal], 'j', tr.Y],  # pyrefly: ignore[missing-attribute]
    ['gu', f.central_approximant + [f.palatal], 'ɰ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['ju', f.central_approximant + [f.uvular], 'ʁ̞', tr.W],  # pyrefly: ignore[missing-attribute]
    ['hhu', f.central_approximant + [f.pharyngeal], 'ʡ̞', tr.H],  # pyrefly: ignore[missing-attribute]
    ['hu', f.central_approximant + [f.glottal], 'ʔ̞', tr.H],  # pyrefly: ignore[missing-attribute]
    ['yw', f.central_approximant + [f.palatal, f.labial], 'ɥ', tr.W + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['wy', f.central_approximant + f.vlr_lbl + [f.palatal], 'ɥ̄', tr.W + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['w', f.central_approximant + f.vlr_lbl, 'w', tr.W],  # pyrefly: ignore[missing-attribute]
]]

LATERAL_APPROXIMANT = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['lv', f.lateral_approximant + [f.dental], 'l̪', tr.L],  # pyrefly: ignore[missing-attribute]
    ['l', f.lateral_approximant + [f.alveolar], 'l', tr.L],  # pyrefly: ignore[missing-attribute]
    ['lx', f.lateral_approximant + [f.postalveolar], 'l̠', tr.L],  # pyrefly: ignore[missing-attribute]
    ['ll', f.lateral_approximant + [f.retroflex], 'ɭ', tr.L],  # pyrefly: ignore[missing-attribute]
    ['ly', f.lateral_approximant + [f.palatal], 'ʎ', tr.L + tr.Y],  # pyrefly: ignore[missing-attribute]
    ['lg', f.lateral_approximant + [f.velar], 'ʟ', tr.W],  # pyrefly: ignore[missing-attribute]
    ['lj', f.lateral_approximant + [f.uvular], 'ʟ̠', tr.W],  # pyrefly: ignore[missing-attribute]
    ['lw', f.lateral_approximant + f.vlr_lbl, 'ɫ', tr.W],  # pyrefly: ignore[missing-attribute]
]]

APPROXIMANT = CENTRAL_APPROXIMANT + LATERAL_APPROXIMANT

VOICED_FLAP = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['bt', f.vcd_flap + [f.bilabial], 'ⱱ̟', tr.B],  # pyrefly: ignore[missing-attribute]
    ['vt', f.vcd_flap + [f.labiodental], 'ⱱ', tr.V],  # pyrefly: ignore[missing-attribute]
    ['vr', f.vcd_flap + [f.dental], 'ɾ̪', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rt', f.vcd_flap + [f.alveolar], 'ɾ', tr.R],  # pyrefly: ignore[missing-attribute]
    ['xr', f.vcd_flap + [f.postalveolar], 'ɾ̠', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rd', f.vcd_flap + [f.retroflex], 'ɽ', tr.S_RD],  # pyrefly: ignore[missing-attribute]
    ['ht', f.vcd_flap + [f.pharyngeal], 'ʡ̆', tr.H],  # pyrefly: ignore[missing-attribute]
    ['vl', f.vcd_flap + [f.dental, f.lateral], 'ɺ̪', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rl', f.vcd_flap + [f.alveolar, f.lateral], 'ɺ', tr.R],  # pyrefly: ignore[missing-attribute]
    ['xl', f.vcd_flap + [f.postalveolar, f.lateral], 'ɺ̠', tr.R],  # pyrefly: ignore[missing-attribute]
    ['lr', f.vcd_flap + [f.retroflex, f.lateral], '𝼈', tr.R],  # pyrefly: ignore[missing-attribute]
]]

DEVOICED_FLAP = [mod.devoiced(phon) for phon in VOICED_FLAP]
FLAP = VOICED_FLAP + DEVOICED_FLAP

VOICED_TRILL = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['bb', f.vcd_trill + [f.bilabial], 'ʙ', tr.B],  # pyrefly: ignore[missing-attribute]
    ['vv', f.vcd_trill + [f.labiodental], 'ⱱ̞', tr.V],  # pyrefly: ignore[missing-attribute]
    ['rv', f.vcd_trill + [f.dental], 'r̪', tr.R],  # pyrefly: ignore[missing-attribute]
    ['r', f.vcd_trill + [f.alveolar], 'r', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rx', f.vcd_trill + [f.postalveolar], 'r̠', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rr', f.vcd_trill + [f.retroflex], 'ɽr', tr.R],  # pyrefly: ignore[missing-attribute]
    ['rj', f.vcd_trill + [f.uvular], 'ʀ', tr.R],  # pyrefly: ignore[missing-attribute]
    ['hh', f.vcd_trill + [f.epiglottal], 'ʢ', tr.H],  # pyrefly: ignore[missing-attribute]
]]

DEVOICED_TRILL = [mod.devoiced(phon) for phon in VOICED_TRILL]
TRILL = VOICED_TRILL + DEVOICED_TRILL

CLICK_RELEASE = [p.Phon.base(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['pk', f.click_release + [f.bilabial], 'ʘ', tr.P],  # pyrefly: ignore[missing-attribute]
    ['ck', f.click_release + [f.dental], 'ǀ', tr.C],  # pyrefly: ignore[missing-attribute]
    ['lk', f.click_release + [f.alveolar, f.lateral], 'ǁ', tr.X],  # pyrefly: ignore[missing-attribute]
    ['tk', f.click_release + [f.alveolar], 'ǃ', tr.Q],  # pyrefly: ignore[missing-attribute]
    ['yk', f.click_release + [f.palatal], 'ǂ', tr.T],  # pyrefly: ignore[missing-attribute]
    ['rk', f.click_release + [f.retroflex], '𝼊', tr.Q],  # pyrefly: ignore[missing-attribute]
]]

SIMPLE_CONS = (
    NASAL + STOP + CLICK_RELEASE + FRICATIVE + APPROXIMANT + FLAP + TRILL
)

SIMPLE_PHON = SIMPLE_VOWEL + SIMPLE_CONS
_S = p.phon_inventory(SIMPLE_PHON)

DIPHTHONG = [mod.diphthong(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [[_S.A, _S.I], tr.S_AI],  # pyrefly: ignore[missing-attribute]
    [[_S.A, _S.U], tr.S_AU],  # pyrefly: ignore[missing-attribute]
]]

# Only the affricates whose default romanizations are different to the
# concatenation of its components are listed.
# For simplicity, stop parts of affricates are conflated.
# The T in T_SS is implicitly retroflex (TT).
VOICELESS_AFFRICATE = mod.ls_affricate(_S.T, [_S.SH, _S.SS, _S.SY], tr.S_CH)  # pyrefly: ignore[missing-attribute]
VOICED_AFFRICATE = mod.ls_affricate(_S.D, [_S.ZH, _S.ZZ, _S.ZY], tr.J)  # pyrefly: ignore[missing-attribute]
AFFRICATE = VOICELESS_AFFRICATE + VOICED_AFFRICATE

CLICK = mod.ls_click(
    [_S.K, _S.G, _S.NG, _S.Q, _S.J, _S.NJ],  # pyrefly: ignore[missing-attribute]
    CLICK_RELEASE
)

STRESS = [mod.stress(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [mod.MOD.HGH, 'ˈ'],  # primary  # pyrefly: ignore[missing-attribute]
    [mod.MOD.MDL, 'ˌ']  # secondary  # pyrefly: ignore[missing-attribute]
]]

PITCH = [mod.pitch(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [mod.MOD.TOP, '̋'],  # top, extra high  # pyrefly: ignore[missing-attribute]
    [mod.MOD.HGH, '́'],  # high  # pyrefly: ignore[missing-attribute]
    [mod.MOD.MDL, '̄'],  # mid  # pyrefly: ignore[missing-attribute]
    [mod.MOD.LOW, '̀'],  # low  # pyrefly: ignore[missing-attribute]
    [mod.MOD.BTM, '̏'],  # bottom, extra low  # pyrefly: ignore[missing-attribute]
]]

CONTOUR = [mod.contour(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [mod.MOD.RSN, '̌'],  # rising  # pyrefly: ignore[missing-attribute]
    [mod.MOD.FLN, '̂'],  # falling  # pyrefly: ignore[missing-attribute]
]]

INTONATION = [mod.intonation(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    [mod.MOD.RSN, '↗︎'],  # global rise  # pyrefly: ignore[missing-attribute]
    [mod.MOD.FLN, '↘︎'],  # globall fall  # pyrefly: ignore[missing-attribute]
    [mod.MOD.TRP, '|'],  # foot break, conflated with intonation break  # pyrefly: ignore[missing-attribute]
]]

VOWEL = SIMPLE_VOWEL + DIPHTHONG
CONSONANT = SIMPLE_CONS + CLICK + AFFRICATE
FEATURE = SILENCE + STANDALONE_FEATURE
SUPRASEGMENTAL = STRESS + PITCH + CONTOUR + INTONATION
PHONEMES = FEATURE + VOWEL + CONSONANT + SUPRASEGMENTAL
COMBINING_MODIFIERS = mod.COMBINER + [mod.MOD.DURH]  # pyrefly: ignore[missing-attribute]
MOD_INVENTORY = p.phon_inventory(COMBINING_MODIFIERS)
PHON_INVENTORY = p.phon_inventory(PHONEMES)
PHONEME_INVENTORY = p.ph_inventory(PHONEMES + COMBINING_MODIFIERS)
