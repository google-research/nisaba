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

"""Alignment class for defining a relation between two expressions.

Attributes:
  alias: Alias of the Expression.
  left: Left side of the Alignment.
  right: Right side of the Alignment.
  preceding: Preceding context.
  following: Following context.
  from_bos: If True, preceding context starts from the beginning of the
    sequence.
  to_eos: If True, the following context ends at the end of the sequence.
  operation: Operation that represents the relation between the sides of the
    alignment.
  priority: Priority of the alignment. When the applied cost of multiple rules
    are equal, the rule with the highest priority will be applied.
  applied_cost: Cost of the alignment when it's applied in context.
  source: Alignments can be defined in an inventory as a set of rules to build
    grammars, or they can be formed by an aligner to assess the structural
    correspondence of two expressions.
    Source Constants:
      ALIGNER: Alignments from an aligner output that doesn't correspond to a
        predefined rule. Eg. identity or token boundary alignments.
      CONSTANT: Alignment class constants.
      ENGLISH: English alignables.
      FOREIGN: Alignables for foreign languages other than English
      LEXICON: Alignables that come from a lexicon that will be prioritised over
        other rules. Eg. frequent affixes or high profile entity names.
      NATIVE: Alignables for the native language.
      SPELLOUT: Alignables for spelled out letters.
      UNSPECIFIED_SOURCE = Alignments from an unspecified source.

For inspection and debugging purposes, alignments are represented as strings in
  the following format, omitting context that matches with any expression as
  well as unassigned operations:

(⌈<preceding>​⌋ <left>∶<right> ⌈​<following>⌋, <operation>, (<base_cost>))

Examples:
  - `(c∶d)` means that expression `c` is is aligned with expression `d` with
    an unassigned operation regardless of the context.
  - `(⌈grapheme∶nasal​⌋ a∶b ⌈​grapheme∶vowel⌋, alignable (0.000))` means that
    expression `a` is aligned with expression `b` with `alignable` operation at
    0 cost when it's preceded by a grapheme that is aligned with a nasal and
    followed by a grapheme that is aligned with a vowel.
"""

from typing import Union
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import operation as op
from nisaba.scripts.natural_translit.utils import type_op as ty


class _BaseAlignment(exp.Expression):
  """Base class for Alignment."""

  def __init__(
      self,
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      alias: str = '',
  ):
    super().__init__(alias)
    self.left = self._set_side(left)
    self.right = self._set_side(right)

  def _set_side(self, side: exp.Expression.OR_SYMBOL) -> exp.Expression:
    if not isinstance(side, exp.Expression):
      return exp.Atomic.read(side)
    return side

  def _side_str(self, side: exp.Expression) -> str:
    if side.is_any() or len(side) != 1:
      return str(side)
    return side.item(0).text

  def _aligned_str(self) -> str:
    return '%s∶%s' % (self._side_str(self.left), self._side_str(self.right))

  def enclosed_str(
      self,
      left_boundary: str = '(',
      right_boundary: str = ')',
      prefix: str = '',
      suffix: str = '',
  ) -> str:
    return (
        left_boundary + prefix + self._aligned_str() + suffix + right_boundary
    )

  def __str__(self) -> str:
    return self.enclosed_str()

  def is_any(self) -> bool:
    return self.left.is_any() and self.right.is_any()

  def is_eps(self) -> bool:
    return self.left.is_eps() and self.right.is_eps()

  def is_nor(self) -> bool:
    return self.left.is_nor() and self.right.is_nor()


