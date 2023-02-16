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

"""txn pronunciation romanization."""

from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

tr = ltn.TRANSLIT_INVENTORY

VOWEL_DIPHTHONG = ls.cross_union([
    [ph.AI, tr.S_AI],
    [ph.AU, tr.S_AU],
])

MAP_VOWEL_DIPHTHONG = rw.rewrite_op(VOWEL_DIPHTHONG)

VOWEL_SHORT = ls.cross_union([
    [ph.A, tr.A],
    [ph.AE, tr.S_AE],
    [ph.E, tr.E],
    [ph.EC, tr.A],
    [ph.I, tr.I],
    [ph.O, tr.O],
    [ph.U, tr.U],
])

MAP_VOWEL_SHORT = rw.rewrite_op(VOWEL_SHORT)

VOWEL_LONG = ls.cross_union([
    [ph.A_L, tr.S_AA],
    [ph.E_L, tr.S_EE],
    [ph.EH_L, tr.S_EE],
    [ph.I_L, tr.S_II],
    [ph.O_L, tr.S_OO],
    [ph.OH_L, tr.S_OO],
    [ph.U_L, tr.S_UU],
])

MAP_VOWEL_LONG = rw.rewrite_op(VOWEL_LONG)

VOWEL_IGNORE_LENGTH = ls.cross_union([
    [ph.A_L, tr.A],
    [ph.E_L, tr.E],
    [ph.EH_L, tr.E],
    [ph.I_L, tr.I],
    [ph.O_L, tr.O],
    [ph.OH_L, tr.O],
    [ph.U_L, tr.U],
])

MAP_VOWEL_IGNORE_LENGTH = rw.rewrite_op(VOWEL_IGNORE_LENGTH)

AFFRICATE = ls.cross_union([
    [ph.DZH, tr.J],
    [ph.TSH, tr.S_CH],
])

CONSONANT = ls.cross_union([
    [ph.B, tr.B],
    [ph.DD, tr.D],
    [ph.DI, tr.D],
    [ph.F, tr.F],
    [ph.G, tr.G],
    [ph.H, tr.H],
    [ph.K, tr.K],
    [ph.L, tr.L],
    [ph.LL, tr.L],
    [ph.M, tr.M],
    [ph.N, tr.N],
    [ph.NG, tr.S_NG],
    [ph.NI, tr.N],
    [ph.NN, tr.N],
    [ph.NY, tr.S_NY],
    [ph.P, tr.P],
    [ph.Q, tr.K],
    [ph.R, tr.R],
    [ph.RRT, tr.S_RD],
    [ph.RRU, tr.S_ZH],
    [ph.RT, tr.R],
    [ph.S, tr.S],
    [ph.SH, tr.S_SH],
    [ph.SS, tr.S_SH],
    [ph.T, tr.T],
    [ph.TI, tr.T],
    [ph.TT, tr.T],
    [ph.VU, tr.V],
    [ph.KH, tr.S_KH],
    [ph.GH, tr.G],
    [ph.Y, tr.Y],
    [ph.Z, tr.Z],
])

MAP_CONSONANT = (rw.rewrite_op(AFFRICATE) @
                 rw.rewrite_op(CONSONANT)).optimize()

FEATURE = ls.cross_union([
    [ph.ASP, tr.H],
    [ph.NSL, tr.N],
    [ph.SIL, tr.DEL],
    [ph.SCHWA, tr.DEL],
    [ph.SYL, tr.I],
    [ph.SYL_L, tr.S_II],
    [ph.CMB, tr.DEL],
])

MAP_FEATURE = rw.rewrite_op(FEATURE)
