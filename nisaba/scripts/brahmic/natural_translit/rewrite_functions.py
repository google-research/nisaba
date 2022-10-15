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
import nisaba.scripts.brahmic.natural_translit.grapheme_inventory as gr
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.transliteration_inventory as tr
import nisaba.scripts.brahmic.natural_translit.util as u

# Right side of an alignment can be phonemes or transliteration strings.
R_SYMS = p.union(ph.PHONEMES, tr.TRANSLITS).optimize()

SYMS = p.union(gr.GRAPHEMES, R_SYMS).optimize()

# The sequence between any string any other string in the immediately preceding
# or following alignment that doesn't block an operation
SKIP = R_SYMS.ques + gr.GRAPHEMES.ques

# Beginning of word
BOW = u.BOS + gr.GRAPHEMES.ques

# End of word
EOW = R_SYMS.ques + u.EOS


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

  return right_1 + gr.GRAPHEMES.ques + right_2


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

  return left_1 + R_SYMS.ques + left_2


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
EXTRACT_RIGHT_SIDE = rewrite(gr.GRAPHEMES, u.EPSILON)


def strip_right_side(syms: p.FstLike) -> p.Fst:
  """Removes graphemes and right side boundaries and returns output string."""
  return (EXTRACT_RIGHT_SIDE @
          delete(syms)
          ).optimize()
