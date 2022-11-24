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

import pynini as p
import nisaba.scripts.brahmic.natural_translit.common.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.common.util as u
import nisaba.scripts.brahmic.natural_translit.latin.ltn_inventory as tr
import nisaba.scripts.brahmic.natural_translit.phonology.phoneme_inventory as ph

STRIP = rw.strip_right_side(u.TR_BOUND)

VOWEL_SHORT = p.union(
    p.cross(ph.A, tr.A),
    p.cross(ph.AE, tr.AE),
    p.cross(ph.E, tr.E),
    p.cross(ph.EC, tr.A),
    p.cross(ph.I, tr.I),
    p.cross(ph.O, tr.O),
    p.cross(ph.U, tr.U),
    ).optimize()

MAP_VOWEL_SHORT = rw.rewrite_operation(VOWEL_SHORT)

VOWEL_LONG = p.union(
    p.cross(ph.A_L, tr.AA),
    p.cross(ph.E_L, tr.EE),
    p.cross(ph.I_L, tr.II),
    p.cross(ph.O_L, tr.OO),
    p.cross(ph.U_L, tr.UU),
    ).optimize()

MAP_VOWEL_LONG = rw.rewrite_operation(VOWEL_LONG)

VOWEL_IGNORE_LENGTH = p.union(
    p.cross(ph.A_L, tr.A),
    p.cross(ph.E_L, tr.E),
    p.cross(ph.I_L, tr.I),
    p.cross(ph.O_L, tr.O),
    p.cross(ph.U_L, tr.U),
    ).optimize()

MAP_VOWEL_IGNORE_LENGTH = rw.rewrite_operation(VOWEL_IGNORE_LENGTH)

CONSONANT = p.union(
    p.cross(ph.B, tr.B),
    p.cross(ph.CH, tr.CH),
    p.cross(ph.DD, tr.D),
    p.cross(ph.DI, tr.D),
    p.cross(ph.F, tr.F),
    p.cross(ph.G, tr.G),
    p.cross(ph.H, tr.H),
    p.cross(ph.JH, tr.J),
    p.cross(ph.K, tr.K),
    p.cross(ph.L, tr.L),
    p.cross(ph.LL, tr.L),
    p.cross(ph.M, tr.M),
    p.cross(ph.N, tr.N),
    p.cross(ph.NG, tr.NG),
    p.cross(ph.NI, tr.N),
    p.cross(ph.NN, tr.N),
    p.cross(ph.NY, tr.NY),
    p.cross(ph.P, tr.P),
    p.cross(ph.Q, tr.K),
    p.cross(ph.R, tr.R),
    p.cross(ph.RRT, tr.RD),
    p.cross(ph.RRU, tr.ZH),
    p.cross(ph.RT, tr.R),
    p.cross(ph.S, tr.S),
    p.cross(ph.SH, tr.SH),
    p.cross(ph.SS, tr.SH),
    p.cross(ph.T, tr.T),
    p.cross(ph.TI, tr.T),
    p.cross(ph.TT, tr.T),
    p.cross(ph.VU, tr.V),
    p.cross(ph.X, tr.KH),
    p.cross(ph.XA, tr.G),
    p.cross(ph.Y, tr.Y),
    p.cross(ph.Z, tr.Z)
    ).optimize()

MAP_CONSONANT = rw.rewrite_operation(CONSONANT)

FEATURE = p.union(
    p.cross(ph.ASP, tr.H),
    p.cross(ph.NSL, tr.N),
    p.cross(ph.SIL, tr.DEL),
    p.cross(ph.SCHWA, tr.DEL),
    p.cross(ph.VCL, tr.I)
    ).optimize()

MAP_FEATURE = rw.rewrite_operation(FEATURE)
