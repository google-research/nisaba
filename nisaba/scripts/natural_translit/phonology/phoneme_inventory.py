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

# Base Phon: Used as building blocks to derive and compose related Phons.
# Simple Phon: Non-composite, i.e. base and derived Phons.

SILENCE = [p.base_phon('sil', [f.silent], '', tr.DEL)]

STANDALONE_FEATURE = ls.apply_foreach(p.base_phon, [
    ['S', [f.syllabic], '̍', tr.U, 'SYL'],
    ['Z', [f.nonsyllabic], '̯', tr.DEL, 'NSY'],
    ['N', [f.nasal], '~', tr.N, 'NSL'],
    ['L', [f.lateral], 'ˡ', tr.L, 'LAT'],
    ['H', [f.aspirated], 'ʰ', tr.H, 'ASP'],
    ['W', [f.labial], 'ʷ', tr.W, 'LBL'],
    ['Y', [f.palatal], 'ʲ', tr.Y, 'PLT'],
    ['G', [f.velar], 'ˠ', tr.G, 'VLR'],
    ['C', [f.pharyngeal], 'ˤ', tr.H, 'PHR'],
    ['X', [f.glottal], 'ˀ', tr.H, 'GLT'],
    ['R', [f.rhotic], '˞', tr.R, 'RHT'],
    ['.', [f.interrupt], '.', tr.DEL, 'SYB']  # syllable break
])

UNASSIGNED_VOWEL = ls.apply_foreach(p.base_phon, [
    ['_', [f.vowel], '', tr.DEL, 'V_TNT'],  # tentative
    ['V', [f.vowel], '', tr.DEL, 'V_PRN'],  # pronounced
])

