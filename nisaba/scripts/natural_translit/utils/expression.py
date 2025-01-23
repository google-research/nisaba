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

"""Interfaces for generating fsts from objects."""

import itertools
from typing import Union
from nisaba.scripts.natural_translit.utils import inventory
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import operation as op
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import type_op as ty


class Expression(ty.IterableThing, sym.Item):
  """Parent class for Expressions."""

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
  ):
    ty.IterableThing.__init__(self, typed=sym.Item)
    sym.Item.__init__(self, alias, text, index)

  def __str__(self) -> str:
    if self == Expression.ANY:
      return '​🝓⋆​'  # U+200B + U+1F753 + U+22C6 + U+200B
    return self.text

  def _str_items_list(self, *items: ...) -> list[str]:
    return [str(item) for item in (items if items else self)]

  def _str_enclosed(
      self,
      str_list: ty.ListOrNothing = ty.UNSPECIFIED,
      separator: str = ' ',
      left: str = '(',
      right: str = ')',
  ) -> str:
    return (
        left
        + separator.join(ty.type_check(str_list, self._str_items_list()))
        + right
    )

  def _add_item(self, item: sym.Item) -> None:
    """Adds an item to the Expression.

    Args:
      item: Items to be added.

    Returns:
      Expression

    By argument type:
      Atomic: Skips controls, adds a copy of other Atomics.
      Other Expression:
        Same type as this Expression: Adds the items of the argument.
        Other Expression: If the argument has a single item, adds the item
          of the argument. Otherwise adds a copy of the argument.
    """
    if isinstance(item, type(self)):
      self.add(*item)
    elif isinstance(item, sym.Symbol):
      if item.is_control():
        log.dbg_message('Skipping control symbol %s.' % str(item.symbol))
      else:
        self._items.append(Atomic.get_instance(item))
    elif len(item) == 1:
      self.add(item.item(0))
    else:
      self._items.append(item.copy())

  def add(self, *items: ...) -> 'Expression':
    """Default method for type consistency and debugging."""
    log.dbg_message('Cannot add items to %s.' % log.class_and_alias(self))
    return self

  def item_list(self) -> list['Expression']:
    return [item for item in self]

  def state_count(self) -> int:
    if isinstance(self, sym.Symbol):
      return 1
    return sum([item.state_count() for item in self])

  def is_any(self) -> bool:
    if isinstance(self, sym.Symbol):
      return False
    if len(self) == 1:
      return self.item(0).is_any()
    return self is Expression.ANY

  def is_eps(self) -> bool:
    return isinstance(self, sym.Symbol) and self.symbol.is_eps()

  def is_nor(self) -> bool:
    return isinstance(self, sym.Symbol) and self.symbol.is_nor()

  def copy(self) -> 'Expression':
    if self == Expression.ANY:
      return self
    return Expression(self.alias)

  def __add__(self, other: 'Expression') -> 'Cat':
    return Cat(self, other)

  def __or__(self, other: 'Expression') -> 'Or':
    return Or(self, other)

  def __rshift__(self, other: 'Expression') -> 'Alignment':
    return Alignment.simple(self, other)

  def repeat(self, n: int = 2) -> 'Cat':
    """Returns a Cat of n repetitions of this expression."""
    return Cat(*([self] * n))

  def ques(self, preferred: bool = False) -> 'Or':
    """Returns an Or of this expression and empty Cat."""
    return Or(self, Cat()) if preferred else Or(Cat(), self)


Expression.ANY = Expression('any_expression')


class Atomic(Expression, sym.Symbol):
  """An instance of a single symbol."""

  def __init__(self, symbol: sym.Symbol, alias: str = ''):
    Expression.__init__(self, symbol.alias)
    sym.Symbol.__init__(
        self,
        symbol.alias,
        symbol.text,
        symbol.raw,
        symbol.index,
        symbol.name,
    )
    self._item_type = Atomic
    self._items = [self]
    self.symbol = symbol.symbol if isinstance(symbol, Atomic) else symbol
    self.features = symbol.features.copy()

  @classmethod
  def get_instance(cls, symbol: sym.Symbol) -> 'Atomic':
    """Reads a Symbol into an Atomic while matching corresponding constants.

    Args:
      symbol: symbol to be read.

    Returns:
      If the argument is a control Symbol or Atomic, returns the corresponding
      Atomic constant.
      Otherwise returns a new Atomic instance of the symbol.
    """
    if symbol in sym.Symbol.CTRL:
      return Atomic.CTRL.atm_sym_dict[symbol]
    if symbol in Atomic.CTRL and isinstance(symbol, Atomic):
      return symbol
    return Atomic(symbol)

  def copy(self) -> 'Atomic':
    return Atomic.get_instance(self)

  def is_control(self) -> bool:
    return self in Atomic.CTRL or self.symbol in sym.Symbol.CTRL


