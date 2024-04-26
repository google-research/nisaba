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

  def copy(self) -> 'Expression':
    return Expression(self.alias)

  def __add__(self, other: 'Expression') -> 'Cat':
    return Cat(self, other)

  def __or__(self, other: 'Expression') -> 'Or':
    return Or(self, other)

  def repeat(self, n: int = 2) -> 'Cat':
    """Returns a Cat of n repetitions of this expression."""
    return Cat(*([self] * n))


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
  def read(cls, symbol: sym.Symbol) -> 'Atomic':
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
    return Atomic.read(self)

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
    exp.Or(
        exp.Cat(_ATM.a, _ATM.b, _ATM.c), exp.Cat(_ATM.a, _ATM.b, _ATM.d)
    ),
    ```
    should return ((a b (c | d)) | ⍜) instead of ((a b c) | (a b d))

    Args:
      *items: Items to be added.

    Returns:
      self
    """
    for item in items:
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
