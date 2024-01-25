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

# Lint as: python3
"""Common rewrite functions."""

import pynini as pyn
from nisaba.scripts.natural_translit.utils import alignment as al


def repeat(sym: pyn.FstLike) -> pyn.FstLike:
  return sym + sym


def concat_r(
    right_1: pyn.FstLike,
    right_2: pyn.FstLike) -> pyn.Fst:
  """Concatanate right side symbols across multiple alignments.

  Current number of args is 2, but will be increased as needed.

  Args:
    right_1: First right side.
    right_2: Second right side.

  Returns:
    Rewrite fst.

  Following call:
  ```
  concat_r(ph.A, ph.B)
  ```
  will return:
  ```
  pyn.union(
      '{a}{b}',
      '{a}gr.GRAPHEMES{b}',
      ...
  )
  ```
  """
  return right_1 + al.SKIP_LEFT_SIDE.ques + right_2


def concat_l(
    left_1: pyn.FstLike,
    left_2: pyn.FstLike) -> pyn.Fst:
  """Concatanate left side symbols across multiple alignments.

  Current number of args is 2, but will be increased as needed.

  Args:
    left_1: First argument.
    left_2: Second argument.

  Returns:
    Rewrite Fst.

  Following call:
  ```
  concat_l(gr.A, gr.B)
  ```
  will return:
  ```
  pyn.union(
      '<a><b>',
      '<a>ph.PHONEMES<b>',
      ...
  )
  ```
  """
  return left_1 + al.SKIP_RIGHT_SIDE + left_2
