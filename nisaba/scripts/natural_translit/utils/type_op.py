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

from typing import Any, Iterable, Union, Type
import pynini as pyn
from nisaba.scripts.natural_translit.utils import log_op as log

# Custom types


class _ObjectWithAliasAndValue:
  """Parent class for Nothing and Thing. See child classes for details."""

  def __init__(self, alias: str):
    self.alias = self._set_alias(alias)
    self.text = '%s_%s' % (log.class_of(self), self.alias)
    self.value = self

  def _set_alias(self, alias: str) -> str:
    # TODO: ensure alias conforms to inventory field name restrictions.
    if alias: return alias
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
      alias: The default string that will be used to access this Thing.
        Alias should conform to attribute naming restrictions, and every item in
        an inventory should have a unique alias. For example, 'bass_fish' and
        'bass_instrument' in an English lexicon.
      text: A text that represents this Thing. Text doesn't have to be unique.
        Eg. bass_fish and bass_instrument can have the same text 'bass'
      value_from: The object that will be used to set the value of the Thing.
        If value_from is not specified, the value of the Thing is itself.
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
    if text: self.text = text
    if is_specified(value_from):
      self.value = get_attribute(value_from, from_attribute, value_from)
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
ThingOrNothing = Union[Thing, Nothing]
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

  def __init__(self, *items: ..., alias: str = ''):
    super().__init__(alias)
    self._items = []
    # TODO: Look into Generic instead of _item_type attribute.
    self._item_type = UNASSIGNED
    self.add(*items)

  def __iter__(self):
    return self._items.__iter__()

  def __len__(self):
    return len(self._items)

  @classmethod
  def typed(
      cls, item_type: TypeOrNothing, *items: ...
  ) -> 'IterableThing':
    """Makes an IterableThing whose items are only of the specified type."""
    new_iterable = cls()
    if not_nothing(item_type): new_iterable._item_type = item_type
    new_iterable.add(*items)
    return new_iterable

  def is_typed(self) -> bool:
    return not_nothing(self._item_type)

  def not_typed(self) -> bool:
    return not self.is_typed()

  def valid_item(self, item: ...) -> bool:
    if self.not_typed():
      return not_nothing(item) and type(self) is not type(item)
    return is_instance(item, self._item_type)

  def invalid_item(self, item: ...) -> bool:
    return not self.valid_item(item)

  def add(self, *items: ...) -> 'IterableThing':
    for item in items:
      if self.valid_item(item):
        if isinstance(self._items, list): self._items.append(item)
        if isinstance(self._items, set): self._items.add(item)
      elif isinstance(item, Iterable) and not isinstance(item, str):
        self.add(*item)
    return self

  def item(self, index: int, default: ... = MISSING) -> ...:
    if index in range(-len(self), len(self)): return self._items[index]
    return default


def value_of(obj: ...) -> ...:
  """If a has no value attribute, returns a."""
  return obj.value if isinstance(obj, Thing) else obj

# Type check.


def is_none(obj: ...) -> bool:
  """Checks None for logging purposes."""
  return log.dbg_return(obj is None, log.class_and_texts(obj))


def not_none(obj: ...) -> bool:
  return not is_none(obj)


def is_assigned(obj: ...) -> bool:
  """Checks UNASSIGNED for logging purposes."""
  return log.dbg_return(obj is not UNASSIGNED, log.class_and_texts(obj))


def not_assigned(obj: ...) -> bool:
  return not is_assigned(obj)


def is_specified(obj: ...) -> bool:
  """Checks UNSPECIFIED for logging purposes."""
  return log.dbg_return(obj is not UNSPECIFIED, log.class_and_texts(obj))


def not_specified(obj: ...) -> bool:
  return not is_specified(obj)


def is_found(obj: ...) -> bool:
  """Checks MISSING for logging purposes."""
  return log.dbg_return(obj is not MISSING, log.class_and_texts(obj))


def not_found(obj: ...) -> bool:
  return not is_found(obj)


