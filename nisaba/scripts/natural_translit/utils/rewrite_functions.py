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
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls


def rewrite_op(
    operation: p.Fst,
    preceding: p.FstLike = al.EPSILON,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """A rewrite fst that uses a predefined operation as input.

  If the context is specified, adds SKIP sequence to look at the adjacent
  alignments.

  Args:
    operation: An operation that yields p.cross() functions.
    preceding: Preceding context.
    following: Following context.

  Returns:
    Rewrite fst.

  Following call:
  ```
  rewrite_op(VOICING_OP, ph.VOWEL, ph.VOWEL)
  ```
  will return:
  ```
  p.cdrewrite(
      p.union(..., p.cross('{ti}', '{di}'), ...),
      p.union('{a}', '{a}{nsl}', '{a}{glide}', '{e}', '{e}{nsl}'...),
      p.union('{a}', '{a}{nsl}', '{a}{glide}', '{e}', '{e}{nsl}'...),
      al.BYTE_STAR)
  ```
  """
  preceding_context = al.EPSILON
  following_context = al.EPSILON
  if preceding is not al.EPSILON:
    preceding_context = preceding + al.SKIP
  if following is not al.EPSILON:
    following_context = al.SKIP + following
  return p.cdrewrite(
      operation,
      preceding_context,
      following_context,
      al.BYTE_STAR).optimize()


def rewrite(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = al.EPSILON,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """Rewrite operation where the operation is a single p.cross."""
  return rewrite_op(
      p.cross(old, new),
      preceding,
      following)


def rewrite_word_initial(
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """Rewrites with preceding = beginning of word."""
  return rewrite(
      old,
      new,
      al.BOW,
      following)


def rewrite_word_final(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = al.EPSILON) -> p.Fst:
  """Rewrites with following = beginning of word."""
  return rewrite(
      old,
      new,
      preceding,
      al.EOW)


def reassign(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = al.EPSILON,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """Changes the right side assignment of a specified left side.

  Args:
    left_side: Specified left side.
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding right side context.
    following: Following right side context.

  Returns:
    Rewrite fst.

  Following call:
  ```
  reassign(
      gr.ANS,
      ph.NSL,
      ph.M,
      following=ph.LABIAL)
  ```
  will return:
  ```
  p.cdrewrite(
      p.cross('<ans>{nsl}', '<ans>{m}'),
      '',
      p.union('{m}', 'gr.GRAPHEMES{m}', ...),,
      al.BYTE_STAR))
  ```
  """
  return rewrite_op(
      al.realign(left_side, old, new),
      preceding,
      following)


def reassign_word_initial(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """Reassigns with preceding = beginning of word."""
  return reassign(
      left_side,
      old,
      new,
      al.BOW,
      following)


def reassign_word_final(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = al.EPSILON) -> p.Fst:
  """Reassigns with following = beginning of word."""
  return reassign(
      left_side,
      old,
      new,
      preceding,
      al.EOW)


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

  Following call:
  ```
  reassign_adjacent_alignments(
      gr.J, ph.JH, ph.G,
      gr.NY, ph.NY, ph.Y)
  ```
  will return:
  ```
  p.cdrewrite(
      p.cross('<j>={jh}<ny>={ny}', '<j>={g}<ny>={y}'),
      '',
      '',
      al.BYTE_STAR)).optimize()
  ```
  """
  return rewrite(
      al.align(left_1, old_right_1) + al.align(left_2, old_right_2),
      al.align(left_1, new_right_1) + al.align(left_2, new_right_2))


def merge(
    left_1: p.FstLike,
    right_1: p.FstLike,
    left_2: p.FstLike,
    right_2: p.FstLike,
    new_right: p.FstLike = al.EPSILON) -> p.Fst:
  """Merge and optionally assign a new right side to two alignments.

  Args:
    left_1: Left side of the first alignment.
    right_1: Right side of the first alignment.
    left_2: Left side of the second alignment.
    right_2: Right side of the second alignment.
    new_right: Right side of the merged alignment.

  Returns:
    Rewrite Fst.

  Following call:
  ```
  merge(
      gr.C, lt.CH,
      gr.CH, lt.CH + lt.H,
      lt.CH + lt.H)
  ```
  will return:
  ```
  p.cdrewrite(
      p.cross('<c>="ch"<ch>="ch""h"', '<c><ch>="ch""h"'),
      '',
      '',
      al.BYTE_STAR)).optimize()
  ```
  """
  right_side = new_right
  if new_right == al.EPSILON:
    right_side = right_1 + right_2

  return rewrite(
      al.align(left_1, right_1) + al.align(left_2, right_2),
      al.align(left_1 + left_2, right_side))


def reduce_repetition(
    left: p.FstLike,
    right: p.FstLike,
    new_right: p.FstLike = al.EPSILON) -> p.Fst:
  """Merges repeated alignments and reduces or changes the right side."""
  right_side = new_right
  if right_side == al.EPSILON:
    right_side = right
  return merge(left, right, left, right, right_side)


def delete(
    syms: p.FstLike,
    preceding: p.FstLike = al.EPSILON,
    following: p.FstLike = al.EPSILON) -> p.Fst:
  """Deletes symbols."""
  return rewrite(
      syms,
      al.EPSILON,
      preceding,
      following)


# Removes graphemes and returns a sequence of phonemes or translit substrings.
EXTRACT_RIGHT_SIDE = delete(ls.union_opt(al.GRAPHEMES, al.ALIGN_SIGN))


def strip_right_side(syms: p.FstLike) -> p.Fst:
  """Removes graphemes and right side boundaries and returns output string."""
  return (EXTRACT_RIGHT_SIDE @
          delete(syms)
          ).optimize()
