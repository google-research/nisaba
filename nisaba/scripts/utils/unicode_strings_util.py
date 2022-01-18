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

"""Utilities for processing Unicode strings from protocol message."""

import logging
from typing import List, Sequence, Tuple, Union

import unicodedata

from nisaba.scripts.utils import proto
from nisaba.scripts.utils import unicode_strings_pb2


def name_to_char(prefixes: Sequence[str], suffix: str) -> Tuple[str, str]:
  """Converts a Unicode character name to the corresponding character string.

  Args:
    prefixes: Character name prefixes
    suffix: Unicode character name suffix.

  Returns:
    Returns a tuple that consists of a character in UTF-8 encoding and the
    character name that fully resolve using `uname_prefixes`.
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
    raise ValueError(f'`{suffix}` does not match a character name '
                     f'with the prefix(es): `{prefixes}`')
  if len(char_names) > 1:
    raise ValueError(f'With prefix(es) `{prefixes}`, suffix `{suffix}` '
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


def proto_entries_to_string(uname_prefixes: Sequence[str],
                            uname: Sequence[str], raw: str) -> str:
  """Computes string from either Unicode names or codepoint sequence.

  Given unicode names and/or raw Unicode codepoint sequence specification
  computes the final string.

  Args:
     uname_prefixes: Character name prefixes.
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

  source_str, char_names = _names_to_string(uname_prefixes, uname)

  if test_str and source_str != test_str:
    # Name lookup may throw ValueError as well.
    test_names = [unicodedata.name(c) for c in test_str]
    raise ValueError('`uname` field (%s) mismatch names of the characters '
                     'in the `raw` field (%s)' % (char_names, test_names))
  return source_str


def convert_item(
    uname_prefixes: Sequence[str],
    to_uname_prefixes: Sequence[str],
    data_item: unicode_strings_pb2.UnicodeStrings.Item) -> Tuple[
        str, Union[str, None]]:
  """Converts individual item into source and destination strings.

  Args:
     uname_prefixes: Character name prefixes.
     to_uname_prefixes: Character name prefixes for those in `to_uname` field.
     data_item: An item message in the data proto.

  Returns:
     A tuple of source and destination strings. The latter can be None if
     destination is not defined.
  Raises:
    ValueError: If parsing fails.
  """
  # We always expect the list item portion to be defined.
  if not data_item.uname and not data_item.raw:
    raise ValueError('Either \'raw\' or \'uname\' have to be defined')

  # Make sure the lists of Unicode prefixes contain unique elements.
  uname_prefixes = list(set(uname_prefixes))
  to_uname_prefixes = list(set(to_uname_prefixes))

  source_str = proto_entries_to_string(
      uname_prefixes, list(data_item.uname), data_item.raw)
  # Check if item defines a mapping.
  if not data_item.to_uname and not data_item.to_raw:
    return source_str, None
  if not to_uname_prefixes:
    to_uname_prefixes = uname_prefixes
  dest_str = proto_entries_to_string(
      to_uname_prefixes, list(data_item.to_uname), data_item.to_raw)
  return source_str, dest_str


def _fill_missing_raw(pb: unicode_strings_pb2.UnicodeStrings):
  """Fills `raw` and `to_raw` fields of the `item`s, if they are missing.

  Invisible characters like ZWJ and combining marks like FATHA cannot be
  reliably displayed in isolation or with Latin punctuation like quotes. So they
  can be omitted from a text proto, in those cases. However, when the text
  proto is parsed into Python data structure, it is useful to have the raw
  fields present for every item, for downstream processing. This routine fills
  `raw` fields from the `uname` fields, if missing.

  Args:
    pb: UnicodeStrings proto buffer to be updated in place.
  Returns:
    None
  """
  for item in pb.item:
    item.raw, item.to_raw = convert_item(
        pb.uname_prefix, pb.to_uname_prefix, item)


def read_textproto(proto_path):
  pb = proto.read_textproto(proto_path, unicode_strings_pb2.UnicodeStrings())
  _fill_missing_raw(pb)
  logging.info('Read %d items.', len(pb.item))
  return pb
