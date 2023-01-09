# Copyright 2022 Nisaba Authors.
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

"""Inventory building functions.

* Store is a versatile named tuple that has an alias field and a content field,
  that allows access to its content by its alias.

* Inventory is a is dynamically created named tuple that has the aliases of the
  items as field names. It is populated with the corresponding lists and fsts.

  Example:

  In a phoneme inventory, `VOWEL_LIST = Store('VOWEL_LIST', [ph.A, ph.E, ...])`
  allows the list of vowels to be accessed by `VOWEL_LIST.content`, and
  `VOWEL = Store('VOWEL', ls.union_opt(*VOWEL_LIST))` allows the union of vowels
  to be accessed by `VOWEL.content` in the inventory.

  When imported as ph = phonemes.ph_inventory in a grammar, they can be used
  for functions like `for vowel in ph.VOWEL_LIST:` and rules like
  `rw.rewrite(voiceless, voiced, ph.VOWEL, ph.VOWEL)`.
"""

import collections
from typing import Union, List
import pynini as p

Store = collections.namedtuple(
    'Store', ['alias', 'content'])

Storable = Union[collections.namedtuple, List, p.FstLike]


def store_as(
    alias: str,
    content: Storable) -> Store:
  """Makes a Store.

  Args:
    alias: The alias that will be used in grammars.
    content: The content of the Store.

  Returns:
    Store

  Following call:
  ```
  store_as('my_list', [item1, item2, item3])
  ```
  will return a store. If this store is added to an inventory 'i', it
  can be accessed from another file as:
  ```
  for item in i.my_list:
    ...
  ```
  """
  return Store(alias, content)


def alias_list(store_list: List[Store]) -> List[str]:
  return [store.alias for store in store_list]


def content_list(store_list: List[Store]) -> List[Storable]:
  return [store.content for store in store_list]


def make_inventory(
    item_list: List[Storable],
    sym_list: List[collections.namedtuple],
    store_list: List[Store] = None) -> collections.namedtuple:
  """Makes an inventory from lists of items, symbols and stores.

  Args:
    item_list: The list of contents that will be accessed by the aliases of the
      symbols and the stores.
    sym_list: The list of symbols the fields will be curated from.
    store_list: The list of additional stores in the inventory.

  Returns:
    Inventory

  Following call:
  ```
  i = make_inventory(
      [a, b, c],
      [Store('A', a), Store('B', b), Store('C', c), Store('AC', [a, c])])
  ```
  will create an Inventory tuple, and return a populated inventory:
  ```
  Inventory('Inventory', ['A', 'B', 'C', 'AB'])
  i = Inventory(a, b, c, [a, c])
  ```
  """
  fields = alias_list(sym_list)
  items = item_list
  if store_list is not None:
    fields = fields + alias_list(store_list)
    items = items + content_list(store_list)
  return collections.namedtuple('Inventory', [*fields])(*items)
