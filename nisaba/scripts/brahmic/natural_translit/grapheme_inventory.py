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
"""Grapheme inventory.

typ is an internal typable representation for ISO characters. typ strings
are enclosed in '< >'. This library provides the constants for ISO - typ
conversion.

ISO - typ mapping

'a': <a>           'd': <d>           'ṉ': <na>          'z': <z>
'ā': <aa>          'ḍ': <dd>          'p': <p>           '’': <avg>
'æ': <ac>          'f': <f>           'q': <q>           'ˑ': <nkt>
'e': <e>           'g': <g>           'r': <r>           'ḥ': <vis>
'ē': <ee>          'ġ': <gg>          'ṛ': <rd>          'ṁ': <ans>
'ê': <ec>          'h': <h>           'ṟ': <rr>          '̐' : <cnd-dia>
'i': <i>           'j': <j>           's': <s>           'ḫ': <upadh>
'ī': <ii>          'k': <k>           'ś': <sh>          'ẖ': <jihva>
'o': <o>           'l': <l>           'ṣ': <ss>          'ʰ': <asp>
'ō': <oo>          'ḷ': <ll>          't': <t>           '̥' : <vcl>
'ô': <oc>          'ḻ': <lr>          'ṭ': <tt>          '̄' : <long>
'õ': <ot>          'm': <m>           'ṯ': <ta>          'ⸯ': <chl>
'u': <u>           'n': <n>           'v': <v>           '̆' : <eye>
'ū': <uu>          'ñ': <ny>          'x': <x>           '.': <ind>
'b': <b>           'ṅ': <ng>          'y': <y>           '+': <zwj>
'c': <c>           'ṇ': <nn>          'ẏ': <yy>          '|': <zwn>

"""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.util as u


def _enclose(sym: str) -> p.Fst():
  """Encloses typ symbols in '<' and '>'."""
  return u.enclose(sym, u.GR_L, u.GR_R)

# ISO mapping

A_ISO = 'a'
AA_ISO = 'ā'
AC_ISO = 'æ'
E_ISO = 'e'
EE_ISO = 'ē'
EC_ISO = 'ê'
I_ISO = 'i'
II_ISO = 'ī'
O_ISO = 'o'
OO_ISO = 'ō'
OC_ISO = 'ô'
OT_ISO = 'õ'
U_ISO = 'u'
UU_ISO = 'ū'
B_ISO = 'b'
C_ISO = 'c'
D_ISO = 'd'
DD_ISO = 'ḍ'
F_ISO = 'f'
G_ISO = 'g'
GG_ISO = 'ġ'
H_ISO = 'h'
J_ISO = 'j'
K_ISO = 'k'
L_ISO = 'l'
LL_ISO = 'ḷ'
LR_ISO = 'ḻ'
M_ISO = 'm'
N_ISO = 'n'
NY_ISO = 'ñ'
NG_ISO = 'ṅ'
NN_ISO = 'ṇ'
NA_ISO = 'ṉ'
P_ISO = 'p'
Q_ISO = 'q'
R_ISO = 'r'
RD_ISO = 'ṛ'
RR_ISO = 'ṟ'
S_ISO = 's'
SH_ISO = 'ś'
SS_ISO = 'ṣ'
T_ISO = 't'
TT_ISO = 'ṭ'
TA_ISO = 'ṯ'
V_ISO = 'v'
X_ISO = 'x'
Y_ISO = 'y'
YY_ISO = 'ẏ'
Z_ISO = 'z'
AVG_ISO = '’'
NKT_ISO = 'ˑ'
VIS_ISO = 'ḥ'
ANS_ISO = 'ṁ'
CND_DIA_ISO = '̐'
UPADH_ISO = 'ḫ'
JIHVA_ISO = 'ẖ'
ASP_ISO = 'ʰ'
VCL_ISO = '̥'
LONG_ISO = '̄'
CHL_ISO = 'ⸯ'
EYE_ISO = '̆'
IND_ISO = '.'
ZWJ_ISO = '+'
ZWN_ISO = '|'

# typ graphemes

# Vowels

# Inherent vowel and combining vowel signs

A = _enclose('a')
AA = _enclose('aa')
AC = _enclose('ac')
E = _enclose('e')
EE = _enclose('ee')
EC = _enclose('ec')
I = _enclose('i')
II = _enclose('ii')
O = _enclose('o')
OO = _enclose('oo')
OC = _enclose('oc')
OT = _enclose('ot')
U = _enclose('u')
UU = _enclose('uu')
AI = _enclose('ai')
AU = _enclose('au')
L_VCL = _enclose('l_vcl')
LL_VCL = _enclose('ll_vcl')
R_VCL = _enclose('r_vcl')
RR_VCL = _enclose('rr_vcl')

