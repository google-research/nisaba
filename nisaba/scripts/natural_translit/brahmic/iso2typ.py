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
from nisaba.scripts.natural_translit.brahmic import iso_inventory as gr
from nisaba.scripts.natural_translit.common import list_util as l
from nisaba.scripts.natural_translit.common import rewrite_functions as rw
from nisaba.scripts.natural_translit.common import util as u


def _iso_to_decomposed_typ() -> p.Fst:
  """ISO to typable fst."""

  iso_to_typ_vowel = l.unite_pcross([
      [[gr.A_ISO], gr.A],
      [[gr.AA_ISO], gr.AA],
      [[gr.AC_ISO], gr.AC],
      [[gr.AN_ISO], gr.AN],
      [[gr.E_ISO], gr.E],
      [[gr.EE_ISO], gr.EE],
      [[gr.EC_ISO], gr.EC],
      [[gr.I_ISO], gr.I],
      [[gr.II_ISO], gr.II],
      [[gr.O_ISO], gr.O],
      [[gr.OO_ISO], gr.OO],
      [[gr.OC_ISO], gr.OC],
      [[gr.OT_ISO], gr.OT],
      [[gr.U_ISO], gr.U],
      [[gr.UU_ISO], gr.UU],
  ])

  iso_to_typ_consonant = l.unite_pcross([
      [[gr.B_ISO], gr.B],
      [[gr.C_ISO], gr.C],
      [[gr.D_ISO], gr.D],
      [[gr.DD_ISO], gr.DD],
      [[gr.F_ISO], gr.F],
      [[gr.G_ISO], gr.G],
      [[gr.GG_ISO], gr.GG],
      [[gr.H_ISO], gr.H],
      [[gr.J_ISO], gr.J],
      [[gr.K_ISO], gr.K],
      [[gr.L_ISO], gr.L],
      [[gr.LL_ISO], gr.LL],
      [[gr.LR_ISO], gr.LR],
      [[gr.M_ISO], gr.M],
      [[gr.N_ISO], gr.N],
      [[gr.NY_ISO], gr.NY],
      [[gr.NG_ISO], gr.NG],
      [[gr.NN_ISO], gr.NN],
      [[gr.NA_ISO], gr.NA],
      [[gr.P_ISO], gr.P],
      [[gr.Q_ISO], gr.Q],
      [[gr.R_ISO], gr.R],
      [[gr.RD_ISO], gr.RD],
      [[gr.RR_ISO], gr.RR],
      [[gr.S_ISO], gr.S],
      [[gr.SH_ISO], gr.SH],
      [[gr.SS_ISO], gr.SS],
      [[gr.T_ISO], gr.T],
      [[gr.TT_ISO], gr.TT],
      [[gr.TA_ISO], gr.TA],
      [[gr.V_ISO], gr.V],
      [[gr.X_ISO], gr.X],
      [[gr.Y_ISO], gr.Y],
      [[gr.YY_ISO], gr.YY],
      [[gr.Z_ISO], gr.Z],
  ])

  iso_to_typ_coda = l.unite_pcross([
      [[gr.AVG_ISO], gr.AVG],
      [[gr.NKT_ISO], gr.NKT],
      [[gr.VIS_ISO], gr.VIS],
      [[gr.ANS_ISO], gr.ANS],
      [[gr.CND_DIA_ISO], gr.CND_DIA],
      [[gr.UPADH_ISO], gr.UPADH],
      [[gr.JIHVA_ISO], gr.JIHVA],
  ])

  iso_to_typ_modifier = l.unite_pcross([
      [[gr.ASP_ISO], gr.ASP],
      [[gr.VCL_ISO], gr.VCL],
      [[gr.LONG_ISO], gr.LONG],
      [[gr.CHL_ISO], gr.CHL],
      [[gr.EYE_ISO], gr.EYE],
  ])

  iso_to_typ_symbol = l.unite_pcross([
      [[gr.IND_ISO], gr.IND],
      [[gr.ZWJ_ISO], gr.ZWJ],
      [[gr.ZWN_ISO], gr.ZWN]
  ])

  return p.union(
      iso_to_typ_vowel,
      iso_to_typ_consonant,
      iso_to_typ_coda,
      iso_to_typ_modifier,
      iso_to_typ_symbol).star.optimize()

# Compose multiple ISO characters to single native characters.

_COMPOSE_DIPHTHONG_OP = l.unite_pcross([
    [[gr.A + gr.I], gr.AI],
    [[gr.A + gr.U], gr.AU],
])

