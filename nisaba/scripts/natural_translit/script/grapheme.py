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
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import symbol as sym


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
      # TODO: Remove temporary phonological grapheme features when
      # phonology/features is updated.
      f.Aspect(
          f.equidistant(
              'ph_class',  # phonological class
              f('none', 'non-phonological'),
              f('vwl', 'vowel'),
              f('cons', 'consonant'),
          )
      ),
  )
  return ftr


class Grapheme(sym.Symbol):
  """Grapheme symbol."""

  GR_FEATURES = _grapheme_features()

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
    name += ' U+' + code_hex.upper()
    return cls(
        alias=alias,
        text=character,
        raw=character,
        index=index,
        name=name,
        features=ft.Feature.Set(cls.SYM_FEATURES.type.raw, features),
    )

  class Inventory(sym.Symbol.Inventory):
    """Grapheme inventory."""

    def __init__(self, script: ft.Feature):
      super().__init__(alias=script.alias, typed=Grapheme)
      self.script = script
