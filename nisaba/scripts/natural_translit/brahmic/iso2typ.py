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

"""ISO to typeable string conversion."""

import pynini as p
import nisaba.scripts.natural_translit.brahmic.iso_inventory as gr
import nisaba.scripts.natural_translit.common.rewrite_functions as rw


def _iso_to_decomposed_typ() -> p.Fst:
  """ISO to typable fst."""

  iso_to_typ_vowel = p.union(
      p.cross(gr.A_ISO, gr.A),
      p.cross(gr.AA_ISO, gr.AA),
      p.cross(gr.AC_ISO, gr.AC),
      p.cross(gr.E_ISO, gr.E),
      p.cross(gr.EE_ISO, gr.EE),
      p.cross(gr.EC_ISO, gr.EC),
      p.cross(gr.I_ISO, gr.I),
      p.cross(gr.II_ISO, gr.II),
      p.cross(gr.O_ISO, gr.O),
      p.cross(gr.OO_ISO, gr.OO),
      p.cross(gr.OC_ISO, gr.OC),
      p.cross(gr.OT_ISO, gr.OT),
      p.cross(gr.U_ISO, gr.U),
      p.cross(gr.UU_ISO, gr.UU)).optimize()

  iso_to_typ_consonant = p.union(
      p.cross(gr.B_ISO, gr.B),
      p.cross(gr.C_ISO, gr.C),
      p.cross(gr.D_ISO, gr.D),
      p.cross(gr.DD_ISO, gr.DD),
      p.cross(gr.F_ISO, gr.F),
      p.cross(gr.G_ISO, gr.G),
      p.cross(gr.GG_ISO, gr.GG),
      p.cross(gr.H_ISO, gr.H),
      p.cross(gr.J_ISO, gr.J),
      p.cross(gr.K_ISO, gr.K),
      p.cross(gr.L_ISO, gr.L),
      p.cross(gr.LL_ISO, gr.LL),
      p.cross(gr.LR_ISO, gr.LR),
      p.cross(gr.M_ISO, gr.M),
      p.cross(gr.N_ISO, gr.N),
      p.cross(gr.NY_ISO, gr.NY),
      p.cross(gr.NG_ISO, gr.NG),
      p.cross(gr.NN_ISO, gr.NN),
      p.cross(gr.NA_ISO, gr.NA),
      p.cross(gr.P_ISO, gr.P),
      p.cross(gr.Q_ISO, gr.Q),
      p.cross(gr.R_ISO, gr.R),
      p.cross(gr.RD_ISO, gr.RD),
      p.cross(gr.RR_ISO, gr.RR),
      p.cross(gr.S_ISO, gr.S),
      p.cross(gr.SH_ISO, gr.SH),
      p.cross(gr.SS_ISO, gr.SS),
      p.cross(gr.T_ISO, gr.T),
      p.cross(gr.TT_ISO, gr.TT),
      p.cross(gr.TA_ISO, gr.TA),
      p.cross(gr.V_ISO, gr.V),
      p.cross(gr.X_ISO, gr.X),
      p.cross(gr.Y_ISO, gr.Y),
      p.cross(gr.YY_ISO, gr.YY),
      p.cross(gr.Z_ISO, gr.Z)).optimize()

  iso_to_typ_coda = p.union(
      p.cross(gr.AVG_ISO, gr.AVG),
      p.cross(gr.NKT_ISO, gr.NKT),
      p.cross(gr.VIS_ISO, gr.VIS),
      p.cross(gr.ANS_ISO, gr.ANS),
      p.cross(gr.CND_DIA_ISO, gr.CND_DIA),
      p.cross(gr.UPADH_ISO, gr.UPADH),
      p.cross(gr.JIHVA_ISO, gr.JIHVA)).optimize()

  iso_to_typ_modifier = p.union(
      p.cross(gr.ASP_ISO, gr.ASP),
      p.cross(gr.VCL_ISO, gr.VCL),
      p.cross(gr.LONG_ISO, gr.LONG),
      p.cross(gr.CHL_ISO, gr.CHL),
      p.cross(gr.EYE_ISO, gr.EYE)).optimize()

  iso_to_typ_symbol = p.union(
      p.cross(gr.IND_ISO, gr.IND),
      p.cross(gr.ZWJ_ISO, gr.ZWJ),
      p.cross(gr.ZWN_ISO, gr.ZWN)).optimize()

  return p.union(
      iso_to_typ_vowel,
      iso_to_typ_consonant,
      iso_to_typ_coda,
      iso_to_typ_modifier,
      iso_to_typ_symbol).star.optimize()

# Compose multiple ISO characters to single native characters.

_COMPOSE_DIPHTHONG_OP = p.union(
    p.cross(gr.A + gr.I, gr.AI),
    p.cross(gr.A + gr.U, gr.AU)).optimize()

_COMPOSE_DIPHTHONG = rw.rewrite_operation(_COMPOSE_DIPHTHONG_OP)

