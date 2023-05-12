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

"""

import logging
import numbers
from typing import Dict, Iterable, List, NamedTuple, Tuple, Union
import pynini as pyn

# Custom types


class Thing(object):
  """Parent class for various custom classes.

  Attributes:
    alias: A string that will be used to refer to this object. An alias should
      be unique in a given context. Eg, every phoneme in an inventory or every
      token in a lexicon should have a unique alias.
    text: A string that represents the surface form of the object. eg. bass_fish
      and bass_instrument in an English lexicon can have the same text 'bass'.
  """

  def __init__(self, alias: str = '', text: str = ''):
    self.alias = alias
    self.text = text

# Constants for undefined Thing objects.
UNASSIGNED = Thing(text='Unassigned')  # Unassigned variable.
UNSPECIFIED = Thing(text='Unspecified')  # Unspecified optional argument.
MISSING = Thing(text='Missing')  # Searched object is not found.

# Union types

# FstLike from pynini doesn't work in isinstance()
FstLike = Union[str, pyn.Fst]
Catalog = Union[Dict, List, NamedTuple]
# Restricted generic class to avoid using Any type.
Valid = Union[None, range, Thing, Catalog, numbers.Number, Tuple, FstLike]

# Log functions


def debug_message(function_name: str, message: str = '') -> None:
  return logging.debug('%s: %s', function_name, message)


def debug_result(function_name: str, result: Valid, detail: str = '') -> None:
  message = 'returns %s' % text_of(result)
  if detail: message += ', ' + detail
  return debug_message(function_name, message)


def debug_true(function_name: str, detail: str = '') -> None:
  return debug_result(function_name, True, detail)


def debug_false(function_name: str, detail: str = '') -> None:
  return debug_result(function_name, False, detail)


def class_of(a: Valid) -> str:
  return a.__class__.__name__


def texts_of(*args) -> str:
  return ' ,'.join([text_of(a) for a in args])

# Type check.


def is_none(a: Valid) -> bool:
  """Checks None for logging purposes."""
  if a is None:
    debug_true('is_none')
    return True
  debug_false('is_none', '%s is %s' % (text_of(a), class_of(a)))
  return False


def not_none(a: Valid) -> bool:
  return not is_none(a)


def is_assigned(a: Valid) -> bool:
  """Checks UNASSIGNED for logging purposes."""
  if a is UNASSIGNED:
    debug_false('is_assigned')
    return False
  debug_true('is_assigned', text_of(a))
  return True


def not_assigned(a: Valid) -> bool:
  return not is_assigned(a)


def is_specified(a: Valid) -> bool:
  """Checks UNSPECIFIED for logging purposes."""
  if a is UNSPECIFIED:
    debug_false('is_specified')
    return False
  debug_true('is_specified', text_of(a))
  return True


def not_specified(a: Valid) -> bool:
  return not is_specified(a)


def is_found(a: Valid) -> bool:
  """Checks MISSING for logging purposes."""
  if a is MISSING:
    debug_false('is_found')
    return False
  debug_true('is_found', text_of(a))
  return True


def not_found(a: Valid) -> bool:
  return not is_found(a)


def is_nothing(a: Valid) -> bool:
  """Checks default Thing constants."""
  return not_assigned(a) or not_specified(a) or not_found(a)


def not_nothing(a: Valid) -> bool:
  return not is_nothing(a)


def exists(a: Valid) -> bool:
  """Combines checking for None and undefined Things."""
  return not_none(a) and not_nothing(a)


def not_exists(a: Valid) -> bool:
  return not exists(a)


def is_instance(a: Valid, want: Valid = UNSPECIFIED) -> bool:
  """Checks instance for logging purposes.

  Args:
    a: Object
    want: Type. Default value is UNSPECIFIED to make type check optional in
      functions that call is_instance, while the case of optional argument
      and specifically checking for Null type as distinct cases.

  Returns:
    bool

  """
  if not_specified(want):
    debug_true('is_instance', 'type check not requested for %s' % text_of(a))
    return True
  try:
    if isinstance(a, want):
      return True
    else:
      debug_false('is_instance', '%s not %s' % (text_of(a), want.__name__))
  except TypeError:
    debug_false('is_instance', 'invalid type')
  return False


def not_instance(a: Valid, want: Valid = UNSPECIFIED) -> bool:
  return not is_instance(a, want)

# Attribute functions with type check.


def has_attribute(a: Valid, attr: str, want: Valid = UNSPECIFIED) -> bool:
  """Adds log and optional type check to hasattr()."""
  if not_exists(a): return False
  if not hasattr(a, attr):
    debug_false(
        'has_attribute', '%s not an attribute of %s' % (attr, text_of(a))
    )
    return False
  return is_instance(getattr(a, attr), want)


def get_attribute(
    a: Valid, attr: str, default: Valid = MISSING, want: Valid = UNSPECIFIED
) -> Valid:
  """Adds log and type check to getattr()."""
  return getattr(a, attr) if has_attribute(a, attr, want) else default

# Handle common attributes for objects of unknown types.


def text_of(a: Valid) -> str:
  """Returns str() for objects with no text attribute."""
  if hasattr(a, 'text'):
    if is_empty(a.text): return 'Textless %s' % class_of(a)
    return a.text
  if isinstance(a, pyn.Fst): return a.string()
  return str(a)


def alias_of(a: Valid) -> str:
  """Returns text_of() for logging objects with no alias."""
  if has_attribute(a, 'alias') and not_empty(a.alias):
    return a.alias
  return text_of(a)

# Equivalence functions.


def is_equal(
    a: Valid, b: Valid,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  """Checks equivalence.

  Never equates None, logs other 'not a' conditions.
  Never equates UNASSIGNED, UNSPECIFIED or MISSING.

  Args:
    a: Object for comparison.
    b: Object for comparison
    empty: When false, empty str, list and dict are not considered equal.
    epsilon: When false, epsilon fsts are not considered equal.
    zero: When false, zero is not considered equal.

  Returns:
    bool

  """
  # Check Fst first, otherwise if Fst == Non-FstLike raises error.
  name = 'is_equal'
  if isinstance(a, pyn.Fst) or isinstance(b, pyn.Fst):
    if not_instance(b, FstLike) or not_instance(a, FstLike):
      debug_false(name, 'type mismatch %s' % texts_of(a, b))
      return False
    if a != b: return False
    if not epsilon and a == pyn.accep(''):
      debug_false(name, 'epsilon fst')
      return False
  if a != b:
    if not_instance(a, type(b)):
      debug_false(name, 'type mismatch %s' % texts_of(a, b))
    return False
  if (
      not_exists(a) or (not zero and a == 0) or (not empty and is_empty(a))
  ):
    debug_false(name, text_of(a))
    return False
  return True


def not_equal(
    a: Valid, b: Valid,
    empty: bool = False, epsilon: bool = False, zero: bool = True
) -> bool:
  return not is_equal(a, b, empty, epsilon, zero)

# Iterable functions


def is_empty(a: Valid) -> bool:
  if not_exists(a): return True
  return is_instance(a, Iterable) and not_instance(a, range) and not a


def not_empty(a: Valid) -> bool:
  return not is_empty(a)


def get_element(
    search_in: Valid, index: int, default: Valid = MISSING
    ) -> bool:
  """Returns a[index] if possible, default value if not."""
  if not_exists(search_in): return default
  if not_instance(search_in, Iterable): return default
  try:
    return search_in[index]
  except IndexError:
    debug_result('get_element', text_of(default), 'index error')
    return default


def enforce_range(
    arg1: Valid, arg2: Valid = UNSPECIFIED, arg3: Valid = UNSPECIFIED,
    def_start: Valid = UNSPECIFIED, def_stop: Valid = UNSPECIFIED,
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

  name = 'enforce_range'
  a3 = 1 if not_specified(arg3) else arg3
  if isinstance(arg1, Tuple):
    if len(arg1) > 3 or (len(arg1) == 3 and is_specified(arg2)):
      debug_result(
          name, range(0),
          'too many arguments range(%s)' % texts_of(arg1, arg2, arg3)
      )
      return range(0)
    debug_message(name, 'range from tuple %s' % text_of(arg1))
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
  debug_result(name, range(0), 'from %s' % texts_of(arg1, arg2, arg3))
  return range(0)


def in_range(
    look_for: Valid, arg1: Valid,
    arg2: Valid = UNSPECIFIED, arg3: Valid = UNSPECIFIED,
) -> bool:
  """Checks if look_for is in an enforced range."""
  if not_exists(look_for): return False
  if not_instance(look_for, int): return False
  return look_for in enforce_range(arg1, arg2, arg3)


def enforce_list(
    l: Valid, enf_dict: bool = True, nonexistent: bool = False
) -> [Valid]:
  """Enforces list type.

  When l is a list, returns l. If l is an iterable returns `list(l)`, except
  for str and dict. For other types returns `[l]`.

  Args:
    l: Valid variable.
    enf_dict: When true, if l is a dict returns the list of values.
    nonexistent: When false, if l is None returns an empty list. When true,
      returns `[None]`.

  Returns:
    List.
  """
  name = 'enforce_list'
  if isinstance(l, list): return l
  if enf_dict and isinstance(l, dict):
    debug_message(name, 'list of dict values')
    return list(l.values())
  if (
      isinstance(l, Iterable) and
      not_instance(l, str) and not_instance(l, dict)
  ):
    debug_message(name, 'list(%s)' % text_of(l))
    return list(l)
  if not nonexistent and not_exists(l):
    debug_message(name, 'empty list from %s' % text_of(l))
    return []
  debug_result(name, '[%s]' % text_of(l))
  return [l]


def in_list(
    look_for: Valid, look_in: Valid,
    enf_dict: bool = True, nonexistent: bool = False
) -> bool:
  """Checks if look_for is an element of a list enforced from look_in."""
  return look_for in enforce_list(look_in, enf_dict, nonexistent)


def enforce_dict(
    d: Valid, add_key: Valid = 'default', nonexistent: bool = False
) -> dict[Valid, []]:
  """Enforces dict type.

  Args:
    d: Valid variable.
      When d is a dict, returns d. Otherwise returns `{add_key: d}`.
    add_key: optional key for adding d as a value to a new list.
    nonexistent: When false, if d is a nonexistant type returns an empty dict.
      When true, returns `{add_key: d}`

  Returns:
    Dict.
  """
  name = 'enforce_dict'
  if isinstance(d, dict): return d
  if isinstance(d, Thing):
    debug_message(name, 'dict from %s' % class_of(d))
    return d.__dict__
  if isinstance(d, Tuple) and hasattr(d, '_fields'):
    debug_message(name, 'dict from namedtuple')
    return d._asdict()
  if not nonexistent and not_exists(d):
    debug_message(name, 'empty dict from none')
    return {}
  debug_message(name, '{%s: %s}' % (text_of(add_key), text_of(d)))
  return {add_key: d}


def dict_get(
    d: Valid, key: Valid = 'default', default: Valid = MISSING,
    add_key: Valid = 'default', nonexistent: bool = False
) -> Valid:
  try:
    return enforce_dict(d, add_key, nonexistent).get(key, default)
  except TypeError:
    debug_result('dict_get', default, 'invalid key type')
    return default


def in_dict(look_for: Valid, look_in: Valid, keys: Valid = UNSPECIFIED) -> bool:
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


def in_enforced(
    look_for: Valid, look_in: Valid, keys: Valid = UNSPECIFIED,
    enf_list: bool = True, enf_dict: bool = True, enf_range: bool = False,
    nonexistent: bool = False
) -> bool:
  """Checks if look_for is in enforced type look_in."""
  if not nonexistent and not_exists(look_for): return False
  if is_specified(keys) and not enf_dict and not_instance(look_in, dict):
    debug_false(
        'in_enforced', 'key for non-dict argument %s' % text_of(look_in)
    )
    return False
  if (
      (enf_list and in_list(look_for, look_in)) or
      (enf_dict and in_dict(look_for, look_in, keys)) or
      (enf_range and in_range(look_for, look_in))
  ): return True
  return False


def in_attribute(
    look_for: Valid, thing: Valid, attr: str, keys: Valid = UNSPECIFIED,
    enf_list: bool = True, enf_dict: bool = True, enf_range: bool = False,
    nonexistent: bool = False
) -> bool:
  """Checks if look_for is in an enforced type attribute of thing."""
  return in_enforced(
      look_for, get_attribute(thing, attr),
      keys, enf_list, enf_dict, enf_range, nonexistent
  )
