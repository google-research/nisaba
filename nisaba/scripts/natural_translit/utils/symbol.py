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
from typing import Any, Iterable, Union
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
              f('abst', 'abstract'),
              f('ctrl', 'control'),
              f('raw'),
          )
      ),
  )
  return ftr


class Symbol(ty.Thing):
  """A symbol in an alphabet.

  Attributes:
    alias: The default string that will be used to access this symbol from an
      inventory. This string needs to be unique in the inventory and conform to
      the attribute name restrictions. For example, a Grapheme with
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
      representation, like schwa which doesn't have a corresponding Devanagari
      grapheme, this field will be an empty string, i.e., `raw=''`.
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
    UNDEFINED_PREFIX = 9_000_000

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

  def is_any(self) -> bool:
    return False

  def is_eps(self) -> bool:
    return self is Symbol.CTRL.eps

  def is_nor(self) -> bool:
    return self is Symbol.CTRL.nor

  def description(self, show_features: bool = False) -> str:
    """A string that describes the symbol."""
    text = 'alias: %s  index: %s' % (self.alias, self.index)
    if self.raw:
      text += '  raw: %s' % self.raw
    if self.text:
      text += '  text: %s' % self.text
    if self.name != self.alias:
      text += '  name: %s' % self.name
    if show_features:
      text += '\n    %s' % str(self.features)
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

    OR_NOTHING = Union['Symbol.Inventory', ty.Nothing]

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
      self.prefix = Symbol.ReservedIndex.UNDEFINED_PREFIX
      self.unknown_count = 0
      self.add_suppl(Symbol.CTRL)
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
        if not show_control and sym in self.CTRL:
          continue
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
      if sym.text:
        self.text_dict[sym.text] = sym
      if sym.raw:
        self.raw_dict[sym.raw] = sym

    def _add_symbol(self, sym: 'Symbol') -> bool:
      """Adds a symbol to the inventory."""
      if not self.add_item(sym):
        return False
      if sym.inventory == Symbol.Inventory.EMPTY and sym not in self.CTRL:
        sym.inventory = self
      self._add_to_dicts(sym)
      return True

    def add_symbols(self, *symbols, list_alias: str = '') -> list['Symbol']:
      """Adds multiple symbols to the inventory.

      Args:
        *symbols: The symbols to be added.
        list_alias: If an alias is provided, makes a suppl with the alias that
          points to the list of successfully added symbols.

      Returns:
        The list of symbols that are successfully added to the inventory.
      """
      syms = []
      for sym in symbols:
        if self._add_symbol(sym):
          syms.append(sym)
      if list_alias:
        self.make_suppl(list_alias, syms)
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
      if ty.not_instance(default, Symbol):
        default = self.CTRL.unk
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

    def raw_from_unknown(self, raw: str = '') -> 'Symbol':
      """Makes and adds a new raw symbol to the inventory from a string."""
      self.unknown_count += 1
      alias = 'from_unk_' + str(self.unknown_count)
      name = alias + '_' + raw
      text = '<' + name + '>'
      index = self.prefix + self.unknown_count
      new = Symbol(alias, text, raw, index, name)
      self._add_symbol(new)
      return new

    def str_to_raw_symbols(
        self,
        raw_text: str,
        inventory: 'Symbol.Inventory.OR_NOTHING' = ty.UNSPECIFIED,
    ) -> Iterable['Symbol']:
      """Makes an iterable of raw symbols from a string.

      Args:
        raw_text: The string to be converted to an iterable of symbols.
        inventory: The inventory which the symbols will be based on. If the
          inventory is not provided, the symbols are based on the current
          inventory.

        For example, a Deva-Latn aligner will use a symbol inventory that
        contains both the Deva and Latn symbols. If the input string is mixed
        script, Deva.str_to_raw_symbols() will recognize the Latn characters as
        existing symbols instead of dynamically creating new symbols from
        unknown. If the input string contains a character that doesn't belong
        to either script, for example an emoji, the new symbol will be added to
        the combined inventory so that when the Latn.str_to_raw_symbols() is
        called, it will recognize the emoji as the same symbol.

      Returns:
        An iterable of raw symbols.
      """
      if not isinstance(inventory, Symbol.Inventory):
        inventory = self
      symbols = []
      for char in raw_text:
        symbol = inventory.raw_lookup(char)
        if symbol == inventory.CTRL.unk:
          symbol = inventory.raw_from_unknown(char)
        symbols.append(symbol)
      return symbols

    def parse(
        self,
        raw_text: str,
        inventory: 'Symbol.Inventory.OR_NOTHING' = ty.UNSPECIFIED,
    ) -> Iterable['Symbol']:
      """Takes a string and returns an iterable of processed symbols.

      The default parser is the same as str_to_raw_symbols. Subclasses
      can override this method to provide different parsing behavior. For
      example, the Brahmic parser can insert an abstract symbol for schwa after
      consonants that aren't followed by a vowel sign, or it can compose the
      raw symbols for 'ja' and 'nukta' into a single abstract symbol 'ja_nukta',
      which can then use the same alignables as 'za'.

      Args:
        raw_text: The string to be parsed.
        inventory: The inventory which the symbols will be based on.

      Returns:
        An iterable of processed symbols.
      """
      return self.str_to_raw_symbols(raw_text, inventory)


def _control_symbols() -> inventory2.Inventory:
  """Control symbol constants."""
  # Next index = 5
  control_args = [
      ['eps', '​ℰ​', 'EPSILON', 0],  # U+200B + U+2130 + U+200B
      ['unk', '​␦​', 'UNKNOWN SYMBOL', 1],  # U+200B + U+2426 + U+200B
      ['bos', '​⊳​', 'BEGINNING OF SEQUENCE', 2],  # U+200B + U+22B3 + U+200B
      ['eos', '​⊲​', 'END OF SEQUENCE', 3],  # U+200B + U+22B2 + U+200B
      ['oos', '​⊽​', 'OUT OF SEQUENCE', 4],  # U+200B + U+22BD + U+200B
      ['nor', '​◎​', 'NO ALTERNATIVE', 5],  # U+200B + U+25CE + U+200B
  ]
  return inventory2.Inventory.from_list(
      [
          Symbol(
              alias=alias,
              text=text,
              name=name,
              index=index + Symbol.ReservedIndex.CONTROL_PREFIX,
              features=Symbol.SYM_FEATURES.type.ctrl,
          )
          for alias, text, name, index in control_args
      ],
      alias='CTRL',
  )


Symbol.CTRL = _control_symbols()
