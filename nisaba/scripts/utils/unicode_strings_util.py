# Copyright 2021 Nisaba Authors.
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

"""Utilities for processing Unicode strings from protocol message."""

from typing import List, Tuple, Union

import unicodedata

from nisaba.scripts.utils import unicode_strings_pb2


def _names_to_string(uname_prefix: str, item_index: int,
                     names: List[str]) -> Tuple[str, List[str]]:
  """Converts list of Unicode character names to the corresponding string.

  Args:
    uname_prefix: Character name prefix.
    item_index: Index of the item in the proto (for debugging).
    names: List of Unicode character names.

  Returns:
    Returns a tuple that consists of a string in UTF-8 encoding and a list
    of character names that fully resolve using `uname_prefix`.
  Raises:
    ValueError: If character cannot be converted.
  """
  u_chars: List[str] = []
  resolved_names: List[str] = []
  for name in names:
    prefix_and_name = (uname_prefix + ' ' + name if uname_prefix and
                       not name.startswith(uname_prefix) else name)
    try:
      # As a first attempt at matching, try to match against a full character
      # name including the prefix `uname_prefix` (if set).
      u_char = unicodedata.lookup(prefix_and_name)
      resolved_names.append(prefix_and_name)
    except KeyError as exc:
      if not uname_prefix:  # Nothing we can do. Pass the exception on.
        raise ValueError('Item %d: Lookup failed: \'%s\'' % (
            item_index, prefix_and_name)) from exc
      # Attempt to match the second time, without a script name.
      try:
        u_char = unicodedata.lookup(name)
        resolved_names.append(name)
      except KeyError as exc:
        raise ValueError('Item %d: Cannot convert \'%s\'' % (
            item_index, name)) from exc
    u_chars.append(u_char)
  return ''.join(u_chars), resolved_names


def proto_entries_to_string(uname_prefix: str, item_index: int,
                            uname: List[str], raw: str) -> str:
  """Computes string from either Unicode names or codepoint sequence.

  Given unicode names and/or raw Unicode codepoint sequence specification
  computes the final string.

  Args:
     uname_prefix: Character name prefix.
     item_index: Index of the item in the proto (for debugging).
     uname: List of Unicode character name strings, possibly empty.
     raw: Raw string, possibly empty.

  Raises:
    ValueError: If parsing fails.
  Returns:
    Final raw string.
  """
  if raw and not uname:
    return raw

  test_str: str = None
  if uname and raw:
    # Use the raw string as a sanity check to compare with the values in uname.
    test_str = raw

  source_str, char_names = _names_to_string(uname_prefix, item_index, uname)
  if test_str and source_str != test_str:
    # Name lookup may throw ValueError as well.
    test_names = [unicodedata.name(c) for c in test_str]
    raise ValueError('Item %d: Names in `uname` (%s) mismatch the contents '
                     'of the `raw` field (%s)' % (
                         item_index, char_names, test_names))
  return source_str


def convert_item(
    uname_prefix: str,
    to_uname_prefix: str,
    item_index: int,
    data_item: unicode_strings_pb2.UnicodeStrings.Item) -> Tuple[
        str, Union[str, None]]:
  """Converts individual item into source and destination strings.

  Args:
     uname_prefix: Character name prefix.
     to_uname_prefix: Character name prefix for those in `to_uname` field.
     item_index: Index of the item in the proto (for debugging).
     data_item: An item message in the data proto.

  Returns:
     A tuple of source and destination strings. The latter can be None if
     destination is not defined.
  Raises:
    ValueError: If parsing fails.
  """
  # We always expect the list item portion to be defined.
  if not data_item.uname and not data_item.raw:
    raise ValueError('Item %d: Either \'raw\' or \'uname\' have to be defined' %
                     item_index)

  source_str = proto_entries_to_string(uname_prefix, item_index,
                                       list(data_item.uname), data_item.raw)
  # Check if item defines a mapping.
  if not data_item.to_uname and not data_item.to_raw:
    return source_str, None
  if not to_uname_prefix:
    to_uname_prefix = uname_prefix
  dest_str = proto_entries_to_string(to_uname_prefix, item_index,
                                     list(data_item.to_uname), data_item.to_raw)
  return source_str, dest_str
