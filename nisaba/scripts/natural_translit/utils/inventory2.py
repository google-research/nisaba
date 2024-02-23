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

"""Inventory class.

This class will replace the named tuples in inventory.py and the functions used
to build or process the inventories currently scattered accross modules.
"""

from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


class Inventory(ty.IterableThing):
  """Inventory is a collection of items and supplements.

  The items of an inventory, eg. the graphemes in a Grapheme Inventory, can be
  accessed by their aliases. For example, if
  `A = ty.Thing(alias='a_uc', value_from='A')` is added to an inventory
  such as `ltn` as an item, `ltn.a_uc` will point to A. All items are included
  when iterating over the inventory and the len of the inventory is the number
  of its items.

  The supplements can also be accessed by an alias, but they are not included
  in iterations.
  For example, the list `L = [A, ...]` can be added to `ltn` as a
  supplement with alias `vowels`. In this case, `ltn.vowels` will point to L,
  but it won't be included in iterations like 'for gr in ltn`.
  """

  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self, alias: str = '', typed: ty.TypeOrNothing = ty.UNSPECIFIED):
    super().__init__(alias=alias)
    if ty.not_nothing(typed): self._item_type = typed
    self.text = alias if alias else 'New Inventory'
    self.item_aliases = []
    self.supl_aliases = []

  @classmethod
  def from_list(
      cls,
      items: list[ty.Thing],
      attr: str = '',
      typed: ty.TypeOrNothing = ty.UNSPECIFIED,
      supls: ty.ListOrNothing = ty.UNSPECIFIED,
      alias: str = '',
  ) -> 'Inventory':
    """Makes an Inventory from a list of things."""
    new = cls(alias, typed)
    for item in items:
      new.add_item(item, attr)
    for s in ty.enforce_list(supls):
      new.add_supl(s)
    return new

  def _add_field(self, alias: str, value: ...) -> bool:
    if alias in self.__dict__.keys():
      return log.dbg_return_false('skipping recurring alias %s' % alias)
    self.__dict__[alias] = value
    return True

  def _get_field_value(
      self, thing: ty.Thing, attr: str = '',
      typed: ty.TypeOrNothing = ty.UNSPECIFIED
  ) -> ...:
    """Gets the value for a field from a Thing.

    Args:
      thing: The source for the field value.
      attr: The attribute of the Thing that will become the value of the field.
        If attr isn't specified, the value will be the Thing itself.
      typed: Optional type restriction for the value.

    Returns:
      Given `N1 = ty.Thing(alias='n', value_from=1)`
      `self._get_field_value(N1)` returns `N1`
      `self._get_field_value(N1, typed=int)` returns `ty.MISSING`
      `self._get_field_value(N1, 'value')` returns `1`
      `self._get_field_value(N1, 'value', typed=ty.Thing)` returns `ty.MISSING`

    """
    field_value = ty.get_attribute(thing, attr) if attr else thing
    return field_value if ty.is_instance(field_value, typed) else ty.MISSING

  def add(self, *args) -> 'Inventory':
    log.dbg_message('Use add_item or add_suppl for Inventories.')
    return self

  def add_item(
      self, thing: ty.Thing, attr: str = '',
  ) -> bool:
    field_value = self._get_field_value(thing, attr)
    if self.invalid_item(field_value) or field_value in self: return False
    added = self._add_field(thing.alias, field_value)
    if added:
      self._items.append(field_value)
      self.item_aliases.append(thing.alias)
    return added

  def add_supl(self, supl: ty.Thing) -> bool:
    """Adds the value of a Thing as a supplement."""
    return self.make_supl(supl.alias, supl.value)

  def make_supl(self, alias: str, value: ...) -> bool:
    """Adds the value as a supplement."""
    added = self._add_field(alias, value)
    if added: self.supl_aliases.append(alias)
    return added

  def get(self, alias: str, default: ... = ty.MISSING) -> ...:
    if alias in self.item_aliases or alias in self.supl_aliases:
      return log.dbg_return(
          getattr(self, alias, default), 'for alias ' + alias
      )
    return default

Inventory.EMPTY = Inventory('empty_inventory')
