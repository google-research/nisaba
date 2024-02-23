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

import pynini as pyn
from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import fst_list as f
from nisaba.scripts.natural_translit.utils import type_op as ty
from nisaba.scripts.utils import test_util

_FST_A = pyn.accep('a')
_FST_B = pyn.accep('b')
_FST_C = pyn.accep('c')
_FST_AXB = pyn.cross(_FST_A, _FST_B)
_FST_BXC = pyn.cross(_FST_B, _FST_C)


class FstListTest(test_util.FstTestCase):

  def assertFstListItemsEqual(
      self, fst_list: f.FstList, expected: list[pyn.Fst]
  ) -> bool:
    return self.assertEqual(fst_list._items, expected)

  def test_empty(self):
    self.assertEmpty(f.FstList())

  def test_bool_false(self):
    self.assertFalse(f.FstList())

  def test_bool_true(self):
    self.assertTrue(f.FstList('a'))

  def test_with_alias(self):
    fst_list = f.FstList(alias='a')
    self.assertEqual(fst_list.alias, 'a')
    self.assertEmpty(fst_list)

  def test_add_nothing(self):
    self.assertEmpty(f.FstList(ty.UNSPECIFIED))

  def test_add_str(self):
    self.assertFstListItemsEqual(f.FstList('a'), [_FST_A])

  def test_add_fst(self):
    self.assertFstListItemsEqual(f.FstList(_FST_A, _FST_B), [_FST_A, _FST_B])

  def test_add_iterable(self):
    self.assertFstListItemsEqual(f.FstList([_FST_A, _FST_B]), [_FST_A, _FST_B])

  def test_add_iterable_nested(self):
    self.assertFstListItemsEqual(
        f.FstList(_FST_A).add([_FST_B, [_FST_A, _FST_C]]),
        [_FST_A, _FST_B, _FST_A, _FST_C])

  def test_add_fst_list(self):
    self.assertFstListItemsEqual(
        f.FstList(f.FstList(_FST_A, _FST_B)), [_FST_A, _FST_B]
    )

  def test_concat(self):
    self.AssertEqualFstLike(f.FstList(_FST_A, _FST_B).concat(), 'ab')

  def test_compose(self):
    self.AssertEqualFstLike(
        (_FST_A @ f.FstList(_FST_AXB, _FST_BXC).compose()), 'c'
    )

  def test_item(self):
    self.assertEqual(f.FstList(_FST_A, _FST_B).item(0), _FST_A)
    self.assertEqual(f.FstList(_FST_A, _FST_B).item(-1), _FST_B)

if __name__ == '__main__':
  absltest.main()