BASE_VOWEL = ls.apply_foreach(p.base_phon, [
    ['i', f.close_vwl + f.front_unr, 'i', tr.I],
    ['ui', f.close_vwl + f.front_rnd, 'y', tr.U],
    ['im', f.close_vwl + f.n_front_unr, 'ï', tr.I],
    ['um', f.close_vwl + f.n_front_rnd, 'ÿ', tr.U],
    ['ic', f.close_vwl + f.center_unr, 'ɨ', tr.I],
    ['uc', f.close_vwl + f.center_rnd, 'ʉ', tr.U],
    ['in', f.close_vwl + f.n_back_unr, 'ɯ̈', tr.U],
    ['un', f.close_vwl + f.n_back_rnd, 'ü', tr.U],
    ['iu', f.close_vwl + f.back_unr, 'ɯ', tr.U],
    ['u', f.close_vwl + f.back_rnd, 'u', tr.U],
    ['ie', f.n_close_vwl + f.front_unr, 'i̞', tr.I],
    ['ue', f.n_close_vwl + f.front_rnd, 'y̞', tr.U],
    ['iy', f.n_close_vwl + f.n_front_unr, 'ɪ', tr.I],
    ['uy', f.n_close_vwl + f.n_front_rnd, 'ʏ', tr.U],
    ['ix', f.n_close_vwl + f.center_unr, 'ɪ̈', tr.U],
    ['ux', f.n_close_vwl + f.center_rnd, 'ʊ̈', tr.U],
    ['iv', f.n_close_vwl + f.n_back_unr, 'ɯ̽', tr.U],
    ['uv', f.n_close_vwl + f.n_back_rnd, 'ʊ', tr.U],
    ['io', f.n_close_vwl + f.back_unr, 'ɯ̞', tr.U],
    ['uo', f.n_close_vwl + f.back_rnd, 'u̞', tr.U],
    ['e', f.c_mid_vwl + f.front_unr, 'e', tr.E],
    ['oi', f.c_mid_vwl + f.front_rnd, 'ø', tr.O],
    ['ey', f.c_mid_vwl + f.n_front_unr, 'ë', tr.E],
    ['oy', f.c_mid_vwl + f.n_front_rnd, 'ø̈', tr.O],
    ['el', f.c_mid_vwl + f.center_unr, 'ɘ', tr.U],
    ['ol', f.c_mid_vwl + f.center_rnd, 'ɵ', tr.O],
    ['en', f.c_mid_vwl + f.n_back_unr, 'ɤ̈', tr.U],
    ['on', f.c_mid_vwl + f.n_back_rnd, 'ö', tr.O],
    ['eo', f.c_mid_vwl + f.back_unr, 'ɤ', tr.U],
    ['o', f.c_mid_vwl + f.back_rnd, 'o', tr.O],
    ['ee', f.mid_vwl + f.front_unr, 'e̞', tr.E],
    ['oee', f.mid_vwl + f.front_rnd, 'ø̞', tr.O],
    ['eem', f.mid_vwl + f.n_front_unr, 'e̽', tr.E],
    ['oem', f.mid_vwl + f.n_front_rnd, 'ø̽', tr.O],
    ['ec', f.mid_vwl + f.center_unr, 'ə', tr.U],
    ['oc', f.mid_vwl + f.center_rnd, 'ɵ̞', tr.O],
    ['aan', f.mid_vwl + f.n_back_unr, 'ɤ̽', tr.U],
    ['oon', f.mid_vwl + f.n_back_rnd, 'o̽', tr.O],
    ['aa', f.mid_vwl + f.back_unr, 'ɤ̞', tr.U],
    ['oo', f.mid_vwl + f.back_rnd, 'o̞', tr.O],
    ['eh', f.o_mid_vwl + f.front_unr, 'ɛ', tr.E],
    ['oe', f.o_mid_vwl + f.front_rnd, 'œ', tr.O],
    ['em', f.o_mid_vwl + f.n_front_unr, 'ɛ̈', tr.E],
    ['om', f.o_mid_vwl + f.n_front_rnd, 'œ̈', tr.O],
    ['ex', f.o_mid_vwl + f.center_unr, 'ɜ', tr.E],
    ['ox', f.o_mid_vwl + f.center_rnd, 'ɞ', tr.O],
    ['ahn', f.o_mid_vwl + f.n_back_unr, 'ʌ̈', tr.A],
    ['ohn', f.o_mid_vwl + f.n_back_rnd, 'ɔ̈', tr.O],
    ['ah', f.o_mid_vwl + f.back_unr, 'ʌ', tr.A],
    ['oh', f.o_mid_vwl + f.back_rnd, 'ɔ', tr.O],
    ['ae', f.n_open_vwl + f.front_unr, 'æ', tr.A],
    ['oae', f.n_open_vwl + f.front_rnd, 'œ̞', tr.O],
    ['al', f.n_open_vwl + f.n_front_unr, 'a̽', tr.A],
    ['oal', f.n_open_vwl + f.n_front_rnd, 'ɶ̽', tr.O],
    ['av', f.n_open_vwl + f.center_unr, 'ɐ', tr.A],
    ['ov', f.n_open_vwl + f.center_rnd, 'ɞ̞', tr.O],
    ['arn', f.n_open_vwl + f.n_back_unr, 'ɑ̽', tr.A],
    ['orn', f.n_open_vwl + f.n_back_rnd, 'ɒ̽', tr.O],
    ['ar', f.n_open_vwl + f.back_unr, 'ʌ̞', tr.A],
    ['or', f.n_open_vwl + f.back_rnd, 'ɔ̞', tr.O],
    ['a', f.open_vwl + f.front_unr, 'a', tr.A],
    ['oa', f.open_vwl + f.front_rnd, 'ɶ', tr.O],
    ['am', f.open_vwl + f.n_front_unr, 'æ̞', tr.A],
    ['oam', f.open_vwl + f.n_front_rnd, 'ɶ̈', tr.O],
    ['au', f.open_vwl + f.center_unr, 'ä', tr.A],
    ['ou', f.open_vwl + f.center_rnd, 'ɒ̈', tr.O],
    ['awn', f.open_vwl + f.n_back_unr, 'ɑ̈', tr.O],
    ['own', f.open_vwl + f.n_back_rnd, 'ɒ̈', tr.O],
    ['aw', f.open_vwl + f.back_unr, 'ɑ', tr.O],
    ['ow', f.open_vwl + f.back_rnd, 'ɒ', tr.O],
])

SIMPLE_VOWEL = UNASSIGNED_VOWEL + BASE_VOWEL