class Alignment(_BaseAlignment):
  """An Expression that represents an alignment of exp.Expressions."""

  ALIGNER = 'aligner'
  CONSTANT = 'constant'
  ENGLISH = 'english'
  FOREIGN = 'foreign'
  LEXICON = 'lexicon'
  NATIVE = 'native'
  SPELLOUT = 'spellout'
  UNSPECIFIED_SOURCE = 'unspecified_source'

  def __init__(
      self,
      alias: str = '',
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.unassigned,
      priority: int = 0,
      applied_cost: Union[float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.UNSPECIFIED_SOURCE',
  ):
    super().__init__(left, right, alias)
    # TODO: Expand context to allow Cat and Or of alignments.
    # Eg. `preceding=((vowel_grapheme:any) | (any:vowel_phoneme)))`
    # will apply if it's preceded by an alignment that has a vowel grapheme on
    # the left side or a vowel phoneme on the right side, regardless of what
    # they are aligned with.
    self.preceding = _BaseAlignment(preceding_left, preceding_right)
    self.following = _BaseAlignment(following_left, following_right)
    self.from_bos = from_bos
    self.to_eos = to_eos
    self.operation = operation
    self.priority = priority
    if isinstance(applied_cost, float):
      self.applied_cost = applied_cost
    else:
      self.applied_cost = self.operation.base_cost
    self.source = source

  def _context_str(
      self, context: _BaseAlignment, prefix: str = '', suffix: str = ''
  ) -> str:
    if context.is_any():
      return ''
    return context.enclosed_str('⌈', '⌋', prefix, suffix)

  def _pre_str(self) -> str:
    prefix = str(exp.Atomic.CTRL.bos) if self.from_bos else ''
    pre_str = self._context_str(self.preceding, prefix)
    return pre_str + ' ' if pre_str else ''

  def _fol_str(self) -> str:
    suffix = str(exp.Atomic.CTRL.eos) if self.to_eos else ''
    fol_str = self._context_str(self.following, suffix=suffix)
    return ' ' + fol_str if fol_str else ''

  def __str__(self):
    op_str = ', %s' % str(self.operation) if self.is_assigned() else ''
    return self.enclosed_str(
        prefix=self._pre_str(),
        suffix=self._fol_str() + op_str,
    )

  def tsv_row(self) -> str:
    return '\t'.join([
        self.alias,
        ''.join([item.text for item in self.left]),
        ''.join([item.text for item in self.right]),
        str(self.operation.match),
        str(self.applied_cost),
    ])

  @classmethod
  def simple(
      cls,
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
  ) -> 'Alignment':
    simple = cls(left=left, right=right)
    simple.preceding = Alignment.ANY
    simple.following = Alignment.ANY
    return simple

  @classmethod
  def rule(
      cls,
      alias: str = '',
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.alignable,
      priority: int = 0,
      applied_cost: Union[float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    rule = cls(
        alias,
        left,
        right,
        preceding_left,
        preceding_right,
        following_left,
        following_right,
        from_bos,
        to_eos,
        operation,
        priority,
        applied_cost,
        source,
    )
    if rule.preceding.is_any():
      rule.preceding = Alignment.ANY
    if rule.following.is_any():
      rule.following = Alignment.ANY
    return rule

  @classmethod
  def deletion(
      cls,
      alias: str = '',
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.deletion,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    return cls.rule(
        alias,
        left,
        exp.Atomic.CTRL.eps,
        preceding_left,
        preceding_right,
        following_left,
        following_right,
        from_bos,
        to_eos,
        operation,
        priority,
        applied_cost,
        source,
    )

  @classmethod
  def insertion(
      cls,
      alias: str = '',
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.insertion,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    return cls.rule(
        alias,
        exp.Atomic.CTRL.eps,
        right,
        preceding_left,
        preceding_right,
        following_left,
        following_right,
        from_bos,
        to_eos,
        operation,
        priority,
        applied_cost,
        source,
    )

  @classmethod
  def interchangeable(
      cls,
      alias: str = '',
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.interchangeable,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> tuple['Alignment', 'Alignment']:
    common = (
        preceding_left,
        preceding_right,
        following_left,
        following_right,
        from_bos,
        to_eos,
        operation,
        priority,
        applied_cost,
        source,
    )
    left_to_right = cls.rule(alias + '_l2r', left, right, *common)
    right_to_left = cls.rule(alias + '_r2l', right, left, *common)
    return left_to_right, right_to_left

  def copy(self) -> 'Alignment':
    if self.source == Alignment.CONSTANT:
      return self
    return Alignment.rule(
        self.alias,
        self.left.copy(),
        self.right.copy(),
        self.preceding.left.copy(),
        self.preceding.right.copy(),
        self.following.left.copy(),
        self.following.right.copy(),
        self.from_bos,
        self.to_eos,
        self.operation,
        self.priority,
        self.applied_cost,
        self.source,
    )

  def is_assigned(self) -> bool:
    return self.operation.is_assigned()


def _constants() -> tuple[Alignment, Alignment, Alignment]:
  """Alignment constants."""
  any_alg = Alignment('any')
  eps = Alignment('eps', exp.Atomic.CTRL.eps, exp.Atomic.CTRL.eps)
  nor = Alignment(
      'nor',
      exp.Atomic.CTRL.nor,
      exp.Atomic.CTRL.nor,
      operation=op.Operation.COMMON.error,
  )
  for alg in [any_alg, eps, nor]:
    alg.source = Alignment.CONSTANT
    alg.preceding = any_alg
    alg.following = any_alg
  return any_alg, eps, nor


Alignment.ANY, Alignment.EPS, Alignment.NOR = _constants()
