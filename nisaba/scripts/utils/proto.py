# Copyright 2025 Nisaba Authors.
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

"""Utility function for reading text protos."""

import logging
import os
from typing import TypeVar, Union

from google.protobuf import message
from google.protobuf import text_format
import nisaba.scripts.utils.file as uf

_ParsableT = TypeVar(
    '_ParsableT',
    bound=message.Message,
)


def read_textproto(
    proto_path: Union[str, os.PathLike[str]], proto: _ParsableT
) -> _ParsableT:
  logging.info('Parsing %s ...', proto_path)
  if not os.path.exists(proto_path):
    proto_path = uf.AsResourcePath(proto_path)
  with open(proto_path, encoding='utf8') as f:
    text_format.Parse(f.read(), proto)
  return proto
