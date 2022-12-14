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

from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

# IPA mapping

SCHWA_IPA = 'ə'
EC_IPA = 'ə'
EC_L_IPA = 'əː'
A_IPA = 'a'
A_L_IPA = 'aː'
AE_IPA = 'æ'
AE_L_IPA = 'æː'
E_IPA = 'e'
E_L_IPA = 'eː'
EH_IPA = 'ɛ'
EH_L_IPA = 'ɛː'
I_IPA = 'i'
I_L_IPA = 'iː'
O_IPA = 'o'
O_L_IPA = 'oː'
OH_IPA = 'ɔ'
OH_L_IPA = 'ɔː'
U_IPA = 'u'
U_L_IPA = 'uː'
B_IPA = 'b'
TSH_IPA = 't͡ʃ'
D_IPA = 'd'
DD_IPA = 'ɖ'
DI_IPA = 'd̪'
F_IPA = 'f'
G_IPA = 'ɡ'
H_IPA = 'h'
DZH_IPA = 'd͡ʒ'
K_IPA = 'k'
L_IPA = 'l'
LL_IPA = 'ɭ'
M_IPA = 'm'
N_IPA = 'n'
NG_IPA = 'ŋ'
NI_IPA = 'n̪'
NN_IPA = 'ɳ'
NY_IPA = 'ɲ'
P_IPA = 'p'
Q_IPA = 'q'
R_IPA = 'r'
RRT_IPA = 'ɽ'
RRU_IPA = 'ɻ'
RT_IPA = 'ɾ'
S_IPA = 's'
SH_IPA = 'ʃ'
SS_IPA = 'ʂ'
T_IPA = 't'
TI_IPA = 't̪'
TT_IPA = 'ʈ'
VU_IPA = 'ʋ'
KH_IPA = 'x'
GH_IPA = 'ɣ'
Y_IPA = 'j'
Z_IPA = 'z'
ZH_IPA = 'ʒ'
ASP_IPA = 'ʰ'
NSL_IPA = '~'
SIL_IPA = ''
GLIDE_IPA = '̯'  # Combining inverted breve below ( ̯ ) U+032F
SYL_IPA = '̍'  # Combining vertical line above ( ̍ ) U+030D
CMB_IPA = '͡'

# txn phonemes

# Modifiers

ASP = al.enclose_phoneme('H')
GLIDE = al.enclose_phoneme('glide')
NSL = al.enclose_phoneme('N')
SYL = al.enclose_phoneme('V')
CMB = al.enclose_phoneme('+')

# Silence

SIL = al.enclose_phoneme('sil')

VOWEL_MODS = ls.union_opt(GLIDE, NSL)
CONSONANT_MODS = ls.union_opt(ASP, SYL)

MODS = ls.union_opt(VOWEL_MODS, CONSONANT_MODS, CMB)

# Vowels

EC = al.enclose_phoneme('ec')
EC_L = al.enclose_phoneme('ec_l')
A = al.enclose_phoneme('a')
A_L = al.enclose_phoneme('a_l')
AE = al.enclose_phoneme('ae')
AE_L = al.enclose_phoneme('ae_l')
E = al.enclose_phoneme('e')
E_L = al.enclose_phoneme('e_l')
EH = al.enclose_phoneme('eh')
EH_L = al.enclose_phoneme('eh_l')
I = al.enclose_phoneme('i')
I_L = al.enclose_phoneme('i_l')
O = al.enclose_phoneme('o')
O_L = al.enclose_phoneme('o_l')
OH = al.enclose_phoneme('oh')
OH_L = al.enclose_phoneme('oh_l')
U = al.enclose_phoneme('u')
U_L = al.enclose_phoneme('u_l')
SCHWA = al.enclose_phoneme('sch')  # unassigned inherent vowel
VCL_SCHWA = al.enclose_phoneme('@')  # pronounced schwa

# Consonants

