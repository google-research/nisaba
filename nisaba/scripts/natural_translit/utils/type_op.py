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

"""Functions for handling and logging type and attribute checks.

The main purpose of these functions is to provide shortcuts for checking and
converting types and attributes, and returning default values when required.
Avoids equating NoneTypes in comparisons. For example if a.features = None and
b.features = None, a and b won't be evaluated as having the same features.

TODO(): Fix typing in natural_translit.
"""

from typing import Any, Iterable, Type, TypeVar, Union
import pynini as pyn
from nisaba.scripts.natural_translit.utils import log_op as log

# Custom types
T = TypeVar('T')


class _ObjectWithAliasAndValue:
  """Parent class for Nothing and Thing. See child classes for details."""

  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(self, alias: str):
    self.alias = self._set_alias(alias)
    self.text = '%s_%s' % (log.class_of(self), self.alias)
    self.value = self

  def _set_alias(self, alias: str) -> str:
    # TODO: ensure alias conforms to inventory field name restrictions.
    if alias:
      return alias
    return log.dbg_return(
        '%s_%d' % (log.class_of(self), hash(self)),
        'empty alias is not allowed',
    )


# TODO: Look into merging Nothing and Thing, and ditch the parent class.
class Nothing(_ObjectWithAliasAndValue):
  """Class for defining constants that stand in for None and empty values.

  UNASSIGNED: Unassigned variable.
  UNSPECIFIED: Optional argument was not specified.
  MISSING: Searched object was not found.

  In the following example, UNSPECIFIED as the optional argument means nothing
  is excluded. The function can return None or UNASSIGNED unless specifically
  excluded. MISSING distinguishes the cases where the index is out of scope from
  where the value of the element is not assigned yet or where the value of the
  item is explicitly assigned as None.

  ```
  def value_from_list(some_list, index, exclude=UNSPECIFIED, instead=0):
    try:
      thing = some_list[index]
    except IndexError:
      return MISSING
    if exclude != UNSPECIFIED and thing.value == exclude:
      return instead
    return thing.value

  A = Thing(value=7)
  B = Thing(value=None)
  C = Thing(value=UNASSIGNED)
  things = [A, B, C]
  ```

  `value_from_list(things, 3)` returns `MISSING`
  `value_from_list(things, 1)` returns `None`
  `value_from_list(things, 1, exclude=None)` returns `0`
  `value_from_list(things, 2)` returns `UNASSIGNED`
  `value_from_list(things, 2, exclude=UNASSIGNED)` returns `0`
  """

  def __len__(self):
    return 0


UNASSIGNED = Nothing('unassigned')
UNSPECIFIED = Nothing('unspecified')
MISSING = Nothing('missing')


class Thing(_ObjectWithAliasAndValue):
  """Parent class for various custom classes."""

  def __init__(
      self,
      alias: str = '',
      text: str = '',
      value_from: ... = UNSPECIFIED,
      from_attribute: str = '',
  ):
    """Initializes a Thing.

    Args:
      alias: The default string that will be used to access this Thing. Alias
        should conform to attribute naming restrictions, and every item in an
        inventory should have a unique alias. For example, 'bass_fish' and
        'bass_instrument' in an English lexicon.
      text: A text that represents this Thing. Text doesn't have to be unique.
        Eg. bass_fish and bass_instrument can have the same text 'bass'
      value_from: The object that will be used to set the value of the Thing. If
        value_from is not specified, the value of the Thing is itself.
      from_attribute: The attribute of value_from that will be used to set the
        value. When setting the value of a Thing from another object, if no
        attribute is specified or if the object doesn't have the specified
        attribute, the value of the Thing will be the argument object. If
        value_from is not specified, the value of the Thing will be itself even
        if an argument is specified.

    Example:
    ```
    T1 = Thing(alias='one', value_from=1)
    T2 = Thing(value_from=T1)
    T3 = Thing(value_from=T1, from_attribute='alias')
    T4 = Thing(value_from=T1, from_attribute='value')
    T5 = Thing(value_from=T1, from_attribute='features')
    T6 = Thing(alias='six', from_attribute='alias')
    ```
    The value of T1 is 1.
    The value of T2 is T1.
    The value of T3 is 'one'.
    The value of T4 is 1.
    The value of T5 is T1.
    The value of T6 is T6.
    """
    super().__init__(alias)
    if text:
      self.text = text
    if not isinstance(value_from, Nothing):
      self.value = log.dbg_return(
          getattr(value_from, from_attribute, value_from)
      )
      self.text += ':' + log.class_and_texts(self.value)


# Union types

# FstLike from pynini doesn't work in isinstance()
FstLike = Union[str, pyn.Fst]
FstIterable = Union[Nothing, FstLike, Iterable]
# <class>OrNothing unions for arguments.
DictOrNothing = Union[dict, Nothing]
IntOrNothing = Union[int, Nothing]
ListOrNothing = Union[list, Nothing]
SetOrNothing = Union[set, Nothing]
TypeOrNothing = Union[Type, Nothing]


