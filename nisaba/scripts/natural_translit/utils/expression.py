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
import enum
from typing import Any, Union
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


def _symbol_features() -> ft.Feature.Inventory:
  """Symbol feature inventory."""
  f = ft.Feature
  ftr = f.Inventory(
      'sym_features',
      f.Aspect(
          f.equidistant(
              'type',
              f('abst', 'abstract'), f('ctrl', 'control'), f('raw'),
          )
      ),
  )
  return ftr


class Symbol(ty.Thing):
  """A symbol in an alphabet.

  Attributes:
    alias: The default string that will be used to access this symbol from an
      inventory. This string needs to be unique in the inventory and conform
      to the attribute name restrictions. For example, a Grapheme with
      `alias='schwa'` in the 'deva' inventory can be accessed by `deva.schwa`.
    text: The string representation of the symbol that will be used for
      inspection and debugging. When it's not same as the raw attribute, it
      can be a predefined string or it can be dynamically assigned. Eg:
      - A non-Devanagari symbol `text='🜔'` can be assigned to schwa while
      building the inventory.
      - When aligning 'w' with 'डब्ल्यू' (ISO: ḍablyū), symbols representing the
      parts of 'w' can be created during runtime and assigned `text='w_part_1'`,
      `text='w_part_2'`, ... etc.
    raw: The conventional string representation of a symbol, eg. the Unicode
      glyph of a grapheme. If the symbol doesn't have a conventional string
      representation, like schwa which doesn't have a corresponding
      Devanagari grapheme, this field will be an empty string, i.e., `raw=''`.
    index: An int that will be used as the index of this symbol in fsts.
    name: A conventional or descriptive name for the symbol, eg. the Unicode
      name of the raw grapheme 'अ' `name='DEVANAGARI LETTER A'`, a descriptive
      name for the abstract grapheme schwa `name='BRAHMIC SCHWA'`, or the
      conventional description of the phoneme /a/
      `name=OPEN FRONT UNROUNDED VOWEL`.
    features: Features to be added to the symbol.
      Eg. `features=SYM_FEATURES.sym_type.raw` for 'अ'
    inventory: The inventory that the symbol is first defined in. The default
      value of the inventory is Symbol.Inventory.EMPTY.
  """

  SYM_FEATURES = _symbol_features()

  class ReservedIndex(enum.IntEnum):
    UNDEFINED_SUFFIX = 999_999
    CONTROL_PREFIX = 1_000_000
    GRAPHEME_PREFIX = 2_000_000
    PHONEME_PREFIX = 3_000_000

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      raw: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
      name: str = '',
      features: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ):
    super().__init__(alias=alias)
    self.text = text if text else self.alias
    self.raw = raw
    self.index = index if ty.is_specified(index) else hash(self)
    self.name = name if name else self.alias
    self.features = ft.Feature.Set(features, alias='features')
    if self.raw:
      self.features.add(self.SYM_FEATURES.type.raw)
    else:
      self.features.add(self.SYM_FEATURES.type.abst)
    self.inventory = Symbol.Inventory.EMPTY

  def __str__(self) -> str:
    return self.text

  def is_control(self) -> bool:
    return self in Symbol.CTRL

  def description(self, show_features: bool = False) -> str:
    """A string that describes the symbol."""
    text = 'alias: %s  index: %s' % (self.alias, self.index)
    if self.raw: text += '  raw: %s' % self.raw
    if self.text: text += '  text: %s' % self.text
    if self.name != self.alias: text += '  name: %s' % self.name
    if show_features: text += '\n    %s' % str(self.features)
    return text

  @classmethod
  def descriptions(
      cls,
      *syms: 'Symbol',
      title: str = '',
      show_features: bool = False,
  ) -> str:
    return (
        '%s:\n  ' % (title if title else 'symbols')
        + '\n  '.join([sym.description(show_features) for sym in syms])
        + '\n'
    )

  class Inventory(inventory2.Inventory):
    """Symbol inventory.

    index_dict: A dictionary of <symbol>.index: <symbol>
    raw_dict: A dictionary of <symbol>.raw: <symbol> for symbols with non-empty
      raw attribute.
    text_dict: A dictionary of <symbol>.text: <symbol> for symbols with
      non-empty text attribute.

    All Symbol inventories have the control symbols in their 'CTRL' supplement.
    Eg. for an inventory such as deva, deva.CTRL.unk is the same object as
    Symbol.CTRL.unk

    """

    def __init__(
        self,
        alias: str,
        *symbols,
        typed: ty.TypeOrNothing = ty.UNSPECIFIED,
    ):
      super().__init__(alias, typed if ty.not_nothing(typed) else Symbol)
      self.index_dict = {}
      self.raw_dict = {}
      self.text_dict = {}
      self.add_supl(Symbol.CTRL)
      for c in self.CTRL:
        self._add_to_dicts(c)
      self.add_symbols(*symbols)

    def __str__(self) -> str:
      return self.description()

    def description(
        self, show_features: bool = False, show_control: bool = False
    ) -> str:
      text = self.alias + ' inventory:\n\n'
      for i in sorted(self.index_dict):
        sym = self.index_lookup(i)
        if not show_control and sym in self.CTRL: continue
        text += '  %s\n\n' % sym.description(show_features)
      return text

    def _add_to_dicts(self, sym: 'Symbol') -> None:
      """Add a symbol to the inventory dicts.

      Args:
        sym: The symbol to be added.

      If multiple symbols have the same non-empty value for a field, the last
      entry overwrites the previous ones.
      TODO: Improve handling of clashing symbol attributes.

      """
      self.index_dict[sym.index] = sym
      if sym.text: self.text_dict[sym.text] = sym
      if sym.raw: self.raw_dict[sym.raw] = sym

    def _add_symbol(self, sym: 'Symbol') -> bool:
      """Adds a symbol to the inventory."""
      if not self.add_item(sym): return False
      if (
          sym.inventory == Symbol.Inventory.EMPTY
          and sym not in self.CTRL
      ):
        sym.inventory = self
      self._add_to_dicts(sym)
      return True

    def add_symbols(self, *symbols, list_alias: str = '') -> list['Symbol']:
      """Adds multiple symbols to the inventory.

      Args:
        *symbols: The symbols to be added.
        list_alias: If an alias is provided, makes a supl with the alias that
          points to the list of successfully added symbols.

      Returns:
        The list of symbols that are successfully added to the inventory.
      """
      syms = []
      for sym in symbols:
        if self._add_symbol(sym): syms.append(sym)
      if list_alias: self.make_supl(list_alias, syms)
      return syms

    def lookup(
        self,
        key: ...,
        source_dict: Union[dict[Any, 'Symbol'], str],
        default: Union['Symbol', ty.Nothing] = ty.UNSPECIFIED,
    ) -> 'Symbol':
      """Get symbol by key from source_dict.

      Args:
        key: A key that will be used to retrieve a symbol from source_dict.
        source_dict: A dictionary or the alias of a dictionary in this
          inventory.
        default: Default return value for when the Symbol is not found. If
          default is unspecified, the default return is Symbol.CTRL.unk

      Returns:
        Symbol
      """
      if isinstance(source_dict, str):
        source_dict = ty.get_attribute(self, source_dict, {}, dict)
      if ty.not_instance(default, Symbol): default = self.CTRL.unk
      return log.dbg_return(ty.dict_get(source_dict, key, default))

    def index_lookup(self, index: int) -> 'Symbol':
      """Get symbol by its index field."""
      return log.dbg_return(self.lookup(index, self.index_dict))

    def raw_lookup(self, raw_text: str) -> 'Symbol':
      """Get symbol by its raw field."""
      return log.dbg_return(self.lookup(raw_text, self.raw_dict))

    def text_lookup(self, text: str) -> 'Symbol':
      """Get symbol by its text field."""
      return log.dbg_return(self.lookup(text, self.text_dict))