B = al.enclose_phoneme('b')
D = al.enclose_phoneme('d')
DD = al.enclose_phoneme('dd')
DI = al.enclose_phoneme('di')
F = al.enclose_phoneme('f')
G = al.enclose_phoneme('g')
H = al.enclose_phoneme('h')
K = al.enclose_phoneme('k')
L = al.enclose_phoneme('l')
LL = al.enclose_phoneme('ll')
M = al.enclose_phoneme('m')
N = al.enclose_phoneme('n')
NG = al.enclose_phoneme('ng')
NI = al.enclose_phoneme('ni')
NN = al.enclose_phoneme('nn')
NY = al.enclose_phoneme('ny')
P = al.enclose_phoneme('p')
Q = al.enclose_phoneme('q')
R = al.enclose_phoneme('r')
RRT = al.enclose_phoneme('rrt')
RRU = al.enclose_phoneme('rru')
RT = al.enclose_phoneme('rt')
S = al.enclose_phoneme('s')
SH = al.enclose_phoneme('sh')
SS = al.enclose_phoneme('ss')
T = al.enclose_phoneme('t')
TI = al.enclose_phoneme('ti')
TT = al.enclose_phoneme('tt')
VU = al.enclose_phoneme('vu')
KH = al.enclose_phoneme('kh')
GH = al.enclose_phoneme('gh')
Y = al.enclose_phoneme('y')
Z = al.enclose_phoneme('z')
ZH = al.enclose_phoneme('zh')

TSH = T + CMB + SH
DZH = D + CMB + ZH

VOWEL_SHORT = (
    ls.union_opt(EC, A, AE, E, EH, I, O, OH, U, SCHWA) +
    ls.star_opt(VOWEL_MODS))

VOWEL_LONG = (
    ls.union_opt(EC_L, A_L, AE_L, E_L, EH_L, I_L, O_L, OH_L, U_L) +
    ls.star_opt(VOWEL_MODS))
VOWEL = ls.union_opt(VOWEL_SHORT, VOWEL_LONG)

LABIAL = ls.union_opt(B, M, P)
DENTAL = ls.union_opt(DI, NI, TI)
ALVEOLAR = ls.union_opt(D, N, T)
PALATAL = ls.union_opt(Y, NY)
RETROFLEX = ls.union_opt(DD, NN, TT)
VELAR = ls.union_opt(G, NG, K)
NASAL = ls.union_opt(M, N, NI, NG, NN, NY)

STOP_UNASP = ls.union_opt(
    P, B,
    TI, DI,
    T, D,
    TT, DD,
    K, G, Q)

STOP_ASP = STOP_UNASP + ASP

STOP = ls.union_opt(STOP_UNASP, STOP_ASP)

FRICATIVE = ls.union_opt(F, S, Z, SH, SS, KH, GH, H)

SIBILANT = ls.union_opt(S, Z, SH, SS)

AFFRICATE_UNASP = ls.union_opt(TSH, DZH)

AFFRICATE_ASP = AFFRICATE_UNASP + ASP

AFFRICATE = ls.union_opt(AFFRICATE_UNASP, AFFRICATE_ASP)

VOICED = ls.union_opt(B, DI, D, DD, G, DZH, F, Z) + ASP.ques

APPROXIMANT = ls.union_opt(VU, RRU, Y)

RHOTIC = ls.union_opt(R, RT, RRT, RRU) + ASP.ques

LATERAL = ls.union_opt(L, LL)

LIQUID = ls.union_opt(RHOTIC, LATERAL)

CONSONANT = ls.union_opt(NASAL, STOP, FRICATIVE, AFFRICATE, APPROXIMANT, LIQUID)

PHONEME = ls.union_opt(
    ASP, GLIDE, NSL, SYL, SIL, EC, EC_L, A, A_L, AE, AE_L, E,
    E_L, EH, EH_L, I, I_L, O, O_L, OH, OH_L, U, U_L, B, TSH,
    D, DD, DI, F, G, H, DZH, K, L, LL, M, N, NG, NI, NN, NY,
    P, Q, R, RRT, RRU, RT, S, SH, SS, T, TI, TT, VU, KH, GH,
    Y, Z, SCHWA)

PHONEMES = ls.star_opt(PHONEME)
