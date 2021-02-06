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
      uchar_name_prefix: "MEETEI MAYEK"
      item { src { uname: "LETTER UN" }    dst_raw: "u"
      item { src { uname: "LETTER I"  }    dst_raw: "i"
      item { src { uname: "LETTER ATIYA" } dst_raw: "a"
      item { uname: ["LETTER MIT", "LETTER SAM"] }
  > cat output.tsv
      ꯎ   u
      ꯏ   i
      ꯑ   a
      ꯃꯁ
"""

from typing import List, Sequence
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


def _names_to_string(uchar_name_prefix: str, item_index: int,
                     names: List[str]) -> str:
  """Converts list of Unicode character names to the corresponding string.

  Args:
    uchar_name_prefix: Character name prefix.
    item_index: Index of the item in the proto (for debugging).
    names: List of Unicode character names.

  Returns:
    String in UTF-8 encoding.
  Raises:
    ValueError: If character cannot be converted.
  """
  u_chars: List[str] = []
  for name in names:
    prefix_and_name = (uchar_name_prefix + ' ' + name if uchar_name_prefix and
                       not name.startswith(uchar_name_prefix) else name)
    try:
      # As a first attempt at matching, try to match against a full character
      # name including the prefix `uchar_name_prefix` (if set).
      u_char = unicodedata.lookup(prefix_and_name)
    except KeyError as exc:
      if not uchar_name_prefix:  # Nothing we can do. Pass the exception on.
        raise
      # Attempt to match the second time, without a script name.
      try:
        u_char = unicodedata.lookup(name)
      except KeyError as exc:
        raise ValueError('Item %d: Cannot convert \'%s\'' % (
            item_index, name)) from exc
    if not u_char:
      raise ValueError('Item %d: Empty char for \'%s\'' % (item_index, name))
    u_chars.append(u_char)
  return ''.join(u_chars)


def _convert_item(uchar_name_prefix: str, item_index: int,
                  data_item: unicode_strings_pb2.UnicodeStrings.Item):
  """Converts individual item into source and destination strings.

  Args:
     uchar_name_prefix: Character name prefix.
     item_index: Index of the item in the proto (for debugging).
     data_item: An item message in the data proto.

  Returns:
     A tuple of source and destination strings. The latter can be None if
     destination is not defined.
  Raises:
    ValueError: If parsing fails.
  """
  # Check if this item belongs to a list.
  if len(data_item.uname) or data_item.raw:
    if len(data_item.uname) and data_item.raw:
      raise ValueError('Item %d: Cannot have both \'raw\' and \'uname\' '
                       'defined for a list' % item_index)
    if (data_item.HasField('src_raw') or data_item.HasField('src') or
        data_item.HasField('dst_raw') or data_item.HasField('dst')):
      # Make sure we disallow defining items for lists and mappings in the same
      # item.
      raise ValueError('Item %d: Encountered both list and mapping '
                       'definitions' % item_index)
    if data_item.raw:
      source_str = data_item.raw
    else:
      source_str = _names_to_string(uchar_name_prefix, item_index,
                                    list(data_item.uname))
    return source_str, None

  # Otherwise, assume an item defines a mapping.
  if data_item.HasField('src_raw'):
    source_str = data_item.src_raw
  elif data_item.HasField('src'):
    source_str = _names_to_string(uchar_name_prefix, item_index,
                                  list(data_item.src.uname))
  else:
    raise ValueError('Item %d: \'src_raw\' or \'src_uname\' is mandatory' %
                     item_index)

  dest_str = None
  if data_item.HasField('dst_raw'):
    dest_str = data_item.dst_raw
  elif data_item.HasField('dst'):
    dest_str = _names_to_string(uchar_name_prefix, item_index,
                                list(data_item.dst.uname))
  return source_str, dest_str


def _convert_data_proto_to_file(data_proto: unicode_strings_pb2.UnicodeStrings):
  """Converts proto message in `UnicodeStrings` format to TSV file.

  Args:
    data_proto: An input script data protocol message.

  Raises:
    ValueError: If we are unable to parse the proto.
  """
  with open(FLAGS.output_tsv, mode='w', encoding='utf8') as output_file:
    for index, item in enumerate(data_proto.item):
      source_str, dest_str = _convert_item(data_proto.uchar_name_prefix,
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