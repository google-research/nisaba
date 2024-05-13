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

from typing import Union
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import operation as op
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import type_op as ty


class Expression(ty.IterableThing):
  """Parent class for Expressions."""

  OR_SYMBOL = Union['Expression', sym.Symbol]

  def __init__(self, alias: str = ''):
    super().__init__(alias=alias)
    self._item_type = Expression
    self.index = hash(self)

  def __str__(self) -> str:
    if self == Expression.ANY:
      return '​🝓⋆​'  # U+200B + U+1F753 + U+22C6 + U+200B
    return self.text

  def _str_items_list(self, *items: ...) -> list[str]:
    if not items:
      items = self
    return [str(item) for item in items]

  def _str_enclosed(
      self,
      str_list: ty.ListOrNothing = ty.UNSPECIFIED,
      separator: str = ' ',
      left: str = '(',
      right: str = ')',
  ) -> str:
    if ty.is_nothing(str_list):
      str_list = self._str_items_list()
    return '%s%s%s' % (left, separator.join(str_list), right)

  def _add_item(self, item: 'Expression') -> None:
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
        self._items.append(item.copy())
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

  def symbols(self) -> list[list[sym.Symbol]]:
    """Default class method for type compatibilty.

    Returns:
      Lists all possible symbol sequences accepted by this expression as flat
      lists of symbols.
    """
    return []

  def symbols_str(self) -> str:
    text = '[\n'
    for sym_list in self.symbols():
      text += '  [%s]\n' % ', '.join([str(sym) for sym in sym_list])
    return text + ']\n'

  def state_count(self) -> int:
    return sum([item.state_count() for item in self])

  def _symbols_of(
      self, other: 'Expression.OR_SYMBOL'
  ) -> list[list[sym.Symbol]]:
    if isinstance(other, Expression):
      return other.symbols()
    else:
      return [[other]]

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

  def accepts(
      self, other: 'Expression.OR_SYMBOL', equivalent: bool = False
  ) -> bool:
    """Checks if this expression accepts all symbol lists of the argument.

    Args:
      other: A symbol or expression.
      equivalent: If True, the argument must accept this expression too.

    Returns:
      bool
    """
    if self.is_any() or other.is_any():
      if equivalent:
        return self.is_any() and other.is_any()
      return True
    self_symbols, other_symbols = self.symbols(), self._symbols_of(other)
    self_len, other_len = len(self_symbols), len(other_symbols)
    if (
        not self_len
        or self_len < other_len
        or (equivalent and self_len != other_len)
    ):
      return False
    for sym_list in other_symbols:
      if sym_list not in self_symbols:
        return False
    return True

  def is_equivalent(self, other: 'Expression.OR_SYMBOL') -> bool:
    return self.accepts(other, equivalent=True)

  def contains_symbol_list(
      self,
      search_for: list[sym.Symbol],
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    """Checks if this expression contains the given symbol list.

    The symbols in the argument must be adjacent and in the same order in at
    least one symbol list of the expression.

    Args:
      search_for: Symbol list to be searched for.
      match_head: If True, the argument must match the beginning of at least one
        symbol list of this expression.
      match_tail: If True, the argument must match the end of at least one
        symbol list of this expression.

    If both head and tail are true, the argument must be equal to at least one
    symbol list of this expression.

    All expressions contain epsilon list [ℰ] in all conditions. No expression
    contains empty Or list [◎], even if both expressions are empty Ors.

    Returns:
      bool.

    Example:
    a.symbols() = [[a, b, c, d], [e, f, g], [h]]
    a.contains_symbol_list(arg, head, tail) for arguments:
      head=False, tail=False
        [ℰ]: True.
        [a, b, c, d]: True, [a, b, c, d] is in the symbol list.
        [b, c]: True, [b, c] is a sublist of [a, b, c, d].
        [a, b, c, d, e, f, g]: False, symbols aren't in the same list.
        [a, c]: False, symbols aren't adjacent in [a, b, c, d].
        [c, b]: False, symbol order doesn't match [a, b, c, d].
      if head=True, tail=False
        [a]: True
        [a, b]: True
        [b, c, d]: False
        [h]: True
      if head=False, tail=True
        [d]: True
        [c, d]: True
        [a, b, c]: False
        [h]: True
      if head=True tail=True
        [a, b, c, d]: True
        [e, f, g]: True
        [h]: True
        [ℰ]: True
        any other argument returns False
    """
    if search_for == [sym.Symbol.CTRL.eps]:
      return True
    if search_for == [sym.Symbol.CTRL.nor]:
      return False
    if self.is_any():
      return True
    # Loop over symbol lists, eg: [[a, b, c, d], [e, f, g]]
    for symbol_list in self.symbols():
      while symbol_list:
        search_in = symbol_list.copy()  # [a, b, c, d]
        while search_in:
          if search_in == search_for:
            return True
          # head=True, tail=True means full match.
          # Move onto the next list [e, f, g]
          if match_head and match_tail:
            break
          # tail=True: trim search_in from start: [b, c, d], [c, d], [d]
          # tail=False: trim search_in from end: [a, b, c], [a, b], [a]
          search_in.pop(0 if match_tail else -1)
        # If head=True or tail=True, move onto the next list [e, f, g]
        if match_head or match_tail:
          break
        # if head=False and tail=False, continue trimming the symbol list
        # The first pass searched in [a, b, c, d], [a, b, c], [a, b], [a]
        # Continue searching in [b, c, d], [b, c], [b], [c, d], [c], [d]
        symbol_list.pop(0)
    return False

  def contains(
      self,
      other: 'Expression.OR_SYMBOL',
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    """Checks if this expression contains a symbol list of the argument.

    Args:
      other: A symbol or expression to search for. If the argument is an
        expression, it's sufficient that at least one symbol list of the
        argument is contained by this expression. It's not necessary for all
        symbol lists of the argument to be contained.
      match_head: If True, at least one symbol list of the argument should be
        contained at the beginning of a symbol list of this expression.
      match_tail: If True, at least one symbol list of the argument should be
        contained at the end of a symbol list of this expression.

    Returns:
      bool

    Example:
      a.symbols() = [[a, b, c, d], [h]]
      b.symbols() = [[a, b], [c], [a, d], [i]]

      a.contains(b): True, a contains [a, b] and [c].
      b.contains(a): False, b doesn't contain [a, b, c, d] or [h].
      a.contains(b, head=True): [a, b, c, d] starts with [a, b]
      a.contains(b, tail=True): False
    """
    if self.is_any() or other.is_any():
      return not self.is_nor() and not other.is_nor()
    for sym_list in self._symbols_of(other):
      if self.contains_symbol_list(sym_list, match_head, match_tail):
        return True
    return False

  def _symbol_contains(self, other: sym.Symbol) -> bool:
    if other.is_any():
      return True
    self_symbols = self.symbols()
    return [sym.Symbol.CTRL.eps] in self_symbols or (
        not other.is_nor() and [other] in self_symbols
    )

  def is_contained(
      self,
      other: 'Expression.OR_SYMBOL',
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    if isinstance(other, Expression):
      return other.contains(self, match_head, match_tail)
    return self._symbol_contains(other)

  # Shorthands for containment conditions

  def matches(self, other: 'Expression.OR_SYMBOL') -> bool:
    return self.contains(other, match_head=True, match_tail=True)

  # head_matches and tail_matches require at least one symbol match unless
  # both expressions are empty Cats or one of the expressions is Expression.ANY
  # For example, if a rule requires a vowel as following context but there is no
  # following context, the rule shouldn't apply.

  def head_matches(self, other: 'Expression.OR_SYMBOL') -> bool:
    if self and not other:
      return other.is_any()
    return self.contains(other, match_head=True)

  def is_prefix(self, other: 'Expression.OR_SYMBOL') -> bool:
    if isinstance(other, Expression):
      return other.head_matches(self)
    return self._symbol_contains(other)

  def tail_matches(self, other: 'Expression.OR_SYMBOL') -> bool:
    if self and not other:
      return other.is_any()
    return self.contains(other, match_tail=True)

  def is_suffix(self, other: 'Expression.OR_SYMBOL') -> bool:
    if isinstance(other, Expression):
      return other.tail_matches(self)
    return self._symbol_contains(other)

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
        symbol.features.copy(),
    )
    self._item_type = Atomic
    self._items = [self]
    self.symbol = symbol.symbol if isinstance(symbol, Atomic) else symbol

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

  def symbols(self) -> list[list[sym.Symbol]]:
    return [[self.symbol]]

  def state_count(self) -> int:
    return 1

  def copy(self) -> 'Atomic':
    return Atomic.get_instance(self)

  def is_control(self) -> bool:
    return self in Atomic.CTRL or self.symbol in sym.Symbol.CTRL


def _control_atomics() -> inventory2.Inventory:
  """Control atomic constants."""
  atm_sym_dict = {ctrl: Atomic(ctrl) for ctrl in sym.Symbol.CTRL}
  atomics = inventory2.Inventory.from_list(
      list(atm_sym_dict.values()), alias='CTRL'
  )
  atomics.make_suppl('atm_sym_dict', atm_sym_dict)
  return atomics


Atomic.CTRL = _control_atomics()


class Cat(Expression):
  """Concatenation of expressions."""

  def __init__(self, *items: Expression, alias: str = ''):
    super().__init__(alias)
    self.add(*items)

  def __str__(self):
    if not self:
      return str(sym.Symbol.CTRL.eps)
    return self._str_enclosed()

  def add(self, *items: Expression) -> 'Cat':
    for item in items:
      if item.is_any():
        self._items.append(item)
      else:
        self._add_item(item)
    return self

  def symbols(self) -> list[list[sym.Symbol]]:
    """Returns the symbol lists for Cat.

    Empty Cat returns the symbol list of CTRL.eps constant, therefore different
    instances of empty Cat are equivalent to both each other and the Atomic
    constant.
    """
    if not self:
      return Atomic.CTRL.eps.symbols()
    self_symbols = [[]]
    for item in self:
      item_symbols = item.symbols()
      for _ in range(len(self_symbols)):
        syms = self_symbols.pop(0)
        self_symbols += [syms.copy() + item_list for item_list in item_symbols]
    return self_symbols

  def copy(self) -> 'Cat':
    return Cat(*self.item_list(), alias=self.alias)


class Or(Expression):
  """Alternation for expressions."""

  def __init__(self, *items: Expression, alias: str = ''):
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

  def _update(self, *items: Expression) -> None:
    self._items = []
    self.add(*items)

  def add(self, *items: Expression) -> 'Or':
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
    symbols = []
    for item in self:
      symbols.extend(item.symbols())
    return symbols


class _BaseAlignment(Expression):
  """Base class for Alignment."""

  def __init__(
      self,
      left: Expression.OR_SYMBOL = Expression.ANY,
      right: Expression.OR_SYMBOL = Expression.ANY,
      alias: str = '',
  ):
    super().__init__(alias)
    self.left = self._set_side(left)
    self.right = self._set_side(right)

  def _set_side(self, side: Expression.OR_SYMBOL) -> Expression:
    if not isinstance(side, Expression):
      return Atomic.get_instance(side)
    return side

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
      self, other: Expression.OR_SYMBOL, checker_name: str, *args
  ) -> bool:
    if not isinstance(other, _BaseAlignment):
      return False
    left = getattr(self.left, checker_name)
    right = getattr(self.right, checker_name)
    return left(other.left, *args) and right(other.right, *args)

  def accepts(
      self, other: Expression.OR_SYMBOL, equivalent: bool = False
  ) -> bool:
    return self._compare(other, 'accepts', equivalent)

  def is_equivalent(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'is_equivalent')

  def contains(
      self,
      other: Expression.OR_SYMBOL,
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    return self._compare(other, 'contains', match_head, match_tail)

  def is_contained(
      self,
      other: Expression.OR_SYMBOL,
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    return self._compare(other, 'is_contained', match_head, match_tail)

  def matches(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'matches')

  def head_matches(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'head_matches')

  def is_prefix(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'is_prefix')

  def tail_matches(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'tail_matches')

  def is_suffix(self, other: Expression.OR_SYMBOL) -> bool:
    return self._compare(other, 'is_suffix')


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
      left: Expression.OR_SYMBOL = Expression.ANY,
      right: Expression.OR_SYMBOL = Expression.ANY,
      preceding_left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_right: Expression.OR_SYMBOL = Expression.ANY,
      following_left: Expression.OR_SYMBOL = Expression.ANY,
      following_right: Expression.OR_SYMBOL = Expression.ANY,
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
      left: Expression.OR_SYMBOL = Expression.ANY,
      right: Expression.OR_SYMBOL = Expression.ANY,
  ) -> 'Alignment':
    """An unassigned alignment with no context."""
    simple = cls(left=left, right=right)
    simple.preceding = Alignment.ANY
    simple.following = Alignment.ANY
    return simple

  @classmethod
  def rule(
      cls,
      alias: str = '',
      left: Expression.OR_SYMBOL = Expression.ANY,
      right: Expression.OR_SYMBOL = Expression.ANY,
      preceding_left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_right: Expression.OR_SYMBOL = Expression.ANY,
      following_left: Expression.OR_SYMBOL = Expression.ANY,
      following_right: Expression.OR_SYMBOL = Expression.ANY,
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
      left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_right: Expression.OR_SYMBOL = Expression.ANY,
      following_left: Expression.OR_SYMBOL = Expression.ANY,
      following_right: Expression.OR_SYMBOL = Expression.ANY,
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
        Atomic.CTRL.eps,
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
      right: Expression.OR_SYMBOL = Expression.ANY,
      preceding_left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_right: Expression.OR_SYMBOL = Expression.ANY,
      following_left: Expression.OR_SYMBOL = Expression.ANY,
      following_right: Expression.OR_SYMBOL = Expression.ANY,
      from_bos: bool = False,
      to_eos: bool = False,
      operation: op.Operation = op.Operation.COMMON.insertion,
      priority: int = 0,
      applied_cost: Union[int, float, ty.Nothing] = ty.UNSPECIFIED,
      source: str = 'Alignment.NATIVE',
  ) -> 'Alignment':
    return cls.rule(
        alias,
        Atomic.CTRL.eps,
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
      left: Expression.OR_SYMBOL = Expression.ANY,
      right: Expression.OR_SYMBOL = Expression.ANY,
      preceding_left: Expression.OR_SYMBOL = Expression.ANY,
      preceding_right: Expression.OR_SYMBOL = Expression.ANY,
      following_left: Expression.OR_SYMBOL = Expression.ANY,
      following_right: Expression.OR_SYMBOL = Expression.ANY,
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