def _control_symbols() -> inventory2.Inventory:
  """Control symbol constants."""
  # Next index = 5
  control_args = [
      ['eps', '⍷', 'EPSILON', 0],  # U+2377
      ['unk', '⍰', 'UNKNOWN SYMBOL', 1],  # U+2370
      ['bos', '⍄', 'BEGINNING OF SEQUENCE', 2],  # U+2344
      ['eos', '⍃', 'END OF SEQUENCE', 3],  # U+2343
      ['oos', '⍔', 'OUT OF SEQUENCE', 4],  # U+2354
      ['nor', '⍜', 'NO ALTERNATIVE', 5]  # U+235C
  ]
  return inventory2.Inventory.from_list([
      Symbol(
          alias=alias,
          text=text,
          name=name,
          index=index + Symbol.ReservedIndex.CONTROL_PREFIX,
          features=Symbol.SYM_FEATURES.type.ctrl,
      )
      for alias, text, name, index in control_args
  ], alias='CTRL')

Symbol.CTRL = _control_symbols()


class Expression(ty.IterableThing):
  """Parent class for Expressions."""

  OR_SYMBOL = Union['Expression', Symbol]

  def __init__(self, alias: str = ''):
    super().__init__(alias=alias)
    self._item_type = Expression
    self.index = hash(self)

  def __str__(self) -> str:
    return self.text

  def _str_items_list(self, *items: ...) -> list[str]:
    if not items: items = self
    return [str(item) for item in items]

  def _str_enclosed(
      self,
      str_list: ty.ListOrNothing = ty.UNSPECIFIED,
      separator: str = ' ',
      left: str = '(',
      right: str = ')',
  ) -> str:
    if ty.is_nothing(str_list): str_list = self._str_items_list()
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
    elif isinstance(item, Symbol):
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

  def symbols(self) -> list[list[Symbol]]:
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

  def accepts(self, other: 'Expression.OR_SYMBOL') -> bool:
    """Checks if this expression accepts all symbol lists of the argument.

    Args:
      other: A symbol or expression.

    Returns:
      bool

    """
    self_symbols = self.symbols()
    if isinstance(other, Expression):
      other_symbols = other.symbols()
    else:
      other_symbols = [[other]]
    for sym_list in other_symbols:
      if sym_list not in self_symbols: return False
    return True

  def is_equivalent(self, other: 'Expression.OR_SYMBOL') -> bool:
    if isinstance(other, Expression):
      return self.accepts(other) and other.accepts(self)
    else:
      return self.accepts(other) and len(self.symbols()) == 1

  def copy(self) -> 'Expression':
    return Expression(self.alias)

  def repeat(self, n: int = 2) -> 'Cat':
    """Returns a Cat of n repetitions of this expression."""
    return Cat(*([self] * n))


