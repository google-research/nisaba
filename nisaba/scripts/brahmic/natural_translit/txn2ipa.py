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

import pynini as p
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw


def _rewrite_txn_to_ipa() -> p.Fst:
  """Internal txn representation to IPA output."""

  txn_to_ipa_op = p.union(
      p.cross(ph.A, ph.A_IPA),
      p.cross(ph.A_L, ph.A_L_IPA),
      p.cross(ph.AE, ph.AE_IPA),
      p.cross(ph.B, ph.B_IPA),
      p.cross(ph.CH, ph.CH_IPA),
      p.cross(ph.D, ph.D_IPA),
      p.cross(ph.DD, ph.DD_IPA),
      p.cross(ph.DI, ph.DI_IPA),
      p.cross(ph.E, ph.E_IPA),
      p.cross(ph.E_L, ph.E_L_IPA),
      p.cross(ph.EC, ph.EC_IPA),
      p.cross(ph.EC_L, ph.EC_L_IPA),
      p.cross(ph.EH, ph.EH_IPA),
      p.cross(ph.EH_L, ph.EH_L_IPA),
      p.cross(ph.F, ph.F_IPA),
      p.cross(ph.G, ph.G_IPA),
      p.cross(ph.H, ph.H_IPA),
      p.cross(ph.I, ph.I_IPA),
      p.cross(ph.I_L, ph.I_L_IPA),
      p.cross(ph.JH, ph.JH_IPA),
      p.cross(ph.K, ph.K_IPA),
      p.cross(ph.L, ph.L_IPA),
      p.cross(ph.LL, ph.LL_IPA),
      p.cross(ph.M, ph.M_IPA),
      p.cross(ph.N, ph.N_IPA),
      p.cross(ph.NG, ph.NG_IPA),
      p.cross(ph.NI, ph.NI_IPA),
      p.cross(ph.NN, ph.NN_IPA),
      p.cross(ph.NY, ph.NY_IPA),
      p.cross(ph.O, ph.O_IPA),
      p.cross(ph.O_L, ph.O_L_IPA),
      p.cross(ph.OH, ph.OH_IPA),
      p.cross(ph.OH_L, ph.OH_L_IPA),
      p.cross(ph.P, ph.P_IPA),
      p.cross(ph.Q, ph.Q_IPA),
      p.cross(ph.R, ph.R_IPA),
      p.cross(ph.RRT, ph.RRT_IPA),
      p.cross(ph.RRU, ph.RRU_IPA),
      p.cross(ph.RT, ph.RT_IPA),
      p.cross(ph.S, ph.S_IPA),
      p.cross(ph.SH, ph.SH_IPA),
      p.cross(ph.SS, ph.SS_IPA),
      p.cross(ph.T, ph.T_IPA),
      p.cross(ph.TI, ph.TI_IPA),
      p.cross(ph.TT, ph.TT_IPA),
      p.cross(ph.U, ph.U_IPA),
      p.cross(ph.U_L, ph.U_L_IPA),
      p.cross(ph.VU, ph.VU_IPA),
      p.cross(ph.X, ph.X_IPA),
      p.cross(ph.XA, ph.XA_IPA),
      p.cross(ph.Y, ph.Y_IPA),
      p.cross(ph.Z, ph.Z_IPA),
      p.cross(ph.ASP, ph.ASP_IPA),
      p.cross(ph.NSL, ph.NSL_IPA),
      p.cross(ph.SIL, ph.SIL_IPA),
      p.cross(ph.SCHWA, ph.SCHWA_IPA)).optimize()

  return rw.rewrite_by_operation(txn_to_ipa_op, sigma=ph.sigma_star())


def txn_to_ipa() -> p.Fst:
  """Converts txn to IPA and outputs only transcription strings."""
  return (_rewrite_txn_to_ipa() @
          rw.extract_right_side(sigma=ph.sigma_star())).optimize()
