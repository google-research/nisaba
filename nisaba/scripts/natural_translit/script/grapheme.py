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

"""Grapheme class and related functions."""

import unicodedata
import pycountry
from nisaba.scripts.natural_translit.phonology import phonological_symbol as ps
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import type_op as ty


class Script(ft.Feature):
  """Script feature for Graphemes.

  See https://en.wikipedia.org/wiki/Script_(Unicode) for ISO 15924 scripts.

  Attributes:
    alias: ISO 15924 code in lowercase if applicable, otherwise a custom string
      that doesn't overlap with ISO 15924. Eg. alias='deva' for ISO 15924 script
      Deva, alias='br' for the inventory of common abstractions of the Brahmic
      family.
    text: ISO 15924 name of the script if applicable, otherwise a descriptive
      string. ISO name can be simplified. Eg. text='Devanagari' for Devanagari
      (Nagari) and text='Brahmic Parent' for the Brahmic abstractions.
    numeric: ISO 15924 number if applicable, otherwise a custom three digit
      number that starts with 8 since it won't overlap with ISO 15924. Eg.
      numeric=315 for Deva, numeric=801 for Brahmic abstractions.
  """

  def __init__(self, alias: str, text: str, numeric: int):
    super().__init__(alias, text)
    self.numeric = numeric

  def __str__(self) -> str:
    return 'alias: %s text: %s numeric: %s' % (
        self.alias,
        self.text,
        self.numeric,
    )

  @classmethod
  def from_iso(cls, iso_code: str) -> 'Script':
    script = pycountry.scripts.get(alpha_4=iso_code)
    return cls(script.alpha_4.lower(), script.name, script.numeric)


def _grapheme_features() -> ft.Feature.Inventory:
  """Grapheme feature inventory."""
  f = ft.Feature
  ftr = f.Inventory(
      'gr_features',
      f.Aspect(
          f.equidistant(
              'script',
              # ISO 15924 scripts
              Script.from_iso('latn'),
              Script.from_iso('deva'),
              # Custom scripts
              Script('und', 'Undefined script', 800),
              Script('br', 'Brahmic Parent', 801),
          )
      ),
      f.Aspect(f.equidistant('case', f('upper'), f('lower'))),
  )
  return ftr


class Grapheme(ps.PhonologicalSymbol):
  """Grapheme symbol."""

  GR_FEATURES = _grapheme_features()
  SCRIPT_PREFIX_MULTIPLIER = 1_000

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      raw: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
      name: str = '',
      features: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ):
    super().__init__(alias, raw, index, name)
    self.text = text if raw else self.alias
    self.features.new_profile(ft.Feature.Profile(self.GR_FEATURES, 'new'))
    self.add_features(features)

  @classmethod
  def from_char(
      cls,
      character: str,
      alias: str = '',
      features: ft.Feature.ITERABLE = ft.Feature.Set(),
  ) -> 'Grapheme':
    """Creates a Grapheme object from a single character.

    Args:
      character: A unicode character.
      alias: A unique string to refer to the grapheme. If no alias is given, it
        is 'u_' followed by the hex value of the character.
      features: Features of the character.

    Index of the grapheme is set to grapheme prefix + the codepoint of the
    character. Name is set as the Unicode name if applicable, otherwise it's
    GRAPHEME followed by the hex value.

    Returns:
      Grapheme.
    """
    code_point = ord(character)
    index = cls.ReservedIndex.GRAPHEME_PREFIX + code_point
    code_hex = hex(code_point)
    if not alias:
      alias = 'u_' + code_hex
    try:
      name = unicodedata.name(character)
    except ValueError:
      name = 'GRAPHEME'
    name += ' U+' + code_hex.upper()[2:]
    return cls(
        alias=alias,
        text=character,
        raw=character,
        index=index,
        name=name,
        features=ft.Feature.Set(cls.SYM_FEATURES.type.raw, features),
    )

  def description(self, show_features: bool = False) -> str:
    """A string that describes the Grapheme."""
    text = 'alias: ' + self.alias
    if self.raw:
      text += '  raw: ' + self.raw
    else:
      text += '  text: ' + self.text
    text += '  name: ' + self.name
    if show_features:
      text += '\n  %s' % str(self.features)
    return text

  def copy(
      self,
      alias: str = '',
      inventory: 'Grapheme.Inventory.OR_NOTHING' = ty.UNSPECIFIED,
  ) -> 'Grapheme':
    """Creates a copy of the Grapheme."""
    return Grapheme(
        alias if alias else self.alias,
        self.text,
        self.raw,
        self.index,
        self.name,
        features=self.features.copy(),
    )

  class Inventory(ps.PhonologicalSymbol.Inventory):
    """Grapheme inventory."""

    def __init__(self, script: Script, language: str = ''):
      if language:
        language += '_'
      super().__init__(alias=language + script.alias, typed=Grapheme)
      self.script = script
      self.prefix = self._prefix()
      self.atomics = i.Inventory()

    def _prefix(self) -> int:
      return (
          Grapheme.ReservedIndex.GRAPHEME_PREFIX
          + int(self.script.numeric) * Grapheme.SCRIPT_PREFIX_MULTIPLIER
      )  # Eg. 2_215_000 for Latn, 2_800_000 for und

    def add_graphemes(
        self, *graphemes: 'Grapheme', list_alias: str = ''
    ) -> list['Grapheme']:
      grs = [gr for gr in graphemes if self._add_symbol_and_atomic(gr)]
      if list_alias:
        self.make_iterable_suppl(list_alias, *grs)
      return grs

    def import_graphemes(
        self, *graphemes: 'Grapheme', list_alias: str = ''
    ) -> list['Grapheme']:
      """Imports graphemes from another inventory."""
      return self.add_graphemes(
          *(gr.copy(inventory=self) for gr in graphemes), list_alias=list_alias
      )

    def import_as_feature_pairs(
        self,
        from_feature: ft.Feature,
        to_feature: ft.Feature,
        *pairs: tuple['Grapheme', 'Grapheme'],
        make_suppls_from_features: bool = True,
    ) -> None:
      """Imports graphemes from another inventory as feature pairs."""
      from_list = []
      to_list = []
      for from_parent, to_parent in pairs:
        from_symbol, to_symbol = tuple(
            self.import_graphemes(from_parent, to_parent)
        )
        from_symbol.feature_pair(to_symbol, from_feature, to_feature)
        from_list.append(from_symbol)
        to_list.append(to_symbol)
      if make_suppls_from_features:
        self.make_iterable_suppl(from_feature.alias, *from_list)
        self.make_iterable_suppl(to_feature.alias, *to_list)

    def raw_from_unknown(self, raw: str = '') -> 'Grapheme':
      new = Grapheme.from_char(raw)
      return new if self._add_symbol_and_atomic(new) else self.CTRL.nor
