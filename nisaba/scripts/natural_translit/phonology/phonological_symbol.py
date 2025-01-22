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

"""Classes for phonological symbols."""

from nisaba.scripts.natural_translit.phonology import descriptive_features
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import type_op as ty


class PhonologicalSymbol(sym.Symbol):
  """Parent class for symbols with phonological features."""

  PH_DESCRIPTIVE_FEATURES = descriptive_features.FEATURES

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      raw: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
      name: str = '',
      features: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ):
    super().__init__(alias, text, raw, index, name)
    self.features.new_profile(
        ft.Feature.Profile(self.PH_DESCRIPTIVE_FEATURES, 'new')
    )

  class Inventory(sym.Symbol.Inventory):
    """Phonological symbol inventory."""

    def __init__(self, alias: str, typed: ty.TypeOrNothing = ty.UNSPECIFIED):
      super().__init__(alias, typed=ty.type_check(typed, PhonologicalSymbol))
      self.atomics = i.Inventory()

    def _add_symbol_and_atomic(self, obj: 'PhonologicalSymbol') -> bool:
      """Adds a phonological symbol to the inventory."""
      return self._add_symbol(obj) and self.atomics.add_item(
          exp.Atomic.get_instance(obj)
      )


class Phon(PhonologicalSymbol):
  """Class for representing phonemes, phones, and phonological modifiers."""

  # TODO: Add pycountry languages as a feature similar to scripts.
  # Phone index will be determined by a combination of the reserved prefix for
  # phonemes, the index of the country code, and the index of the phon in
  # the language inventory.
  def __init__(
      self,
      language: str = '',
      alias: str = '',
      ipa: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
      name: str = '',  # TODO: Derive name automatically from features.
      features: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ):
    super().__init__(
        alias=alias,
        index=index,
        name=name,
    )
    self.language = language if language else 'x_mul'  # Custom multilingual.
    self.ipa = ipa
    self.add_features(features)

  def description(self, show_features: bool = False) -> str:
    """A string that describes the Phon."""
    text = 'alias: %s  ipa: %s  name: %s' % (self.alias, self.ipa, self.name)
    if show_features:
      text += '\n  %s' % str(self.features)
    return text

  def copy(
      self,
      language: str = '',
      alias: str = '',
      ipa: str = '',
      ) -> 'Phon':
    """Creates a copy of the Phon."""
    return Phon(
        language=language if language else self.language,
        alias=alias if alias else self.alias,
        ipa=ipa if ipa else self.ipa,
        index=self.index,
        name=self.name,
        features=self.features.copy(),
    )

  def update_descriptives(
      self, *features: ft.Feature.ITERABLE
  ) -> 'Phon':
    """Updates the descriptive features of the Phon."""
    self.features.phonology_descriptive.update(*features)
    return self

  class Inventory(PhonologicalSymbol.Inventory):
    """Phon inventory."""

    def __init__(self, language: str = ''):
      language = language if language else 'x_mul'  # Custom multilingual.
      super().__init__(alias=language, typed=Phon)
      self.language = language
      self.atomics = i.Inventory()

    def _add_phoneme(self, phoneme: 'Phon') -> bool:
      """Adds a phoneme to the inventory."""
      phoneme.index = Phon.ReservedIndex.PHONEME_PREFIX + len(self) + 1
      return self._add_symbol_and_atomic(phoneme)

    def add_phonemes(
        self, *phonemes: 'Phon', list_alias: str = ''
    ) -> list['Phon']:
      phs = [ph for ph in phonemes if self._add_phoneme(ph)]
      if list_alias:
        self.make_suppl(list_alias, phs)
      return phs
