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

"""IPA pronunciation output."""

import pynini as pyn
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw


def _rewrite_txn_to_ipa() -> pyn.Fst:
  """Internal txn representation to IPA output."""
  return ls.cross_union_star([
      [ph.A, ph.A_IPA],
      [ph.A_L, ph.A_L_IPA],
      [ph.AE, ph.AE_IPA],
      [ph.B, ph.B_IPA],
      [ph.TSH, ph.TSH_IPA],
      [ph.D, ph.D_IPA],
      [ph.DD, ph.DD_IPA],
      [ph.DI, ph.DI_IPA],
      [ph.E, ph.E_IPA],
      [ph.E_L, ph.E_L_IPA],
      [ph.EC, ph.EC_IPA],
      [ph.EC_L, ph.EC_L_IPA],
      [ph.EH, ph.EH_IPA],
      [ph.EH_L, ph.EH_L_IPA],
      [ph.F, ph.F_IPA],
      [ph.G, ph.G_IPA],
      [ph.H, ph.H_IPA],
      [ph.I, ph.I_IPA],
      [ph.I_L, ph.I_L_IPA],
      [ph.DZH, ph.DZH_IPA],
      [ph.K, ph.K_IPA],
      [ph.L, ph.L_IPA],
      [ph.LL, ph.LL_IPA],
      [ph.M, ph.M_IPA],
      [ph.N, ph.N_IPA],
      [ph.NG, ph.NG_IPA],
      [ph.NI, ph.NI_IPA],
      [ph.NN, ph.NN_IPA],
      [ph.NY, ph.NY_IPA],
      [ph.O, ph.O_IPA],
      [ph.O_L, ph.O_L_IPA],
      [ph.OH, ph.OH_IPA],
      [ph.OH_L, ph.OH_L_IPA],
      [ph.P, ph.P_IPA],
      [ph.Q, ph.Q_IPA],
      [ph.R, ph.R_IPA],
      [ph.RRT, ph.RRT_IPA],
      [ph.RRU, ph.RRU_IPA],
      [ph.RT, ph.RT_IPA],
      [ph.S, ph.S_IPA],
      [ph.SH, ph.SH_IPA],
      [ph.SS, ph.SS_IPA],
      [ph.T, ph.T_IPA],
      [ph.TI, ph.TI_IPA],
      [ph.TT, ph.TT_IPA],
      [ph.U, ph.U_IPA],
      [ph.U_L, ph.U_L_IPA],
      [ph.VU, ph.VU_IPA],
      [ph.KH, ph.KH_IPA],
      [ph.GH, ph.GH_IPA],
      [ph.Y, ph.Y_IPA],
      [ph.Z, ph.Z_IPA],
      [ph.ASP, ph.ASP_IPA],
      [ph.NSL, ph.NSL_IPA],
      [ph.SIL, ph.SIL_IPA],
      [ph.SYL, ph.SYL_IPA],
      [ph.SCHWA, ph.SCHWA_IPA],
  ])


def txn_to_ipa() -> pyn.Fst:
  """Converts txn to IPA and outputs only transcription strings."""
  return (rw.EXTRACT_RIGHT_SIDE @
          _rewrite_txn_to_ipa()).optimize()