def is_nothing(obj: ...) -> bool:
  """Checks Nothing constants."""
  return log.dbg_return(isinstance(obj, Nothing), log.class_and_texts(obj))


def not_nothing(obj: ...) -> bool:
  return not is_nothing(obj)


def exists(obj: ...) -> bool:
  """Combines checking for None and undefined Things."""
  return log.dbg_return(
      obj is not None and not isinstance(obj, Nothing),
      log.class_and_texts(obj)
  )


def not_exists(obj: ...) -> bool:
  return not exists(obj)


def is_instance(obj: ..., typeinfo: TypeOrNothing = UNSPECIFIED) -> bool:
  """Checks instance for logging purposes.

  Args:
    obj: Object
    typeinfo: Type. Default value is UNSPECIFIED to make type check optional in
      functions that call is_instance, while the case of optional argument
      and specifically checking for Null type as distinct cases.

  Returns:
    bool

  """
  if isinstance(typeinfo, Nothing): return log.dbg_return_true(
      'typeinfo %s for %s' % (typeinfo.text, log.class_and_texts(obj))
  )
  if isinstance(obj, typeinfo):
    return log.dbg_return_true(log.class_and_texts(obj))
  return log.dbg_return_false(
      '%s not %s' % (log.class_and_texts(obj), log.name_of(typeinfo))
  )


def not_instance(obj: ..., typeinfo: TypeOrNothing = UNSPECIFIED) -> bool:
  return not is_instance(obj, typeinfo)

# Attribute functions with type check.


def has_attribute(
    obj: ..., attr: str, typeinfo: TypeOrNothing = UNSPECIFIED
) -> bool:
  """Adds log and optional type check to hasattr()."""
  if not hasattr(obj, attr): return log.dbg_return_false(
      '%s has no attribute %s' % (log.class_and_texts(obj), attr)
  )
  return log.dbg_return(is_instance(getattr(obj, attr), typeinfo))


def get_attribute(
    obj: ..., attr: str, default: ... = MISSING,
    typeinfo: TypeOrNothing = UNSPECIFIED
) -> ...:
  """Adds log and type check to getattr()."""
  return log.dbg_return(
      getattr(obj, attr) if has_attribute(obj, attr, typeinfo) else default,
      '%s of %s' % (attr, log.class_and_texts(obj))
  )

# Equivalence functions.


