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
  priority: Priority of the alignment. When the applied cost of multiple
    rules are equal, the rule with the highest priority will be applied.
  applied_cost: Cost of the alignment when it's applied in context.
  source: Source of the alignment.

For inspection and debugging purposes, alignments are represented as strings in
  the following format:

([<preceding context>] <input>:<output> [<following context>], operation)

Alignments can be defined in an inventory as a set of rules to build grammars,
  or to assess the structural correspondence of two expressions.

Example:
  `([grapheme:nasal] a:b [grapheme:vowel], alignable (0.00))` means that
  expression `a` is rewritten as expression `b` with `alignable` operation with
  0 cost when it's preceded by a grapheme that corresponds to a nasal and
  followed by a grapheme that corresponds to a vowel.

Alignment sources:
  ALIGNER: Alignments from an aligner output that doesn't correspond to a
    predefined rule. Eg. identity or token boundary alignments.
  CONSTANT: Alignment class constants.
  ENGLISH: English alignables.
  FOREIGN: Alignables for foreign languages other than English
  LEXICON: Alignables that come from a lexicon that will be prioritised over
    other rules. Eg. frequent affixes or high profile entity names.
  NATIVE: Alignables for the native language.
  SPELLOUT: Alignables for spelled out letters.
  UNSPECIFIED = Alignments from an unspecified source.
