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


class Nothing:
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

  def __init__(self, name: str):
    self.alias = name.upper()
    self.text = name
    self.value = self

UNASSIGNED = Nothing('Unassigned')
UNSPECIFIED = Nothing('Unspecified')
MISSING = Nothing('Missing')


class Thing:
  """Parent class for various custom classes.

  Attributes:
    alias: A string that will be used to refer to this object. An alias should
      be unique in a given context. Eg, every phoneme in an inventory or every
      token in a lexicon should have a unique alias.
    text: A string that represents the surface form of the object. eg. bass_fish
      and bass_instrument in an English lexicon can have the same text 'bass'.
    value: The value of the Object. The initial value of the
      thing is itself.

    For example, the value of a phoneme in an inventory is itself. Each
    occurence of the phoneme in a pronunciation is a new instance, but their
    values point to the same phoneme in the inventory.
  """

  def __init__(self):
    c = log.class_of(self)
    self.alias = '%s_%d' % (c, hash(self))
    self.text = 'Undefined %s' % c
    self.value = self

  @classmethod
  def with_alias(cls, alias: str) -> 'Thing':
    new = cls()
    new.set_alias(alias)
    new.text = log.class_and_alias(new)
    return new

  @classmethod
  def from_value_of(cls, entry: ...) -> 'Thing':
    """Makes a Thing from the value of the entry.

    Args:
      entry: If the entry is an object with 'value' attribute, the value is
        set to entry.value in order to avoid nesting values in dynamically
        created things and making their equivalence invisible to is_equal().
        If this is undesirable, use with_alias_and_value().

    Returns:
      Thing
    """
    new = cls()
    new.text = log.from_class_and_text(entry)
    new.value = value_of(entry)
    return new

  @classmethod
  def with_alias_and_value(cls, alias: str, value: ...) -> 'Thing':
    """Makes a Thing with a custom alias and value."""
    new = cls()
    new.set_alias(alias)
    new.text = '%s:%s' % (log.class_and_alias(new), log.class_and_texts(value))
    new.value = value
    return new

  def set_alias(self, alias: str) -> None:
    # TODO: ensure alias conforms to inventory field name restrictions.
    if alias:
      self.alias = alias
    else:
      log.dbg_message('empty alias is not allowed')

# Union types

# FstLike from pynini doesn't work in isinstance()
FstLike = Union[str, pyn.Fst]
# <class>OrNothing unions for arguments.
DictOrNothing = Union[dict, Nothing]
IntOrNothing = Union[int, Nothing]
ListOrNothing = Union[list, Nothing]
SetOrNothing = Union[set, Nothing]
ThingOrNothing = Union[Thing, Nothing]
TypeOrNothing = Union[Type, Nothing]


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
