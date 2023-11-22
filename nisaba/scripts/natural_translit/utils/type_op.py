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

"""Functions for handling and logging type and attribute checks.

The main purpose of these functions is to provide shortcuts for checking and
converting types and attributes, and returning default values when required.
Avoids equating NoneTypes in comparisons. For example if a.features = None and
b.features = None, a and b won't be evaluated as having the same features.

TODO(): Fix typing in natural_translit.
"""

from typing import Any, Dict, Iterable, List, Tuple, Union, Type
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
    new.text = '%s:%s' % (log.class_and_alias(new), log.class_and_text(value))
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
  return log.dbg_return(obj is None, log.class_and_text(obj))


def not_none(obj: ...) -> bool:
  return not is_none(obj)


def is_assigned(obj: ...) -> bool:
  """Checks UNASSIGNED for logging purposes."""
  return log.dbg_return(obj is not UNASSIGNED, log.class_and_text(obj))


def not_assigned(obj: ...) -> bool:
  return not is_assigned(obj)


def is_specified(obj: ...) -> bool:
  """Checks UNSPECIFIED for logging purposes."""
  return log.dbg_return(obj is not UNSPECIFIED, log.class_and_text(obj))


def not_specified(obj: ...) -> bool:
  return not is_specified(obj)


def is_found(obj: ...) -> bool:
  """Checks MISSING for logging purposes."""
  return log.dbg_return(obj is not MISSING, log.class_and_text(obj))


def not_found(obj: ...) -> bool:
  return not is_found(obj)


def is_nothing(obj: ...) -> bool:
  """Checks Nothing constants."""
  return log.dbg_return(isinstance(obj, Nothing), log.class_and_text(obj))


def not_nothing(obj: ...) -> bool:
  return not is_nothing(obj)


def exists(obj: ..., allow_none: bool = False) -> bool:
  """Combines checking for None and undefined Things."""
  return (not_none(obj) or allow_none) and not_nothing(obj)


def not_exists(obj: ..., allow_none: bool = False) -> bool:
  return not exists(obj, allow_none)


def is_instance_dbg(obj: ..., want: TypeOrNothing = UNSPECIFIED) -> bool:
  """Checks instance for logging purposes.

  Args:
    obj: Object
    want: Type. Default value is UNSPECIFIED to make type check optional in
      functions that call is_instance_dbg, while the case of optional argument
      and specifically checking for Null type as distinct cases.

  Returns:
    bool

  """
  if not_specified(want):
    return log.dbg_return_true(
        'type check not requested for %s' % log.text_of(obj)
    )
  try:
    if isinstance(obj, want): return True
    return log.dbg_return_false('%s not %s' % (log.text_of(obj), want.__name__))
  except TypeError:
    return log.dbg_return_false('invalid type')


def not_instance(obj: ..., want: TypeOrNothing = UNSPECIFIED) -> bool:
  return not is_instance_dbg(obj, want)


def enforce_thing(t: ...) -> Thing:
  """Enforces thing type. If t is not Thing, puts t in value of a new Thing."""
  if isinstance(t, Thing): return t
  return log.dbg_return(Thing.from_value_of(t))

# Attribute functions with type check.


def has_attribute(
    obj: ..., attr: str, want: TypeOrNothing = UNSPECIFIED
) -> bool:
  """Adds log and optional type check to hasattr()."""
  if not_exists(obj): return False
  if not hasattr(obj, attr):
    return log.dbg_return_false(
        '%s not an attribute of %s' % (attr, log.text_of(obj))
    )
  return is_instance_dbg(getattr(obj, attr), want)


def get_attribute(
    obj: ..., attr: str, default: ... = MISSING,
    want: TypeOrNothing = UNSPECIFIED
) -> ...:
  """Adds log and type check to getattr()."""
  return getattr(obj, attr) if has_attribute(obj, attr, want) else default

# Equivalence functions.


