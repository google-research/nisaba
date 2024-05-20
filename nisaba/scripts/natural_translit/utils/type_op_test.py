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

"""Tests for type_op."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import test_op
from nisaba.scripts.natural_translit.utils import type_op as ty

# Test objects

_T0 = ty.Thing(alias='T0', value_from=0)
_T1 = ty.Thing(alias='T1', text='one')
_T2 = ty.Thing(value_from=_T0, from_attribute='value')
_T3 = ty.Thing(alias='', value_from=_T1)
_T4 = ty.Thing(alias='T4', value_from=_T1)


class TypeOpTest(test_op.TestCase):

  def test_nothing_bool(self):
    self.assertFalse(ty.UNASSIGNED)

  def test_nothing_alias(self):
    self.assertEqual(ty.UNASSIGNED.alias, 'unassigned')

  def test_nothing_text(self):
    self.assertEqual(ty.UNASSIGNED.text, 'Nothing_unassigned')

  def test_thing(self):
    self.assertEqual(_T0.value, 0)

  def test_thing_default_value(self):
    self.assertEqual(_T1.value, _T1)

  def test_thing_alias_text(self):
    self.assertEqual(_T1.alias, 'T1')
    self.assertEqual(_T1.text, 'one')

  def test_thing_inherit_value(self):
    self.assertEqual(_T2.value, 0)

  def test_is_equal(self):
    self.AssertEqualValue(1, 1)

  def test_not_equal(self):
    self.AssertNotEqualValue(0, 1)

  def test_is_equal_value_to_int(self):
    self.AssertEqualValue(_T0, 0)

  def test_is_equal_int_to_value(self):
    self.AssertEqualValue(0, _T0)

  def test_equal_thing_to_value(self):
    self.AssertEqualValue(_T1, _T3)

  def test_equal_value_to_value(self):
    self.AssertEqualValue(_T3, _T4)

  def test_is_equal_zero(self):
    self.AssertEqualValue(0, 0)

  def test_equal_int_float(self):
    self.AssertEqualValue(0, 0.0)

  def test_equal_empty(self):
    self.AssertEqualValue({}, {})

  def test_is_equal_fst(self):
    self.AssertEqualValue(ty.pyn.accep('a'), ty.pyn.accep('a'))

  def test_is_equal_fstlike(self):
    self.AssertEqualValue(ty.pyn.accep('a'), 'a')

  def test_not_equal_fst(self):
    self.AssertNotEqualValue(ty.pyn.accep('a'), ty.pyn.accep('b'))

  def test_equal_epsilon(self):
    self.AssertEqualValue(ty.pyn.accep(''), ty.pyn.accep(''))

  def test_equal_epsilon_2(self):
    self.AssertEqualValue('', ty.pyn.accep(''))

  def test_not_equal_none_1(self):
    self.AssertNotEqualValue(None, 1)

  def test_not_equal_none_2(self):
    self.AssertNotEqualValue(1, None)

  def test_equal_none_both(self):
    self.AssertEqualValue(None, None)

  def test_not_equal_nothing(self):
    self.AssertNotEqualValue(ty.UNSPECIFIED, ty.UNSPECIFIED)

  def test_iterable_thing_untyped(self):
    untyped = ty.IterableThing()
    self.assertTrue(untyped.valid_item(1))
    self.assertFalse(untyped.valid_item(ty.MISSING))

  def test_iterable_thing_typed(self):
    typed = ty.IterableThing(typed=int)
    self.assertTrue(typed.valid_item(1))
    self.assertFalse(typed.valid_item('a'))
    self.assertFalse(typed.valid_item(ty.MISSING))

  def test_iterable_thing_untyped_add(self):
    untyped1 = ty.IterableThing(1)
    untyped2 = ty.IterableThing(untyped1, 'a', ['b'], ty.UNASSIGNED)
    self.assertIn(1, untyped1)
    self.assertIn('a', untyped2)
    self.assertIn(['b'], untyped2)
    self.assertNotIn(untyped1, untyped2)
    self.assertIn(1, untyped2)
    self.assertNotIn(ty.UNASSIGNED, untyped2)

  def test_iterable_thing_typed_add(self):
    untyped = ty.IterableThing(1, 'a')
    typed = ty.IterableThing(int, untyped, 2, [3], ty.UNASSIGNED, typed=int)
    self.assertIn(1, typed)
    self.assertIn(2, typed)
    self.assertIn(3, typed)
    self.assertNotIn(untyped, typed)
    self.assertNotIn('a', typed)
    self.assertNotIn(ty.UNASSIGNED, typed)

  def test_iterable_thing_item(self):
    iterable = ty.IterableThing(0, 1, 2, 3)
    self.assertEqual(iterable.item(0), 0)
    self.assertEqual(iterable.item(3), 3)
    self.assertEqual(iterable.item(5), ty.MISSING)
    self.assertEqual(iterable.item(-4), 0)
    self.assertIsNone(iterable.item(-5, None))


if __name__ == '__main__':
  absltest.main()
