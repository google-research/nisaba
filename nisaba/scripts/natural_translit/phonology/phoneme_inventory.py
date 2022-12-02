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

import pynini as p
import nisaba.scripts.natural_translit.common.util as u


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

ASP = u.enclose_phoneme('H')
GLIDE = u.enclose_phoneme('glide')
NSL = u.enclose_phoneme('N')
SYL = u.enclose_phoneme('V')
CMB = u.enclose_phoneme('+')

# Silence

SIL = u.enclose_phoneme('sil')

VOWEL_MODS = p.union(GLIDE, NSL).optimize()
CONSONANT_MODS = p.union(ASP, SYL).optimize()

MODS = p.union(VOWEL_MODS, CONSONANT_MODS, CMB).optimize()

# Vowels

EC = u.enclose_phoneme('ec')
EC_L = u.enclose_phoneme('ec_l')
A = u.enclose_phoneme('a')
A_L = u.enclose_phoneme('a_l')
AE = u.enclose_phoneme('ae')
AE_L = u.enclose_phoneme('ae_l')
E = u.enclose_phoneme('e')
E_L = u.enclose_phoneme('e_l')
EH = u.enclose_phoneme('eh')
EH_L = u.enclose_phoneme('eh_l')
I = u.enclose_phoneme('i')
I_L = u.enclose_phoneme('i_l')
O = u.enclose_phoneme('o')
O_L = u.enclose_phoneme('o_l')
OH = u.enclose_phoneme('oh')
OH_L = u.enclose_phoneme('oh_l')
U = u.enclose_phoneme('u')
U_L = u.enclose_phoneme('u_l')
SCHWA = u.enclose_phoneme('sch')  # unassigned inherent vowel
VCL_SCHWA = u.enclose_phoneme('@')  # pronounced schwa

# Consonants

B = u.enclose_phoneme('b')
D = u.enclose_phoneme('d')
DD = u.enclose_phoneme('dd')
DI = u.enclose_phoneme('di')
F = u.enclose_phoneme('f')
G = u.enclose_phoneme('g')
H = u.enclose_phoneme('h')
K = u.enclose_phoneme('k')
L = u.enclose_phoneme('l')
LL = u.enclose_phoneme('ll')
M = u.enclose_phoneme('m')
N = u.enclose_phoneme('n')
NG = u.enclose_phoneme('ng')
NI = u.enclose_phoneme('ni')
NN = u.enclose_phoneme('nn')
NY = u.enclose_phoneme('ny')
P = u.enclose_phoneme('p')
Q = u.enclose_phoneme('q')
R = u.enclose_phoneme('r')
RRT = u.enclose_phoneme('rrt')
RRU = u.enclose_phoneme('rru')
RT = u.enclose_phoneme('rt')
S = u.enclose_phoneme('s')
SH = u.enclose_phoneme('sh')
SS = u.enclose_phoneme('ss')
T = u.enclose_phoneme('t')
TI = u.enclose_phoneme('ti')
TT = u.enclose_phoneme('tt')
VU = u.enclose_phoneme('vu')
KH = u.enclose_phoneme('kh')
GH = u.enclose_phoneme('gh')
Y = u.enclose_phoneme('y')
Z = u.enclose_phoneme('z')
ZH = u.enclose_phoneme('zh')

TSH = T + CMB + SH
DZH = D + CMB + ZH

VOWEL_SHORT = (
    p.union(EC, A, AE, E, EH, I, O, OH, U, SCHWA).optimize() +
    VOWEL_MODS.star.optimize())
VOWEL_LONG = (
    p.union(EC_L, A_L, AE_L, E_L, EH_L, I_L, O_L, OH_L, U_L).optimize() +
    VOWEL_MODS.star)
VOWEL = p.union(VOWEL_SHORT, VOWEL_LONG).optimize()

LABIAL = p.union(B, M, P).optimize()
DENTAL = p.union(DI, NI, TI).optimize()
ALVEOLAR = p.union(D, N, T).optimize()
PALATAL = p.union(Y, NY).optimize()
RETROFLEX = p.union(DD, NN, TT).optimize()
VELAR = p.union(G, NG, K).optimize()
NASAL = p.union(M, N, NI, NG, NN, NY).optimize()

STOP_UNASP = p.union(
    P, B,
    TI, DI,
    T, D,
    TT, DD,
    K, G, Q).optimize()

STOP_ASP = STOP_UNASP + ASP

STOP = p.union(STOP_UNASP, STOP_ASP).optimize()

FRICATIVE = p.union(F, S, Z, SH, SS, KH, GH, H).optimize()

SIBILANT = p.union(S, Z, SH, SS).optimize()

AFFRICATE_UNASP = p.union(TSH, DZH).optimize()

AFFRICATE_ASP = AFFRICATE_UNASP + ASP

AFFRICATE = p.union(AFFRICATE_UNASP, AFFRICATE_ASP).optimize()

VOICED = p.union(B, DI, D, DD, G, DZH, F, Z).optimize() + ASP.ques

APPROXIMANT = p.union(VU, RRU, Y).optimize()

RHOTIC = p.union(R, RT, RRT, RRU).optimize() + ASP.ques

LATERAL = p.union(L, LL).optimize()

LIQUID = p.union(RHOTIC, LATERAL).optimize()

CONSONANT = p.union(NASAL, STOP, FRICATIVE, AFFRICATE,
                    APPROXIMANT, LIQUID).optimize()

PHONEME = p.union(ASP, GLIDE, NSL, SYL, SIL,
                  EC, EC_L, A, A_L, AE, AE_L,
                  E, E_L, EH, EH_L, I, I_L,
                  O, O_L, OH, OH_L, U, U_L,
                  B, TSH, D, DD, DI, F, G, H,
                  DZH, K, L, LL, M,
                  N, NG, NI, NN, NY,
                  P, Q, R, RRT, RRU, RT,
                  S, SH, SS, T, TI, TT, VU,
                  KH, GH, Y, Z, SCHWA).optimize()

PHONEMES = PHONEME.star.optimize()
