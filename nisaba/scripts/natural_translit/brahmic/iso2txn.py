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

"""South Asian multilingual phoneme assignment."""

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso2typ
from nisaba.scripts.natural_translit.brahmic import iso_inventory as gr
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

_ASSIGN_UNMODIFIED = ls.apply_union(al.assign, [
    [gr.A, ph.SCHWA],
    [gr.AA, ph.A_L],
    [gr.AC, ph.AE],
    [gr.AN, ph.A],
    [gr.AAN, ph.A_L],
    [gr.AI, ph.AE],
    [gr.AU, ph.O_L],
    [gr.E, ph.E],
    [gr.EE, ph.E_L],
    [gr.EC, ph.AE],
    [gr.I, ph.I],
    [gr.II, ph.I_L],
    [gr.O, ph.O],
    [gr.OO, ph.O_L],
    [gr.OC, ph.O_L],
    [gr.U, ph.U],
    [gr.UU, ph.U_L],
    [gr.A_I, ph.A],
    [gr.AA_I, ph.A_L],
    [gr.AC_I, ph.AE],
    [gr.AI_I, ph.AE],
    [gr.AU_I, ph.O_L],
    [gr.E_I, ph.E],
    [gr.EE_I, ph.E_L],
    [gr.EC_I, ph.AE],
    [gr.I_I, ph.I],
    [gr.II_I, ph.I_L],
    [gr.O_I, ph.O],
    [gr.OO_I, ph.O_L],
    [gr.OC_I, ph.O_L],
    [gr.U_I, ph.U],
    [gr.UU_I, ph.U_L],
    [gr.B, ph.B],
    [gr.C, ph.TSH],
    [gr.D, ph.DI],
    [gr.DD, ph.DD],
    [gr.F, ph.F],
    [gr.G, ph.G],
    [gr.GG, ph.GH],
    [gr.H, ph.H],
    [gr.J, ph.DZH],
    [gr.K, ph.K],
    [gr.L, ph.L],
    [gr.LL, ph.L],
    [gr.LR, ph.RRU],
    [gr.M, ph.M],
    [gr.N, ph.NI],
    [gr.NY, ph.NY],
    [gr.NG, ph.NG],
    [gr.NN, ph.NN],
    [gr.NA, ph.N],
    [gr.P, ph.P],
    [gr.Q, ph.Q],
    [gr.R, ph.RT],
    [gr.RD, ph.RRT],
    [gr.RR, ph.R],
    [gr.S, ph.S],
    [gr.SH, ph.SH],
    [gr.SS, ph.SS],
    [gr.T, ph.TI],
    [gr.TT, ph.TT],
    [gr.TA, ph.T],
    [gr.V, ph.VU],
    [gr.X, ph.KH],
    [gr.Y, ph.Y],
    [gr.Z, ph.Z],
    [gr.K_CHL, ph.K],
    [gr.L_CHL, ph.L],
    [gr.LL_CHL, ph.LL],
    [gr.N_CHL, ph.NI],
    [gr.NN_CHL, ph.NN],
    [gr.RR_CHL, ph.RT],
    [gr.REPH, ph.RT],
    [gr.R_EYE, ph.RT],
    [gr.AVG, ph.SIL],
    [gr.VIS, ph.H],
    [gr.ANS, ph.NSL],
    [gr.CND, ph.NSL],
    [gr.UPADH, ph.H],
    [gr.JIHVA, ph.H],
    [gr.OM, ph.O_L + ph.M],
])


def _aspirated(left_side: p.FstLike, base: p.FstLike):
  """Assigns aspirated letters with aspiration modifier."""
  return al.assign(left_side, base + ph.ASP)

_ASSIGN_ASPIRATED = ls.apply_union(_aspirated, [
    [gr.BH, ph.B],
    [gr.CH, ph.TSH],
    [gr.DH, ph.DI],
    [gr.DDH, ph.DD],
    [gr.GH, ph.G],
    [gr.JH, ph.DZH],
    [gr.KH, ph.K],
    [gr.PH, ph.P],
    [gr.RDH, ph.RRT],
    [gr.TH, ph.TI],
    [gr.TTH, ph.TT],
    [gr.YY, ph.Y],
])


def _vocalic(left_side: p.FstLike, base: p.FstLike):
  """Assigns vocal letters with syllabic modifier."""
  return al.assign(left_side, base + ph.SYL)

_ASSIGN_VOCALIC = ls.apply_union(_vocalic, [
    [gr.L_VCL, ph.L],
    [gr.LL_VCL, ph.LL],
    [gr.R_VCL, ph.RT],
    [gr.RR_VCL, ph.R],
    [gr.L_VCL_I, ph.L],
    [gr.LL_VCL_I, ph.LL],
    [gr.R_VCL_I, ph.RT],
    [gr.RR_VCL_I, ph.R],
])

# Naive grapheme to phoneme assignment.
TYP_TO_TXN = ls.union_star(
    _ASSIGN_UNMODIFIED,
    _ASSIGN_VOCALIC,
    _ASSIGN_ASPIRATED,
)


def iso_to_txn() -> p.Fst:
  """ISO graphemes to txn pronunciation."""
  return (iso2typ.iso_to_typ() @ TYP_TO_TXN).optimize()
