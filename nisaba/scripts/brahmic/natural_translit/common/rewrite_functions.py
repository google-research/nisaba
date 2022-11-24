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
"""Common rewrite functions."""

import pynini as p
from nisaba.scripts.brahmic.natural_translit.common import util as u

# Right side of an alignment can be phonemes or transliteration strings.
R_SYM = p.union(u.PHONEME, u.TRANSLIT).optimize()
R_SYMS = p.union(u.PHONEMES, u.TRANSLITS).optimize()

SYMS = p.union(u.GRAPHEMES, R_SYMS).optimize()

# Skip sequences to look at either the adjacent symbol, the closest left or
# right side symbol of an adjacent alignment.
SKIP_LEFT_SIDE = (u.GRAPHEME.plus + u.ALIGN_SIGN).ques
SKIP_RIGHT_SIDE = (u.ALIGN_SIGN + R_SYM.plus).ques
SKIP = p.union(SKIP_LEFT_SIDE, SKIP_RIGHT_SIDE).ques


# Beginning of word
BOW = u.BOS + SKIP_LEFT_SIDE.ques

# End of word
EOW = SKIP_RIGHT_SIDE.ques + u.EOS


def concat_r(
    right_1: p.FstLike,
    right_2: p.FstLike) -> p.Fst:
  """Concatanate right side symbols across multiple alignments.

  Current number of args is 2, but will be increased as needed.

  Args:
    right_1: First right side.
    right_2: Second right side.

  Returns:
      Following call

  ```
  concat_r(ph.A, ph.B)
  ```
  would return:
  p.union(
      '{a}{b}',
      '{a}gr.GRAPHEMES{b}',
      ...
  )
  """

  return right_1 + SKIP_LEFT_SIDE.ques + right_2


def concat_l(
    left_1: p.FstLike,
    left_2: p.FstLike) -> p.Fst:
  """Concatanate left side symbols across multiple alignments.

  Current number of args is 2, but will be increased as needed.

  Args:
    left_1: First argument.
    left_2: Second argument.

  Returns:
      Following call

  ```
  concat_l(gr.A, gr.B)
  ```
  would return:
  p.union(
      '<a><b>',
      '<a>ph.PHONEMES<b>',
      ...
  )
  """

  return left_1 + SKIP_RIGHT_SIDE + left_2


def rewrite(
    old: p.FstLike,
    new: p.FstLike) -> p.Fst:
  """A shorthand for generic rewrites with no context.

  Args:
    old: Input of the rewrite.
    new: Output of the rewrite.

  Returns:
    Rewrite Fst.

  """
  return p.cdrewrite(
      p.cross(old, new),
      u.EPSILON,
      u.EPSILON,
      u.BYTE_STAR).optimize()


