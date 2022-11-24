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


def _enclose(sym: str) -> p.Fst:
  """Encloses typ symbols in '“' and '”'."""
  return u.enclose(sym, u.TR_L, u.TR_R)

A = _enclose('a')
AA = _enclose('aa')
AE = _enclose('ae')
B = _enclose('b')
C = _enclose('c')
CH = _enclose('ch')
D = _enclose('d')
E = _enclose('e')
EE = _enclose('ee')
F = _enclose('f')
G = _enclose('g')
H = _enclose('h')
I = _enclose('i')
II = _enclose('ii')
J = _enclose('j')
K = _enclose('k')
KH = _enclose('kh')
L = _enclose('l')
M = _enclose('m')
N = _enclose('n')
NG = _enclose('ng')
NY = _enclose('ny')
O = _enclose('o')
OO = _enclose('oo')
P = _enclose('p')
Q = _enclose('q')
R = _enclose('r')
RD = _enclose('rd')
S = _enclose('s')
SH = _enclose('sh')
T = _enclose('t')
TH = _enclose('th')
U = _enclose('u')
UU = _enclose('uu')
V = _enclose('v')
W = _enclose('w')
X = _enclose('x')
Y = _enclose('y')
Z = _enclose('z')
ZH = _enclose('zh')
DEL = _enclose(u.EPSILON)

TRANSLIT = p.union(A, AA, AE, B, C, CH, D, E, EE,
                   F, G, H, I, II, J, K, KH, L, M,
                   N, NG, NY, O, OO, P, Q, R, RD, S, SH,
                   T, TH, U, UU, V, W, Y, Z, ZH).optimize()

TRANSLITS = TRANSLIT.star.optimize()
