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
from nisaba.scripts.natural_translit.script import grapheme as g
from nisaba.scripts.natural_translit.script.inventories import latn
from nisaba.scripts.natural_translit.utils import test_op

_latn = latn.graphemes


class BasicLatinTest(test_op.TestCase):

  def test_lowercase_from_char(self):
    self.assertEqual(_latn.a.text, 'a')

  def test_lowercase_from_char_feature(self):
    self.AssertHasFeature(_latn.a, g.Grapheme.GR_FEATURES.script.latn)
    self.AssertHasFeature(
        _latn.a, g.Grapheme.PH_DESCRIPTIVE_FEATURES.ph_class.vowel
    )

  def test_in_raw_dict(self):
    self.assertEqual(_latn.raw_lookup('a'), _latn.a)

  def test_lowercase_list(self):
    self.assertIn(_latn.a, _latn.lower)

if __name__ == '__main__':
  absltest.main()
