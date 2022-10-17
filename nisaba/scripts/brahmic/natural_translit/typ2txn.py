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
import nisaba.scripts.brahmic.natural_translit.grapheme_inventory as gr
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.util as u

_ASSIGN_VOWEL = p.union(
    u.assign(gr.A, ph.A),
    u.assign(gr.AA, ph.A_L),
    u.assign(gr.AC, ph.AE),
    u.assign(gr.AI, ph.AE),
    u.assign(gr.AU, ph.O_L),
    u.assign(gr.E, ph.E),
    u.assign(gr.EE, ph.E_L),
    u.assign(gr.EC, ph.AE),
    u.assign(gr.I, ph.I),
    u.assign(gr.II, ph.I_L),
    u.assign(gr.O, ph.O),
    u.assign(gr.OO, ph.O_L),
    u.assign(gr.OC, ph.O_L),
    u.assign(gr.U, ph.U),
    u.assign(gr.UU, ph.U_L),
    u.assign(gr.A_I, ph.A),
    u.assign(gr.AA_I, ph.A_L),
    u.assign(gr.AC_I, ph.AE),
    u.assign(gr.AI_I, ph.AE),
    u.assign(gr.AU_I, ph.O_L),
    u.assign(gr.E_I, ph.E),
    u.assign(gr.EE_I, ph.E_L),
    u.assign(gr.EC_I, ph.AE),
    u.assign(gr.I_I, ph.I),
    u.assign(gr.II_I, ph.I_L),
    u.assign(gr.O_I, ph.O),
    u.assign(gr.OO_I, ph.O_L),
    u.assign(gr.OC_I, ph.O_L),
    u.assign(gr.U_I, ph.U),
    u.assign(gr.UU_I, ph.U_L)
    ).optimize()

# Vocalic characters are assigned a consonant followed by a vowel
_ASSIGN_VOCALIC = p.union(
    u.assign(gr.L_VCL, ph.L + ph.VCL),
    u.assign(gr.LL_VCL, ph.LL + ph.VCL),
    u.assign(gr.R_VCL, ph.RT + ph.VCL),
    u.assign(gr.RR_VCL, ph.R + ph.VCL),
    u.assign(gr.L_VCL_I, ph.L + ph.VCL),
    u.assign(gr.LL_VCL_I, ph.LL + ph.VCL),
    u.assign(gr.R_VCL_I, ph.RT + ph.VCL),
    u.assign(gr.RR_VCL_I, ph.R + ph.VCL)
    ).optimize()

_ASSIGN_CONSONANT = p.union(
    u.assign(gr.B, ph.B),
    u.assign(gr.C, ph.CH),
    u.assign(gr.D, ph.DI),
    u.assign(gr.DD, ph.DD),
    u.assign(gr.F, ph.F),
    u.assign(gr.G, ph.G),
    u.assign(gr.GG, ph.XA),
    u.assign(gr.H, ph.H),
    u.assign(gr.J, ph.JH),
    u.assign(gr.K, ph.K),
    u.assign(gr.L, ph.L),
    u.assign(gr.LL, ph.L),
    u.assign(gr.LR, ph.RRU),
    u.assign(gr.M, ph.M),
    u.assign(gr.N, ph.NI),
    u.assign(gr.NY, ph.NY),
    u.assign(gr.NG, ph.NG),
    u.assign(gr.NN, ph.NN),
    u.assign(gr.NA, ph.N),
    u.assign(gr.P, ph.P),
    u.assign(gr.Q, ph.Q),
    u.assign(gr.R, ph.RT),
    u.assign(gr.RD, ph.RRT),
    u.assign(gr.RR, ph.R),
    u.assign(gr.S, ph.S),
    u.assign(gr.SH, ph.SH),
    u.assign(gr.SS, ph.SS),
    u.assign(gr.T, ph.TI),
    u.assign(gr.TT, ph.TT),
    u.assign(gr.TA, ph.T),
    u.assign(gr.V, ph.VU),
    u.assign(gr.X, ph.X),
    u.assign(gr.Y, ph.Y),
    u.assign(gr.Z, ph.Z),
    u.assign(gr.K_CHL, ph.K),
    u.assign(gr.L_CHL, ph.L),
    u.assign(gr.LL_CHL, ph.LL),
    u.assign(gr.N_CHL, ph.NI),
    u.assign(gr.NN_CHL, ph.NN),
    u.assign(gr.RR_CHL, ph.RT),
    u.assign(gr.REPH, ph.RT),
    u.assign(gr.R_EYE, ph.RT)
    ).optimize()

# Aspirated consonants are featurised into a consonant
# followed by an aspirated release.
_ASSIGN_ASPIRATED = p.union(
    u.assign(gr.BH, ph.B + ph.ASP),
    u.assign(gr.CH, ph.CH + ph.ASP),
    u.assign(gr.DH, ph.DI + ph.ASP),
    u.assign(gr.DDH, ph.DD + ph.ASP),
    u.assign(gr.GH, ph.G + ph.ASP),
    u.assign(gr.JH, ph.JH + ph.ASP),
    u.assign(gr.KH, ph.K + ph.ASP),
    u.assign(gr.PH, ph.P + ph.ASP),
    u.assign(gr.RDH, ph.RRT + ph.ASP),
    u.assign(gr.TH, ph.TI + ph.ASP),
    u.assign(gr.TTH, ph.TT + ph.ASP),
    u.assign(gr.YY, ph.Y + ph.ASP)
    ).optimize()

_ASSIGN_CODA = p.union(
    u.assign(gr.AVG, ph.SIL),
    u.assign(gr.VIS, ph.H),
    u.assign(gr.ANS, ph.NSL),
    u.assign(gr.CND, ph.NSL),
    u.assign(gr.UPADH, ph.H),
    u.assign(gr.JIHVA, ph.H)
    ).optimize()

_ASSIGN_OM = u.assign(gr.OM, ph.O_L + ph.M)

# Naive grapheme to phoneme assignment.
TYP_TO_TXN = p.union(
    _ASSIGN_VOWEL,
    _ASSIGN_VOCALIC,
    _ASSIGN_CONSONANT,
    _ASSIGN_ASPIRATED,
    _ASSIGN_CODA,
    _ASSIGN_OM
    ).star.optimize()

TAP_TO_TRILL = rw.rewrite(ph.RT, ph.R)
