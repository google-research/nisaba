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

from __future__ import annotations

from nisaba.scripts.natural_translit.phonology.features import descriptive
from nisaba.scripts.natural_translit.phonology.features import language as lang
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import type_op as ty


class PhonologicalSymbol(sym.Symbol):
  """Parent class for symbols with phonological features."""

  DESCRIPTIVE_FEATURES = descriptive.FEATURES
  LANGUAGE = lang.FEATURES.language
  LANG_PREFIX_MULTIPLIER = 100

  def __init__(
      self,
      alias: str = '',
      raw: str = '',
      index: ty.IntOrNothing = ty.UNSPECIFIED,
      name: str = '',
      features: ft.Feature.ITERABLE = ty.UNSPECIFIED,
  ):
    super().__init__(alias, raw=raw, index=index, name=name)
    self.text = raw if raw else self.alias
    self.language = self.LANGUAGE.x_uni  # Default Unified Multilingual.
    self.features.new_profile(
        ft.Feature.Profile(self.DESCRIPTIVE_FEATURES, 'new')
    )

  def descriptives(self) -> ft.Feature.Profile:
    return self.features.descriptive

  def update_descriptives(
      self, *features: ft.Feature.ITERABLE
  ) -> PhonologicalSymbol:
    """Updates the descriptive features of the PhonologicalSymbol."""
    self.descriptives().update(*features)
    return self

  def update_descriptives_from_symbol(
      self, *symbols: PhonologicalSymbol
  ) -> PhonologicalSymbol:
    """Updates the descriptives from the union of the given symbols."""
    self.update_descriptives(*(s.descriptives() for s in symbols))
    return self

  def has_feature(self, value: ft.Feature.Aspect.VALUES) -> bool:
    return value.is_in(ft.Feature.Set(self.features, self.language))

  class Inventory(sym.Symbol.Inventory):
    """Phonological symbol inventory."""

    def __init__(
        self,
        alias,
        language: lang.Language.OR_NOTHING = ty.UNSPECIFIED,
        typed: ty.TypeOrNothing = ty.UNSPECIFIED,
    ):
      super().__init__(alias, typed=ty.type_check(typed, PhonologicalSymbol))
      self.language = ty.type_check(language, Phon.LANGUAGE.x_uni)
      self.atomics = i.Inventory()

    def _add_symbol_and_atomic(self, symbol: PhonologicalSymbol) -> bool:
      """Adds a phonological symbol to the inventory."""
      return self._add_symbol(symbol) and self.atomics.add_item(
          exp.Atomic.get_instance(symbol)
      )

    def or_from_suppl(self, suppl: ty.IterableThing) -> bool:
      """Makes an Or from a supplement and adds it to the atomics."""
      return self.atomics.add_suppl(exp.Or(*suppl, alias=suppl.alias))

    def sync_atomics(
        self, update_ors_from_suppls: ty.ListOrNothing = ty.UNSPECIFIED
    ) -> PhonologicalSymbol.Inventory:
      """Syncs the atomic inventory with the symbol inventory.

      Updates the features of the atomic instance of each phonological symbol
      to match the features of the symbol. Optionally updates the members of
      Or supplements in atomics to include all members of the given supplements
      in the list. For example, if an `inventory.vowel` iterable and a
      corresponding `inventory.atomics.vowel` Or were initiated as `[a, e, i]`
      and `(a | e | i)` respectively, and later `[o, u]` was added to
      `inventory.vowel`, this function will update `inventory.atomics.vowel` to
      `(a | e | i | o | u)`.

      Args:
        update_ors_from_suppls: Optional list of iterable supplements. When
          specified, - if there's no corresponding Or in the atomics, a new one
          is created. - if there is a corresponding Or, it's updated to include
          all symbols in the given supplement.

      Returns:
        The inventory.
      """
      for atomic in self.atomics:
        for profile in atomic.features:
          profile.update(atomic.symbol.features.get(profile.inventory))
      for suppl in ty.type_check(update_ors_from_suppls, []):
        if suppl.alias not in self.atomics.suppl_aliases:
          self.or_from_suppl(suppl)
        self.atomics.get(suppl.alias).add(*suppl)
      return self


class Phon(PhonologicalSymbol):
  """Class for representing phonemes, phones, and phonological modifiers."""

  def __init__(
      self,
      language: lang.Language.OR_NOTHING = ty.UNSPECIFIED,
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
    self.language = ty.type_check(language, self.LANGUAGE.x_uni)
    self.ipa = ipa
    self.add_features(features)

  def description(self, show_features: bool = False) -> str:
    """A string that describes the Phon."""
    text = f'alias: {self.alias}\tipa: {self.ipa}\tname: {self.name}'
    if show_features:
      text += f'\n  {self.features}'
    return text

  def copy(
      self,
      language: lang.Language.OR_NOTHING = ty.UNSPECIFIED,
      alias: str = '',
      ipa: str = '',
  ) -> Phon:
    """Creates a copy of the Phon."""
    return Phon(
        language=ty.type_check(language, self.language),
        alias=alias if alias else self.alias,
        ipa=ipa if ipa else self.ipa,
        index=self.index,
        name=self.name,
        features=self.features.copy(),
    )

  class Inventory(PhonologicalSymbol.Inventory):
    """Phon inventory."""

    def __init__(self, language: lang.Language.OR_NOTHING = ty.UNSPECIFIED):
      language = ty.type_check(language, Phon.LANGUAGE.x_uni)
      super().__init__(language.alias, language, Phon)

    def _add_phoneme(self, phoneme: Phon) -> bool:
      """Adds a phoneme to the inventory."""
      phoneme.language = self.language
      phoneme.index = (
          Phon.ReservedIndex.PHONEME_PREFIX
          + int(self.language.index) * Phon.LANG_PREFIX_MULTIPLIER
          + len(self)
          + 1
      )
      return self._add_symbol_and_atomic(phoneme)

    def add_phonemes(self, *phonemes: Phon, list_alias: str = '') -> list[Phon]:
      phs = [ph for ph in phonemes if self._add_phoneme(ph)]
      if list_alias:
        self.make_iterable_suppl(list_alias, *phs)
      return phs
