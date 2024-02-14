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

r"""Converts the data file in `UnicodeStrings` textual proto to TSV format.

Example:
--------
  > bazel-bin/nisaba/scripts/utils/unicode_strings_to_tsv \
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

from typing import Sequence

from absl import app
from absl import flags
from absl import logging
from google.protobuf import text_format
from nisaba.scripts.utils import unicode_strings_pb2
from nisaba.scripts.utils import unicode_strings_util as lib

_INPUT = flags.DEFINE_string(
    'input_text_proto', None,
    ('Input proto file in textual format corresponding to '
     '`nisaba.UnicodeStrings` protocol buffer message.'))

_OUTPUT = flags.DEFINE_string(
    'output_tsv', None,
    ('Output file in tab-separated (tsv) format ready for consumption by '
     'Pynini/Thrax grammars.'))

flags.mark_flag_as_required('input_text_proto')
flags.mark_flag_as_required('output_tsv')


def _convert_data_proto_to_file(data_proto: unicode_strings_pb2.UnicodeStrings):
  """Converts proto message in `UnicodeStrings` format to TSV file.

  Args:
    data_proto: An input script data protocol message.

  Raises:
    ValueError: If we are unable to parse the proto.
  """
  # TODO: Disallow duplicate items.
  with open(_OUTPUT.value, mode='w', encoding='utf8') as output_file:
    output_file.write(
        "# Auto-generated using 'nisaba/scripts/utils/unicode_strings_to_tsv'\n"
    )
    for index, item in enumerate(data_proto.item):
      try:
        source_str, dest_str = lib.convert_item(
            list(data_proto.uname_prefix), list(data_proto.to_uname_prefix),
            item)
      except ValueError as e:
        msg = f'Lookup failed: item #{index}'
        raise ValueError(msg).with_traceback(e.__traceback__)

      if dest_str:
        output_file.write('%s\t%s\n' % (source_str, dest_str))
      else:
        output_file.write('%s\n' % source_str)


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  logging.info('Parsing %s ...', _INPUT.value)
  data_proto = unicode_strings_pb2.UnicodeStrings()
  with open(_INPUT.value, encoding='utf8') as input_file:
    text_format.Parse(input_file.read(), data_proto)
  _convert_data_proto_to_file(data_proto)


if __name__ == '__main__':
  app.run(main)
