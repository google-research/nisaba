# Copyright 2026 Nisaba Authors.
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

"""Brahmic to English letter spell-out rules."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import grapheme_inventory as iso
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

gr = iso.GRAPHEME_INVENTORY
tr = ltn.TRANSLIT_INVENTORY


def _letter(*graphemes: pyn.Fst) -> pyn.Fst:
  """Concatenate graphemes ignoring the right side of the alignments."""
  spelling = al.EPSILON
  for grapheme in graphemes:
    spelling = spelling + al.align(grapheme, al.R_SYMS)
  return spelling


# Vowel length is not standardised in acronyms.
_A_SGN = fl.FstList(gr.A, gr.AA).union_opt()  # pyrefly: ignore[missing-attribute]
_A_IND = fl.FstList(gr.A_I, gr.AA_I).union_opt()  # pyrefly: ignore[missing-attribute]
_E_SGN = fl.FstList(gr.E, gr.EE).union_opt()  # pyrefly: ignore[missing-attribute]
_E_IND = fl.FstList(gr.E_I, gr.EE_I).union_opt()  # pyrefly: ignore[missing-attribute]
_I_SGN = fl.FstList(gr.I, gr.II).union_opt()  # pyrefly: ignore[missing-attribute]
_I_IND = fl.FstList(gr.I_I, gr.II_I).union_opt()  # pyrefly: ignore[missing-attribute]
_O_IND = fl.FstList(gr.O_I, gr.OO_I).union_opt()  # pyrefly: ignore[missing-attribute]
_U_SGN = fl.FstList(gr.U, gr.UU).union_opt()  # pyrefly: ignore[missing-attribute]

# Nukta is frequently omitted in F and Z
_FPH = fl.FstList(gr.F, gr.PH).union_opt()  # pyrefly: ignore[missing-attribute]
_ZJ = fl.FstList(gr.J, gr.Z).union_opt()  # pyrefly: ignore[missing-attribute]


# English letter pronunciation - Brahmic character sequence matching.
_A_E = _letter(_E_IND)
_B_BI = _letter(gr.B, _I_SGN)  # pyrefly: ignore[missing-attribute]
_C_SI = _letter(gr.S, _I_SGN)  # pyrefly: ignore[missing-attribute]
_D_DDI = _letter(gr.DD, _I_SGN)  # pyrefly: ignore[missing-attribute]
_E_I = _letter(_I_IND)
_F_EFPHA = _letter(_E_IND, _FPH, gr.A)  # pyrefly: ignore[missing-attribute]
_G_JI = _letter(gr.J, _I_SGN)  # pyrefly: ignore[missing-attribute]
_H_ECA = _letter(_E_IND, gr.C, gr.A)  # pyrefly: ignore[missing-attribute]
_I_A_I = _letter(_A_IND, _I_IND)
_J_JE = _letter(gr.J, _E_SGN)  # pyrefly: ignore[missing-attribute]
_K_KE = _letter(gr.K, _E_SGN)  # pyrefly: ignore[missing-attribute]
_L_ELA = _letter(_E_IND, gr.L, gr.A)  # pyrefly: ignore[missing-attribute]
_M_EMA = _letter(_E_IND, gr.M, gr.A)  # pyrefly: ignore[missing-attribute]
_N_ENA = _letter(_E_IND, gr.N, gr.A)  # pyrefly: ignore[missing-attribute]
_O_O = _letter(_O_IND)
_P_PI = _letter(gr.P, _I_SGN)  # pyrefly: ignore[missing-attribute]
_Q_KYU = _letter(gr.K, gr.Y, _U_SGN)  # pyrefly: ignore[missing-attribute]
_R_ARA = _letter(_A_IND, gr.R, gr.A)  # pyrefly: ignore[missing-attribute]
_S_ESA = _letter(_E_IND, gr.S, gr.A)  # pyrefly: ignore[missing-attribute]
_T_TTI = _letter(gr.TT, _I_SGN)  # pyrefly: ignore[missing-attribute]
_U_YU = _letter(gr.Y, _U_SGN)  # pyrefly: ignore[missing-attribute]
_V_VI = _letter(gr.V, _I_SGN)  # pyrefly: ignore[missing-attribute]
_W_DDABLU = _letter(gr.DD, gr.A, gr.B, gr.L, _U_SGN)  # pyrefly: ignore[missing-attribute]
_W_DDABLYU = _letter(gr.DD, gr.A, gr.B, gr.L, gr.Y, _U_SGN)  # pyrefly: ignore[missing-attribute]
_W_DDABALYU = _letter(gr.DD, gr.A, gr.B, gr.A, gr.L, gr.Y, _U_SGN)  # pyrefly: ignore[missing-attribute]
_W_DDABLAYU = _letter(gr.DD, gr.A, gr.B, gr.L, gr.A, gr.Y, _U_SGN)  # pyrefly: ignore[missing-attribute]
_X_EKSA = _letter(_E_IND, gr.K, gr.S, gr.A)  # pyrefly: ignore[missing-attribute]
_Y_VA_I = _letter(gr.V, _A_SGN, _I_IND)  # pyrefly: ignore[missing-attribute]
_Z_JZEDA = _letter(_ZJ, _E_SGN, gr.DD, gr.A)  # pyrefly: ignore[missing-attribute]

_LETTERS = fl.FstList(
    _A_E, _B_BI, _C_SI, _D_DDI, _E_I, _F_EFPHA, _G_JI,
    _H_ECA, _I_A_I, _J_JE, _K_KE, _L_ELA, _M_EMA, _N_ENA,
    _O_O, _P_PI, _Q_KYU, _R_ARA, _S_ESA, _T_TTI, _U_YU, _V_VI,
    _W_DDABLU, _W_DDABLYU, _W_DDABLAYU, _W_DDABALYU,
    _X_EKSA, _Y_VA_I, _Z_JZEDA).union_star()

HI_ACRONYM_SET = [
    (_A_E, tr.A_UC),  # pyrefly: ignore[missing-attribute]
    (_B_BI, tr.B_UC),  # pyrefly: ignore[missing-attribute]
    (_C_SI, tr.C_UC),  # pyrefly: ignore[missing-attribute]
    (_D_DDI, tr.D_UC),  # pyrefly: ignore[missing-attribute]
    (_E_I, tr.E_UC),  # pyrefly: ignore[missing-attribute]
    (_F_EFPHA, tr.F_UC),  # pyrefly: ignore[missing-attribute]
    (_G_JI, tr.G_UC),  # pyrefly: ignore[missing-attribute]
    (_H_ECA, tr.H_UC),  # pyrefly: ignore[missing-attribute]
    (_I_A_I, tr.I_UC),  # pyrefly: ignore[missing-attribute]
    (_J_JE, tr.J_UC),  # pyrefly: ignore[missing-attribute]
    (_K_KE, tr.K_UC),  # pyrefly: ignore[missing-attribute]
    (_L_ELA, tr.L_UC),  # pyrefly: ignore[missing-attribute]
    (_M_EMA, tr.M_UC),  # pyrefly: ignore[missing-attribute]
    (_N_ENA, tr.N_UC),  # pyrefly: ignore[missing-attribute]
    (_O_O, tr.O_UC),  # pyrefly: ignore[missing-attribute]
    (_P_PI, tr.P_UC),  # pyrefly: ignore[missing-attribute]
    (_Q_KYU, tr.Q_UC),  # pyrefly: ignore[missing-attribute]
    (_R_ARA, tr.R_UC),  # pyrefly: ignore[missing-attribute]
    (_S_ESA, tr.S_UC),  # pyrefly: ignore[missing-attribute]
    (_T_TTI, tr.T_UC),  # pyrefly: ignore[missing-attribute]
    (_U_YU, tr.U_UC),  # pyrefly: ignore[missing-attribute]
    (_V_VI, tr.V_UC),  # pyrefly: ignore[missing-attribute]
    (_W_DDABLU, tr.W_UC),  # pyrefly: ignore[missing-attribute]
    (_W_DDABLYU, tr.W_UC),  # pyrefly: ignore[missing-attribute]
    (_W_DDABALYU, tr.W_UC),  # pyrefly: ignore[missing-attribute]
    (_W_DDABLAYU, tr.W_UC),  # pyrefly: ignore[missing-attribute]
    (_X_EKSA, tr.X_UC),  # pyrefly: ignore[missing-attribute]
    (_Y_VA_I, tr.Y_UC),  # pyrefly: ignore[missing-attribute]
    (_Z_JZEDA, tr.Z_UC),  # pyrefly: ignore[missing-attribute]
]

HI_ACR_TYP_TO_TR = rw.rewrite_ls(
    HI_ACRONYM_SET,  # pyrefly: ignore[bad-argument-type]
    al.BOS + tr.EN_LETTERS,  # pyrefly: ignore[missing-attribute]
    _LETTERS + al.EOS)

HI_ACR_TYP_TO_LTN = HI_ACR_TYP_TO_TR @ ltn.print_only_ltn()
