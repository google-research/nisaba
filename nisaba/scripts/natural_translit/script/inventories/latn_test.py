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

from absl.testing import absltest
from nisaba.scripts.natural_translit.language_params import en
from nisaba.scripts.natural_translit.script import grapheme as g
from nisaba.scripts.natural_translit.script.inventories import latn
from nisaba.scripts.natural_translit.utils import test_op

_G = g.Grapheme
_EN = en.LATN
_LATN = latn.LATN


class LatnTest(test_op.TestCase):

  def test_latn(self):
    self.assertEqual(_LATN.raw_lookup('a'), _LATN.a)
    self.AssertHasFeature(_LATN.a, _G.GR_FEATURES.script.latn)
    self.AssertHasFeature(_LATN.a, _G.GR_FEATURES.case.lower)
    self.AssertHasFeature(_LATN.a, _G.DESCRIPTIVE_FEATURES.ph_class.vowel)
    self.assertIn(_LATN.a, _LATN.vowel)
    self.assertIn(_LATN.a, _LATN.lower)
    self.AssertAccepts(_LATN.atomics.vowel, _LATN.a)
    self.assertNotIn(_LATN.a, _LATN.upper)
    self.assertIn(_LATN.a_upper, _LATN.vowel)
    self.assertIn(_LATN.a_upper, _LATN.upper)
    self.AssertAccepts(_LATN.atomics.vowel, _LATN.a_upper)
    self.assertNotIn(_LATN.a_upper, _LATN.lower)
    self.assertIn(_LATN.a, _LATN.letter)
    self.assertIn(_LATN.a_upper, _LATN.letter)
    self.assertIs(_LATN.a.upper, _LATN.a_upper)
    self.assertIs(_LATN.a_upper.lower, _LATN.a)
    self.assertIs(_LATN.a.lower, _LATN.a)
    self.assertIs(_LATN.a_upper.upper, _LATN.a_upper)
    self.AssertHasFeature(_LATN.one, _G.GR_FEATURES.gr_class.number)
    self.assertIn(_LATN.one, _LATN.number)

  def test_en_latn(self):
    self.assertNotEqual(_LATN.a, _EN.a)
    self.assertIn(_EN.a, _EN.vowel)
    self.assertIn(_EN.y, _EN.vowel)
    self.AssertStrEqual(_EN.a.descriptives(), _EN.a_upper.descriptives())


if __name__ == '__main__':
  absltest.main()