_COMPOSE_VOCALIC_OP = p.union(
    p.cross(gr.L + gr.VCL, gr.L_VCL),
    p.cross(gr.R + gr.VCL, gr.R_VCL)).optimize()

_COMPOSE_VOCALIC = rw.rewrite_operation(_COMPOSE_VOCALIC_OP)

_COMPOSE_RETROFLEX_OP = p.union(
    p.cross(gr.L_VCL + gr.LONG, gr.LL_VCL),
    p.cross(gr.R_VCL + gr.LONG, gr.RR_VCL)).optimize()

_COMPOSE_RETROFLEX = rw.rewrite_operation(_COMPOSE_RETROFLEX_OP)

_COMPOSE_IND_VOWEL_OP = p.union(
    p.cross(gr.IND + gr.A, gr.A_I),
    p.cross(gr.IND + gr.AA, gr.AA_I),
    p.cross(gr.IND + gr.AC, gr.AC_I),
    p.cross(gr.IND + gr.E, gr.E_I),
    p.cross(gr.IND + gr.EE, gr.EE_I),
    p.cross(gr.IND + gr.EC, gr.EC_I),
    p.cross(gr.IND + gr.I, gr.I_I),
    p.cross(gr.IND + gr.II, gr.II_I),
    p.cross(gr.IND + gr.O, gr.O_I),
    p.cross(gr.IND + gr.OO, gr.OO_I),
    p.cross(gr.IND + gr.OC, gr.OC_I),
    p.cross(gr.IND + gr.U, gr.U_I),
    p.cross(gr.IND + gr.UU, gr.UU_I),
    p.cross(gr.IND + gr.AI, gr.AI_I),
    p.cross(gr.IND + gr.AU, gr.AU_I),
    p.cross(gr.IND + gr.L_VCL, gr.L_VCL_I),
    p.cross(gr.IND + gr.LL_VCL, gr.LL_VCL_I),
    p.cross(gr.IND + gr.R_VCL, gr.R_VCL_I),
    p.cross(gr.IND + gr.RR_VCL, gr.RR_VCL_I)).optimize()

_COMPOSE_IND_VOWEL = rw.rewrite_operation(_COMPOSE_IND_VOWEL_OP)

_COMPOSE_IND_A = rw.rewrite_word_initial(gr.A, gr.A_I)

_COMPOSE_ASPIRATION_OP = p.union(
    p.cross(gr.B + gr.ASP, gr.BH),
    p.cross(gr.C + gr.ASP, gr.CH),
    p.cross(gr.D + gr.ASP, gr.DH),
    p.cross(gr.DD + gr.ASP, gr.DDH),
    p.cross(gr.G + gr.ASP, gr.GH),
    p.cross(gr.J + gr.ASP, gr.JH),
    p.cross(gr.K + gr.ASP, gr.KH),
    p.cross(gr.P + gr.ASP, gr.PH),
    p.cross(gr.RD + gr.ASP, gr.RDH),
    p.cross(gr.T + gr.ASP, gr.TH),
    p.cross(gr.TT + gr.ASP, gr.TTH)).optimize()

_COMPOSE_ASPIRATION = rw.rewrite_operation(_COMPOSE_ASPIRATION_OP)

_COMPOSE_CANDRA = rw.rewrite(gr.M + gr.CND_DIA, gr.CND)

# Malayalam chillu characters
_COMPOSE_CHILLU_OP = p.union(
    p.cross(gr.K + gr.CHL, gr.K_CHL),
    p.cross(gr.L + gr.CHL, gr.L_CHL),
    p.cross(gr.LL + gr.CHL, gr.LL_CHL),
    p.cross(gr.N + gr.CHL, gr.N_CHL),
    p.cross(gr.NN + gr.CHL, gr.NN_CHL),
    p.cross(gr.RR + gr.CHL, gr.RR_CHL),
    p.cross(gr.R + gr.CHL, gr.REPH)).optimize()

_COMPOSE_CHILLU = rw.rewrite_operation(_COMPOSE_CHILLU_OP)

# Marathi eyelash ra
_COMPOSE_EYELASH = rw.rewrite(gr.R + gr.EYE, gr.R_EYE)

_COMPOSE_OM = rw.rewrite(gr.OT + gr.M, gr.OM)

_COMPOSE_TYP = (
    _COMPOSE_DIPHTHONG @
    _COMPOSE_VOCALIC @
    _COMPOSE_RETROFLEX @
    _COMPOSE_IND_VOWEL @
    _COMPOSE_IND_A @
    _COMPOSE_ASPIRATION @
    _COMPOSE_CANDRA @
    _COMPOSE_CHILLU @
    _COMPOSE_EYELASH @
    _COMPOSE_OM).optimize()


def iso_to_typ() -> p.Fst:
  return (_iso_to_decomposed_typ() @ _COMPOSE_TYP).optimize()