_COMPOSE_DIPHTHONG = rw.rewrite_operation(_COMPOSE_DIPHTHONG_OP)

_COMPOSE_VOCALIC_OP = l.unite_pcross([
    [[gr.L + gr.VCL], gr.L_VCL],
    [[gr.R + gr.VCL], gr.R_VCL],
])

_COMPOSE_VOCALIC = rw.rewrite_operation(_COMPOSE_VOCALIC_OP)

_COMPOSE_RETROFLEX_OP = l.unite_pcross([
    [[gr.L_VCL + gr.LONG], gr.LL_VCL],
    [[gr.R_VCL + gr.LONG], gr.RR_VCL],
])

_COMPOSE_RETROFLEX = rw.rewrite_operation(_COMPOSE_RETROFLEX_OP)

_IND_VOWEL_OP = l.unite_pcross([
    [[gr.A], gr.A_I],
    [[gr.AA], gr.AA_I],
    [[gr.AC], gr.AC_I],
    [[gr.E], gr.E_I],
    [[gr.EE], gr.EE_I],
    [[gr.EC], gr.EC_I],
    [[gr.I], gr.I_I],
    [[gr.II], gr.II_I],
    [[gr.O], gr.O_I],
    [[gr.OO], gr.OO_I],
    [[gr.OC], gr.OC_I],
    [[gr.U], gr.U_I],
    [[gr.UU], gr.UU_I],
    [[gr.AI], gr.AI_I],
    [[gr.AU], gr.AU_I],
    [[gr.L_VCL], gr.L_VCL_I],
    [[gr.LL_VCL], gr.LL_VCL_I],
    [[gr.R_VCL], gr.R_VCL_I],
    [[gr.RR_VCL], gr.RR_VCL_I],
])

_COMPOSE_IND_VOWEL = rw.rewrite_operation_by_context(
    _IND_VOWEL_OP,
    p.union(u.BOS, gr.IND))

_DELETE_IND = rw.delete(gr.IND)

_COMPOSE_AAN = rw.rewrite(gr.AN + gr.LONG, gr.AAN)

_COMPOSE_ASPIRATION_OP = l.unite_pcross([
    [[gr.B + gr.ASP], gr.BH],
    [[gr.C + gr.ASP], gr.CH],
    [[gr.D + gr.ASP], gr.DH],
    [[gr.DD + gr.ASP], gr.DDH],
    [[gr.G + gr.ASP], gr.GH],
    [[gr.J + gr.ASP], gr.JH],
    [[gr.K + gr.ASP], gr.KH],
    [[gr.P + gr.ASP], gr.PH],
    [[gr.RD + gr.ASP], gr.RDH],
    [[gr.T + gr.ASP], gr.TH],
    [[gr.TT + gr.ASP], gr.TTH],
])

_COMPOSE_ASPIRATION = rw.rewrite_operation(_COMPOSE_ASPIRATION_OP)

_COMPOSE_CANDRA = rw.rewrite(gr.M + gr.CND_DIA, gr.CND)

# Malayalam chillu characters
_COMPOSE_CHILLU_OP = l.unite_pcross([
    [[gr.K + gr.CHL], gr.K_CHL],
    [[gr.L + gr.CHL], gr.L_CHL],
    [[gr.LL + gr.CHL], gr.LL_CHL],
    [[gr.N + gr.CHL], gr.N_CHL],
    [[gr.NN + gr.CHL], gr.NN_CHL],
    [[gr.RR + gr.CHL], gr.RR_CHL],
    [[gr.R + gr.CHL], gr.REPH],
])

_COMPOSE_CHILLU = rw.rewrite_operation(_COMPOSE_CHILLU_OP)

# Marathi eyelash ra
_COMPOSE_EYELASH = rw.rewrite(gr.R + gr.EYE, gr.R_EYE)

_COMPOSE_OM = rw.rewrite(gr.OT + gr.M, gr.OM)

_COMPOSE_TYP = (
    _COMPOSE_DIPHTHONG @
    _COMPOSE_VOCALIC @
    _COMPOSE_RETROFLEX @
    _COMPOSE_IND_VOWEL @
    _DELETE_IND @
    _COMPOSE_AAN @
    _COMPOSE_ASPIRATION @
    _COMPOSE_CANDRA @
    _COMPOSE_CHILLU @
    _COMPOSE_EYELASH @
    _COMPOSE_OM).optimize()


def iso_to_typ() -> p.Fst:
  return (_iso_to_decomposed_typ() @ _COMPOSE_TYP).optimize()
