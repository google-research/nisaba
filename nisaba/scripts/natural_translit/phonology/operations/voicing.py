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

import pynini as pyn
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as phn
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

ph = phn.PHONEME_INVENTORY

# Voicing

VOICING_OP = ls.cross_union([
    [ph.TSH, ph.DZH],
    [ph.K, ph.G],
    [ph.P, ph.B],
    [ph.T, ph.D],
    [ph.TI, ph.DI],
    [ph.TT, ph.DD]
])


def voicing(
    preceding: pyn.FstLike,
    following: pyn.FstLike) -> pyn.Fst:
  """Voicing. See rewrite_by_operation for argument details."""
  return rw.rewrite_op(
      VOICING_OP,
      preceding,
      following)

