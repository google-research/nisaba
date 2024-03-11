# Copyright 2024 Nisaba Authors.
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

"""Multilingual phonological operations."""

import pynini as pyn
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as mul
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

ph = mul.PHONEME_INVENTORY

# Voicing

K_G = [ph.K, ph.G]
P_B = [ph.P, ph.B]
T_D = [ph.T, ph.D]
TI_DI = [ph.TI, ph.DI]
TT_DD = [ph.TT, ph.DD]
TSH_DZH = [ph.T_SH, ph.D_ZH]
TSH_S = [ph.T_SH, ph.S]


def voicing(
    ops: list[list[pyn.Fst]],
    preceding: pyn.FstLike = al.EPSILON,
    following: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Voicing. See rewrite_by_operation for argument details."""
  return rw.rewrite_ls(
      ops,
      preceding,
      following)

