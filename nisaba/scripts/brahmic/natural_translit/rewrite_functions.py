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

# Left side of an alignment
L_SIDE = (u.AL_L + gr.GRAPHEMES + u.ALIGN_SIGN)

# Right side of an alignment
R_SIDE = (u.ALIGN_SIGN +
          p.union(ph.PHONEMES, tr.TRANSLITS)
          + u.AL_R)

# The symbol sequence between a symbol and the next right side symbol.
NEXT_R = p.union(u.EPSILON, L_SIDE, u.AL_R + L_SIDE)

# Beginning of word
BOW = p.union(u.BOS, u.BOS + u.AL_L, u.BOS + L_SIDE)

# End of word
EOW = p.union(u.EOS, u.AL_R + u.EOS)


def preceding_context(
    preceding: p.FstLike,
    modifiers: p.FstLike = u.EPSILON) -> p.Fst:
  """The preceding context for a rewrite.

  The preceding context can be an alignment, a position, or a symbol and the
  modifiers that doesn't block the operation. The symbols and the modifiers
  can be in the same alignment or in the immediately preceding alignment.

  Args:
    preceding: Symbols necessary for the operation.
    modifiers: Modifiers that doesn't block the operation.

  Returns:
    Preceding context Fst for a rewrite Fst.

  Eg: Voicing requires a vowel to the right. For the following examples
  (<a>={a})(<t>={ti})
  (<a_g>={a}{glide})(<t>={ti})
  (<a><t>={a}{ti})
  (<a_g><t>={a}{glide}{ti})

  Following call

  ```
  preceding_context(ph.VOWEL, ph.GLIDE)
  ```
  would return:
  ```
  p.union('{a}',
          '{a}{glide}',
          '{a})(GRAPHEMES=',
          '{a}{glide})(GRAPHEMES='
          ...)

  """
  return p.union(
      preceding,
      preceding + modifiers.star + NEXT_R)


def following_context(
    following: p.FstLike,
    modifiers: p.FstLike = u.EPSILON) -> p.Fst:
  """The following symbol for a rewrite.

  The preceding context can be an alignment, a position, or a symbol and the
  modifiers that doesn't block the operation. The symbols and the modifiers
  can be in the same alignment or in the immediately following alignment.

  Args:
    following: Symbols necessary for the operation.
    modifiers: Modifiers that doesn't block the operation.

  Returns:
    Following context Fst for a rewrite Fst.

  Eg: Voicing requires a vowel to the left. For the following examples
  (<t>={ti})(<a>={a})
  (<t><asp>={ti}{asp})(<a>={a})
  (<t><a>={ti}{a})
  (<t><asp><a>={ti}{asp}{a})

  Following call

  ```
  following_context(ph.VOWEL, ph.ASP)
  ```
  would return:
  ```
  p.union('{a}',
          '{asp}{a}',
          ')(GRAPHEMES={a}',
          ')(GRAPHEMES={asp}{a}'
          ...)

  """
  return p.union(
      following,
      NEXT_R + following + modifiers.star)


def rewrite(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON,
    sigma: p.FstLike = u.BYTE_STAR) -> p.Fst:
  """A shorthand for generic rewrites.

  Args:
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding context of the rewrite.
    following: Following context of the rewrite.
    sigma: The set of characters which the operation will be carried over.

  Returns:
    Rewrite Fst.

  """
  return p.cdrewrite(
      p.cross(old, new),
      preceding,
      following,
      sigma).optimize()


