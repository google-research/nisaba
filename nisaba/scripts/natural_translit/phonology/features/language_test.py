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

from absl.testing import absltest
from nisaba.scripts.natural_translit.phonology.features import language
from nisaba.scripts.natural_translit.utils import test_op

_LANG = language.FEATURES.language


class LanguageTest(test_op.TestCase):

  def test_language(self):
    self.assertEqual(_LANG.bn.index, 624)
    self.assertEqual(_LANG.x_uni.index, 8_000)

  def test_no_duplicate_indices(self):
    index_list = [l.index for l in _LANG]
    self.assertEqual(len(set(index_list)), len(index_list))

if __name__ == '__main__':
  absltest.main()
