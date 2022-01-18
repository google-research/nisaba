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

"""Utility function for reading text protos."""

import logging
import os
from google.protobuf import text_format
import nisaba.scripts.utils.file as uf


def read_textproto(proto_path, proto):
  logging.info('Parsing %s ...', proto_path)
  if not os.path.exists(proto_path):
    proto_path = uf.AsResourcePath(proto_path)
  with open(proto_path, encoding='utf8') as f:
    text_format.Parse(f.read(), proto)
  logging.info('Read %d items.', len(proto.item))
  return proto
