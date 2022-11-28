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

# Lint as: python3
"""Common constants and symbol and alignment forming functions."""

import pynini as p
from pynini.lib import byte

BYTE_STAR = byte.BYTE.star.optimize()
BOS = p.accep('[BOS]')  # Beginning of string
EOS = p.accep('[EOS]')  # End of string
EPSILON = p.accep('')  # Epsilon, empty string
USC = p.accep('_')
PLUS = p.accep('+')
GR_L = p.accep('<')  # Grapheme left boundary
GR_R = p.accep('>')  # Grapheme right boundary
GR_BOUND = p.union(GR_L, GR_R).optimize()
PH_L = p.accep('{')  # Phoneme left boundary
PH_R = p.accep('}')  # Phoneme right boundary
PH_BOUND = p.union(PH_L, PH_R).optimize()
TR_L = p.accep('“')  # Translit left boundary (left double quote)
TR_R = p.accep('”')  # Translit right boundary (right double quote)
TR_BOUND = p.union(TR_L, TR_R).optimize()
ALIGN_SIGN = p.accep('=')  # Substring alignment


def enclose(
    string: p.FstLike,
    left_boundary: p.FstLike,
    right_boundary: p.FstLike) -> p.Fst:
  """Encloses a string in the boundary symbols of the relevant type."""
  return left_boundary + string + right_boundary

SYM = p.union(byte.ALPHA, USC, PLUS).star.optimize()
GRAPHEME = enclose(SYM, GR_L, GR_R)
GRAPHEMES = GRAPHEME.star.optimize()
PHONEME = enclose(SYM, PH_L, PH_R)
PHONEMES = PHONEME.star.optimize()
TRANSLIT = enclose(SYM, TR_L, TR_R)
TRANSLITS = TRANSLIT.star.optimize()


def align(left_side: p.FstLike, right_side: p.FstLike) -> p.Fst:
  """Alignment structure (left_side=right_side)."""
  return left_side + ALIGN_SIGN + right_side


def assign(left_side: p.FstLike, right_side: p.FstLike) -> p.Fst:
  """Takes left side, returns an alignment of left and right sides."""
  return p.cross(left_side, align(left_side, right_side))
