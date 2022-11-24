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

"""Multilingual phonological operations."""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.common.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.phonology.phoneme_inventory as ph

# Voicing

VOICING_OP = p.union(
    p.cross(ph.CH, ph.JH),
    p.cross(ph.K, ph.G),
    p.cross(ph.P, ph.B),
    p.cross(ph.T, ph.D),
    p.cross(ph.TI, ph.DI),
    p.cross(ph.TT, ph.DD)).optimize()


def voicing(
    preceding: p.FstLike,
    following: p.FstLike) -> p.Fst:
  """Voicing. See rewrite_by_operation for argument details."""
  return rw.rewrite_operation_by_context(
      VOICING_OP,
      preceding,
      following)