VOWEL_S = p.union(
    A, AA, AC, E, EE, EC, I, II,
    O, OO, OC, OT, U, UU, AI, AU,
    L_VCL, LL_VCL, R_VCL, RR_VCL).optimize()

# Independent vowels

A_I = _enclose('a_i')
AA_I = _enclose('aa_i')
AC_I = _enclose('ac_i')
E_I = _enclose('e_i')
EE_I = _enclose('ee_i')
EC_I = _enclose('ec_i')
I_I = _enclose('i_i')
II_I = _enclose('ii_i')
O_I = _enclose('o_i')
OO_I = _enclose('oo_i')
OC_I = _enclose('oc_i')
U_I = _enclose('u_i')
UU_I = _enclose('uu_i')
AI_I = _enclose('ai_i')
AU_I = _enclose('au_i')
L_VCL_I = _enclose('l_vcl_i')
LL_VCL_I = _enclose('ll_vcl_i')
R_VCL_I = _enclose('r_vcl_i')
RR_VCL_I = _enclose('rr_vcl_i')


VOWEL_I = p.union(
    A_I, AA_I, AC_I, E_I, EE_I, EC_I, I_I, II_I,
    O_I, OO_I, OC_I, U_I, UU_I, AI_I, AU_I,
    L_VCL_I, LL_VCL_I, R_VCL_I, RR_VCL_I).optimize()

VOWEL = p.union(VOWEL_S, VOWEL_I).optimize()

# Consonants

# Consonants with inherent vowel

B = _enclose('b')
BH = _enclose('bh')
C = _enclose('c')
CH = _enclose('ch')
D = _enclose('d')
DH = _enclose('dh')
DD = _enclose('dd')
DDH = _enclose('ddh')
F = _enclose('f')
G = _enclose('g')
GH = _enclose('gh')
GG = _enclose('gg')
H = _enclose('h')
J = _enclose('j')
JH = _enclose('jh')
K = _enclose('k')
KH = _enclose('kh')
L = _enclose('l')
LL = _enclose('ll')
LR = _enclose('lr')
M = _enclose('m')
N = _enclose('n')
NY = _enclose('ny')
NG = _enclose('ng')
NN = _enclose('nn')
NA = _enclose('na')
P = _enclose('p')
PH = _enclose('ph')
Q = _enclose('q')
R = _enclose('r')
RD = _enclose('rd')
RDH = _enclose('rdh')
RR = _enclose('rr')
S = _enclose('s')
SH = _enclose('sh')
SS = _enclose('ss')
T = _enclose('t')
TH = _enclose('th')
TT = _enclose('tt')
TTH = _enclose('tth')
TA = _enclose('ta')
V = _enclose('v')
X = _enclose('x')
Y = _enclose('y')
YY = _enclose('yy')
Z = _enclose('z')

CONSONANT_INH = p.union(
    B, BH, C, CH, D, DH, DD, DDH,
    F, G, GH, GG, H, J, JH, K, KH,
    L, LL, LR, M, N, NY, NG, NN, NA,
    P, PH, Q, R, RD, RDH, RR, S, SH, SS,
    T, TH, TT, TTH, TA, V, X, Y, YY, Z).optimize()

# Chillu consonants

K_CHL = _enclose('k_chl')
L_CHL = _enclose('l_chl')
LL_CHL = _enclose('ll_chl')
N_CHL = _enclose('n_chl')
NN_CHL = _enclose('nn_chl')
RR_CHL = _enclose('rr_chl')
REPH = _enclose('reph')

CHILLU = p.union(K_CHL, L_CHL, LL_CHL, N_CHL, NN_CHL, RR_CHL, REPH).optimize()

CONSONANT = p.union(CONSONANT_INH, CHILLU).optimize()

# Coda

AVG = _enclose('avg')
NKT = _enclose('nkt')
VIS = _enclose('vis')
ANS = _enclose('ans')
CND = _enclose('cnd')
UPADH = _enclose('upadh')
JIHVA = _enclose('jihva')

CODA = p.union(AVG, NKT, VIS, ANS, CND, UPADH, JIHVA).optimize()

# Eyelash

R_EYE = _enclose('r_eye')

# Om

OM = _enclose('om')

# Modifiers

ASP = _enclose('asp')
VCL = _enclose('vcl')
LONG = _enclose('long')
CHL = _enclose('chl')
CND_DIA = _enclose('cnd_dia')
EYE = _enclose('eye')

MOD = p.union(ASP, VCL, LONG, CHL, CND_DIA, EYE).optimize()

# Symbols

IND = _enclose('ind')
ZWJ = _enclose('zwj')
ZWN = _enclose('zwn')

SYM = p.union(IND, ZWJ, ZWN).optimize()

GRAPHEME = p.union(VOWEL, CONSONANT, CODA, R_EYE, OM, MOD, SYM).optimize()
GRAPHEMES = GRAPHEME.star.optimize()
