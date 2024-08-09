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
from nisaba.scripts.natural_translit.utils import inventory
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


class Item(ty.Thing):
  """Parent class for arguments of add and contain methods of Expressions."""

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
  ):
    super().__init__(alias, text)
    self.index = ty.type_check(index, hash(self))

  # Default methods for type compatibility.

  def __str__(self):
    return self.text

  def copy(self) -> 'Item':
    return Item(self.alias + '_copy')

  def is_control(self) -> bool:
    return False

  def is_any(self) -> bool:
    return False

  def is_expression_any(self) -> bool:
    return not isinstance(self, Symbol) and self.is_any()

  def is_eps(self) -> bool:
    return False

  def is_nor(self) -> bool:
    return False

  def state_count(self) -> int:
    return 1 if isinstance(self, Symbol) else 0

  def symbols(self) -> list[list['Symbol']]:
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

  def accepts(self, other: 'Item', equivalent: bool = False) -> bool:
    """Checks if this Item accepts all symbol lists of the argument.

    Args:
      other: Item to be checked.
      equivalent: If True, the argument must accept this item too.

    Returns:
      bool
    """
    if self.is_expression_any() or other.is_expression_any():
      return (
          equivalent and self.is_expression_any() and other.is_expression_any()
      ) or not equivalent
    self_symbols, other_symbols = self.symbols(), other.symbols()
    self_len, other_len = len(self_symbols), len(other_symbols)
    if (
        not self_len
        or self_len < other_len
        or (equivalent and self_len != other_len)
    ):
      return False
    return all(sym_list in self_symbols for sym_list in other_symbols)

  def is_equivalent(self, other: 'Item') -> bool:
    return self.accepts(other, equivalent=True)

  def contains_symbol_list(
      self,
      search_for: list['Symbol'],
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    """Checks if this this contains the given symbol list.

    The symbols in the argument must be adjacent and in the same order in at
    least one symbol list of the item.

    Args:
      search_for: Symbol list to be searched for.
      match_head: If True, the argument must match the beginning of at least one
        symbol list of this item.
      match_tail: If True, the argument must match the end of at least one
        symbol list of this item.

    If both head and tail are true, the argument must be equal to at least one
    symbol list of this item.

    All items contain eps list [ℰ] in all conditions. No item contains nor list
      [◎], even if the nor symbols are the same instance.

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
    if search_for == [Symbol.CTRL.eps]:
      return True
    if search_for == [Symbol.CTRL.nor]:
      return False
    if self.is_expression_any():
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
      other: 'Item',
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    """Checks if this item contains a symbol list of the argument.

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
    if self.is_expression_any() or other.is_expression_any():
      return not self.is_nor() and not other.is_nor()
    return any(
        self.contains_symbol_list(sym_list, match_head, match_tail)
        for sym_list in other.symbols()
    )

  # Shorthands for containment conditions

  def is_contained(
      self,
      other: 'Item',
      match_head: bool = False,
      match_tail: bool = False,
  ) -> bool:
    return other.contains(self, match_head, match_tail)

  def matches(self, other: 'Item') -> bool:
    return self.contains(other, match_head=True, match_tail=True)

  # head_matches and tail_matches require at least one symbol match unless
  # both expressions are only contain [ℰ] or one of the arguments is
  # Expression.ANY.
  # For example, if a rule requires a vowel as following context but there is no
  # following context, the rule shouldn't apply.

  def head_matches(self, other: 'Item') -> bool:
    if self and not other:
      return other.is_expression_any()
    return self.contains(other, match_head=True)

  def is_prefix(self, other: 'Item') -> bool:
    return other.head_matches(self)

  def tail_matches(self, other: 'Item') -> bool:
    if self and not other:
      return other.is_expression_any()
    return self.contains(other, match_tail=True)

  def is_suffix(self, other: 'Item') -> bool:
    return other.tail_matches(self)


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
              f('imp', 'implicit'),
              f('raw'),
          )
      ),
  )
  return ftr


