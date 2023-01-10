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

"""ISO to acronym conversion."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

gr = iso.GRAPHEME_INVENTORY
tr = ltn.TRANSLIT_INVENTORY


def _letter(graphemes: [pyn.Fst]) -> pyn.Fst:
  """Concatenate graphemes ignoring the right side of the alignments."""
  spelling = al.EPSILON
  for grapheme in graphemes:
    spelling = spelling + al.align(grapheme, al.R_SYMS)
  return spelling


# Vowel length is not standardised in acronyms.
_A_SGN = ls.union_opt(gr.A, gr.AA)
_A_IND = ls.union_opt(gr.A_I, gr.AA_I)
_E_SGN = ls.union_opt(gr.E, gr.EE)
_E_IND = ls.union_opt(gr.E_I, gr.EE_I)
_I_SGN = ls.union_opt(gr.I, gr.II)
_I_IND = ls.union_opt(gr.I_I, gr.II_I)
_O_IND = ls.union_opt(gr.O_I, gr.OO_I)
_U_SGN = ls.union_opt(gr.U, gr.UU)

# Nukta is frequently omitted in F and Z
_FPH = ls.union_opt(gr.F, gr.PH)
_ZJ = ls.union_opt(gr.J, gr.Z)


# English letter pronunciation - Brahmic character sequence matching.
_A_E = _letter([_E_IND])
_B_BI = _letter([gr.B, _I_SGN])
_C_SI = _letter([gr.S, _I_SGN])
_D_DDI = _letter([gr.DD, _I_SGN])
_E_I = _letter([_I_IND])
_F_EFPHA = _letter([_E_IND, _FPH, gr.A])
_G_JI = _letter([gr.J, _I_SGN])
_H_ECA = _letter([_E_IND, gr.C, gr.A])
_I_A_I = _letter([_A_IND, _I_IND])
_J_JE = _letter([gr.J, _E_SGN])
_K_KE = _letter([gr.K, _E_SGN])
_L_ELA = _letter([_E_IND, gr.L, gr.A])
_M_EMA = _letter([_E_IND, gr.M, gr.A])
_N_ENA = _letter([_E_IND, gr.N, gr.A])
_O_O = _letter([_O_IND])
_P_PI = _letter([gr.P, _I_SGN])
_Q_KYU = _letter([gr.K, gr.Y, _U_SGN])
_R_ARA = _letter([_A_IND, gr.R, gr.A])
_S_ESA = _letter([_E_IND, gr.S, gr.A])
_T_TTI = _letter([gr.TT, _I_SGN])
_U_YU = _letter([gr.Y, _U_SGN])
_V_VI = _letter([gr.V, _I_SGN])
_W_DDABLU = _letter([gr.DD, gr.A, gr.B, gr.L, _U_SGN])
_W_DDABLYU = _letter([gr.DD, gr.A, gr.B, gr.L, gr.Y, _U_SGN])
_W_DDABALYU = _letter([gr.DD, gr.A, gr.B, gr.A, gr.L, gr.Y, _U_SGN])
_W_DDABLAYU = _letter([gr.DD, gr.A, gr.B, gr.L, gr.A, gr.Y, _U_SGN])
_X_EKSA = _letter([_E_IND, gr.K, gr.S, gr.A])
_Y_VA_I = _letter([gr.V, _A_SGN, _I_IND])
_Z_JZEDA = _letter([_ZJ, _E_SGN, gr.DD, gr.A])

_LETTERS = ls.union_star(
    _A_E, _B_BI, _C_SI, _D_DDI, _E_I, _F_EFPHA, _G_JI,
    _H_ECA, _I_A_I, _J_JE, _K_KE, _L_ELA, _M_EMA, _N_ENA,
    _O_O, _P_PI, _Q_KYU, _R_ARA, _S_ESA, _T_TTI, _U_YU, _V_VI,
    _W_DDABLU, _W_DDABLYU, _W_DDABLAYU, _W_DDABALYU,
    _X_EKSA, _Y_VA_I, _Z_JZEDA)

HI_ACRONYM_SET = ls.cross_union([
    [_A_E, tr.A_UC],
    [_B_BI, tr.B_UC],
    [_C_SI, tr.C_UC],
    [_D_DDI, tr.D_UC],
    [_E_I, tr.E_UC],
    [_F_EFPHA, tr.F_UC],
    [_G_JI, tr.G_UC],
    [_H_ECA, tr.H_UC],
    [_I_A_I, tr.I_UC],
    [_J_JE, tr.J_UC],
    [_K_KE, tr.K_UC],
    [_L_ELA, tr.L_UC],
    [_M_EMA, tr.M_UC],
    [_N_ENA, tr.N_UC],
    [_O_O, tr.O_UC],
    [_P_PI, tr.P_UC],
    [_Q_KYU, tr.Q_UC],
    [_R_ARA, tr.R_UC],
    [_S_ESA, tr.S_UC],
    [_T_TTI, tr.T_UC],
    [_U_YU, tr.U_UC],
    [_V_VI, tr.V_UC],
    [_W_DDABLU, tr.W_UC],
    [_W_DDABLYU, tr.W_UC],
    [_W_DDABALYU, tr.W_UC],
    [_W_DDABLAYU, tr.W_UC],
    [_X_EKSA, tr.X_UC],
    [_Y_VA_I, tr.Y_UC],
    [_Z_JZEDA, tr.Z_UC],
])

HI_ACR_TYP_TO_TR = rw.rewrite_op(
    HI_ACRONYM_SET,
    al.BOS + tr.EN_LETTERS,
    _LETTERS + al.EOS)

HI_ACR_TYP_TO_LTN = HI_ACR_TYP_TO_TR @ ltn.print_only_ltn()