def rewrite_by_context(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites the right side of an alignment based on right side contexts.

  Args:
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding right side context.
    following: Following right side context.

  Returns:
    Rewrite fst.

  Eg. If a schwa between two nasals is always pronounced,

  Following call

  ```
  rewrite_by_context(ph.SCHWA, ph.EC, ph.NASAL, ph.NASAL)

  ```
  would return:
  ```
  p.cdrewrite(
      p.cross('{schwa}', '{ec}'),
      p.union('{m}', '{m}gr.GRAPHEMES', ...),
      p.union('{m}', 'gr.GRAPHEMES{m}', ...),,
      u.BYTE_STAR))

  """
  return p.cdrewrite(
      p.cross(old, new),
      preceding + SKIP,
      SKIP + following,
      u.BYTE_STAR).optimize()


def rewrite_operation(operation: p.Fst) -> p.Fst:
  """Rewrite using a pre-defined operation without context."""
  return p.cdrewrite(
      operation,
      u.EPSILON,
      u.EPSILON,
      u.BYTE_STAR).optimize()


def rewrite_operation_by_context(
    operation: p.Fst,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """A rewrite fst that uses a predefined operation as input.

  Args:
    operation: An operation that yields p.cross() functions.
    preceding: Preceding right side context.
    following: Following right side context.

  Returns:
    Rewrite fst.

  Eg. Voicing rewrites are predefined.
  VOICING _OP= p.union(..., p.cross(ph.TI, ph.DI), ...)

  Following call

  ```
  rewrite_operation_by_context(VOICING_OP, ph.VOWEL, ph.VOWEL)

  ```
  would return:
  ```
  p.cdrewrite(
      p.union(..., p.cross('{ti}', '{di}'), ...),
      p.union('{a}', '{a}{nsl}', '{a}{glide}', '{e}', '{e}{nsl}'...),
      p.union('{a}', '{a}{nsl}', '{a}{glide}', '{e}', '{e}{nsl}'...),
      u.BYTE_STAR)

  """
  return p.cdrewrite(
      operation,
      preceding + SKIP,
      SKIP + following,
      u.BYTE_STAR).optimize()


def rewrite_word_initial(
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites with preceding = beginning of word."""
  return rewrite_by_context(
      old,
      new,
      BOW,
      following)


def rewrite_word_final(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites with following = beginning of word."""
  return rewrite_by_context(
      old,
      new,
      preceding,
      EOW)


def realign(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike) -> p.Fst:
  """Changes the right side assignment of a specified left side."""
  return p.cross(
      u.align(left_side, old),
      u.align(left_side, new))


def reassign(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike) -> p.Fst:
  """Changes the right side assignment of a specified left side."""
  return rewrite_operation(realign(left_side, old, new))


def reassign_by_context(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Changes the right side assignment of a specified left side.

  Args:
    left_side: Specified left side.
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding right side context.
    following: Following right side context.

  Returns:
    Rewrite fst.

  Eg. Anusvara assimilates to {m} before labials.

  Following call

  ```
  reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.M,
      following=ph.LABIAL)

  ```
  would return:
  ```
  p.cdrewrite(
      p.cross('<ans>{nsl}', '<ans>{m}'),
      '',
      p.union('{m}', 'gr.GRAPHEMES{m}', ...),,
      u.BYTE_STAR))

  """
  return rewrite_operation_by_context(
      realign(left_side, old, new),
      preceding,
      following)


def reassign_word_initial(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Reassigns with preceding = beginning of word."""
  return reassign_by_context(
      left_side,
      old,
      new,
      BOW,
      following)


def reassign_word_final(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON) -> p.Fst:
  """Reassigns with following = beginning of word."""
  return reassign_by_context(
      left_side,
      old,
      new,
      preceding,
      EOW)


def reassign_adjacent_alignments(
    left_1: p.FstLike,
    old_right_1: p.FstLike,
    new_right_1: p.FstLike,
    left_2: p.FstLike,
    old_right_2: p.FstLike,
    new_right_2: p.FstLike) -> p.Fst:
  """Assigns new right sides to two adjacent alignments.

  Args:
    left_1: Left side of the first alignment.
    old_right_1: Old right side of the first alignment.
    new_right_1: New right side of the first alignment.
    left_2: Left side of the second alignment.
    old_right_2: Old right side of the second alignment.
    new_right_2: New right side of the second alignment.

  Returns:
    Rewrite Fst.

  Eg. <j><ny> is pronounced {g}{y}

  Following call

  ```
  reassign_adjacent_alignments(
      gr.J, ph.JH, ph.G,
      gr.NY, ph.NY, ph.Y)
  ```

  Would return

  ```
  p.cdrewrite(
      p.cross('<j>={jh}<ny>={ny}', '<j>={g}<ny>={y}'),
      '',
      '',
      u.BYTE_STAR)).optimize()
  ```
  """
  return rewrite(
      u.align(left_1, old_right_1) + u.align(left_2, old_right_2),
      u.align(left_1, new_right_1) + u.align(left_2, new_right_2))


def merge(
    left_1: p.FstLike,
    right_1: p.FstLike,
    left_2: p.FstLike,
    right_2: p.FstLike,
    new_right: p.FstLike = u.EPSILON) -> p.Fst:
  """Merge and optionally assign a new right side to two alignments.

  Args:
    left_1: Left side of the first alignment.
    right_1: Right side of the first alignment.
    left_2: Left side of the second alignment.
    right_2: Right side of the second alignment.
    new_right: Right side of the merged alignment.

  Returns:
    Rewrite Fst.

  Eg. <c>={ch}<ch>={ch}{asp} is transliterated "chh"

  Following call

  ```
  merge(
      gr.C, lt.CH,
      gr.CH, lt.CH + lt.H,
      lt.CH + lt.H)
  ```

  Would return

  ```
  p.cdrewrite(
      p.cross('<c>="ch"<ch>="ch""h"', '<c><ch>="ch""h"'),
      '',
      '',
      u.BYTE_STAR)).optimize()
  ```

  """
  right_side = new_right
  if new_right == u.EPSILON:
    right_side = right_1 + right_2

  return rewrite(
      u.align(left_1, right_1) + u.align(left_2, right_2),
      u.align(left_1 + left_2, right_side))


def reduce_repetition(
    left: p.FstLike,
    right: p.FstLike,
    new_right: p.FstLike = u.EPSILON) -> p.Fst:
  """Merges repeated alignments and reduces or changes the right side."""
  right_side = new_right
  if right_side == u.EPSILON:
    right_side = right
  return merge(left, right, left, right, right_side)


def delete(
    syms: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Deletes symbols."""
  return rewrite_by_context(
      syms,
      u.EPSILON,
      preceding,
      following)


# Removes graphemes and returns a sequence of phonemes or translit substrings.
EXTRACT_RIGHT_SIDE = delete(p.union(u.GRAPHEMES, u.ALIGN_SIGN))


def strip_right_side(syms: p.FstLike) -> p.Fst:
  """Removes graphemes and right side boundaries and returns output string."""
  return (EXTRACT_RIGHT_SIDE @
          delete(syms)
          ).optimize()
