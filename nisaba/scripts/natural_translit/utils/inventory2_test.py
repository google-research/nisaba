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
from nisaba.scripts.natural_translit.utils import inventory2 as i
from nisaba.scripts.natural_translit.utils import type_op as ty

_A_FST = pyn.accep('a')
_B_STR = 'b'
_C_STR = 'c'
_D_INT = 4

_T_A_FST = ty.Thing.with_alias_and_value('a', _A_FST)
_T_B_STR = ty.Thing.with_alias_and_value('b', _B_STR)
_T_BC_STR = ty.Thing.with_alias_and_value('b', _C_STR)
_T_CB_STR = ty.Thing.with_alias_and_value('c', _B_STR)
_T_C_STR = ty.Thing.with_alias_and_value('c', _C_STR)
_T_D_INT = ty.Thing.with_alias_and_value('d', _D_INT)

_i1 = i.Inventory.from_list([_T_B_STR])

_i2 = i.Inventory.from_list(
    [_T_B_STR, _T_C_STR], 'value', typed=str, supps=[_T_D_INT]
)


class InventoryTest(absltest.TestCase):

  def test_empty_alias(self):
    self.assertEqual(i.Inventory.EMPTY.alias, 'empty_inventory')

  def test_empty_size(self):
    self.assertEmpty(i.Inventory.EMPTY)

  def test_get_field_value_default(self):
    self.assertEqual(_i1._get_field_value(_T_A_FST), _T_A_FST)

  def test_get_field_value_typed(self):
    self.assertEqual(_i1._get_field_value(_T_A_FST, typed=int), ty.MISSING)

  def test_get_field_value_attr(self):
    self.assertEqual(_i1._get_field_value(_T_A_FST, 'value'), _A_FST)

  def test_get_field_value_attr_typed(self):
    self.assertEqual(
        _i1._get_field_value(_T_A_FST, 'value', typed=int), ty.MISSING
    )

  def test_alias(self):
    self.assertEqual(_i1.b, _T_B_STR)

  def test_in(self):
    self.assertIn(_T_B_STR, _i1)

  def test_len(self):
    self.assertLen(_i1, 1)

  def test_add_item_recurring_alias(self):
    _i1.add_item(_T_BC_STR)
    self.assertEqual(_i1.b, _T_B_STR)

  def test_add_item_recurring_alias_return_false(self):
    self.assertFalse(_i1.add_item(_T_BC_STR))

  def test_add_item_wrong_type(self):
    _i1.add_item(_T_A_FST, typed=str)
    self.assertNotIn(_T_A_FST, _i1)

  def test_add_item_wrong_type_return_false(self):
    self.assertFalse(_i1.add_item(_T_A_FST, typed=str))

  def test_add_supp(self):
    _i1.add_supp(_T_D_INT)
    self.assertEqual(_i1.d, 4)

  def test_make_supp(self):
    _i1.make_supp('e', 5)
    self.assertEqual(_i1.e, 5)

  def test_from_list_value(self):
    self.assertEqual(_i2.b, _B_STR)

  def test_from_list_supp(self):
    self.assertEqual(_i2.d, _D_INT)

  def test_from_list_item_aliases(self):
    self.assertEqual(_i2.item_aliases, ['b', 'c'])

  def test_from_list_supp_aliases(self):
    self.assertEqual(_i2.supp_aliases, ['d'])

  def test_add_item_recurring_item(self):
    _i2.add_item(_T_CB_STR, 'value')
    self.assertLen(_i2, 2)

  def test_get_item(self):
    self.assertEqual(_i2.get('b'), _B_STR)

  def test_get_supp(self):
    self.assertEqual(_i2.get('d'), _D_INT)

  def test_get_out_of_inventory(self):
    self.assertEqual(_i2.get('x'), ty.MISSING)

  def test_get_out_of_inventory_default(self):
    self.assertIsNone(_i2.get('x', None))

if __name__ == '__main__':
  absltest.main()