class Atomic(Expression, Symbol):
  """An instance of a single symbol."""

  def __init__(self, symbol: Symbol, alias: str = ''):
    Expression.__init__(self, symbol.alias)
    Symbol.__init__(
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
  def read(cls, symbol: 'Symbol') -> 'Atomic':
    """Reads a Symbol into an Atomic while matching corresponding constants.

    Args:
      symbol: symbol to be read.

    Returns:
      If the argument is a control Symbol or Atomic, returns the corresponding
        Atomic constant.
      Otherwise returns a new Atomic instance of the symbol.

    """
    if symbol in Symbol.CTRL: return Atomic.CTRL.atm_sym_dict[symbol]
    if symbol in Atomic.CTRL and isinstance(symbol, Atomic): return symbol
    return Atomic(symbol)

  def symbols(self) -> list[list[Symbol]]:
    return [[self.symbol]]

  def state_count(self) -> int:
    return 1

  def copy(self) -> 'Atomic':
    return Atomic.read(self)

  def is_control(self) -> bool:
    return self in Atomic.CTRL or self.symbol in Symbol.CTRL


def _control_atomics() -> inventory2.Inventory:
  """Control atomic constants."""
  atm_sym_dict = {ctrl: Atomic(ctrl) for ctrl in Symbol.CTRL}
  atomics = inventory2.Inventory.from_list(
      list(atm_sym_dict.values()), alias='CTRL'
  )
  atomics.make_supl('atm_sym_dict', atm_sym_dict)
  return atomics

Atomic.CTRL = _control_atomics()


class Cat(Expression):
  """Concatenation of expressions."""

  def __init__(self, *items: Expression, alias: str = ''):
    super().__init__(alias)
    self.add(*items)

  def __str__(self):
    if not self: return str(Symbol.CTRL.eps)
    return self._str_enclosed()

  def add(self, *items: Expression) -> 'Cat':
    for item in items:
      self._add_item(item)
    return self

  def symbols(self) -> list[list[Symbol]]:
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
    if not self: return str(Symbol.CTRL.nor)
    separator = ' | '
    if len(self) == 1:
      return self._str_enclosed(
          self._str_items_list(self.item(0), Symbol.CTRL.nor), separator
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

  def symbols(self) -> list[list[Symbol]]:
    """Returns the symbol lists for Or.

    In order to avoid accidental context matches, empty Or returns a new
    instance of CTRL.nor instead of the constant.

    For example, given a rule that requires the preceding context to be a close
    vowel and an inventory with `close_vowel = Or(*close_vowel_list)` where
    `close_vowel_list` is empty, the rule should never apply even if the
    preceding context is the same empty Or.
    """
    if not self: return [[Atomic(Symbol.CTRL.nor)]]
    symbols = []
    for item in self:
      symbols.extend(item.symbols())
    return symbols