def is_equal(
    obj1: ..., obj2: ...,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  """Checks equivalence.

  Never equates None, logs other 'not a' conditions.
  Never equates Nothing.
  Thing instances are equal if their values are equal.

  Args:
    obj1: Object for comparison.
    obj2: Object for comparison
    empty: When false, empty str, list and dict are not considered equal.
    epsilon: When false, epsilon fsts are not considered equal.
    zero: When false, zero is not considered equal.

  Returns:
    bool

  """
  # Check Fst first, otherwise if Fst == Non-FstLike raises error.
  if isinstance(obj1, pyn.Fst) or isinstance(obj2, pyn.Fst):
    if (
        not isinstance(obj1, FstLike) or
        not isinstance(obj2, FstLike) or
        obj1 != obj2
    ):
      return log.dbg_return_false(log.class_and_texts(obj1, obj2))
    if not epsilon and obj1 == pyn.accep(''):
      return log.dbg_return_false('epsilon fst')
    return log.dbg_return_true(log.class_and_texts(obj1, obj2))
  obj1_val = value_of(obj1)
  obj2_val = value_of(obj2)
  if obj1_val != obj2_val:
    return log.dbg_return_false(log.class_and_texts(obj1_val, obj2_val))
  if (
      obj1_val is None or
      isinstance(obj1_val, Nothing) or
      (not zero and obj1_val == 0) or
      (not empty and is_empty(obj1_val))
  ): return log.dbg_return_false(log.class_and_texts(obj1_val))
  return log.dbg_return_true(log.class_and_texts(obj1_val, obj2_val))


def not_equal(
    obj1: ..., obj2: ...,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  return not is_equal(obj1, obj2, empty, epsilon, zero)

# Iterable functions


# TODO: Restrict the arg type of is_empty() to IterableOrNothing.
def is_empty(obj: ...) -> bool:
  try:
    return log.dbg_return(len(obj) < 1, log.class_and_texts(obj))
  except TypeError:
    return log.dbg_return_false('no size for ' + log.class_and_texts(obj))


def not_empty(obj: ...) -> bool:
  return not is_empty(obj)


def get_element(
    search_in: ..., index: int, default: ... = MISSING
    ) -> ...:
  """Returns a[index] if possible, default value if not."""
  if not isinstance(search_in, Iterable): return log.dbg_return(
      default, log.class_and_texts(search_in) + ' not iterable'
  )
  try:
    return search_in[index]
  except IndexError:
    return log.dbg_return(default, 'index error')


def enforce_range(
    start: IntOrNothing, stop: IntOrNothing,
    default_start: IntOrNothing = UNSPECIFIED,
    default_stop: IntOrNothing = UNSPECIFIED,
) -> range:
  """Enforces range type for int or Nothing arguments.

  Args:
    start: Start of range.
    stop: Stop of range.
    default_start: Optional start value if start is Nothing.
    default_stop: Optional stop value if stop is Nothing.

  Fail value is range(0) to ensure type but in_range() always returns false.

  Eg.
  `enforce_range(1, 5)` returns `range(1, 5)`
  `enforce_range(MISSING, 5)` returns `range(0)`
  `enforce_range(1, 5, 0, 10)` returns `range(1, 5)`
  `enforce_range(MISSING, 5, 0, 10)` returns `range(0, 5)`
  `enforce_range(1, MISSING, 0, 10)` returns `range(1, 10)`
  `enforce_range(1, MISSING, 0, MISSING)` returns `range(0)`

  default_start and default_stop values for Nothing start and stop args for
  cases like:
  ```
    enforce_range(
        previous_vowel_index,
        next_vowel_index,
        default_start=0,
        default_stop=len(word))
  ```

  Returns:
    range
  """
  r_start = start if isinstance(start, int) else default_start
  r_stop = stop if isinstance(stop, int) else default_stop
  if isinstance(r_start, int) and isinstance(r_stop, int):
    r = range(r_start, r_stop)
  else: r = range(0)
  return log.dbg_return(
      r, log.class_and_texts(start, stop, default_start, default_stop)
  )


def in_range(
    look_for: IntOrNothing, start: IntOrNothing, stop: IntOrNothing,
    default_start: IntOrNothing = UNSPECIFIED,
    default_stop: IntOrNothing = UNSPECIFIED
) -> bool:
  """Checks if look_for is in an enforced range."""
  return log.dbg_return_in(
      look_for, enforce_range(start, stop, default_start, default_stop)
  )


def enforce_list(obj: ListOrNothing) -> list[Any]:
  """Enforces list type for list or Nothing arguments."""
  # TODO: catch dict iterables as list
  if isinstance(obj, list): return obj
  return log.dbg_return([], log.from_class_and_text(obj))


def in_list(look_for: ..., look_in: ListOrNothing) -> bool:
  """Checks if look_for is an element of a list enforced from look_in."""
  return log.dbg_return_in(look_for, enforce_list(look_in))


def enforce_dict(obj: DictOrNothing) -> dict[Any, Any]:
  """Enforces dict type for dict or Nothing arguments."""
  if isinstance(obj, dict): return obj
  return log.dbg_return({}, log.from_class_and_text(obj))


def dict_get(obj: DictOrNothing, key: ..., default: ... = MISSING) -> ...:
  try:
    return log.dbg_return(enforce_dict(obj).get(key, default))
  except TypeError:
    return log.dbg_return(default, 'invalid key type')


def enforce_set(obj: SetOrNothing) -> set[Any]:
  """Enforces set type for set or Nothing arguments."""
  if isinstance(obj, set): return obj
  return log.dbg_return(set(), log.from_class_and_text(obj))


def in_set(look_for: ..., look_in: ...) -> bool:
  return log.dbg_return_in(look_for, enforce_set(look_in))