def rewrite_by_operation(
    operation: p.Fst,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON,
    preceding_modifier: p.FstLike = u.EPSILON,
    following_modifier: p.FstLike = u.EPSILON,
    sigma: p.FstLike = u.BYTE_STAR) -> p.Fst:
  """A rewrite fst that uses a predefined operation as input.

  Args:
    operation: An operation that yields p.cross() functions.
    preceding: Preceding right side context.
    following: Following right side context.
    preceding_modifier: Preceding modifier that doesn't block the operation.
    following_modifier: Following modifier that doesn't block the operation.
    sigma: The set of characters which the operation will be carried over.

  Returns:
    Rewrite fst.

  Eg. Voicing rewrites are predefined.
  VOICING _OP= p.union(..., p.cross(ph.TI, ph.DI), ...)

  Following call

  ```
  rewrite_by_operation(VOICING_OP, ph.VOWEL, ph.VOWEL, ph.GLIDE, ph.ASP)

  ```
  would return:
  ```
  p.cdrewrite(
      p.union(..., p.cross('{ti}', '{di}'), ...),
      p.union('{a}', '{a}{glide}', ...),
      p.union('{a}', '{asp}{a}', ...),
      u.BYTE_STAR)

  """
  return p.cdrewrite(
      operation,
      preceding_context(preceding, preceding_modifier),
      following_context(following, following_modifier),
      sigma).optimize()


def rewrite_by_context(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON,
    preceding_modifier: p.FstLike = u.EPSILON,
    following_modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites the right side of an alignment based on right side contexts.

  Args:
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding right side context.
    following: Following right side context.
    preceding_modifier: Preceding modifier that doesn't block the operation.
    following_modifier: Following modifier that doesn't block the operation.

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
      p.union('{m}', '{m})(GRAPHEMES=', ...),
      p.union('{m}', ')(GRAPHEMES={m}', ...),,
      u.BYTE_STAR))

  """
  return rewrite(
      p.cross(old, new),
      preceding_context(preceding, preceding_modifier),
      following_context(following, following_modifier))


def rewrite_word_initial(
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = u.EPSILON,
    modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites with preceding = beginning of word."""
  return rewrite_by_context(
      old,
      new,
      BOW,
      following,
      following_modifier=modifier)


def rewrite_word_final(
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Rewrites with following = beginning of word."""
  return rewrite_by_context(
      old,
      new,
      preceding,
      EOW,
      modifier)


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
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON,
    preceding_modifier: p.FstLike = u.EPSILON,
    following_modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Changes the right side assignment of a specified left side.

  Args:
    left_side: Specified left side.
    old: Input of the rewrite.
    new: Output of the rewrite.
    preceding: Preceding right side context.
    following: Following right side context.
    preceding_modifier: Preceding modifier that doesn't block the operation.
    following_modifier: Following modifier that doesn't block the operation.

  Returns:
    Rewrite fst.

  Eg. Anusvara assimilates to {m} before labials.

  Following call

  ```
  reassign(
      gr.ANS,
      ph.NSL,
      ph.M,
      following=ph.LABIAL)

  ```
  would return:
  ```
  p.cdrewrite(
      p.cross('(<ans>={nsl})', '(<ans>={m})'),
      '',
      p.union('{m}', ')(GRAPHEMES={m}', ...),,
      u.BYTE_STAR))

  """
  return rewrite_by_operation(
      realign(left_side, old, new),
      preceding_context(preceding, preceding_modifier),
      following_context(following, following_modifier))


def reassign_word_initial(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    following: p.FstLike = u.EPSILON,
    modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Reassigns with preceding = beginning of word."""
  return rewrite_by_operation(
      realign(left_side, old, new),
      BOW,
      following,
      following_modifier=modifier)


def reassign_word_final(
    left_side: p.FstLike,
    old: p.FstLike,
    new: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    modifier: p.FstLike = u.EPSILON) -> p.Fst:
  """Reassigns with following = beginning of word."""
  return rewrite_by_operation(
      realign(left_side, old, new),
      preceding,
      EOW,
      modifier)


def delete(
    syms: p.FstLike,
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON,
    sigma: p.FstLike = u.BYTE_STAR) -> p.Fst:
  """Deletes symbols."""
  return rewrite(
      syms,
      u.EPSILON,
      preceding,
      following,
      sigma)


def extract_right_side(
    sigma: p.FstLike = u.BYTE_STAR) -> p.Fst:
  """Removes everything other than the right side symbols."""
  return delete(p.union(L_SIDE, u.AL_R), sigma=sigma)
