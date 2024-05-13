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

"""Grapheme inventory for basic Latin characters."""

from nisaba.scripts.natural_translit.script import grapheme
from nisaba.scripts.natural_translit.utils import feature


def _build_inventory() -> grapheme.Grapheme.Inventory:
  """Builds a grapheme inventory for basic Latin characters."""
  f = feature.Feature
  g = grapheme.Grapheme
  grf = g.GR_FEATURES
  inventory = g.Inventory(g.GR_FEATURES.script.latn)
  lowercase_features = f.Set(
      grf.script.latn,
      grf.case.lower,
  )
  lowercase_args = [
      ['a', grf.ph_class.vwl],
      ['k', grf.ph_class.cons],
      ['l', grf.ph_class.cons],
      ['p', grf.ph_class.cons],
      ['s', grf.ph_class.cons],
      ['u', grf.ph_class.vwl],
  ]
  inventory.add_graphemes(
      *[
          g.from_char(char, char, f.Set(lowercase_features, features))
          for char, features in lowercase_args
      ],
      list_alias='lower',
  )
  return inventory

graphemes = _build_inventory()