VOICED_NASAL = ls.apply_foreach(p.base_phon, [
    ['m', f.vcd_nasal + [f.bilabial], 'm', tr.M],
    ['mi', f.vcd_nasal + [f.labiodental], 'ɱ', tr.M],
    ['ni', f.vcd_nasal + [f.dental], 'n̪', tr.N],
    ['n', f.vcd_nasal + [f.alveolar], 'n', tr.N],
    ['nx', f.vcd_nasal + [f.postalveolar], 'n̠', tr.N],
    ['nn', f.vcd_nasal + [f.retroflex], 'ɳ', tr.N],
    ['ny', f.vcd_nasal + [f.palatal], 'ɲ', tr.S_NY],
    ['ng', f.vcd_nasal + [f.velar], 'ŋ', tr.S_NG],
    ['nj', f.vcd_nasal + [f.uvular], 'ɴ', tr.S_NG],
])

DEVOICED_NASAL = [mod.devoiced(phon) for phon in VOICED_NASAL]
SHORT_NASAL = VOICED_NASAL + DEVOICED_NASAL
NASAL = SHORT_NASAL

VOICELESS_STOP = ls.apply_foreach(p.base_phon, [
    ['p', f.vcl_stop + [f.bilabial], 'p', tr.P],
    ['pi', f.vcl_stop + [f.labiodental], 'p̪', tr.P],
    ['ti', f.vcl_stop + [f.dental], 't̪', tr.T],
    ['t', f.vcl_stop + [f.alveolar], 't', tr.T],
    ['tx', f.vcl_stop + [f.postalveolar], 't̠', tr.T],
    ['tt', f.vcl_stop + [f.retroflex], 'ʈ', tr.T],
    ['ky', f.vcl_stop + [f.palatal], 'c', tr.K + tr.Y],
    ['k', f.vcl_stop + [f.velar], 'k', tr.K],
    ['q', f.vcl_stop + [f.uvular], 'q', tr.K],
    ['c', f.vcl_stop + [f.epiglottal], 'ʡ', tr.K],
    ['x', f.vcl_stop + [f.glottal], 'ʔ', tr.T],
])

VOICED_STOP = ls.apply_foreach(p.base_phon, [
    ['b', f.vcd_stop + [f.bilabial], 'b', tr.B],
    ['bi', f.vcd_stop + [f.labiodental], 'b̪', tr.B],
    ['di', f.vcd_stop + [f.dental], 'd̪', tr.D],
    ['d', f.vcd_stop + [f.alveolar], 'd', tr.D],
    ['dx', f.vcd_stop + [f.postalveolar], 'd̠', tr.D],
    ['dd', f.vcd_stop + [f.retroflex], 'ɖ', tr.D],
    ['gy', f.vcd_stop + [f.palatal], 'ɟ', tr.G + tr.Y],
    ['g', f.vcd_stop + [f.velar], 'ɡ', tr.G],
    ['j', f.vcd_stop + [f.uvular], 'ɢ', tr.G],
])

EJECTIVE_STOP = [mod.nonpulmonic(phon) for phon in VOICELESS_STOP]
VOICED_IMPLOSIVE = [mod.nonpulmonic(phon) for phon in VOICED_STOP]
DEVOICED_IMPLOSIVE = [mod.devoiced(phon) for phon in VOICED_IMPLOSIVE]
IMPLOSIVE = VOICED_IMPLOSIVE + DEVOICED_IMPLOSIVE
STOP = VOICELESS_STOP + VOICED_STOP + EJECTIVE_STOP + IMPLOSIVE

