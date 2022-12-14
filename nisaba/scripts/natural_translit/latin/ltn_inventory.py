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
"""Transliteration inventory.

tr is an internal representation of transliteration strings. A tr string has
the same character sequence as the corresponding latin transliteration string
enclosed in “ ”. This allows for keeping track of grapheme-transliteration
alignments and disambiguates substrings.

For example, the ambiguous string 'au' is represented using the tr symbols:

'a' : “a”
'u' : “u”
'au': “au”

An operation that changes the transliteration of the phoneme {au}
from “au” to “o” only applies to “au” substrings and not “a”“u” sequences.

Currently ltn only has tranliteration symbols as all existing grammars involving
ltn are romanization grammars. When the source script is ltn the grammars will
use ltn graphemes enclosed in < >.

"""

from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

A = al.enclose_translit('a')
AA = al.enclose_translit('aa')
AE = al.enclose_translit('ae')
B = al.enclose_translit('b')
C = al.enclose_translit('c')
CH = al.enclose_translit('ch')
D = al.enclose_translit('d')
E = al.enclose_translit('e')
EE = al.enclose_translit('ee')
F = al.enclose_translit('f')
G = al.enclose_translit('g')
H = al.enclose_translit('h')
I = al.enclose_translit('i')
II = al.enclose_translit('ii')
J = al.enclose_translit('j')
K = al.enclose_translit('k')
KH = al.enclose_translit('kh')
L = al.enclose_translit('l')
M = al.enclose_translit('m')
N = al.enclose_translit('n')
NG = al.enclose_translit('ng')
NY = al.enclose_translit('ny')
O = al.enclose_translit('o')
OO = al.enclose_translit('oo')
P = al.enclose_translit('p')
Q = al.enclose_translit('q')
R = al.enclose_translit('r')
RD = al.enclose_translit('rd')
S = al.enclose_translit('s')
SH = al.enclose_translit('sh')
T = al.enclose_translit('t')
TH = al.enclose_translit('th')
U = al.enclose_translit('u')
UU = al.enclose_translit('uu')
V = al.enclose_translit('v')
W = al.enclose_translit('w')
X = al.enclose_translit('x')
Y = al.enclose_translit('y')
Z = al.enclose_translit('z')
ZH = al.enclose_translit('zh')
DEL = al.enclose_translit(al.EPSILON)

A_UPPER = al.enclose_translit('A')
B_UPPER = al.enclose_translit('B')
C_UPPER = al.enclose_translit('C')
D_UPPER = al.enclose_translit('D')
E_UPPER = al.enclose_translit('E')
F_UPPER = al.enclose_translit('F')
G_UPPER = al.enclose_translit('G')
H_UPPER = al.enclose_translit('H')
I_UPPER = al.enclose_translit('I')
J_UPPER = al.enclose_translit('J')
K_UPPER = al.enclose_translit('K')
L_UPPER = al.enclose_translit('L')
M_UPPER = al.enclose_translit('M')
N_UPPER = al.enclose_translit('N')
O_UPPER = al.enclose_translit('O')
P_UPPER = al.enclose_translit('P')
Q_UPPER = al.enclose_translit('Q')
R_UPPER = al.enclose_translit('R')
S_UPPER = al.enclose_translit('S')
T_UPPER = al.enclose_translit('T')
U_UPPER = al.enclose_translit('U')
V_UPPER = al.enclose_translit('V')
W_UPPER = al.enclose_translit('W')
X_UPPER = al.enclose_translit('X')
Y_UPPER = al.enclose_translit('Y')
Z_UPPER = al.enclose_translit('Z')

TRANSLIT_LOWER = ls.union_opt(
    A, AA, AE, B, C, CH, D, E, EE,
    F, G, H, I, II, J, K, KH, L, M,
    N, NG, NY, O, OO, P, Q, R, RD, S, SH,
    T, TH, U, UU, V, W, Y, Z, ZH)

TRANSLIT_UPPER = ls.union_opt(
    A_UPPER, B_UPPER, C_UPPER, D_UPPER, E_UPPER, F_UPPER, G_UPPER,
    H_UPPER, I_UPPER, J_UPPER, K_UPPER, L_UPPER, M_UPPER, N_UPPER,
    O_UPPER, P_UPPER, Q_UPPER, R_UPPER, S_UPPER, T_UPPER, U_UPPER,
    V_UPPER, W_UPPER, X_UPPER, Y_UPPER, Z_UPPER)

TRANSLIT = ls.union_opt(TRANSLIT_LOWER, TRANSLIT_UPPER)

TRANSLITS = ls.star_opt(TRANSLIT)

EN_LETTERS = ls.star_opt(TRANSLIT_UPPER)
