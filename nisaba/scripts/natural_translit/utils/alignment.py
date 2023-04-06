# Copyright 2023 Nisaba Authors.
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
"""Alignment forming functions and constants."""

import pynini as pyn
from pynini.lib import byte
from nisaba.scripts.natural_translit.utils import list_op as ls

# Constants

# Default sigma for rewrites that don't involve UTF-8 character
BYTE_STAR = ls.star_opt(byte.BYTE)

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
EQUAL = '='
GRAVE_ACCENT = '`'
FULL_STOP = '.'
ASTERISK = '*'
MINUS = '-'
AMPERSAND = '&'
EXCLAMATION = '!'
COLON = ':'
SPACE = ' '

# Acceptors

BOS = pyn.accep(BOS_STR)
EOS = pyn.accep(EOS_STR)
EPSILON = pyn.accep(EMPTY_STR)
AFFIX = pyn.accep(UNDERSCORE)
COMBINE = pyn.accep(PLUS)
GR_L = pyn.accep(LESS_THAN)  # Grapheme left boundary
GR_R = pyn.accep(GREATER_THAN)  # Grapheme right boundary
GR_B = [GR_L, GR_R]
GR_BOUND = ls.union_opt(*GR_B)
PH_L = pyn.accep(CURLY_L)  # Phoneme left boundary
PH_R = pyn.accep(CURLY_R)  # Phoneme right boundary
PH_B = [PH_L, PH_R]
PH_BOUND = ls.union_opt(*PH_B)
TR_B = pyn.accep(GRAVE_ACCENT)  # Translit boundary
ALIGN_SIGN = pyn.accep(EQUAL)  # Substring alignment
DOT = pyn.accep(FULL_STOP)
STRESS = pyn.accep(ASTERISK)
PITCH = pyn.accep(MINUS)
CONTOUR = pyn.accep(AMPERSAND)
INTONATION = pyn.accep(EXCLAMATION)
DURATION = pyn.accep(COLON)

# Functions


def _enclose(
    base: pyn.FstLike,
    left_boundary: pyn.FstLike,
    right_boundary: pyn.FstLike) -> pyn.Fst:
  """Encloses a string with the boundary symbols of the relevant type."""
  return left_boundary + base + right_boundary


def enclose_grapheme(base: pyn.FstLike) -> pyn.Fst:
  """Encloses a string with grapheme boundaries."""
  return _enclose(base, *GR_B)


def enclose_phoneme(base: pyn.FstLike) -> pyn.Fst:
  """Encloses a string with phoneme boundaries."""
  return _enclose(base, *PH_B)


def enclose_translit(base: pyn.FstLike) -> pyn.Fst:
  """Encloses a string with translit boundaries."""
  return _enclose(base, TR_B, TR_B)


def align(left_side: pyn.FstLike, right_side: pyn.FstLike) -> pyn.Fst:
  """Alignment structure (left_side=right_side)."""
  return left_side + ALIGN_SIGN + right_side


def realign(
    left_side: pyn.FstLike,
    old: pyn.FstLike,
    new: pyn.FstLike) -> pyn.Fst:
  """Changes the right side assignment of a specified left side."""
  return pyn.cross(
      align(left_side, old),
      align(left_side, new))


def assign(left_side: pyn.FstLike, right_side: pyn.FstLike) -> pyn.Fst:
  """Takes left side, returns an alignment of left and right sides."""
  return pyn.cross(left_side, align(left_side, right_side))

PUNCTUATION = (
    AFFIX | COMBINE | DOT | STRESS | PITCH | CONTOUR | INTONATION | DURATION
)
SYM = ls.union_star(byte.ALPHA, PUNCTUATION)
GRAPHEME = enclose_grapheme(SYM)
GRAPHEMES = ls.star_opt(GRAPHEME)
PHONEME = enclose_phoneme(SYM)
PHONEMES = ls.star_opt(PHONEME)
TRANSLIT = enclose_translit(SYM)
TRANSLITS = ls.star_opt(TRANSLIT)

# Right side of an alignment can be phonemes or transliteration string
R_SYM = ls.union_star(PHONEME, TRANSLIT)
R_SYMS = ls.union_star(PHONEMES, TRANSLITS)

SYMS = ls.union_opt(GRAPHEMES, R_SYMS)

# Skip sequences to look at either the adjacent symbol, the closest left or
# right side symbol of an adjacent alignment.
SKIP_LEFT_SIDE = (GRAPHEME.plus + ALIGN_SIGN).ques
SKIP_RIGHT_SIDE = (ALIGN_SIGN + R_SYM.plus).ques
SKIP = ls.union_opt(SKIP_LEFT_SIDE, SKIP_RIGHT_SIDE).ques


# Beginning of word
BOW = BOS + SKIP_LEFT_SIDE.ques

# End of word
EOW = SKIP_RIGHT_SIDE.ques + EOS


