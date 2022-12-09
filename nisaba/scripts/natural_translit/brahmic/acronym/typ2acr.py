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

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso_inventory as gr
from nisaba.scripts.natural_translit.common import rewrite_functions as rw
from nisaba.scripts.natural_translit.common import util as u
from nisaba.scripts.natural_translit.latin import ltn_inventory as tr


def _letter(graphemes: [p.Fst]) -> p.Fst:
  """Concatenate graphemes ignoring the right side of the alignments."""
  spelling = u.EPSILON
  for grapheme in graphemes:
    spelling = spelling + u.align(grapheme, u.PHONEMES)
  return spelling


# Vowel length is not standardised in acronyms.
_AS = p.union(gr.A, gr.AA)
_A_IS = p.union(gr.A_I, gr.AA_I)
_ES = p.union(gr.E, gr.EE)
_E_IS = p.union(gr.E_I, gr.EE_I)
_IS = p.union(gr.I, gr.II)
_I_IS = p.union(gr.I_I, gr.II_I)
_O_IS = p.union(gr.O_I, gr.OO_I)
_US = p.union(gr.U, gr.UU)


# English letter pronunciation - Brahmic character sequence matching.
_A_E = _letter([_E_IS])
_B_BI = _letter([gr.B, _IS])
_C_SI = _letter([gr.S, _IS])
_D_DDI = _letter([gr.DD, _IS])
_E_I = _letter([_I_IS])
_F_EFPHA = _letter([_E_IS, p.union(gr.F, gr.PH), gr.A])
_G_JI = _letter([gr.J, _IS])
_H_ECA = _letter([_E_IS, gr.C, gr.A])
_I_A_I = _letter([_A_IS, _I_IS])
_J_JE = _letter([gr.J, _ES])
_K_KE = _letter([gr.K, _ES])
_L_ELA = _letter([_E_IS, gr.L, gr.A])
_M_EMA = _letter([_E_IS, gr.M, gr.A])
_N_ENA = _letter([_E_IS, gr.N, gr.A])
_O_O = _letter([_O_IS])
_P_PI = _letter([gr.P, _IS])
_Q_KYU = _letter([gr.K, gr.Y, _US])
_R_ARA = _letter([_A_IS, gr.R, gr.A])
_S_ESA = _letter([_E_IS, gr.S, gr.A])
_T_TTI = _letter([gr.TT, _IS])
_U_YU = _letter([gr.Y, _US])
_V_VI = _letter([gr.V, _IS])
_W_DDABLU = _letter([gr.DD, gr.A, gr.B, gr.L, _US])
_W_DDABLYU = _letter([gr.DD, gr.A, gr.B, gr.L, gr.Y, _US])
_W_DDABALYU = _letter([gr.DD, gr.A, gr.B, gr.A, gr.L, gr.Y, _US])
_W_DDABLAYU = _letter([gr.DD, gr.A, gr.B, gr.L, gr.A, gr.Y, _US])
_X_EKSA = _letter([_E_IS, gr.K, gr.S, gr.A])
_Y_VA_I = _letter([gr.V, _AS, _I_IS])
_Z_JZEDA = _letter([p.union(gr.J, gr.Z), _ES, gr.DD, gr.A])

_LETTERS = p.union(
    _A_E, _B_BI, _C_SI, _D_DDI, _E_I, _F_EFPHA, _G_JI,
    _H_ECA, _I_A_I, _J_JE, _K_KE, _L_ELA, _M_EMA, _N_ENA,
    _O_O, _P_PI, _Q_KYU, _R_ARA, _S_ESA, _T_TTI, _U_YU, _V_VI,
    _W_DDABLU, _W_DDABLYU, _W_DDABLAYU, _W_DDABALYU,
    _X_EKSA, _Y_VA_I, _Z_JZEDA,
).star.optimize()

HI_ACRONYM_SET = p.union(
    p.cross(_A_E, tr.A_UPPER),
    p.cross(_B_BI, tr.B_UPPER),
    p.cross(_C_SI, tr.C_UPPER),
    p.cross(_D_DDI, tr.D_UPPER),
    p.cross(_E_I, tr.E_UPPER),
    p.cross(_F_EFPHA, tr.F_UPPER),
    p.cross(_G_JI, tr.G_UPPER),
    p.cross(_H_ECA, tr.H_UPPER),
    p.cross(_I_A_I, tr.I_UPPER),
    p.cross(_J_JE, tr.J_UPPER),
    p.cross(_K_KE, tr.K_UPPER),
    p.cross(_L_ELA, tr.L_UPPER),
    p.cross(_M_EMA, tr.M_UPPER),
    p.cross(_N_ENA, tr.N_UPPER),
    p.cross(_O_O, tr.O_UPPER),
    p.cross(_P_PI, tr.P_UPPER),
    p.cross(_Q_KYU, tr.Q_UPPER),
    p.cross(_R_ARA, tr.R_UPPER),
    p.cross(_S_ESA, tr.S_UPPER),
    p.cross(_T_TTI, tr.T_UPPER),
    p.cross(_U_YU, tr.U_UPPER),
    p.cross(_V_VI, tr.V_UPPER),
    p.cross(_W_DDABLU, tr.W_UPPER),
    p.cross(_W_DDABLYU, tr.W_UPPER),
    p.cross(_W_DDABALYU, tr.W_UPPER),
    p.cross(_W_DDABLAYU, tr.W_UPPER),
    p.cross(_X_EKSA, tr.X_UPPER),
    p.cross(_Y_VA_I, tr.Y_UPPER),
    p.cross(_Z_JZEDA, tr.Z_UPPER)).optimize()

HI_ACR_TYP_TO_TR = rw.rewrite_operation_by_context(
    HI_ACRONYM_SET,
    u.BOS + tr.EN_LETTERS,
    _LETTERS + u.EOS)

HI_ACR_TYP_TO_LTN = HI_ACR_TYP_TO_TR @ rw.delete(u.TR_BOUND)
