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
'ạ': <an>

"""

from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls


# ISO mapping

A_ISO = 'a'
AA_ISO = 'ā'
AC_ISO = 'æ'
AN_ISO = 'ạ'
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

A = al.enclose_grapheme('a')
AA = al.enclose_grapheme('aa')
AC = al.enclose_grapheme('ac')
AN = al.enclose_grapheme('an')
AAN = al.enclose_grapheme('aan')
E = al.enclose_grapheme('e')
EE = al.enclose_grapheme('ee')
EC = al.enclose_grapheme('ec')
I = al.enclose_grapheme('i')
II = al.enclose_grapheme('ii')
O = al.enclose_grapheme('o')
OO = al.enclose_grapheme('oo')
OC = al.enclose_grapheme('oc')
OT = al.enclose_grapheme('ot')
U = al.enclose_grapheme('u')
UU = al.enclose_grapheme('uu')
AI = al.enclose_grapheme('ai')
AU = al.enclose_grapheme('au')
L_VCL = al.enclose_grapheme('l_vcl')
LL_VCL = al.enclose_grapheme('ll_vcl')
R_VCL = al.enclose_grapheme('r_vcl')
RR_VCL = al.enclose_grapheme('rr_vcl')

VOWEL_S = ls.union_opt(
    A, AA, AC, AN, AAN, E, EE, EC, I, II,
    O, OO, OC, OT, U, UU, AI, AU,
    L_VCL, LL_VCL, R_VCL, RR_VCL)

# Independent vowels

A_I = al.enclose_grapheme('a_i')
AA_I = al.enclose_grapheme('aa_i')
AC_I = al.enclose_grapheme('ac_i')
E_I = al.enclose_grapheme('e_i')
EE_I = al.enclose_grapheme('ee_i')
EC_I = al.enclose_grapheme('ec_i')
I_I = al.enclose_grapheme('i_i')
II_I = al.enclose_grapheme('ii_i')
O_I = al.enclose_grapheme('o_i')
OO_I = al.enclose_grapheme('oo_i')
OC_I = al.enclose_grapheme('oc_i')
U_I = al.enclose_grapheme('u_i')
UU_I = al.enclose_grapheme('uu_i')
AI_I = al.enclose_grapheme('ai_i')
AU_I = al.enclose_grapheme('au_i')
L_VCL_I = al.enclose_grapheme('l_vcl_i')
LL_VCL_I = al.enclose_grapheme('ll_vcl_i')
R_VCL_I = al.enclose_grapheme('r_vcl_i')
RR_VCL_I = al.enclose_grapheme('rr_vcl_i')


VOWEL_I = ls.union_opt(
    A_I, AA_I, AC_I, E_I, EE_I, EC_I, I_I, II_I,
    O_I, OO_I, OC_I, U_I, UU_I, AI_I, AU_I,
    L_VCL_I, LL_VCL_I, R_VCL_I, RR_VCL_I)

VOCALICS = ls.union_opt(
    L_VCL, LL_VCL, R_VCL, RR_VCL,
    L_VCL_I, LL_VCL_I, R_VCL_I, RR_VCL_I)

VOWEL = ls.union_opt(VOWEL_S, VOWEL_I)

# Consonants

# Consonants with inherent vowel

B = al.enclose_grapheme('b')
BH = al.enclose_grapheme('bh')
C = al.enclose_grapheme('c')
CH = al.enclose_grapheme('ch')
D = al.enclose_grapheme('d')
DH = al.enclose_grapheme('dh')
DD = al.enclose_grapheme('dd')
DDH = al.enclose_grapheme('ddh')
F = al.enclose_grapheme('f')
G = al.enclose_grapheme('g')
GH = al.enclose_grapheme('gh')
GG = al.enclose_grapheme('gg')
H = al.enclose_grapheme('h')
J = al.enclose_grapheme('j')
JH = al.enclose_grapheme('jh')
K = al.enclose_grapheme('k')
KH = al.enclose_grapheme('kh')
L = al.enclose_grapheme('l')
LL = al.enclose_grapheme('ll')
LR = al.enclose_grapheme('lr')
M = al.enclose_grapheme('m')
N = al.enclose_grapheme('n')
NY = al.enclose_grapheme('ny')
NG = al.enclose_grapheme('ng')
NN = al.enclose_grapheme('nn')
NA = al.enclose_grapheme('na')
P = al.enclose_grapheme('p')
PH = al.enclose_grapheme('ph')
Q = al.enclose_grapheme('q')
R = al.enclose_grapheme('r')
RD = al.enclose_grapheme('rd')
RDH = al.enclose_grapheme('rdh')
RR = al.enclose_grapheme('rr')
S = al.enclose_grapheme('s')
SH = al.enclose_grapheme('sh')
SS = al.enclose_grapheme('ss')
T = al.enclose_grapheme('t')
TH = al.enclose_grapheme('th')
TT = al.enclose_grapheme('tt')
TTH = al.enclose_grapheme('tth')
TA = al.enclose_grapheme('ta')
V = al.enclose_grapheme('v')
X = al.enclose_grapheme('x')
Y = al.enclose_grapheme('y')
YY = al.enclose_grapheme('yy')
Z = al.enclose_grapheme('z')

CONSONANT_INH = ls.union_opt(
    B, BH, C, CH, D, DH, DD, DDH,
    F, G, GH, GG, H, J, JH, K, KH,
    L, LL, LR, M, N, NY, NG, NN, NA,
    P, PH, Q, R, RD, RDH, RR, S, SH, SS,
    T, TH, TT, TTH, TA, V, X, Y, YY, Z)
# Chillu consonants

K_CHL = al.enclose_grapheme('k_chl')
L_CHL = al.enclose_grapheme('l_chl')
LL_CHL = al.enclose_grapheme('ll_chl')
N_CHL = al.enclose_grapheme('n_chl')
NN_CHL = al.enclose_grapheme('nn_chl')
RR_CHL = al.enclose_grapheme('rr_chl')
REPH = al.enclose_grapheme('reph')

CHILLU = ls.union_opt(K_CHL, L_CHL, LL_CHL, N_CHL, NN_CHL, RR_CHL, REPH)

CONSONANT = ls.union_opt(CONSONANT_INH, CHILLU)

# Coda

AVG = al.enclose_grapheme('avg')
NKT = al.enclose_grapheme('nkt')
VIS = al.enclose_grapheme('vis')
ANS = al.enclose_grapheme('ans')
CND = al.enclose_grapheme('cnd')
UPADH = al.enclose_grapheme('upadh')
JIHVA = al.enclose_grapheme('jihva')

CODA = ls.union_opt(AVG, NKT, VIS, ANS, CND, UPADH, JIHVA)

# Eyelash

R_EYE = al.enclose_grapheme('r_eye')

# Om

OM = al.enclose_grapheme('om')

# Modifiers

ASP = al.enclose_grapheme('asp')
VCL = al.enclose_grapheme('vcl')
LONG = al.enclose_grapheme('long')
CHL = al.enclose_grapheme('chl')
CND_DIA = al.enclose_grapheme('cnd_dia')
EYE = al.enclose_grapheme('eye')

MOD = ls.union_opt(ASP, VCL, LONG, CHL, CND_DIA, EYE)

# Symbols

IND = al.enclose_grapheme('ind')
ZWJ = al.enclose_grapheme('zwj')
ZWN = al.enclose_grapheme('zwn')

SYM = ls.union_opt(IND, ZWJ, ZWN)

GRAPHEME = ls.union_opt(VOWEL, CONSONANT, CODA, R_EYE, OM, MOD, SYM)
GRAPHEMES = ls.star_opt(GRAPHEME)