def _control_atomics() -> inventory.Inventory:
  """Control atomic constants."""
  atm_sym_dict = {ctrl: Atomic(ctrl) for ctrl in sym.Symbol.CTRL}
  atomics = inventory.Inventory.from_list(
      list(atm_sym_dict.values()), alias='CTRL'
  )
  atomics.make_suppl('atm_sym_dict', atm_sym_dict)
  return atomics


Atomic.CTRL = _control_atomics()


class Cat(Expression):
  """Concatenation of expressions."""

  def __init__(self, *items: sym.Item, alias: str = ''):
    super().__init__(alias)
    self.add(*items)

  def __str__(self):
    if not self:
      return str(sym.Symbol.CTRL.eps)
    return self._str_enclosed()

  def add(self, *items: sym.Item) -> 'Cat':
    for item in items:
      if item.is_any():
        self._items.append(item)
      else:
        self._add_item(item)
    return self

  def _add_sym_lists(
      self, list1: list[sym.Symbol], list2: list[sym.Symbol]
  ) -> list[sym.Symbol]:
    if list1 == [Atomic.CTRL.eps.symbol]:
      return list2
    if list2 == [Atomic.CTRL.eps.symbol]:
      return list1
    return list1 + list2

  def symbols(self) -> list[list[sym.Symbol]]:
    """Returns the symbol lists for Cat.

    Empty Cat returns the symbol list of CTRL.eps constant, therefore different
    instances of empty Cat are equivalent to both each other and the Atomic
    constant.
    """
    self_symbols = Atomic.CTRL.eps.symbols()
    for item in self:
      item_symbols = item.symbols()
      for _ in range(len(self_symbols)):
        syms = self_symbols.pop(0)
        self_symbols += [
            self._add_sym_lists(syms, sym_list) for sym_list in item_symbols
        ]
    return self_symbols

  def copy(self) -> 'Cat':
    return Cat(*self.item_list(), alias=self.alias)


class Or(Expression):
  """Alternation for expressions.

  The order of the items in an Or expression reflects the precedence of the
  alternatives. Eg. for rule `a >> (b | c)`, both 'b' and 'c' will be accepted
  as the output for input 'a', however 'b' will get a slightly higher
  evaluation score than 'c' and will be the top rewrite.
  """

  def __init__(self, *items: sym.Item, alias: str = ''):
    super().__init__(alias)
    self.add(*items)

  def __str__(self):
    if not self:
      return str(sym.Symbol.CTRL.nor)
    separator = ' | '
    if len(self) == 1:
      return self._str_enclosed(
          self._str_items_list(self.item(0), sym.Symbol.CTRL.nor), separator
      )
    return self._str_enclosed(separator=separator)

  def _update(self, *items: sym.Item) -> None:
    self._items = []
    self.add(*items)

  def add(self, *items: sym.Item) -> 'Or':
    """Adds items to Or.

    Or shouldn't have recurring symbol lists.
    If an argument is equivalent to this Or and has fewer states, or if the
      argument accepts this Or as well as more symbol lists, existing items are
      reset and the argument is added as an item.
    If an argument is equivalent to this Or but has an equal number of states or
      more, or it's accepted by this Or with fewer symbol lists, it's skipped.
    Otherwise, the argument is added as an item.
    TODO: Minimize the number of states during add. For example,
    ```
    Or(
        Cat(_ATM.a, _ATM.b, _ATM.c), Cat(_ATM.a, _ATM.b, _ATM.d)
    ),
    ```
    should return ((a b (c | d)) | ◎) instead of ((a b c) | (a b d))

    Args:
      *items: Items to be added.

    Returns:
      self
    """
    for item in items:
      # If the Expression.ANY is in Or, don't add any items.
      if Expression.ANY in self:
        break
      # If the item is any, the other items are irrelevant.
      if item.is_any():
        self._items = [item]
        break
      if self.accepts(item):
        if item.accepts(self) and item.state_count() < self.state_count():
          self._update(item)
        else:
          continue
      elif item.accepts(self):
        self._update(item)
      else:
        self._add_item(item)
    return self

  def copy(self) -> 'Or':
    return Or(*self.item_list(), alias=self.alias)

  def symbols(self) -> list[list[sym.Symbol]]:
    """Returns the symbol lists for Or.

    In order to avoid accidental context matches, empty Or returns a new
    instance of CTRL.nor instead of the constant.

    For example, given a rule that requires the preceding context to be a close
    vowel and an inventory with `close_vowel = Or(*close_vowel_list)` where
    `close_vowel_list` is empty, the rule should never apply even if the
    preceding context is the same empty Or.
    """
    if not self:
      return [[Atomic(sym.Symbol.CTRL.nor)]]
    return list(itertools.chain.from_iterable(item.symbols() for item in self))


