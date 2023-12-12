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

# -*- coding: utf-8 -*-
r"""Calculate Earth movers distance.
"""

import io
import json
import re

from absl import app
from absl import flags

import numpy as np
import pyemd
from nisaba.translit.tools import emd_cer

FLAGS = flags.FLAGS
flags.DEFINE_string('json_path', '', 'Input file')

def main(unused_argv):
  parsed_json = []
  TotEdits = 0
  TotLen = 0
  with io.open(FLAGS.json_path, mode='r',
               encoding='UTF-8', closefd=True) as data_json:
    parsed_json.extend([json.loads(line) for line in data_json.readlines()])
    for jline in parsed_json:
      [Edits, RefLen] = emd_cer.emd_error_and_length(jline)
      # We don't separate subst/ins/del, hence the two zero columns in output.
      print(str(RefLen) + '\t' + str(Edits) + '\t0\t0\t' + str(Edits/RefLen))
      TotEdits += Edits
      TotLen += RefLen
  print('Total edits:\t' + str(TotEdits))
  print('Total reference length:\t' + str(TotLen))
  print('Overall CER:\t' + str(TotEdits/TotLen))

if __name__ == '__main__':
  app.run(main)