VOICELESS_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['si', f.vcl_sib_fricative + [f.dental], 's̪', tr.S],
    ['s', f.vcl_sib_fricative + [f.alveolar], 's', tr.S],
    ['sh', f.vcl_sib_fricative + [f.postalveolar], 'ʃ', tr.S_SH],
    ['ss', f.vcl_sib_fricative + [f.retroflex], 'ʂ', tr.S_SH],
    ['sy', f.vcl_sib_fricative + [f.palatal], 'ɕ', tr.S_SH + tr.Y],
    ['ph', f.vcl_nonsib_fricative + [f.bilabial], 'ɸ', tr.F],
    ['f', f.vcl_nonsib_fricative + [f.labiodental], 'f', tr.F],
    ['th', f.vcl_nonsib_fricative + [f.dental], 'θ', tr.S_TH],
    ['sf', f.vcl_nonsib_fricative + [f.alveolar], 'θ̠', tr.S_SH],
    ['sx', f.vcl_nonsib_fricative + [f.postalveolar], 'ɹ̠̊˔', tr.S_SH],
    ['sr', f.vcl_nonsib_fricative + [f.retroflex], 'ɻ˔̊', tr.S_SH],
    ['hy', f.vcl_nonsib_fricative + [f.palatal], 'ç', tr.S_SH + tr.Y],
    ['kh', f.vcl_nonsib_fricative + [f.velar], 'x', tr.H],
    ['qh', f.vcl_nonsib_fricative + [f.uvular], 'χ', tr.H],
    ['ch', f.vcl_nonsib_fricative + [f.pharyngeal], 'ħ', tr.H],
    ['h', f.vcl_nonsib_fricative + [f.glottal], 'h', tr.H],
    ['svl', f.vcl_lat_fricative + [f.dental], 'ɬ̪', tr.S_SH],
    ['sl', f.vcl_lat_fricative + [f.alveolar], 'ɬ', tr.S_SH],
    ['shl', f.vcl_lat_fricative + [f.postalveolar], 'ɬ', tr.S_SH],
    ['ssl', f.vcl_lat_fricative + [f.retroflex], 'ꞎ', tr.S_SH],
    ['sly', f.vcl_lat_fricative + [f.palatal], '𝼆', tr.S_SH],
    ['khl', f.vcl_lat_fricative + [f.velar], '𝼄', tr.H],
    ['qhl', f.vcl_lat_fricative + [f.uvular], '𝼄̠', tr.H],
    ['fy', f.vcl_nonsib_fricative + [f.palatal, f.labial], 'ɥ̊', tr.F + tr.Y],
    ['hw', f.vcl_nonsib_fricative + f.vlr_lbl, 'ʍ', tr.W],
    ['sj', f.vcl_nonsib_fricative + f.vlr_lbl + [f.palatal], 'ɧ', tr.W],
])

VOICED_FRICATIVE = ls.apply_foreach(p.base_phon, [
    ['zi', f.vcd_sib_fricative + [f.dental], 'z̪', tr.Z],
    ['z', f.vcd_sib_fricative + [f.alveolar], 'z', tr.Z],
    ['zh', f.vcd_sib_fricative + [f.postalveolar], 'ʒ', tr.S_ZH],
    ['zz', f.vcd_sib_fricative + [f.retroflex], 'ʐ', tr.S_ZH],
    ['zy', f.vcd_sib_fricative + [f.palatal], 'ʑ', tr.S_ZH + tr.Y],
    ['bh', f.vcd_nonsib_fricative + [f.bilabial], 'β', tr.V],
    ['v', f.vcd_nonsib_fricative + [f.labiodental], 'v', tr.V],
    ['dh', f.vcd_nonsib_fricative + [f.dental], 'ð', tr.S_DH],
    ['zv', f.vcd_nonsib_fricative + [f.alveolar], 'ð̠', tr.S_ZH],
    ['zx', f.vcd_nonsib_fricative + [f.postalveolar], 'ɹ̠˔', tr.S_ZH],
    ['zr', f.vcd_nonsib_fricative + [f.retroflex], 'ɻ˔', tr.S_ZH],
    ['yy', f.vcd_nonsib_fricative + [f.palatal], 'ʝ', tr.S_ZH + tr.Y],
    ['gh', f.vcd_nonsib_fricative + [f.velar], 'ɣ', tr.W],
    ['jh', f.vcd_nonsib_fricative + [f.uvular], 'ʁ', tr.W],
    ['cha', f.vcd_nonsib_fricative + [f.pharyngeal], 'ʕ', tr.W],
    ['ha', f.vcd_nonsib_fricative + [f.glottal], 'ɦ', tr.H],
    ['zvl', f.vcd_lat_fricative + [f.dental], 'ɮ̪', tr.S_ZH],
    ['zl', f.vcd_lat_fricative + [f.alveolar], 'ɮ', tr.S_ZH],
    ['zhl', f.vcd_lat_fricative + [f.postalveolar], 'ɮ', tr.S_ZH],
    ['zzl', f.vcd_lat_fricative + [f.retroflex], 'ɭ˔', tr.S_ZH],
    ['zly', f.vcd_lat_fricative + [f.palatal], 'ʎ̝', tr.S_ZH],
    ['ghl', f.vcd_lat_fricative + [f.velar], 'ʟ̝', tr.W],
    ['jhl', f.vcd_lat_fricative + [f.uvular], 'ʟ̠̝', tr.W],
])