class Symbol(Item):
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
    super().__init__(alias, text, index)
    self.raw = raw
    self.name = name if name else self.alias
    self.features = ft.Feature.Set(features, alias='features')
    if self.raw:
      self.features.add(self.SYM_FEATURES.type.raw)
    else:
      self.features.add(self.SYM_FEATURES.type.abst)
    self.inventory = Symbol.Inventory.EMPTY
    self.symbol = self

  def symbols(self) -> list[list['Symbol']]:
    return [[self.symbol]]

  def is_control(self) -> bool:
    return self in Symbol.CTRL

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

  def has_feature(self, value: ft.Feature.Aspect.VALUES) -> bool:
    return value.is_in(self.features)

  # Placeholder function to avoid rewrites when the features attribute is
  # changed from feature set to multiple feature profiles.
  def add_features(self, *features: ft.Feature.ITERABLE) -> None:
    self.features.add(features)

  def set_attribute(
      self,
      attribute: str,
      value: ...,
      features_to_add: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ) -> None:
    """Sets the attribute of the symbol as value. Optionally adds features.

    Args:
      attribute: The name of the attribute to be set.
      value: The value to be assigned to the attribute.
      features_to_add: If specified, features will be added to the symbol.

    If the symbol is a control symbol, the attributes and features are not
      changed.

    Example:
    Given `roman_five = Symbol('roman_five', 'V')`, the call:
    ```
    roman_five.set_attribute('numeric', 5, gr_class.digit)
    ```
    results in:
    ```
    roman_five.numeric = 5
    roman_five.features = {gr_class.digit}
    ```
    """
    if not self.is_control():
      setattr(self, attribute, value)
      self.add_features(features_to_add)

  def feature_pair(
      self,
      symbol: 'Symbol',
      from_feature: ft.Feature,
      to_feature: ft.Feature,
      add_aspect: bool = True,
      add_features: bool = True,
  ) -> None:
    """Defines a relation from this symbol to another based on a feature pair.

    For both symbols, sets attributes for each feature as the other symbol.
    Optionally sets the aspect of the feature as an attribute and/or adds the
    given features to the symbol's compositional features. The attributes and
    features of control symbols are never changed. If a non-control symbol is
    paired with a control symbol, the pair of the non-control symbol will be
    set as Symbol.CTRL.nos (NO SYMBOL).

    Feature pairs are Symbols that are behavioral counterparts of each other in
    terms of a pair of features, regardless of the compositional features of the
    Symbols.

    Example:

    /tʃ/: `tsh.features = {voiceless, post_alveolar, affricate}`
    /dʒ/: `dzh.features = {voiced, post_alveolar, affricate}`
    is a prototypical voicing pair. However in Tamil `tsh` changes to `s`
    instead of `dzh` in voicing context, even though the features of `s` are
    `{voiceless, alveolar, fricative}`.
    Setting `ta.t.voiced = ta.s` allows the voicing rule to be generalized as
    `([vowel], phoneme >> phoneme.voiced, [vowel])` instead of having to list
    the phoneme pairs for each language, while setting
    `ta.s.voicing = voiced, ta.s.voiceless = ta.tsh` results in the correct
    deromanization of 'selloor' to 'செல்லூர்' (cellūr). At the same time,
    preserving the compositional features of `ta.s` allows for a more accurate
    description of its actual articulation so that it doesn't affect other
    applications, for example when assessing the similarity of `ta.s` to other
    voiceless or fricative consonants.

    Args:
      symbol: The symbol to be paired.
      from_feature: The feature that is associated with this symbol.
      to_feature: The feature that is associated with the other symbol.
      add_aspect: If true, the feature of each symbol will be set as its
        attribute named after the aspect of the feature.
      add_features: If True, the feature associated with each symbol will be
        added to its features.
    """
    self.set_attribute(from_feature.text, self)
    symbol.set_attribute(to_feature.text, symbol)
    self.set_attribute(
        to_feature.text,
        symbol if not symbol.is_control() else Symbol.CTRL.nos,
        from_feature if add_features else ty.UNSPECIFIED,
    )
    symbol.set_attribute(
        from_feature.text,
        self if not self.is_control() else Symbol.CTRL.nos,
        to_feature if add_features else ty.UNSPECIFIED,
    )
    if add_aspect:
      self.set_attribute(from_feature.aspect.text, from_feature)
      symbol.set_attribute(to_feature.aspect.text, to_feature)

  class Inventory(inventory.Inventory):
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
      super().__init__(alias, ty.type_check(typed, Symbol))
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
      syms = list(filter(self._add_symbol, [sym for sym in symbols]))
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
        source_dict = getattr(self, source_dict, {})
      return log.dbg_return(
          source_dict.get(key, ty.type_check(default, Symbol.CTRL.unk))
      )

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
        sym_inventory: 'Symbol.Inventory.OR_NOTHING' = ty.UNSPECIFIED,
    ) -> Iterable['Symbol']:
      """Makes an iterable of raw symbols from a string.

      Args:
        raw_text: The string to be converted to an iterable of symbols.
        sym_inventory: The inventory which the symbols will be based on. If
          the inventory is not provided, the symbols are based on the current
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
      sym_inventory = ty.type_check(sym_inventory, self)
      return [
          sym_inventory.raw_lookup(char)
          if char in sym_inventory.raw_dict
          else sym_inventory.raw_from_unknown(char)
          for char in raw_text
      ]

    def parse(
        self,
        raw_text: str,
        sym_inventory: 'Symbol.Inventory.OR_NOTHING' = ty.UNSPECIFIED,
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
        sym_inventory: The inventory which the symbols will be based on.

      Returns:
        An iterable of processed symbols.
      """
      return self.str_to_raw_symbols(raw_text, sym_inventory)


def _control_symbols() -> inventory.Inventory:
  """Control symbol constants."""
  # Next index = 5
  control_args = [
      ['eps', '​ℰ​', 'EPSILON', 0],  # U+200B + U+2130 + U+200B
      ['unk', '​␦​', 'UNKNOWN SYMBOL', 1],  # U+200B + U+2426 + U+200B
      ['bos', '​⊳​', 'BEGINNING OF SEQUENCE', 2],  # U+200B + U+22B3 + U+200B
      ['eos', '​⊲​', 'END OF SEQUENCE', 3],  # U+200B + U+22B2 + U+200B
      ['oos', '​⊽​', 'OUT OF SEQUENCE', 4],  # U+200B + U+22BD + U+200B
      ['nor', '​◎​', 'NO ALTERNATIVE', 5],  # U+200B + U+25CE + U+200B
      ['nos', '​⨱​', 'NO SYMBOL', 6],  # U+200B + U+2A31 + U+200B
  ]
  return inventory.Inventory.from_list(
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
