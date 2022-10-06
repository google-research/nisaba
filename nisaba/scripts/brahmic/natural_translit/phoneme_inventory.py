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

'ə' : {ec}         'ɔ'  : {oh}        'l': {l}           's': {s}
'əː': {ec_l}       'ɔː' : {oh_l}      'ɭ': {ll}          'ʃ': {sh}
'a' : {a}          'u'  : {u}         'm': {m}           'ʂ': {ss}
'aː': {a_l}        'uː' : {u_l}       'n': {n}           't': {t}
'æ' : {ae}         'b'  : {b}         'ŋ': {ng}          't̪': {ti}
'æː': {ae_l}       't͡ʃ': {ch}        'n̪': {ni}          'ʈ': {tt}
'e' : {e}          'd'  : {d}         'ɳ': {nn}          'ʋ': {vu}
'eː': {e_l}        'ɖ'  : {dd}        'ɲ': {ny}          'x': {x}
'ɛ' : {eh}         'd̪'  : {di}        'p': {p}           'ɣ': {xa}
'ɛː': {eh_l}       'f'  : {f}         'q': {q}           'j': {y}
'i' : {i}          'ɡ'  : {g}         'r': {r}           'z': {z}
'iː': {i_l}        'h'  : {h}         'ɽ': {rrt}         'ʰ': {asp}
'o' : {o}          'd͡ʒ': {jh}        'ɻ': {rru}         '̯' : {glide}
'oː': {o_l}        'k'  : {k}         'ɾ': {rt}          '~': {nsl}

"""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.util as u


def _enclose(sym: str) -> p.Fst():
  """Encloses txn symbols in '{' and '}'."""
  return u.enclose(sym, u.PH_L, u.PH_R)

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
CH_IPA = 't͡ʃ'
D_IPA = 'd'
DD_IPA = 'ɖ'
DI_IPA = 'd̪'
F_IPA = 'f'
G_IPA = 'ɡ'
H_IPA = 'h'
JH_IPA = 'd͡ʒ'
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
X_IPA = 'x'
XA_IPA = 'ɣ'
Y_IPA = 'j'
Z_IPA = 'z'
ZH_IPA = 'ʒ'
ASP_IPA = 'ʰ'
GLIDE_IPA = '̯'
NSL_IPA = '~'
SIL_IPA = ''
COMBINE_IPA = '͡'
LONG_IPA = 'ː'
FRONT_IPA = '̪'  # Combining bridge below ( ̪ )

# txn phonemes

# Modifiers

ASP = _enclose('asp')
GLIDE = _enclose('glide')
NSL = _enclose('nsl')
VCL = _enclose('vcl')

# Silence

SIL = _enclose('sil')

# Vowels

EC = _enclose('ec')
EC_L = _enclose('ec_l')
A = _enclose('a')
A_L = _enclose('a_l')
AE = _enclose('ae')
AE_L = _enclose('ae_l')
E = _enclose('e')
E_L = _enclose('e_l')
EH = _enclose('eh')
EH_L = _enclose('eh_l')
I = _enclose('i')
I_L = _enclose('i_l')
O = _enclose('o')
O_L = _enclose('o_l')
OH = _enclose('oh')
OH_L = _enclose('oh_l')
U = _enclose('u')
U_L = _enclose('u_l')
SCHWA = _enclose('schwa')

# Consonants

B = _enclose('b')
CH = _enclose('ch')
D = _enclose('d')
DD = _enclose('dd')
DI = _enclose('di')
F = _enclose('f')
G = _enclose('g')
H = _enclose('h')
JH = _enclose('jh')
K = _enclose('k')
L = _enclose('l')
LL = _enclose('ll')
M = _enclose('m')
N = _enclose('n')
NG = _enclose('ng')
NI = _enclose('ni')
NN = _enclose('nn')
NY = _enclose('ny')
P = _enclose('p')
Q = _enclose('q')
R = _enclose('r')
RRT = _enclose('rrt')
RRU = _enclose('rru')
RT = _enclose('rt')
S = _enclose('s')
SH = _enclose('sh')
SS = _enclose('ss')
T = _enclose('t')
TI = _enclose('ti')
TT = _enclose('tt')
VU = _enclose('vu')
X = _enclose('x')
XA = _enclose('xa')
Y = _enclose('y')
Z = _enclose('z')

VOWEL_SHORT = p.union(EC, A, AE, E, EH, I, O, OH, U, SCHWA).optimize()
VOWEL_LONG = p.union(EC_L, A_L, AE_L, E_L, EH_L, I_L, O_L, OH_L, U_L).optimize()
VOWEL = p.union(VOWEL_SHORT, VOWEL_LONG).optimize()

LABIAL = p.union(B, M, P).optimize()
DENTAL = p.union(DI, NI, TI).optimize()
ALVEOLAR = p.union(D, N, T).optimize()
PALATAL = p.union(Y, NY).optimize()
RETROFLEX = p.union(DD, NN, TT).optimize()
VELAR = p.union(G, NG, K).optimize()
NASAL = p.union(M, N, NI, NG, NN, NY, NSL).optimize()

STOP = p.union(P, B,
               TI, DI,
               T, D,
               TT, DD,
               K, G).optimize()

AFFRICATE = p.union(CH, JH).optimize()

APPROXIMANT = p.union(Y).optimize()

PHONEME = p.union(ASP, GLIDE, NSL, VCL, SIL,
                  EC, EC_L, A, A_L, AE, AE_L,
                  E, E_L, EH, EH_L, I, I_L,
                  O, O_L, OH, OH_L, U, U_L,
                  B, CH, D, DD, DI, F, G, H,
                  JH, K, L, LL, M,
                  N, NG, NI, NN, NY,
                  P, Q, R, RRT, RRU, RT,
                  S, SH, SS, T, TI, TT, VU,
                  X, XA, Y, Z, SCHWA).optimize()

PHONEMES = PHONEME.star.optimize()


def _ipa_utf8_characters() -> p.Fst:
  """UTF-8 IPA symbols."""
  return p.union(
      EC_IPA, EH_IPA, OH_IPA, DD_IPA, G_IPA, LL_IPA,
      NG_IPA, NY_IPA, NN_IPA, RRT_IPA, RRU_IPA, RT_IPA,
      SH_IPA, SH_IPA, SS_IPA, ZH_IPA, TT_IPA, VU_IPA, XA_IPA,
      LONG_IPA, GLIDE_IPA, FRONT_IPA, COMBINE_IPA, ASP_IPA
      ).optimize()


def sigma_star() -> p.Fst:
  """Add utf8 IPA symbols to sigma_star."""
  return p.union(u.byte.BYTE, _ipa_utf8_characters()).star.optimize()
