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

r"""Converts the data file in `UnicodeStrings` textual proto to TSV format.

Example:
--------
  > bazel-bin/nisaba/utils/unicode_strings_to_tsv \
    --input_text_proto input.textproto --output_tsv output.tsv
  > cat input.textproto
      uname_prefix: "MEETEI MAYEK"
      item { uname: "LETTER UN" }    to_raw: "u"
      item { uname: "LETTER I"  }    to_raw: "i"
      item { uname: "LETTER ATIYA" } to_raw: "a"
      item { uname: ["LETTER MIT", "LETTER SAM"] }
  > cat output.tsv
      ꯎ   u
      ꯏ   i
      ꯑ   a
      ꯃꯁ
"""

import sys
from typing import List, Sequence, Tuple, Union
import unicodedata

from absl import app
from absl import flags
from absl import logging
from google.protobuf import text_format
from nisaba.utils import unicode_strings_pb2

flags.DEFINE_string(
    'input_text_proto', None,
    ('Input proto file in textual format corresponding to '
     '`nisaba.UnicodeStrings` protocol buffer message.'))

flags.DEFINE_string(
    'output_tsv', None,
    ('Output file in tab-separated (tsv) format ready for consumption by '
     'Pynini/Thrax grammars.'))

flags.mark_flag_as_required('input_text_proto')
flags.mark_flag_as_required('output_tsv')

FLAGS = flags.FLAGS


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


def _proto_entries_to_string(uname_prefix: str, item_index: int,
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


def _convert_item(
    uname_prefix: str, item_index: int,
    data_item: unicode_strings_pb2.UnicodeStrings.Item) -> Tuple[
        str, Union[str, None]]:
  """Converts individual item into source and destination strings.

  Args:
     uname_prefix: Character name prefix.
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

  source_str = _proto_entries_to_string(uname_prefix, item_index,
                                        list(data_item.uname), data_item.raw)
  # Check if item defines a mapping.
  if not data_item.to_uname and not data_item.to_raw:
    return source_str, None
  dest_str = _proto_entries_to_string(uname_prefix, item_index,
                                      list(data_item.to_uname),
                                      data_item.to_raw)
  return source_str, dest_str


def _convert_data_proto_to_file(data_proto: unicode_strings_pb2.UnicodeStrings):
  """Converts proto message in `UnicodeStrings` format to TSV file.

  Args:
    data_proto: An input script data protocol message.

  Raises:
    ValueError: If we are unable to parse the proto.
  """
  # TODO: Disallow duplicate items.
  with open(FLAGS.output_tsv, mode='w', encoding='utf8') as output_file:
    output_file.write('# Auto-generated using \'%s\'\n' % sys.argv[0])
    for index, item in enumerate(data_proto.item):
      source_str, dest_str = _convert_item(data_proto.uname_prefix,
                                           index, item)
      if dest_str:
        output_file.write('%s\t%s\n' % (source_str, dest_str))
      else:
        output_file.write('%s\n' % source_str)


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  logging.info('Parsing %s ...', FLAGS.input_text_proto)
  data_proto = unicode_strings_pb2.UnicodeStrings()
  with open(FLAGS.input_text_proto, encoding='utf8') as input_file:
    text_format.Parse(input_file.read(), data_proto)
  _convert_data_proto_to_file(data_proto)


if __name__ == '__main__':
  app.run(main)
