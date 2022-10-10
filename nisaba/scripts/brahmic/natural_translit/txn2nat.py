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

"""Pan-South Asian natural romanization."""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.grapheme_inventory as gr
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.transliteration_inventory as tr
import nisaba.scripts.brahmic.natural_translit.util as u

# Palatal and velar assimilated anusvara is transliterated as “n”.
_NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,
    p.union(ph.NG, ph.NY),
    tr.N)


def _rewrite_txn_to_psaf() -> p.Fst:
  """Fine-grained Pan South Asian romanization."""

  txn_to_psaf = p.union(
      p.cross(ph.A, tr.A),
      p.cross(ph.A_L, tr.AA),
      p.cross(ph.AE, tr.AE),
      p.cross(ph.B, tr.B),
      p.cross(ph.CH, tr.CH),
      p.cross(ph.DD, tr.D),
      p.cross(ph.DI, tr.D),
      p.cross(ph.E, tr.E),
      p.cross(ph.E_L, tr.EE),
      p.cross(ph.F, tr.F),
      p.cross(ph.G, tr.G),
      p.cross(ph.H, tr.H),
      p.cross(ph.I, tr.I),
      p.cross(ph.I_L, tr.II),
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
      p.cross(ph.O, tr.O),
      p.cross(ph.O_L, tr.OO),
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
      p.cross(ph.U, tr.U),
      p.cross(ph.U_L, tr.UU),
      p.cross(ph.VU, tr.V),
      p.cross(ph.X, tr.KH),
      p.cross(ph.XA, tr.G),
      p.cross(ph.Y, tr.Y),
      p.cross(ph.Z, tr.Z),
      p.cross(ph.ASP, tr.H),
      p.cross(ph.NSL, tr.N),
      p.cross(ph.SIL, u.EPSILON),
      p.cross(ph.SCHWA, tr.A)).optimize()

  return rw.rewrite_operation(txn_to_psaf)

_REWRITE_TXN_TO_PSAF = (_NON_LABIAL_ANUSVARA @
                        _rewrite_txn_to_psaf()).optimize()


def _psaf_to_psac() -> p.Fst:
  """Coarse-grained Pan South Asian romanization."""

  psaf_to_psac = p.union(
      p.cross(tr.AA, tr.A),
      p.cross(tr.EE, tr.E),
      p.cross(tr.II, tr.I),
      p.cross(tr.OO, tr.O),
      p.cross(tr.UU, tr.U)).optimize()

  return rw.rewrite_operation(psaf_to_psac)

_PSAF_TO_PSAC = _psaf_to_psac()

_STRIP = (rw.extract_right_side() @ rw.delete(u.TR_BOUND)).optimize()


def _txn_to_psaf() -> p.Fst:
  """Converts txn to PSAF and outputs only translit strings."""
  return (_REWRITE_TXN_TO_PSAF @ _STRIP).optimize()

TXN_TO_PSAF = _txn_to_psaf()


def _txn_to_psac() -> p.Fst:
  """Converts txn to PSAC and outputs only translit strings."""
  return (_REWRITE_TXN_TO_PSAF @ _PSAF_TO_PSAC @ _STRIP).optimize()

TXN_TO_PSAC = _txn_to_psac()