class IterableThing(Thing):
  """Parent class for iterable Things.

  IterableThings have size, meaning that they have length and an IterableThing
  with 0 length will return False as boolean.

  IterableThings are not subscriptable by default. Items can be accesed by
  their index with item() method, but can't be modified.

  IterableThings can be typed or untyped.

  Untyped Iterable: Anything other than Nothing and its own type can be added
  as an item. Nothing arguments are discarded. Arguments of its own type are
  flattened, i.e. the items of the argument are added. For example:
  ```
  iterable1 = IterableThing(0, 1)
  iterable2 = IterableThing(iterable1, 2, [3, 4], '567', MISSING)
  ```
  `iterable1 in iterable2` returns `False`: Self type is flattened.
  `0 in iterable2` returns `True`: Added by flattening self type argument.
  `2 in iterable2` returns `True`.
  `[3, 4] in iterable2` returns `True`.
  `3 in iterable2` returns `False`: Elements of items are not accesible.
  `'567' in iterable2` returns `True`.
  `'5' in iterable2` returns `False`.
  `MISSING in iterable2` returns `False`: Nothing type is never added.

  Typed Iterable: Only items of the specified type will be added. All
  iterables other than strings are flattened unless explicity specified in the
  item type. Self type can be included as a valid item type. In that case, the
  elements of the item will be inaccesible from the outer IterableThing.
  Arguments of other types are discarded. For example:
  ```
  iterable1 = IterableThing(0, 1)
  iterable2 = IterableThing.typed(
      Union(int, IterableThing),
      iterable1, 2, [3, 4], '567', MISSING,
  )
  ```
  `iterable1 in iterable2` returns `True`: IterableThing is a valid item type.
  `0 in iterable2` returns `False`: Elements of items are not accessible.
  `2 in iterable2` returns `True`.
  `[3, 4] in iterable2` returns `False`: list is not a valid type.
  `3 in iterable2` returns `True`: Iterables of invalid types are flattened.
  `'567' in iterable2` returns `False`: string is not a valid type.
  `'5' in iterable2` returns `False`: Invalid type, also strings are never
    flattened.
  `MISSING in iterable2` returns `False`.

  TODO: Move type_op and list_op functions to IterableThing where
    possible.
  """

  def __init__(
      self, *items: ..., alias: str = '', typed: TypeOrNothing = UNSPECIFIED
  ):
    super().__init__(alias)
    self._items = []
    # TODO: Look into Generic instead of _item_type attribute.
    self._item_type = typed if not isinstance(typed, Nothing) else Any
    self.add(*items)

  def __iter__(self):
    return self._items.__iter__()

  def __len__(self):
    return len(self._items)

  def valid_item(self, item: ...) -> bool:
    return (
        self._item_type is Any
        and not isinstance(item, Nothing)
        and type(self) is not type(item)
    ) or (self._item_type is not Any and isinstance(item, self._item_type))

  def add(self, *items: ...) -> 'IterableThing':
    for item in items:
      if self.valid_item(item):
        self._items.append(item)
      elif isinstance(item, Iterable) and not isinstance(item, str):
        self.add(*item)
    return self

  def item(self, index: int, default: T = MISSING) -> T:
    if index in range(-len(self), len(self)):
      return self._items[index]
    return default


def value_of(obj: ...) -> ...:
  """If a has no value attribute, returns a."""
  return obj.value if isinstance(obj, Thing) else obj


# Type check.


def type_check(obj: ..., default: T) -> T:
  """Checks type of obj and returns default if not of the right type."""
  return log.dbg_return(
      obj if isinstance(obj, type(default)) else default,
      log.class_and_texts(obj, default),
  )


# Equivalence functions.


def is_string(obj: ...) -> bool:
  """Returns true if the object is a string or a string Fst."""
  if isinstance(obj, str):
    return True
  if isinstance(obj, pyn.Fst):
    try:
      obj.string()
      return True
    except pyn.FstOpError:
      return False
  return False


def str_of_fstlike(fstlike: pyn.FstLike) -> str:
  if isinstance(fstlike, pyn.Fst):
    return fstlike.string()
  return fstlike


def is_equal(
    obj1: ...,
    obj2: ...,
) -> bool:
  """Checks equivalence.

  Thing instances are equal if their values are equal. Nothing constants are
    never equal even if they are the same constant.

  Args:
    obj1: Object for comparison.
    obj2: Object for comparison

  Returns:
    bool
  """
  # Check Fst first, otherwise if Fst == Non-FstLike raises error.
  if isinstance(obj1, pyn.Fst) or isinstance(obj2, pyn.Fst):
    if not isinstance(obj1, FstLike) or not isinstance(obj2, FstLike):
      return log.dbg_return_false(log.class_and_texts(obj1, obj2))
    if is_string(obj1) and is_string(obj2):
      return log.dbg_return(
          str_of_fstlike(obj1) == str_of_fstlike(obj2),
          log.class_and_texts(obj1, obj2),
      )
    return log.dbg_return(
        pyn.equal(obj1, obj2), log.class_and_texts(obj1, obj2)
    )
  obj1_val = value_of(obj1)
  obj2_val = value_of(obj2)
  if (
      isinstance(obj1_val, Nothing)
      or isinstance(obj2_val, Nothing)
      or obj1_val != obj2_val
  ):
    return log.dbg_return_false(log.class_and_texts(obj1_val))
  return log.dbg_return_true(log.class_and_texts(obj1_val, obj2_val))
