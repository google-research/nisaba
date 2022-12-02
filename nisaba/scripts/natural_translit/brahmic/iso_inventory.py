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
'ê': <ec>          'h': <h>           'ṟ': <rr>          '̐' : <cnd_dia>
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
import nisaba.scripts.natural_translit.common.util as u


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

A = u.enclose_grapheme('a')
AA = u.enclose_grapheme('aa')
AC = u.enclose_grapheme('ac')
E = u.enclose_grapheme('e')
EE = u.enclose_grapheme('ee')
EC = u.enclose_grapheme('ec')
I = u.enclose_grapheme('i')
II = u.enclose_grapheme('ii')
O = u.enclose_grapheme('o')
OO = u.enclose_grapheme('oo')
OC = u.enclose_grapheme('oc')
OT = u.enclose_grapheme('ot')
U = u.enclose_grapheme('u')
UU = u.enclose_grapheme('uu')
AI = u.enclose_grapheme('ai')
AU = u.enclose_grapheme('au')
L_VCL = u.enclose_grapheme('l_vcl')
LL_VCL = u.enclose_grapheme('ll_vcl')
R_VCL = u.enclose_grapheme('r_vcl')
RR_VCL = u.enclose_grapheme('rr_vcl')

VOWEL_S = p.union(
    A, AA, AC, E, EE, EC, I, II,
    O, OO, OC, OT, U, UU, AI, AU,
    L_VCL, LL_VCL, R_VCL, RR_VCL).optimize()

# Independent vowels

A_I = u.enclose_grapheme('a_i')
AA_I = u.enclose_grapheme('aa_i')
AC_I = u.enclose_grapheme('ac_i')
E_I = u.enclose_grapheme('e_i')
EE_I = u.enclose_grapheme('ee_i')
EC_I = u.enclose_grapheme('ec_i')
I_I = u.enclose_grapheme('i_i')
II_I = u.enclose_grapheme('ii_i')
O_I = u.enclose_grapheme('o_i')
OO_I = u.enclose_grapheme('oo_i')
OC_I = u.enclose_grapheme('oc_i')
U_I = u.enclose_grapheme('u_i')
UU_I = u.enclose_grapheme('uu_i')
AI_I = u.enclose_grapheme('ai_i')
AU_I = u.enclose_grapheme('au_i')
L_VCL_I = u.enclose_grapheme('l_vcl_i')
LL_VCL_I = u.enclose_grapheme('ll_vcl_i')
R_VCL_I = u.enclose_grapheme('r_vcl_i')
RR_VCL_I = u.enclose_grapheme('rr_vcl_i')


VOWEL_I = p.union(
    A_I, AA_I, AC_I, E_I, EE_I, EC_I, I_I, II_I,
    O_I, OO_I, OC_I, U_I, UU_I, AI_I, AU_I,
    L_VCL_I, LL_VCL_I, R_VCL_I, RR_VCL_I).optimize()

VOCALICS = p.union(
    L_VCL, LL_VCL, R_VCL, RR_VCL,
    L_VCL_I, LL_VCL_I, R_VCL_I, RR_VCL_I).optimize()

VOWEL = p.union(VOWEL_S, VOWEL_I).optimize()

# Consonants

# Consonants with inherent vowel

B = u.enclose_grapheme('b')
BH = u.enclose_grapheme('bh')
C = u.enclose_grapheme('c')
CH = u.enclose_grapheme('ch')
D = u.enclose_grapheme('d')
DH = u.enclose_grapheme('dh')
DD = u.enclose_grapheme('dd')
DDH = u.enclose_grapheme('ddh')
F = u.enclose_grapheme('f')
G = u.enclose_grapheme('g')
GH = u.enclose_grapheme('gh')
GG = u.enclose_grapheme('gg')
H = u.enclose_grapheme('h')
J = u.enclose_grapheme('j')
JH = u.enclose_grapheme('jh')
K = u.enclose_grapheme('k')
KH = u.enclose_grapheme('kh')
L = u.enclose_grapheme('l')
LL = u.enclose_grapheme('ll')
LR = u.enclose_grapheme('lr')
M = u.enclose_grapheme('m')
N = u.enclose_grapheme('n')
NY = u.enclose_grapheme('ny')
NG = u.enclose_grapheme('ng')
NN = u.enclose_grapheme('nn')
NA = u.enclose_grapheme('na')
P = u.enclose_grapheme('p')
PH = u.enclose_grapheme('ph')
Q = u.enclose_grapheme('q')
R = u.enclose_grapheme('r')
RD = u.enclose_grapheme('rd')
RDH = u.enclose_grapheme('rdh')
RR = u.enclose_grapheme('rr')
S = u.enclose_grapheme('s')
SH = u.enclose_grapheme('sh')
SS = u.enclose_grapheme('ss')
T = u.enclose_grapheme('t')
TH = u.enclose_grapheme('th')
TT = u.enclose_grapheme('tt')
TTH = u.enclose_grapheme('tth')
TA = u.enclose_grapheme('ta')
V = u.enclose_grapheme('v')
X = u.enclose_grapheme('x')
Y = u.enclose_grapheme('y')
YY = u.enclose_grapheme('yy')
Z = u.enclose_grapheme('z')

CONSONANT_INH = p.union(
    B, BH, C, CH, D, DH, DD, DDH,
    F, G, GH, GG, H, J, JH, K, KH,
    L, LL, LR, M, N, NY, NG, NN, NA,
    P, PH, Q, R, RD, RDH, RR, S, SH, SS,
    T, TH, TT, TTH, TA, V, X, Y, YY, Z).optimize()

# Chillu consonants

K_CHL = u.enclose_grapheme('k_chl')
L_CHL = u.enclose_grapheme('l_chl')
LL_CHL = u.enclose_grapheme('ll_chl')
N_CHL = u.enclose_grapheme('n_chl')
NN_CHL = u.enclose_grapheme('nn_chl')
RR_CHL = u.enclose_grapheme('rr_chl')
REPH = u.enclose_grapheme('reph')

CHILLU = p.union(K_CHL, L_CHL, LL_CHL, N_CHL, NN_CHL, RR_CHL, REPH).optimize()

CONSONANT = p.union(CONSONANT_INH, CHILLU).optimize()

# Coda

AVG = u.enclose_grapheme('avg')
NKT = u.enclose_grapheme('nkt')
VIS = u.enclose_grapheme('vis')
ANS = u.enclose_grapheme('ans')
CND = u.enclose_grapheme('cnd')
UPADH = u.enclose_grapheme('upadh')
JIHVA = u.enclose_grapheme('jihva')

CODA = p.union(AVG, NKT, VIS, ANS, CND, UPADH, JIHVA).optimize()

# Eyelash

R_EYE = u.enclose_grapheme('r_eye')

# Om

OM = u.enclose_grapheme('om')

# Modifiers

ASP = u.enclose_grapheme('asp')
VCL = u.enclose_grapheme('vcl')
LONG = u.enclose_grapheme('long')
CHL = u.enclose_grapheme('chl')
CND_DIA = u.enclose_grapheme('cnd_dia')
EYE = u.enclose_grapheme('eye')

MOD = p.union(ASP, VCL, LONG, CHL, CND_DIA, EYE).optimize()

# Symbols

IND = u.enclose_grapheme('ind')
ZWJ = u.enclose_grapheme('zwj')
ZWN = u.enclose_grapheme('zwn')

SYM = p.union(IND, ZWJ, ZWN).optimize()

GRAPHEME = p.union(VOWEL, CONSONANT, CODA, R_EYE, OM, MOD, SYM).optimize()
GRAPHEMES = GRAPHEME.star.optimize()
