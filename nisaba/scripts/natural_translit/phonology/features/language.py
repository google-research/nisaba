# Copyright 2025 Nisaba Authors.
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

"""Language feature for PhonologicalSymbol."""

from __future__ import annotations

from typing import Union

import pycountry

from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import type_op as ty


class Language(ft.Feature):
  """Language feature for Phon."""

  OR_NOTHING = Union['Language', ty.Nothing]

  def __init__(self, alias: str, text: str, index: int):
    super().__init__(alias, text)
    self.index = index

  @classmethod
  def from_iso(cls, iso_code: str) -> Language:
    if len(iso_code) == 2:
      language = pycountry.languages.get(alpha_2=iso_code)
    elif len(iso_code) == 3:
      language = pycountry.languages.get(alpha_3=iso_code)
    else:
      raise ValueError(f'Invalid ISO code: {iso_code}')
    return cls(
        iso_code.lower(),
        language.name,
        list(pycountry.languages).index(language)
    )

  class Inventory(ft.Feature.Inventory):
    """Language feature inventory."""

    def __str__(self) -> str:
      """Language family tree as markdown dot code block."""
      # Currently all languages are equidistant and have 1 distance from each
      # other so there is no need for distance tables. If the subgroup steps
      # are changed to reflect similarity of related languages, the distance
      # tables should be appended below.
      return self.language.visualize()


def _features() -> Language.Inventory:
  """Language feature inventory.

  Returns:
    An inventory of languages.

  The language inventory is organised by language families. The depth and the
  granularity of the family hierarchy is pragmatic and can be updated as needed.
  """
  f = ft.Feature
  features = Language.Inventory(
      'languages',
      f.Aspect(
          f.equidistant(
              'language',
              f.equidistant(
                  'dravidian',
                  Language.from_iso('kn'),
                  Language.from_iso('te'),
                  f.equidistant(
                      ('tamil_kota', 'Tamil-Kota'),
                      Language.from_iso('ml'),
                      Language.from_iso('ta'),
                  ),
              ),
              f.equidistant(
                  ('indo_european', 'Indo-European'),
                  f.equidistant(
                      ('indo_aryan', 'Indo-Aryan'),
                      Language.from_iso('bn'),
                      Language.from_iso('gu'),
                      Language.from_iso('hi'),
                      Language.from_iso('mr'),
                      Language.from_iso('pa'),
                  ),
                  f.equidistant(
                      'germanic',
                      Language.from_iso('en'),
                  ),
              ),
              f.equidistant(
                  ('mixed_family', 'Mixed Family Tags'),
                  # ISO 'mul' is a generic code for mixed-language datasets.
                  Language.from_iso('mul'),
                  Language.from_iso('und'),
                  # x_uni is a custom code for the unified phoneme inventory
                  # that will cover all IPA symbols and most common PHOIBLE
                  # segments. Index 8000 is reserved for the unified inventory.
                  # This will provide unique indices for all phonemes as long as
                  # the number of pycountry languages is less than 8000
                  # (currently 7874). If the number of pycounty languages
                  # exceeds 8000, we can change
                  # Symbol.ReservedIndex.PHONEME_PREFIX to 30_000_000 and
                  # PhonologicalSymbol.LANG_PREFIX_MULTIPLIER to 1_000 to
                  # accommodate.
                  Language('x_uni', 'Unified Phonology', 8_000),
                  # x_uni will potentially cover 2k to 6k segments, resulting in
                  # symbol indices from 3_800_001 up to 3_806_xxx. In order to
                  # avoid symbol index collision, we start other custom language
                  # indices from 9000.
                  Language('x_psa', 'Pan South Asian', 9_001),
              ),
          ),
      ),
  )
  return features


FEATURES = _features()
