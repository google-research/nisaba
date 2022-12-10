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

from nisaba.scripts.natural_translit.common import list_util as l
from nisaba.scripts.natural_translit.common import rewrite_functions as rw
from nisaba.scripts.natural_translit.common import util as u
from nisaba.scripts.natural_translit.latin import ltn_inventory as tr
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph

STRIP = rw.strip_right_side(u.TR_BOUND)

VOWEL_SHORT = l.unite_pcross([
    [[ph.A], tr.A],
    [[ph.AE], tr.AE],
    [[ph.E], tr.E],
    [[ph.EC], tr.A],
    [[ph.I], tr.I],
    [[ph.O], tr.O],
    [[ph.U], tr.U],
])

MAP_VOWEL_SHORT = rw.rewrite_operation(VOWEL_SHORT)

VOWEL_LONG = l.unite_pcross([
    [[ph.A_L], tr.AA],
    [[ph.E_L], tr.EE],
    [[ph.I_L], tr.II],
    [[ph.O_L], tr.OO],
    [[ph.U_L], tr.UU],
])

MAP_VOWEL_LONG = rw.rewrite_operation(VOWEL_LONG)

VOWEL_IGNORE_LENGTH = l.unite_pcross([
    [[ph.A_L], tr.A],
    [[ph.E_L], tr.E],
    [[ph.I_L], tr.I],
    [[ph.O_L], tr.O],
    [[ph.U_L], tr.U],
])

MAP_VOWEL_IGNORE_LENGTH = rw.rewrite_operation(VOWEL_IGNORE_LENGTH)

AFFRICATE = l.unite_pcross([
    [[ph.DZH], tr.J],
    [[ph.TSH], tr.CH],
])

CONSONANT = l.unite_pcross([
    [[ph.B], tr.B],
    [[ph.TSH], tr.CH],
    [[ph.DD], tr.D],
    [[ph.DI], tr.D],
    [[ph.F], tr.F],
    [[ph.G], tr.G],
    [[ph.H], tr.H],
    [[ph.DZH], tr.J],
    [[ph.K], tr.K],
    [[ph.L], tr.L],
    [[ph.LL], tr.L],
    [[ph.M], tr.M],
    [[ph.N], tr.N],
    [[ph.NG], tr.NG],
    [[ph.NI], tr.N],
    [[ph.NN], tr.N],
    [[ph.NY], tr.NY],
    [[ph.P], tr.P],
    [[ph.Q], tr.K],
    [[ph.R], tr.R],
    [[ph.RRT], tr.RD],
    [[ph.RRU], tr.ZH],
    [[ph.RT], tr.R],
    [[ph.S], tr.S],
    [[ph.SH], tr.SH],
    [[ph.SS], tr.SH],
    [[ph.T], tr.T],
    [[ph.TI], tr.T],
    [[ph.TT], tr.T],
    [[ph.VU], tr.V],
    [[ph.KH], tr.KH],
    [[ph.GH], tr.G],
    [[ph.Y], tr.Y],
    [[ph.Z], tr.Z],
])

MAP_CONSONANT = (rw.rewrite_operation(AFFRICATE) @
                 rw.rewrite_operation(CONSONANT)).optimize()

FEATURE = l.unite_pcross([
    [[ph.ASP], tr.H],
    [[ph.NSL], tr.N],
    [[ph.SIL], tr.DEL],
    [[ph.SCHWA], tr.DEL],
    [[ph.SYL], tr.I],
])

MAP_FEATURE = rw.rewrite_operation(FEATURE)
