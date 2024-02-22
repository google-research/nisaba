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
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


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

  """

  def __init__(
      self, alias: str = '', text: str = '', raw: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
  ):
    # TODO: Move alias to Thing's init() and remove set_alias() from child
    # classes.
    super().__init__()
    self.set_alias(alias)
    self.text = text if text else self.alias
    self.raw = raw
    self.index = index if ty.is_specified(index) else hash(self)

  def __str__(self) -> str:
    return self.text


class Expression(ty.IterableThing):
  """Parent class for Expressions."""

  def __init__(self, alias: str = ''):
    super().__init__(alias=alias)
    self._item_type = Expression
    self.index = hash(self)

  def __str__(self) -> str:
    return self.text


class Atomic(Expression, Symbol):
  """An instance of a single symbol."""

  def __init__(self, symbol: Symbol, alias: str = ''):
    Expression.__init__(self, symbol.alias)
    Symbol.__init__(self, symbol.alias, symbol.text, symbol.raw, symbol.index)
    self._item_type = Atomic
    self._items = [self]
    self.symbol = symbol.symbol if isinstance(symbol, Atomic) else symbol

  def add(self, *items: ...) -> 'Atomic':
    log.dbg_message('Cannot add items to Atomic.')
    return self
