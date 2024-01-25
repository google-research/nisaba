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

"""Utilities for processing LetterLanguages proto."""

import logging
import os
from typing import Union
from nisaba.scripts.utils import letter_languages_pb2 as ll
from nisaba.scripts.utils import proto
from nisaba.scripts.utils import unicode_strings_util as us


def _fill_missing_raw(pb: ll.LetterLanguages) -> None:
  """Fill `raw` fields of the `item.letter`, if they are missing.

  Invisible characters like ZWJ and combining marks like FATHA cannot be
  reliably displayed in isolation or with Latin punctuation like quotes. So they
  can be omitted from a text proto, in those cases. However, when the text
  proto is parsed into Python data structure, it is useful to have the raw
  field present for every `item.letter`, for downstream processing. This routine
  fills `raw` field from the `uname` field, if missing.

  Args:
    pb: LetterLanguages proto buffer to be updated in place.
  Returns:
    None
  """
  for item in pb.item:
    item.letter.raw, _ = us.convert_item(pb.uname_prefix, [], item.letter)


def read_textproto(proto_path: Union[str, os.PathLike]) -> ll.LetterLanguages:
  pb = proto.read_textproto(proto_path, ll.LetterLanguages())
  _fill_missing_raw(pb)
  logging.info('Read %d letters.', len(pb.item))
  return pb