"""

import enum
# from typing import Union
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import operation as op
# from nisaba.scripts.natural_translit.utils
# import type_op as ty


class Alignment(exp.Expression):
  """An Expression that represents an alignment of exp.Expressions."""

  class Source(enum.StrEnum):
    ALIGNER = 'aligner'
    CONSTANT = 'constant'
    ENGLISH = 'english'
    FOREIGN = 'foreign'
    LEXICON = 'lexicon'
    NATIVE = 'native'
    SPELLOUT = 'spellout'
    UNSPECIFIED = 'unspecified'

  def __init__(self, alias: str = ''):
    super().__init__(alias)
    self.left = exp.Expression.ANY
    self.right = exp.Expression.ANY
    self.preceding = exp.Expression.ANY
    self.following = exp.Expression.ANY
    self.from_bos = False
    self.to_eos = False
    self.operation = op.Operation.COMMON.unassigned
    self.priority = 0
    self.applied_cost = self.operation.base_cost
    self.source = Alignment.Source.UNSPECIFIED

  def _side_str(self, side: exp.Expression) -> str:
    if side.is_any() or len(side) != 1:
      return str(side)
    return side.item(0).text

  def _context_str(self, context: exp.Expression) -> str:
    if context.is_any() or not isinstance(context, Alignment):
      return ''
    return '%s:%s' % (
        self._side_str(context.left),
        self._side_str(context.right),
    )

  def _pre_str(self) -> str:
    text = self._context_str(self.preceding)
    prefix = exp.Atomic.CTRL.bos.text if self.from_bos else ''
    return '[%s%s] ' % (prefix, text) if text else ''

  def _fol_str(self) -> str:
    text = self._context_str(self.following)
    suffix = exp.Atomic.CTRL.eos.text if self.to_eos else ''
    return ' [%s%s]' % (text, suffix) if text else ''

  def __str__(self):
    if self.operation.is_assigned():
      operation = ', %s' % str(self.operation)
    else:
      operation = ''
    return '(%s%s:%s%s%s)' % (
        self._pre_str(),
        self._side_str(self.left),
        self._side_str(self.right),
        self._fol_str(),
        operation,
    )

  def tsv_row(self) -> str:
    return '\t'.join([
        self.alias,
        ''.join([item.text for item in self.left]),
        ''.join([item.text for item in self.right]),
        str(self.operation.match),
        str(self.applied_cost),
    ])

  def _set_side(self, side: exp.Expression.OR_SYMBOL) -> exp.Expression:
    if not isinstance(side, exp.Expression):
      return exp.Atomic.read(side)
    return side

  @classmethod
  def simple(
      cls,
      left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
      right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
  ) -> 'Alignment':
    alignment = cls()
    alignment.left = alignment._set_side(left)
    alignment.right = alignment._set_side(right)
    return alignment

#   @classmethod
#   def constant(
#       cls,
#       alias: str = '',
#       left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       operation: op.Operation = op.Operation.COMMON.unassigned,
#   ) -> 'Alignment':
#     alignment = cls(alias)
#     alignment.left = alignment._set_side(left)
#     alignment.right = alignment._set_side(right)
#     alignment.operation = operation
#     alignment.source = Alignment.Source.CONSTANT
#     return alignment

  # TODO: Expand context to allow Cat and Or of alignments.
  # Eg. a rule with `preceding=((vowel_grapheme:any) | (any:vowel_phoneme)))`
  # will apply if it's preceded by an alignment that has a vowel grapheme on the
  # left side or a vowel phoneme on the right side, regardless of what they are
  # aligned with.
#   def _set_context(
#       self, left: exp.Expression.OR_SYMBOL, right: exp.Expression.OR_SYMBOL
#   ) -> 'Alignment':
#     if left.is_any() and right.is_any():
#       return Alignment.ANY
#     return Alignment.simple(left, right)

#   @classmethod
#   def rule(
#       cls,
#       alias: str = '',
#       left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       from_bos: bool = False,
#       to_eos: bool = False,
#       operation: op.Operation = op.Operation.COMMON.alignable,
#       priority: int = 0,
#       applied_cost: Union[float, ty.Nothing] = ty.UNSPECIFIED,
#       source: Source = Source.UNSPECIFIED,
#   ) -> 'Alignment':
#     rule = cls()
#     rule.alias = alias
#     rule.left = rule._set_side(left)
#     rule.right = rule._set_side(right)
#     rule.preceding = rule._set_context(preceding_left, preceding_right)
#     rule.following = rule._set_context(following_left, following_right)
#     rule.from_bos = from_bos
#     rule.to_eos = to_eos
#     rule.operation = operation
#     rule.priority = priority
#     if isinstance(applied_cost, float):
#       rule.applied_cost = applied_cost
#     else:
#       rule.applied_cost = rule.operation.base_cost
#     rule.source = source
#     return rule

#   @classmethod
#   def deletion(
#       cls,
#       alias: str = '',
#       left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       from_bos: bool = False,
#       to_eos: bool = False,
#       operation: op.Operation = op.Operation.COMMON.deletion,
#       priority: int = 0,
#       applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
#       source: Source = Source.UNSPECIFIED,
#   ) -> 'Alignment':
#     return cls.rule(
#         alias,
#         left,
#         exp.Atomic.CTRL.eps,
#         preceding_left,
#         preceding_right,
#         following_left,
#         following_right,
#         from_bos,
#         to_eos,
#         operation,
#         priority,
#         applied_cost,
#         source,
#     )

#   @classmethod
#   def insertion(
#       cls,
#       alias: str = '',
#       right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       from_bos: bool = False,
#       to_eos: bool = False,
#       operation: op.Operation = op.Operation.COMMON.insertion,
#       priority: int = 0,
#       applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
#       source: Source = Source.UNSPECIFIED,
#   ) -> 'Alignment':
#     return cls.rule(
#         alias,
#         exp.Atomic.CTRL.eps,
#         right,
#         preceding_left,
#         preceding_right,
#         following_left,
#         following_right,
#         from_bos,
#         to_eos,
#         operation,
#         priority,
#         applied_cost,
#         source,
#     )

#   @classmethod
#   def interchangeable(
#       cls,
#       alias: str = '',
#       left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       preceding_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_left: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       following_right: exp.Expression.OR_SYMBOL = exp.Expression.ANY,
#       from_bos: bool = False,
#       to_eos: bool = False,
#       operation: op.Operation = op.Operation.COMMON.interchangeable,
#       priority: int = 0,
#       applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
#       source: Source = Source.UNSPECIFIED,
#   ) -> tuple['Alignment', 'Alignment']:
#     common = (
#         preceding_left,
#         preceding_right,
#         following_left,
#         following_right,
#         from_bos,
#         to_eos,
#         operation,
#         priority,
#         applied_cost,
#         source,
#     )
#     left_to_right = cls.rule(alias + '_l2r', left, right, *common)
#     right_to_left = cls.rule(alias + '_r2l', right, left, *common)
#     return left_to_right, right_to_left

#   def is_any(self) -> bool:
#     return self.left.is_any() and self.right.is_any()

#   def is_eps(self) -> bool:
#     return self.left.is_eps() and self.right.is_eps()

#   def is_nor(self) -> bool:
#     return self.left.is_nor() and self.right.is_nor()

#   def _copy_context(
#       self, context: exp.Expression
#   ) -> tuple[exp.Expression, exp.Expression]:
#     if isinstance(context, Alignment):
#       return context.left.copy(), context.right.copy()
#     return exp.Expression.ANY, exp.Expression.ANY

#   def copy(self) -> 'Alignment':
#     if (
#         self == Alignment.ANY
#         or self == Alignment.EPSILON
#         or self == Alignment.ERROR
#     ):
#       return self
#     return Alignment.rule(
#         self.alias,
#         self.left.copy(),
#         self.right.copy(),
#         *self._copy_context(self.preceding),
#         *self._copy_context(self.following),
#         self.from_bos,
#         self.to_eos,
#         self.operation,
#         self.priority,
#         self.applied_cost,
#         self.source,
#     )


# Alignment.ANY = Alignment.constant('any')
# Alignment.EPSILON = Alignment.constant(
#     'empty', exp.Atomic.CTRL.eps, exp.Atomic.CTRL.eps
# )
# Alignment.ERROR = Alignment.constant(
#     'error',
# exp.Atomic.CTRL.nor, exp.Atomic.CTRL.nor, op.Operation.COMMON.error
# )