def is_equal(
    obj1: ..., obj2: ...,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  """Checks equivalence.

  Never equates None, logs other 'not a' conditions.
  Never equates UNASSIGNED, UNSPECIFIED or MISSING.
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
    if not_instance(obj1, FstLike) or not_instance(obj2, FstLike):
      return log.dbg_return_false(
          'type mismatch between %s and %s' %
          (log.class_and_text(obj1), log.class_and_text(obj2))
      )
    if obj1 != obj2: return False
    if not epsilon and obj1 == pyn.accep(''):
      return log.dbg_return_false('epsilon fst')
  obj1_val = value_of(obj1)
  obj2_val = value_of(obj2)
  if obj1_val != obj2_val:
    if not_instance(obj1_val, type(obj2_val)):
      log.dbg_message('type mismatch %s' % log.texts_of(obj1_val, obj2_val))
    return False
  if (
      not_exists(obj1_val) or
      (not zero and obj1_val == 0) or
      (not empty and is_empty(obj1_val))
  ): return log.dbg_return_false(log.text_of(obj1_val))
  return True


def not_equal(
    obj1: ..., obj2: ...,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  return not is_equal(obj1, obj2, empty, epsilon, zero)

# Iterable functions


def is_empty(obj: ..., allow_none: bool = False) -> bool:
  return not_exists(obj, allow_none) or (isinstance(obj, Iterable) and not obj)


def not_empty(obj: ..., allow_none: bool = False) -> bool:
  return not is_empty(obj, allow_none)


def get_element(
    search_in: ..., index: int, default: ... = MISSING
    ) -> ...:
  """Returns a[index] if possible, default value if not."""
  if not_exists(search_in): return default
  if not_instance(search_in, Iterable): return default
  try:
    return search_in[index]
  except IndexError:
    return log.dbg_return(default, 'index error')


def enforce_range(
    arg1: ..., arg2: ... = UNSPECIFIED, arg3: ... = UNSPECIFIED,
    def_start: ... = UNSPECIFIED, def_stop: ... = UNSPECIFIED,
) -> range:
  """Ensures range type for tuple arguments.

  Args:
    arg1: If int, start or stop. If Tuple(int, int), provides range arguments.
    arg2: If arg1 is int, stop. If arg1 is (int, int) step.
    arg3: If arg1 and arg2 are int, step.
    def_start: Optional start value if range starts at None.
    def_stop: Optional stop value if range stops at None.

  Fail value is range(0) to ensure type but in_range() always returns false.
  Default values are UNSPECIFIED to differentiate NoneType from optional args.

  Eg. `enforce_range(1, 5, 2)` returns `range(1, 5, 2)`
      `enforce_range((1, 5), 2)` returns `range(1, 5, 2)`
      `enforce_range(5)` returns `range(5)`.
      `enforce_range(5, None)` returns `range(0)`.

  def_start and def_stop values for None start and stop args for cases like:
  ```
    enforce_range(
        previous_vowel_index,
        next_vowel_index,
        def_start=0,
        def_stop=len(word))
  ```

  Returns:
    range
  """

  a3 = 1 if not_specified(arg3) else arg3
  if isinstance(arg1, Tuple):
    if len(arg1) > 3 or (len(arg1) == 3 and is_specified(arg2)):
      return log.dbg_return(
          range(0),
          'too many arguments range(%s)' % log.texts_of(arg1, arg2, arg3)
      )
    log.dbg_message(log.from_class_and_text(arg1))
    e1 = get_element(arg1, 0)
    e2 = get_element(arg1, 1)
    e3 = get_element(arg1, 2)
    a1, a2 = (e1, e2)
    a3 = arg2 if not_found(e3) and exists(arg2) else e3
  else:
    if not_specified(arg2):
      a1, a2 = (0, arg1)
    else:
      a1, a2 = (arg1, arg2)
  if not_exists(a1) and exists(def_start): a1 = def_start
  if not_exists(a2) and exists(def_stop): a2 = def_stop
  if isinstance(a1, int) and isinstance(a2, int):
    if isinstance(a3, int): return range(a1, a2, a3)
    if is_nothing(a3): return range(a1, a2)
  return log.dbg_return(range(0), log.texts_of(arg1, arg2, arg3))


def in_range(
    look_for: ..., arg1: ...,
    arg2: ... = UNSPECIFIED, arg3: ... = UNSPECIFIED,
) -> bool:
  """Checks if look_for is in an enforced range."""
  if not_exists(look_for): return False
  if not_instance(look_for, int): return False
  return look_for in enforce_range(arg1, arg2, arg3)


def enforce_list(
    l: ..., enf_dict: bool = True, allow_none: bool = False
) -> List[Any]:
  """Enforces list type.

  When l is a list, returns l. If l is an iterable returns `list(l)`, except
  for str and dict. For other types returns `[l]`.

  Args:
    l: ... variable.
    enf_dict: When true, if l is a dict returns the list of values.
    allow_none: When false, if l is None returns an empty list. When true,
      returns `[None]`.

  Returns:
    List.
  """
  if isinstance(l, list): return l
  log.dbg_message(log.from_class_and_text(l))
  if enf_dict and isinstance(l, dict): return log.dbg_return(list(l.values()))
  if (
      isinstance(l, Iterable) and
      not_instance(l, str) and not_instance(l, dict)
  ): return log.dbg_return(list(l))
  if not_exists(l, allow_none): return log.dbg_return([])
  return log.dbg_return([l])


def in_list(
    look_for: ..., look_in: ...,
    enf_dict: bool = True, allow_none: bool = False
) -> bool:
  """Checks if look_for is an element of a list enforced from look_in."""
  return look_for in enforce_list(look_in, enf_dict, allow_none)


def enforce_dict(
    d: ..., add_key: ... = 'default', allow_none: bool = False
) -> Dict[Any, Any]:
  """Enforces dict type.

  Args:
    d: ... variable.
      When d is a dict, returns d. Otherwise returns `{add_key: d}`.
    add_key: optional key for adding d as a value to a new list.
    allow_none: When false, if d is a nonexistant type returns an empty dict.
      When true, returns `{add_key: d}`

  Returns:
    Dict.
  """
  if isinstance(d, dict): return d
  log.dbg_message(log.from_class_and_text(d))
  if isinstance(d, Thing): return log.dbg_return(d.__dict__)
  if isinstance(d, Tuple) and hasattr(d, '_fields'):
    return log.dbg_return(d._asdict())
  if not_exists(d, allow_none): return log.dbg_return({})
  return log.dbg_return(
      {add_key: d},
      '{%s: %s}' % (log.text_of(add_key), log.text_of(d))
  )


def dict_get(
    d: ..., key: ... = 'default', default: ... = MISSING,
    add_key: ... = 'default', allow_none: bool = False
) -> ...:
  try:
    return enforce_dict(d, add_key, allow_none).get(key, default)
  except TypeError:
    return log.dbg_return(default, 'invalid key type')


def in_dict(look_for: ..., look_in: ..., keys: ... = UNSPECIFIED) -> bool:
  """Checks if look_for is a value of a dict enforced from look_in.

  If the value of a key is a list, searches the elements of the list.
  Example: `i in {key: i}` and `i in {key: [i, j, k]}` will both return True.

  Args:
    look_for: Item to be checked.
    look_in: Dictionary. If not dict type will be converted to dict.
    keys: If unspecified, will look in the values of all keys of dict.

  Returns:
    bool.
  """
  enforced = enforce_dict(look_in)
  key_list = enforce_list(keys) if is_specified(keys) else list(enforced.keys())
  for k in key_list:
    if in_list(look_for, dict_get(enforced, k)): return True
  return False


def enforce_set(
    s: ..., enf_dict: bool = True, allow_none: bool = False
) -> set[Any]:
  """Enforces set type.

  If s is a set, returns s. If s is iterable returns set(s). Else returns {s}.
  If an object is unhashable, converts it to a Thing whose value is the
  unhashable object.

  Args:
    s: Object to be converted to set.
    enf_dict: When true, returns a set of values of dict. When false, returns
      a set of tuples where the first element is the key and the second is the
      value.
    allow_none: When false, if s is None returns an empty set. When true,
      returns `{None}`.

  Returns:
    Set.
  """
  if isinstance(s, set): return s
  log.dbg_message(log.from_class_and_text(s))
  if not_exists(s, allow_none): return log.dbg_return(set())
  if isinstance(s, str): return log.dbg_return({s})
  if isinstance(s, dict):
    s = set(enforce_list(s)) if enf_dict else {(k, v) for k, v in s.items()}
    return log.dbg_return(s)
  result = set()
  if isinstance(s, Iterable):
    for element in s:
      try:
        result.add(element)
      except TypeError:
        result.add(Thing.from_value_of(element))
  else:
    try:
      result.add(s)
    except TypeError:
      result.add(Thing.from_value_of(s))
  return log.dbg_return(result)


def in_set(
    look_for: ..., look_in: ...,
    enf_dict: bool = True, allow_none: bool = False
) -> bool:
  return look_for in enforce_set(look_in, enf_dict, allow_none)


def in_enforced(
    look_for: ..., look_in: ..., keys: ... = UNSPECIFIED,
    enf_list: bool = True, enf_dict: bool = True, enf_set: bool = True,
    enf_range: bool = False, allow_none: bool = False
) -> bool:
  """Checks if look_for is in enforced type look_in."""
  if not_exists(look_for, allow_none): return False
  if is_specified(keys) and not enf_dict and not_instance(look_in, dict):
    return log.dbg_return_false(
        'key for non-dict argument %s' % log.text_of(look_in)
    )
  if (
      (enf_list and in_list(look_for, look_in)) or
      (enf_dict and in_dict(look_for, look_in, keys)) or
      (enf_range and in_range(look_for, look_in)) or
      (enf_set and in_set(look_for, look_in))
  ): return True
  return False


def in_attribute(
    look_for: ..., thing: ..., attr: str, keys: ... = UNSPECIFIED,
    enf_list: bool = True, enf_dict: bool = True, enf_range: bool = False,
    allow_none: bool = False
) -> bool:
  """Checks if look_for is in an enforced type attribute of thing."""
  return in_enforced(
      look_for, get_attribute(thing, attr),
      keys, enf_list, enf_dict, enf_range, allow_none
  )
