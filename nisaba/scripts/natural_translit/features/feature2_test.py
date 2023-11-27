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

from absl.testing import absltest
from nisaba.scripts.natural_translit.features import feature2 as f
from nisaba.scripts.natural_translit.utils import type_op as ty

_f0 = f.Feature('f0', 'c0')
_f1 = f.Feature('f1', 'c1')
_f2 = f.Feature('f2', 'c2')
_f3 = f.Feature('f3', 'c3')
_f4 = f.Feature('f4', 'c4')
_fs0 = f.FeatureSet()
_fs1 = f.FeatureSet(_f1, _f2)
_fs2 = f.FeatureSet(ty.UNSPECIFIED)
_fs3 = f.FeatureSet(_fs1, _f3)
_test = f.FeatureInventory('test')


class Feature2Test(absltest.TestCase):

  def test_feature(self):
    self.assertEqual(_f0.alias, 'f0')
    self.assertEqual(_f0.category, 'c0')
    self.assertEqual(_f0.group, ty.UNASSIGNED)

  def test_feature_set_empty(self):
    self.assertEmpty(_fs0)
    self.assertEqual(_fs0.str(), '()')

  def test_feature_set_items(self):
    self.assertIn(_f1, _fs1)
    self.assertIn(_f2, _fs1)

  def test_feature_set_nothing(self):
    self.assertEmpty(_fs2)

  def test_feature_set_feature_set(self):
    self.assertEqual(_fs3._items, {_f1, _f2, _f3})

  def test_feature_inventory_group(self):
    _test.make_group('g', ['gf1', 'gf2'])
    self.assertEqual(_test.gf1.group, 'g')
    self.assertEqual(_test.g, [_test.gf1, _test.gf2])


if __name__ == '__main__':
  absltest.main()
