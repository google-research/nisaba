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

import pynini as p
import nisaba.scripts.natural_translit.common.util as u


A = u.enclose_translit('a')
AA = u.enclose_translit('aa')
AE = u.enclose_translit('ae')
B = u.enclose_translit('b')
C = u.enclose_translit('c')
CH = u.enclose_translit('ch')
D = u.enclose_translit('d')
E = u.enclose_translit('e')
EE = u.enclose_translit('ee')
F = u.enclose_translit('f')
G = u.enclose_translit('g')
H = u.enclose_translit('h')
I = u.enclose_translit('i')
II = u.enclose_translit('ii')
J = u.enclose_translit('j')
K = u.enclose_translit('k')
KH = u.enclose_translit('kh')
L = u.enclose_translit('l')
M = u.enclose_translit('m')
N = u.enclose_translit('n')
NG = u.enclose_translit('ng')
NY = u.enclose_translit('ny')
O = u.enclose_translit('o')
OO = u.enclose_translit('oo')
P = u.enclose_translit('p')
Q = u.enclose_translit('q')
R = u.enclose_translit('r')
RD = u.enclose_translit('rd')
S = u.enclose_translit('s')
SH = u.enclose_translit('sh')
T = u.enclose_translit('t')
TH = u.enclose_translit('th')
U = u.enclose_translit('u')
UU = u.enclose_translit('uu')
V = u.enclose_translit('v')
W = u.enclose_translit('w')
X = u.enclose_translit('x')
Y = u.enclose_translit('y')
Z = u.enclose_translit('z')
ZH = u.enclose_translit('zh')
DEL = u.enclose_translit(u.EPSILON)

A_UPPER = u.enclose_translit('A')
B_UPPER = u.enclose_translit('B')
C_UPPER = u.enclose_translit('C')
D_UPPER = u.enclose_translit('D')
E_UPPER = u.enclose_translit('E')
F_UPPER = u.enclose_translit('F')
G_UPPER = u.enclose_translit('G')
H_UPPER = u.enclose_translit('H')
I_UPPER = u.enclose_translit('I')
J_UPPER = u.enclose_translit('J')
K_UPPER = u.enclose_translit('K')
L_UPPER = u.enclose_translit('L')
M_UPPER = u.enclose_translit('M')
N_UPPER = u.enclose_translit('N')
O_UPPER = u.enclose_translit('O')
P_UPPER = u.enclose_translit('P')
Q_UPPER = u.enclose_translit('Q')
R_UPPER = u.enclose_translit('R')
S_UPPER = u.enclose_translit('S')
T_UPPER = u.enclose_translit('T')
U_UPPER = u.enclose_translit('U')
V_UPPER = u.enclose_translit('V')
W_UPPER = u.enclose_translit('W')
X_UPPER = u.enclose_translit('X')
Y_UPPER = u.enclose_translit('Y')
Z_UPPER = u.enclose_translit('Z')

TRANSLIT_LOWER = p.union(
    A, AA, AE, B, C, CH, D, E, EE,
    F, G, H, I, II, J, K, KH, L, M,
    N, NG, NY, O, OO, P, Q, R, RD, S, SH,
    T, TH, U, UU, V, W, Y, Z, ZH).optimize()

TRANSLIT_UPPER = p.union(
    A_UPPER, B_UPPER, C_UPPER, D_UPPER, E_UPPER, F_UPPER, G_UPPER,
    H_UPPER, I_UPPER, J_UPPER, K_UPPER, L_UPPER, M_UPPER, N_UPPER,
    O_UPPER, P_UPPER, Q_UPPER, R_UPPER, S_UPPER, T_UPPER, U_UPPER,
    V_UPPER, W_UPPER, X_UPPER, Y_UPPER, Z_UPPER).optimize()

TRANSLIT = p.union(TRANSLIT_LOWER, TRANSLIT_UPPER).optimize()

TRANSLITS = TRANSLIT.star.optimize()

EN_LETTERS = TRANSLIT_UPPER.star.optimize()