EJECTIVE_FRICATIVE = [mod.nonpulmonic(phon) for phon in VOICELESS_FRICATIVE]
FRICATIVE = VOICELESS_FRICATIVE + VOICED_FRICATIVE + EJECTIVE_FRICATIVE

CENTRAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['bu', f.central_approximant + [f.bilabial], 'β̞', tr.W],
    ['vu', f.central_approximant + [f.labiodental], 'ʋ', tr.V],
    ['du', f.central_approximant + [f.dental], 'ɹ̪', tr.R],
    ['ru', f.central_approximant + [f.alveolar], 'ɹ', tr.R],
    ['rxu', f.central_approximant + [f.postalveolar], 'ɹ̠', tr.R],
    ['rru', f.central_approximant + [f.retroflex], 'ɻ', tr.R],
    ['y', f.central_approximant + [f.palatal], 'j', tr.Y],
    ['gu', f.central_approximant + [f.palatal], 'ɰ', tr.W],
    ['ju', f.central_approximant + [f.uvular], 'ʁ̞', tr.W],
    ['hhu', f.central_approximant + [f.pharyngeal], 'ʡ̞', tr.H],
    ['hu', f.central_approximant + [f.glottal], 'ʔ̞', tr.H],
    ['yw', f.central_approximant + [f.palatal, f.labial], 'ɥ', tr.W + tr.Y],
    ['wy', f.central_approximant + f.vlr_lbl + [f.palatal], 'ɥ̄', tr.W + tr.Y],
    ['w', f.central_approximant + f.vlr_lbl, 'w', tr.W],
])

LATERAL_APPROXIMANT = ls.apply_foreach(p.base_phon, [
    ['lv', f.lateral_approximant + [f.dental], 'l̪', tr.L],
    ['l', f.lateral_approximant + [f.alveolar], 'l', tr.L],
    ['lx', f.lateral_approximant + [f.postalveolar], 'l̠', tr.L],
    ['ll', f.lateral_approximant + [f.retroflex], 'ɭ', tr.L],
    ['ly', f.lateral_approximant + [f.palatal], 'ʎ', tr.L + tr.Y],
    ['lg', f.lateral_approximant + [f.velar], 'ʟ', tr.W],
    ['lj', f.lateral_approximant + [f.uvular], 'ʟ̠', tr.W],
    ['lw', f.lateral_approximant + f.vlr_lbl, 'ɫ', tr.W],
])

APPROXIMANT = CENTRAL_APPROXIMANT + LATERAL_APPROXIMANT

VOICED_FLAP = ls.apply_foreach(p.base_phon, [
    ['bt', f.vcd_flap + [f.bilabial], 'ⱱ̟', tr.B],
    ['vt', f.vcd_flap + [f.labiodental], 'ⱱ', tr.V],
    ['vr', f.vcd_flap + [f.dental], 'ɾ̪', tr.R],
    ['rt', f.vcd_flap + [f.alveolar], 'ɾ', tr.R],
    ['xr', f.vcd_flap + [f.postalveolar], 'ɾ̠', tr.R],
    ['rd', f.vcd_flap + [f.retroflex], 'ɽ', tr.S_RD],
    ['ht', f.vcd_flap + [f.pharyngeal], 'ʡ̆', tr.H],
    ['vl', f.vcd_flap + [f.dental, f.lateral], 'ɺ̪', tr.R],
    ['rl', f.vcd_flap + [f.alveolar, f.lateral], 'ɺ', tr.R],
    ['xl', f.vcd_flap + [f.postalveolar, f.lateral], 'ɺ̠', tr.R],
    ['lr', f.vcd_flap + [f.retroflex, f.lateral], '𝼈', tr.R],
])

DEVOICED_FLAP = [mod.devoiced(phon) for phon in VOICED_FLAP]
FLAP = VOICED_FLAP + DEVOICED_FLAP

