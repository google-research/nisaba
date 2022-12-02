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

# Constants

# Default sigma for rewrites that don't involve UTF-8 characters.
BYTE_STAR = byte.BYTE.star.optimize()

# String literals

BOS_STR = '[BOS]'  # Beginning of string
EOS_STR = '[EOS]'  # End of string
EMPTY_STR = ''
UNDERSCORE = '_'
PLUS = '+'
LESS_THAN = '<'
GREATER_THAN = '>'
CURLY_L = '{'
CURLY_R = '}'
DBL_QUOTE_L = '“'  # U+201C
DBL_QUOTE_R = '”'  # U+201D
EQUAL = '='

# Acceptors

BOS = p.accep(BOS_STR)
EOS = p.accep(EOS_STR)
EPSILON = p.accep(EMPTY_STR)
AFFIX = p.accep(UNDERSCORE)
COMBINE = p.accep(PLUS)
GR_L = p.accep(LESS_THAN)  # Grapheme left boundary
GR_R = p.accep(GREATER_THAN)  # Grapheme right boundary
GR_B = [GR_L, GR_R]
GR_BOUND = p.union(*GR_B).optimize()
PH_L = p.accep(CURLY_L)  # Phoneme left boundary
PH_R = p.accep(CURLY_R)  # Phoneme right boundary
PH_B = [PH_L, PH_R]
PH_BOUND = p.union(*PH_B).optimize()
TR_L = p.accep(DBL_QUOTE_L)  # Translit left boundary
TR_R = p.accep(DBL_QUOTE_R)  # Translit right boundary
TR_B = [TR_L, TR_R]
TR_BOUND = p.union(*TR_B).optimize()
ALIGN_SIGN = p.accep(EQUAL)  # Substring alignment

# Functions


def _enclose(
    base: p.FstLike,
    left_boundary: p.FstLike,
    right_boundary: p.FstLike) -> p.Fst:
  """Encloses a string with the boundary symbols of the relevant type."""
  return left_boundary + base + right_boundary


def enclose_grapheme(base: p.FstLike) -> p.Fst:
  """Encloses a string with grapheme boundaries."""
  return _enclose(base, *GR_B)


def enclose_phoneme(base: p.FstLike) -> p.Fst:
  """Encloses a string with phoneme boundaries."""
  return _enclose(base, *PH_B)


def enclose_translit(base: p.FstLike) -> p.Fst:
  """Encloses a string with translit boundaries."""
  return _enclose(base, *TR_B)

SYM = p.union(byte.ALPHA, AFFIX, COMBINE).star.optimize()
GRAPHEME = enclose_grapheme(SYM)
GRAPHEMES = GRAPHEME.star.optimize()
PHONEME = enclose_phoneme(SYM)
PHONEMES = PHONEME.star.optimize()
TRANSLIT = enclose_translit(SYM)
TRANSLITS = TRANSLIT.star.optimize()


def align(left_side: p.FstLike, right_side: p.FstLike) -> p.Fst:
  """Alignment structure (left_side=right_side)."""
  return left_side + ALIGN_SIGN + right_side


def assign(left_side: p.FstLike, right_side: p.FstLike) -> p.Fst:
  """Takes left side, returns an alignment of left and right sides."""
  return p.cross(left_side, align(left_side, right_side))
