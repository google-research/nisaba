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

from typing import List, Sequence, Tuple, Union

import unicodedata

from nisaba.scripts.utils import unicode_strings_pb2


class NoMatchError(ValueError):
  pass


class MultipleMatchesError(ValueError):
  pass


def name_to_char(prefixes: Sequence[str], suffix: str) -> Tuple[str, str]:
  """Converts a Unicode character name to the corresponding character string.

  Args:
    prefixes: Character name prefixes
    suffix: Unicode character name suffix.

  Returns:
    Returns a tuple that consists of a character in UTF-8 encoding and the
    character name that fully resolve using `uname_prefixes`.

  Raises:
    MultipleMatchesError: When multiple character names match the prefix and
    suffix.
    NoMatchError: When no character name matches the prefix and suffix.
  """

  char_names = []
  for prefix in list(prefixes) + ['']:
    uname = (prefix + ' ' + suffix).lstrip()
    try:
      char = unicodedata.lookup(uname)
      if unicodedata.category(char) != 'Cc':
        char_names.append((char, uname))
    except KeyError:
      pass
  if not char_names:
    raise NoMatchError(f'`{suffix}` does not match a character name '
                       f'with the prefix(es): `{prefixes}`')
  if len(char_names) > 1:
    raise MultipleMatchesError(
        f'With prefix(es) `{prefixes}`, suffix `{suffix}` '
        f'resolves to more than one character: `{char_names}`.')
  return char_names[0]


def _names_to_string(uname_prefixes: Sequence[str], names: Sequence[str]
                     ) -> Tuple[str, List[str]]:
  """Converts list of Unicode character names to the corresponding string.

  Args:
    uname_prefixes: Character name prefixes.
    names: List of Unicode character names.

  Returns:
    Returns a tuple that consists of a string in UTF-8 encoding and a list
    of character names that fully resolve using `uname_prefixes`.
  Raises:
    ValueError: If character cannot be converted.
  """
  u_chars, resolved_names = zip(*(name_to_char(uname_prefixes, name)
                                  for name in names))
  return ''.join(u_chars), resolved_names


def proto_entries_to_string(uname_prefixes: Sequence[str], item_index: int,
                            uname: Sequence[str], raw: str) -> str:
  """Computes string from either Unicode names or codepoint sequence.

  Given unicode names and/or raw Unicode codepoint sequence specification
  computes the final string.

  Args:
     uname_prefixes: Character name prefixes.
     item_index: Index of the item in the proto (for debugging).
     uname: List of Unicode character name strings, possibly empty.
     raw: Raw string, possibly empty.

  Raises:
    ValueError: If parsing fails.
  Returns:
    Final raw string. None if uname does not match any character, while no raw
    field is specified for comparision.
  """
  if raw and not uname:
    return raw

  test_str: str = None
  if uname and raw:
    # Use the raw string as a sanity check to compare with the values in uname.
    test_str = raw

  source_str: str = None
  try:
    source_str, char_names = _names_to_string(uname_prefixes, uname)
  except ValueError as exc:
    if test_str or isinstance(exc, MultipleMatchesError):
      raise ValueError(f'Lookup failed: item #{item_index}') from exc

  if test_str and source_str != test_str:
    # Name lookup may throw ValueError as well.
    test_names = [unicodedata.name(c) for c in test_str]
    raise ValueError('Item %d: Names in `uname` (%s) mismatch the contents '
                     'of the `raw` field (%s)' % (
                         item_index, char_names, test_names))
  return source_str


def convert_item(
    uname_prefixes: Sequence[str],
    to_uname_prefixes: Sequence[str],
    item_index: int,
    data_item: unicode_strings_pb2.UnicodeStrings.Item) -> Tuple[
        str, Union[str, None]]:
  """Converts individual item into source and destination strings.

  Args:
     uname_prefixes: Character name prefixes.
     to_uname_prefixes: Character name prefixes for those in `to_uname` field.
     item_index: Index of the item in the proto (for debugging).
     data_item: An item message in the data proto.

  Returns:
     A tuple of source and destination strings. The latter can be None if
     destination is not defined. Source can be None if name does not match any
     character; but no raw specified for comparision.
  Raises:
    ValueError: If parsing fails.
  """
  # We always expect the list item portion to be defined.
  if not data_item.uname and not data_item.raw:
    raise ValueError('Item %d: Either \'raw\' or \'uname\' have to be defined' %
                     item_index)

  source_str = proto_entries_to_string(uname_prefixes, item_index,
                                       list(data_item.uname), data_item.raw)
  # Check if item defines a mapping.
  if not data_item.to_uname and not data_item.to_raw:
    return source_str, None
  if not to_uname_prefixes:
    to_uname_prefixes = uname_prefixes
  dest_str = proto_entries_to_string(to_uname_prefixes, item_index,
                                     list(data_item.to_uname), data_item.to_raw)
  return source_str, dest_str