VOICED_TRILL = ls.apply_foreach(p.base_phon, [
    ['bb', f.vcd_trill + [f.bilabial], 'ʙ', tr.B],
    ['vv', f.vcd_trill + [f.labiodental], 'ⱱ̞', tr.V],
    ['rv', f.vcd_trill + [f.dental], 'r̪', tr.R],
    ['r', f.vcd_trill + [f.alveolar], 'r', tr.R],
    ['rx', f.vcd_trill + [f.postalveolar], 'r̠', tr.R],
    ['rr', f.vcd_trill + [f.retroflex], 'ɽr', tr.R],
    ['rj', f.vcd_trill + [f.uvular], 'ʀ', tr.R],
    ['hh', f.vcd_trill + [f.epiglottal], 'ʢ', tr.H],
])

DEVOICED_TRILL = [mod.devoiced(phon) for phon in VOICED_TRILL]
TRILL = VOICED_TRILL + DEVOICED_TRILL

CLICK_RELEASE = ls.apply_foreach(p.base_phon, [
    ['pk', f.click_release + [f.bilabial], 'ʘ', tr.P],
    ['ck', f.click_release + [f.dental], 'ǀ', tr.C],
    ['lk', f.click_release + [f.alveolar, f.lateral], 'ǁ', tr.X],
    ['tk', f.click_release + [f.alveolar], 'ǃ', tr.Q],
    ['yk', f.click_release + [f.palatal], 'ǂ', tr.T],
    ['rk', f.click_release + [f.retroflex], '𝼊', tr.Q],
])

SIMPLE_CONS = (
    NASAL + STOP + CLICK_RELEASE + FRICATIVE + APPROXIMANT + FLAP + TRILL
)

SIMPLE_PHON = SIMPLE_VOWEL + SIMPLE_CONS
_S = p.phon_inventory(SIMPLE_PHON)

DIPHTHONG = ls.apply_foreach(mod.diphthong, [
    [[_S.A, _S.I], tr.S_AI],
    [[_S.A, _S.U], tr.S_AU],
])

# Only the affricates whose default romanizations are different to the
# concatenation of its componenets are listed.
# For simplicity, stop parts of affricates are conflated.
# The T in T_SS is implicitly retroflex (TT).
VOICELESS_AFFRICATE = mod.ls_affricate(_S.T, [_S.SH, _S.SS, _S.SY], tr.S_CH)
VOICED_AFFRICATE = mod.ls_affricate(_S.D, [_S.ZH, _S.ZZ, _S.ZY], tr.J)
AFFRICATE = VOICELESS_AFFRICATE + VOICED_AFFRICATE

CLICK = mod.ls_click(
    [_S.K, _S.G, _S.NG, _S.Q, _S.J, _S.NJ],
    CLICK_RELEASE
)

STRESS = ls.apply_foreach(mod.stress, [
    [mod.MOD.HGH, 'ˈ'],  # primary
    [mod.MOD.MDL, 'ˌ']  # secondary
])

PITCH = ls.apply_foreach(mod.pitch, [
    [mod.MOD.TOP, '̋'],  # top, extra high
    [mod.MOD.HGH, '́'],  # high
    [mod.MOD.MDL, '̄'],  # mid
    [mod.MOD.LOW, '̀'],  # low
    [mod.MOD.BTM, '̏'],  # bottom, extra low
])

CONTOUR = ls.apply_foreach(mod.contour, [
    [mod.MOD.RSN, '̌'],  # rising
    [mod.MOD.FLN, '̂'],  # falling
])

INTONATION = ls.apply_foreach(mod.intonation, [
    [mod.MOD.RSN, '↗︎'],  # global rise
    [mod.MOD.FLN, '↘︎'],  # globall fall
    [mod.MOD.TRP, '|'],  # foot break, conflated with intonation break
])

VOWEL = SIMPLE_VOWEL + DIPHTHONG
CONSONANT = SIMPLE_CONS + CLICK + AFFRICATE
FEATURE = SILENCE + STANDALONE_FEATURE
SUPRASEGMENTAL = STRESS + PITCH + CONTOUR + INTONATION
PHONEMES = FEATURE + VOWEL + CONSONANT + SUPRASEGMENTAL
COMBINING_MODIFIERS = mod.COMBINER + [mod.MOD.DURH]
MOD_INVENTORY = p.phon_inventory(COMBINING_MODIFIERS)
PHON_INVENTORY = p.phon_inventory(PHONEMES)
PHONEME_INVENTORY = p.ph_inventory(PHONEMES + COMBINING_MODIFIERS)
