# Copyright 2023 Nisaba Authors.
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

"""Converts feature inventories to str inventories for backward compatibility.

TODO: Remove after updating modify_phon and phoneme_inventory to use
feature2.

"""

from nisaba.scripts.natural_translit.features import phonological
from nisaba.scripts.natural_translit.features import qualifier
from nisaba.scripts.natural_translit.utils import inventory2


def _convert_and_add(
    feature_inventory: inventory2.Inventory,
    str_inventory: inventory2.Inventory,
) -> None:
  for alias in feature_inventory.item_aliases:
    str_inventory.add_item(feature_inventory.get(alias), 'alias')
  for alias in feature_inventory.supp_aliases:
    str_inventory.make_supp(
        alias, [f.alias for f in feature_inventory.get(alias)]
    )


def _str_inventory() -> inventory2.Inventory:
  """Str feature inventory for backward compatibility."""
  f = inventory2.Inventory()
  _convert_and_add(phonological.articulatory, f)
  _convert_and_add(phonological.suprasegmental, f)
  _convert_and_add(qualifier.qualifier, f)
  return f


FEATURE_INVENTORY = _str_inventory()
