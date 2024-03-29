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

  def test_is_none(self):
    self.assertTrue(ty.is_none(None))

  def test_not_none_zero(self):
    self.assertTrue(ty.not_none(0))

  def test_not_none_list(self):
    self.assertTrue(ty.not_none([]))

  def test_is_assigned(self):
    self.assertTrue(ty.is_assigned(0))

  def test_nothing_bool(self):
    self.assertFalse(ty.UNASSIGNED)

  def test_nothing_alias(self):
    self.assertEqual(ty.UNASSIGNED.alias, 'unassigned')

  def test_nothing_text(self):
    self.assertEqual(ty.UNASSIGNED.text, 'Nothing_unassigned')

  def test_not_assigned(self):
    self.assertTrue(ty.not_assigned(ty.UNASSIGNED))

  def test_is_specified(self):
    self.assertTrue(ty.is_specified(None))

  def test_not_specified(self):
    self.assertTrue(ty.not_specified(ty.UNSPECIFIED))

  def test_is_found(self):
    self.assertTrue(ty.is_found(0))

  def test_not_found(self):
    self.assertTrue(ty.not_found(ty.MISSING))

  def test_is_nothing(self):
    self.assertTrue(ty.is_nothing(ty.MISSING))

  def test_not_nothing(self):
    self.assertTrue(ty.not_nothing(None))

  def test_exists(self):
    self.assertTrue(ty.exists(0))

  def test_not_exists_none(self):
    self.assertTrue(ty.not_exists(None))

  def test_not_exists_nothing(self):
    self.assertTrue(ty.not_exists(ty.UNSPECIFIED))

  def test_not_exists_empty(self):
    self.assertTrue(ty.not_exists(ty.MISSING))

  def test_is_instance(self):
    self.assertTrue(ty.is_instance(1, int))

  def test_not_instance(self):
    self.assertTrue(ty.not_instance(1, str))

  def test_thing(self):
    self.assertEqual(_T0.value, 0)

  def test_thing_default_value(self):
    self.assertEqual(_T1.value, _T1)

  def test_thing_alias_text(self):
    self.assertEqual(_T1.alias, 'T1')
    self.assertEqual(_T1.text, 'one')

  def test_thing_inherit_value(self):
    self.assertEqual(_T2.value, 0)

  def test_has_attribute(self):
    self.assertTrue(ty.has_attribute(complex(1, 2), 'real'))

  def test_has_attribute_false(self):
    self.assertFalse(ty.has_attribute(complex(1, 2), 'rea'))

  def test_has_attribute_none(self):
    self.assertFalse(ty.has_attribute(None, 'real'))

  def test_has_attribute_type(self):
    self.assertTrue(ty.has_attribute(complex(1, 2), 'real', typeinfo=float))

  def test_has_attribute_type_false(self):
    self.assertFalse(ty.has_attribute(complex(1, 2), 'real', typeinfo=str))

  def test_get_attribute(self):
    self.assertEqual(ty.get_attribute(complex(1, 2), 'real'), 1.0)

  def test_get_attribute_default(self):
    self.assertEqual(ty.get_attribute(complex(1, 2), 'rea', default=0), 0)

  def test_get_attribute_type(self):
    self.assertEqual(
        ty.get_attribute(complex(1, 2), 'real', typeinfo=int, default=-1), -1
    )

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

  def test_not_equal_zero(self):
    self.AssertNotEqualValue(0.0, 0.0, zero=False)

  def test_not_equal_empty(self):
    self.AssertNotEqualValue({}, {})

  def test_is_equal_empty(self):
    self.AssertEqualValue(range(0), range(0), empty=True)

  def test_is_equal_fst(self):
    self.AssertEqualValue(ty.pyn.accep('a'), ty.pyn.accep('a'))

  def test_is_equal_fstlike(self):
    self.AssertEqualValue(ty.pyn.accep('a'), 'a')

  def test_not_equal_fst(self):
    self.AssertNotEqualValue(ty.pyn.accep('a'), ty.pyn.accep('b'))

  def test_not_equal_epsilon(self):
    self.AssertNotEqualValue(ty.pyn.accep(''), ty.pyn.accep(''))

  def test_not_equal_epsilon_2(self):
    self.AssertNotEqualValue('', ty.pyn.accep(''))

  def test_is_equal_epsilon(self):
    self.AssertEqualValue(ty.pyn.accep(''), ty.pyn.accep(''), epsilon=True)

  def test_is_equal_epsilon_str(self):
    self.AssertEqualValue(ty.pyn.accep(''), '', epsilon=True)

  def test_not_equal_epsilon_zero(self):
    self.AssertNotEqualValue(ty.pyn.accep(''), 0, epsilon=True)

  def test_not_equal_zero_epsilon(self):
    self.AssertNotEqualValue(0, ty.pyn.accep(''), epsilon=True)

  def test_not_equal_none_1(self):
    self.AssertNotEqualValue(None, 1)

  def test_not_equal_none_2(self):
    self.AssertNotEqualValue(1, None)

  def test_not_equal_none_both(self):
    self.AssertNotEqualValue(None, None)

  def test_not_equal_nothing(self):
    self.AssertNotEqualValue(ty.UNSPECIFIED, ty.UNSPECIFIED)

  def test_is_empty_list(self):
    self.assertTrue(ty.is_empty([]))

  def test_is_empty_range(self):
    self.assertTrue(ty.is_empty(range(0)))

  def test_is_empty_set(self):
    self.assertTrue(ty.is_empty(set()))

  def test_not_empty_set(self):
    self.assertTrue(ty.not_empty({1}))

  def test_is_empty_non_iterable(self):
    self.assertFalse(ty.is_empty(_T1))

  def test_is_empty_none(self):
    self.assertFalse(ty.is_empty(None))

  def test_not_empty_none(self):
    self.assertTrue(ty.not_empty(None))

  def test_get_element(self):
    self.assertEqual(ty.get_element([1, 2, 3], 1), 2)

  def test_get_element_none(self):
    self.assertTrue(ty.not_found(ty.get_element(None, 1)))

  def test_get_element_non_iterable(self):
    self.assertTrue(ty.not_found(ty.get_element(0, 1)))

  def test_get_element_out_of_index(self):
    self.assertTrue(ty.not_found(ty.get_element([1, 2, 3], 4)))

  def test_get_element_default(self):
    self.assertEqual(ty.get_element([1, 2, 3], 4, default=0), 0)

  def test_enforce_range(self):
    self.assertEqual(ty.enforce_range(1, 3, 0, 10), range(1, 3))

  def test_enforce_range_start_nothing(self):
    self.assertEqual(ty.enforce_range(ty.MISSING, 3), range(0))

  def test_enforce_range_stop_nothing(self):
    self.assertEqual(ty.enforce_range(1, ty.MISSING), range(0))

  def test_enforce_range_default(self):
    self.assertEqual(
        ty.enforce_range(ty.MISSING, ty.MISSING, 0, 10), range(0, 10)
    )

  def test_in_range(self):
    self.assertTrue(ty.in_range(1, 0, 5))

  def test_in_range_nothing(self):
    self.assertFalse(ty.in_range(ty.MISSING, 0, 5))

  def test_in_range_tuple(self):
    self.assertNotIn(ty.MISSING, range(0, 5))

  def test_enforce_list(self):
    self.assertEqual(ty.enforce_list([0, 1]), [0, 1])

  def test_enforce_list_nothing(self):
    self.assertEqual(ty.enforce_list(ty.UNSPECIFIED), [])

  def test_in_list(self):
    self.assertTrue(ty.in_list(1, [0, 1]))

  def test_in_list_nothing(self):
    self.assertFalse(ty.in_list(3, ty.MISSING))

  def test_enforce_dict(self):
    self.assertEqual(ty.enforce_dict({'k': 'v'}), {'k': 'v'})

  def test_enforce_dict_nothing(self):
    self.assertEqual(ty.enforce_dict(ty.UNSPECIFIED), {})

  def test_dict_get_existing_key(self):
    self.assertEqual(ty.dict_get({'k': 'v'}, 'k'), 'v')

  def test_dict_get_missing_key(self):
    self.assertEqual(ty.dict_get({'k': 'v'}, 'k2'), ty.MISSING)

  def test_dict_get_missing_key_with_default(self):
    self.assertEqual(ty.dict_get({'k': 'v'}, 'k2', 'def'), 'def')

  def test_dict_get_unhashable_key(self):
    self.assertEqual(ty.dict_get({'k': 'v'}, ['k']), ty.MISSING)

  def test_dict_get_nothing(self):
    self.assertEqual(ty.dict_get(ty.UNSPECIFIED, 'k'), ty.MISSING)

  def test_enforce_set(self):
    self.assertEqual(ty.enforce_set({1, 2, 3}), {1, 2, 3})

  def test_enforce_set_nothing(self):
    self.assertEqual(ty.enforce_set(ty.MISSING), set())

  def test_in_set(self):
    self.assertTrue(ty.in_set(1, {1, 2, 3}))

  def test_in_set_nothing(self):
    self.assertFalse(ty.in_set(1, ty.UNSPECIFIED))

  def test_iterable_thing_untyped(self):
    untyped = ty.IterableThing()
    self.assertTrue(untyped.valid_item(1))
    self.assertTrue(untyped.invalid_item(ty.MISSING))

  def test_iterable_thing_typed(self):
    typed = ty.IterableThing.typed(int)
    self.assertTrue(typed.valid_item(1))
    self.assertTrue(typed.invalid_item('a'))
    self.assertTrue(typed.invalid_item(ty.MISSING))

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
    typed = ty.IterableThing.typed(int, untyped, 2, [3], ty.UNASSIGNED)
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