class _BaseAlignment(Expression):
  """Base class for Alignment."""

  def __init__(
      self,
      left: sym.Item = Expression.ANY,
      right: sym.Item = Expression.ANY,
      alias: str = '',
  ):
    super().__init__(alias)
    self.left = self._set_side(left)
    self.right = self._set_side(right)

  def _set_side(self, side: sym.Item) -> Expression:
    if isinstance(side, sym.Symbol):
      return Atomic.get_instance(side)
    return ty.type_check(side, Expression(side.alias, side.text, side.index))

  # String formatting functions.

  def _side_str(self, side: Expression) -> str:
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

  def _compare(
      self, other: sym.Item, checker_name: str, *args
  ) -> bool:
    if not isinstance(other, _BaseAlignment):
      return False
    left = getattr(self.left, checker_name)
    right = getattr(self.right, checker_name)
    return left(other.left, *args) and right(other.right, *args)

  def accepts(
      self, other: sym.Item, equivalent: bool = False
  ) -> bool:
    return self._compare(other, 'accepts', equivalent)

  def is_equivalent(self, other: sym.Item) -> bool:
    return self._compare(other, 'is_equivalent')

  def contains(
      self,
      other: sym.Item,
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    return self._compare(other, 'contains', match_head, match_tail)

  def is_contained(
      self,
      other: sym.Item,
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    return self._compare(other, 'is_contained', match_head, match_tail)

  def matches(self, other: sym.Item) -> bool:
    return self._compare(other, 'matches')

  def head_matches(self, other: sym.Item) -> bool:
    return self._compare(other, 'head_matches')

  def is_prefix(self, other: sym.Item) -> bool:
    return self._compare(other, 'is_prefix')

  def tail_matches(self, other: sym.Item) -> bool:
    return self._compare(other, 'tail_matches')

  def is_suffix(self, other: sym.Item) -> bool:
    return self._compare(other, 'is_suffix')


_BASE_ANY = _BaseAlignment(Expression.ANY, Expression.ANY)


class Alignment(_BaseAlignment):
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
    LEXICON: Alignables that come from a lexicon that will be prioritised
      over other rules. Eg. frequent affixes or high profile entity names.
    NATIVE: Alignables for the native language.
    SPELLOUT: Alignables for spelled out letters.
    UNSPECIFIED_SOURCE = Alignments from an unspecified source.
  """

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
      left: sym.Item = Expression.ANY,
      right: sym.Item = Expression.ANY,
      preceding_left: sym.Item = Expression.ANY,
      preceding_right: sym.Item = Expression.ANY,
      following_left: sym.Item = Expression.ANY,
      following_right: sym.Item = Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.unassigned,
      priority: int = 0,
      applied_cost: Union[float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.UNSPECIFIED_SOURCE',
  ):
    super().__init__(left, right, alias)
    # TODO(): Expand context to allow Cat and Or of alignments.
    # Eg. `preceding=((vowel_grapheme >> ANY) | (ANY >> vowel_phoneme)))`
    # will apply if it's preceded by an alignment that has a vowel grapheme on
    # the left side or a vowel phoneme on the right side, regardless of what
    # they are aligned with.
    self.preceding = _BaseAlignment(preceding_left, preceding_right)
    self.following = _BaseAlignment(following_left, following_right)
    self.from_bos = from_bos
    self.to_eos = to_eos
    self.operation = operation
    self.priority = priority
    self.applied_cost = ty.type_check(
        applied_cost, float(self.operation.base_cost)
    )
    self.source = source

  def _context_str(
      self, context: _BaseAlignment, prefix: str = '', suffix: str = ''
  ) -> str:
    if context.is_any():
      return ''
    return context.enclosed_str('⌈', '⌋', prefix, suffix)

  def _pre_str(self) -> str:
    prefix = str(Atomic.CTRL.bos) if self.from_bos else ''
    pre_str = self._context_str(self.preceding, prefix)
    return pre_str + ' ' if pre_str else ''

  def _fol_str(self) -> str:
    suffix = str(Atomic.CTRL.eos) if self.to_eos else ''
    fol_str = self._context_str(self.following, suffix=suffix)
    return ' ' + fol_str if fol_str else ''

  def string(self) -> str:
    """Detailed string representation of the alignment.

    Returns:
      String is formatted as:
      (⌈<preceding>​⌋ <left>∶<right> ⌈​<following>⌋, <operation> (<base_cost>))
      ANY context and unassigned operations are omitted.

    Examples:
    - `(c∶d)` means that expression `c` is is aligned with expression `d` with
      an unassigned operation regardless of the context.
    - `(⌈grapheme∶nasal​⌋ a∶b ⌈​grapheme∶vowel⌋, alignable (0.000))` means that
      expression `a` is aligned with expression `b` with `alignable` operation
      at 0 cost when it's preceded by a grapheme that is aligned with a nasal
      and followed by a grapheme that is aligned with a vowel.
    """
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
      left: sym.Item = Expression.ANY,
      right: sym.Item = Expression.ANY,
  ) -> 'Alignment':
    """An unassigned alignment with no context."""
    simple = cls(left=left, right=right)
    simple.preceding = Alignment.ANY
    simple.following = Alignment.ANY
    return simple

  @classmethod
  def rule(
      cls,
      alias: str,
      alignment: 'Alignment',
      preceding: 'Alignment' = _BASE_ANY,
      following: 'Alignment' = _BASE_ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.alignable,
      priority: int = 0,
      applied_cost: Union[float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    rule = cls(
        alias,
        alignment.left,
        alignment.right,
        preceding.left,
        preceding.right,
        following.left,
        following.right,
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
      alias: str,
      left: sym.Item,
      preceding: 'Alignment' = _BASE_ANY,
      following: 'Alignment' = _BASE_ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.deletion,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    return cls.rule(
        alias,
        left >> Atomic.CTRL.eps,
        preceding,
        following,
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
      alias: str,
      right: sym.Item,
      preceding: 'Alignment' = _BASE_ANY,
      following: 'Alignment' = _BASE_ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.insertion,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    return cls.rule(
        alias,
        Atomic.CTRL.eps >> right,
        preceding,
        following,
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
      alias: str,
      alignment: 'Alignment',
      preceding: 'Alignment' = _BASE_ANY,
      following: 'Alignment' = _BASE_ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.interchangeable,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> tuple['Alignment', 'Alignment']:
    common = (
        preceding,
        following,
        from_bos,
        to_eos,
        operation,
        priority,
        applied_cost,
        source,
    )
    left_to_right = cls.rule(
        alias + '_l2r', alignment.left >> alignment.right, *common
    )
    right_to_left = cls.rule(
        alias + '_r2l', alignment.right >> alignment.left, *common
    )
    return left_to_right, right_to_left

  def copy(self) -> 'Alignment':
    if self.source == Alignment.CONSTANT:
      return self
    return Alignment.rule(
        self.alias,
        self.left.copy() >> self.right.copy(),
        self.preceding.left.copy() >> self.preceding.right.copy(),
        self.following.left.copy() >> self.following.right.copy(),
        self.from_bos,
        self.to_eos,
        self.operation,
        self.priority,
        self.applied_cost,
        self.source,
    )

  def is_assigned(self) -> bool:
    return self.operation.is_assigned()

  def context_matches(
      self, preceding: _BaseAlignment, following: _BaseAlignment
  ) -> bool:
    return (
        (self.from_bos and self.preceding.matches(preceding))
        or (not self.from_bos and self.preceding.is_suffix(preceding))
    ) and (
        (self.to_eos and self.following.matches(following))
        or (not self.to_eos and self.following.is_prefix(following))
    )


def _constants() -> tuple[Alignment, Alignment, Alignment]:
  """Alignment constants."""
  any_alg = Alignment('any')
  eps = Alignment('eps', Atomic.CTRL.eps, Atomic.CTRL.eps)
  nor = Alignment(
      'nor',
      Atomic.CTRL.nor,
      Atomic.CTRL.nor,
      operation=op.Operation.COMMON.error,
  )
  for alg in [any_alg, eps, nor]:
    alg.source = Alignment.CONSTANT
    alg.preceding = any_alg
    alg.following = any_alg
  return any_alg, eps, nor


Alignment.ANY, Alignment.EPS, Alignment.NOR = _constants()
