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

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.utils import test_util

_TEST_CASES = [
    (al.enclose_phoneme, [
        (['a'], '{a}'),
        ]),
    (al.enclose_grapheme, [
        (['a'], '<a>'),
        ]),
    (al.enclose_translit, [
        (['a'], '`a`'),
        ]),
    (al.align, [
        (['<a>', '{a}'], '<a>={a}'),
        ]),
]


class AlignmentTest(test_util.FstTestCase):

  def test_all(self):
    self.assertEqualFstLikeTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
