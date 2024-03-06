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
from nisaba.scripts.natural_translit.utils import type_op as t

# Test objects

_T0 = t.Thing(alias='T0', value_from=0)
_T1 = t.Thing(alias='T1', text='one')
_T2 = t.Thing(value_from=_T0, from_attribute='value')
_T3 = t.Thing(alias='', value_from=_T1)
_T4 = t.Thing(alias='T4', value_from=_T1)


class TypeOpTest(absltest.TestCase):

  def assertEqualTypeOp(
      self, a: ..., b: ...,
      empty: bool = False, epsilon: bool = False, zero: bool = True
  ):
    self.assertTrue(t.is_equal(a, b, empty, epsilon, zero))

  def assertNotEqualTypeOp(
      self, a: ..., b: ...,
      empty: bool = False, epsilon: bool = False, zero: bool = True
  ):
    self.assertTrue(t.not_equal(a, b, empty, epsilon, zero))

  def test_is_none(self):
    self.assertTrue(t.is_none(None))

  def test_not_none_zero(self):
    self.assertTrue(t.not_none(0))

  def test_not_none_list(self):
    self.assertTrue(t.not_none([]))

  def test_is_assigned(self):
    self.assertTrue(t.is_assigned(0))

  def test_nothing_bool(self):
    self.assertFalse(t.UNASSIGNED)

  def test_nothing_alias(self):
    self.assertEqual(t.UNASSIGNED.alias, 'unassigned')

  def test_nothing_text(self):
    self.assertEqual(t.UNASSIGNED.text, 'Nothing_unassigned')

  def test_not_assigned(self):
    self.assertTrue(t.not_assigned(t.UNASSIGNED))

  def test_is_specified(self):
    self.assertTrue(t.is_specified(None))

  def test_not_specified(self):
    self.assertTrue(t.not_specified(t.UNSPECIFIED))

  def test_is_found(self):
    self.assertTrue(t.is_found(0))

  def test_not_found(self):
    self.assertTrue(t.not_found(t.MISSING))

  def test_is_nothing(self):
    self.assertTrue(t.is_nothing(t.MISSING))

  def test_not_nothing(self):
    self.assertTrue(t.not_nothing(None))

  def test_exists(self):
    self.assertTrue(t.exists(0))

  def test_not_exists_none(self):
    self.assertTrue(t.not_exists(None))

  def test_not_exists_nothing(self):
    self.assertTrue(t.not_exists(t.UNSPECIFIED))

  def test_not_exists_empty(self):
    self.assertTrue(t.not_exists(t.MISSING))

  def test_is_instance(self):
    self.assertTrue(t.is_instance(1, int))

  def test_not_instance(self):
    self.assertTrue(t.not_instance(1, str))

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
    self.assertTrue(t.has_attribute(complex(1, 2), 'real'))

  def test_has_attribute_false(self):
    self.assertFalse(t.has_attribute(complex(1, 2), 'rea'))

  def test_has_attribute_none(self):
    self.assertFalse(t.has_attribute(None, 'real'))

  def test_has_attribute_type(self):
    self.assertTrue(t.has_attribute(complex(1, 2), 'real', typeinfo=float))

  def test_has_attribute_type_false(self):
    self.assertFalse(t.has_attribute(complex(1, 2), 'real', typeinfo=str))

  def test_get_attribute(self):
    self.assertEqual(t.get_attribute(complex(1, 2), 'real'), 1.0)

  def test_get_attribute_default(self):
    self.assertEqual(t.get_attribute(complex(1, 2), 'rea', default=0), 0)

  def test_get_attribute_type(self):
    self.assertEqual(
        t.get_attribute(complex(1, 2), 'real', typeinfo=int, default=-1), -1
    )

  def test_is_equal(self):
    self.assertEqualTypeOp(1, 1)

  def test_not_equal(self):
    self.assertNotEqualTypeOp(0, 1)

  def test_is_equal_value_to_int(self):
    self.assertEqualTypeOp(_T0, 0)

  def test_is_equal_int_to_value(self):
    self.assertEqualTypeOp(0, _T0)

  def test_equal_thing_to_value(self):
    self.assertEqualTypeOp(_T1, _T3)

  def test_equal_value_to_value(self):
    self.assertEqualTypeOp(_T3, _T4)

  def test_is_equal_zero(self):
    self.assertEqualTypeOp(0, 0)

  def test_equal_int_float(self):
    self.assertEqualTypeOp(0, 0.0)

  def test_not_equal_zero(self):
    self.assertNotEqualTypeOp(0.0, 0.0, zero=False)

  def test_not_equal_empty(self):
    self.assertNotEqualTypeOp({}, {})

  def test_is_equal_empty(self):
    self.assertEqualTypeOp(range(0), range(0), empty=True)

  def test_is_equal_fst(self):
    self.assertEqualTypeOp(t.pyn.accep('a'), t.pyn.accep('a'))

  def test_is_equal_fstlike(self):
    self.assertEqualTypeOp(t.pyn.accep('a'), 'a')

  def test_not_equal_fst(self):
    self.assertNotEqualTypeOp(t.pyn.accep('a'), t.pyn.accep('b'))

  def test_not_equal_epsilon(self):
    self.assertNotEqualTypeOp(t.pyn.accep(''), t.pyn.accep(''))

  def test_not_equal_epsilon_2(self):
    self.assertNotEqualTypeOp('', t.pyn.accep(''))

  def test_is_equal_epsilon(self):
    self.assertEqualTypeOp(
        t.pyn.accep(''), t.pyn.accep(''), epsilon=True
    )

  def test_is_equal_epsilon_str(self):
    self.assertEqualTypeOp(t.pyn.accep(''), '', epsilon=True)

  def test_not_equal_epsilon_zero(self):
    self.assertNotEqualTypeOp(t.pyn.accep(''), 0, epsilon=True)

  def test_not_equal_zero_epsilon(self):
    self.assertNotEqualTypeOp(0, t.pyn.accep(''), epsilon=True)

  def test_not_equal_none_1(self):
    self.assertNotEqualTypeOp(None, 1)

  def test_not_equal_none_2(self):
    self.assertNotEqualTypeOp(1, None)

  def test_not_equal_none_both(self):
    self.assertNotEqualTypeOp(None, None)

  def test_not_equal_nothing(self):
    self.assertNotEqualTypeOp(t.UNSPECIFIED, t.UNSPECIFIED)

  def test_is_empty_list(self):
    self.assertTrue(t.is_empty([]))

  def test_is_empty_range(self):
    self.assertTrue(t.is_empty(range(0)))

  def test_is_empty_set(self):
    self.assertTrue(t.is_empty(set()))

  def test_not_empty_set(self):
    self.assertTrue(t.not_empty({1}))

  def test_is_empty_non_iterable(self):
    self.assertFalse(t.is_empty(_T1))

  def test_is_empty_none(self):
    self.assertFalse(t.is_empty(None))

  def test_not_empty_none(self):
    self.assertTrue(t.not_empty(None))

  def test_get_element(self):
    self.assertEqual(t.get_element([1, 2, 3], 1), 2)

  def test_get_element_none(self):
    self.assertTrue(t.not_found(t.get_element(None, 1)))

  def test_get_element_non_iterable(self):
    self.assertTrue(t.not_found(t.get_element(0, 1)))

  def test_get_element_out_of_index(self):
    self.assertTrue(t.not_found(t.get_element([1, 2, 3], 4)))

  def test_get_element_default(self):
    self.assertEqual(t.get_element([1, 2, 3], 4, default=0), 0)

  def test_enforce_range(self):
    self.assertEqual(t.enforce_range(1, 3, 0, 10), range(1, 3))

  def test_enforce_range_start_nothing(self):
    self.assertEqual(t.enforce_range(t.MISSING, 3), range(0))

  def test_enforce_range_stop_nothing(self):
    self.assertEqual(t.enforce_range(1, t.MISSING), range(0))

  def test_enforce_range_default(self):
    self.assertEqual(t.enforce_range(t.MISSING, t.MISSING, 0, 10), range(0, 10))

  def test_in_range(self):
    self.assertTrue(t.in_range(1, 0, 5))

  def test_in_range_nothing(self):
    self.assertFalse(t.in_range(t.MISSING, 0, 5))

  def test_in_range_tuple(self):
    self.assertNotIn(t.MISSING, range(0, 5))

  def test_enforce_list(self):
    self.assertEqual(t.enforce_list([0, 1]), [0, 1])

  def test_enforce_list_nothing(self):
    self.assertEqual(t.enforce_list(t.UNSPECIFIED), [])

  def test_in_list(self):
    self.assertTrue(t.in_list(1, [0, 1]))

  def test_in_list_nothing(self):
    self.assertFalse(t.in_list(3, t.MISSING))

  def test_enforce_dict(self):
    self.assertEqual(t.enforce_dict({'k': 'v'}), {'k': 'v'})

  def test_enforce_dict_nothing(self):
    self.assertEqual(t.enforce_dict(t.UNSPECIFIED), {})

  def test_dict_get_existing_key(self):
    self.assertEqual(t.dict_get({'k': 'v'}, 'k'), 'v')

  def test_dict_get_missing_key(self):
    self.assertEqual(t.dict_get({'k': 'v'}, 'k2'), t.MISSING)

  def test_dict_get_missing_key_with_default(self):
    self.assertEqual(t.dict_get({'k': 'v'}, 'k2', 'def'), 'def')

  def test_dict_get_unhashable_key(self):
    self.assertEqual(t.dict_get({'k': 'v'}, ['k']), t.MISSING)

  def test_dict_get_nothing(self):
    self.assertEqual(t.dict_get(t.UNSPECIFIED, 'k'), t.MISSING)

  def test_enforce_set(self):
    self.assertEqual(t.enforce_set({1, 2, 3}), {1, 2, 3})

  def test_enforce_set_nothing(self):
    self.assertEqual(t.enforce_set(t.MISSING), set())

  def test_in_set(self):
    self.assertTrue(t.in_set(1, {1, 2, 3}))

  def test_in_set_nothing(self):
    self.assertFalse(t.in_set(1, t.UNSPECIFIED))

  def test_iterable_thing_untyped(self):
    untyped = t.IterableThing()
    self.assertTrue(untyped.valid_item(1))
    self.assertTrue(untyped.invalid_item(t.MISSING))

  def test_iterable_thing_typed(self):
    typed = t.IterableThing.typed(int)
    self.assertTrue(typed.valid_item(1))
    self.assertTrue(typed.invalid_item('a'))
    self.assertTrue(typed.invalid_item(t.MISSING))

  def test_iterable_thing_untyped_add(self):
    untyped1 = t.IterableThing(1)
    untyped2 = t.IterableThing(untyped1, 'a', ['b'], t.UNASSIGNED)
    self.assertIn(1, untyped1)
    self.assertIn('a', untyped2)
    self.assertIn(['b'], untyped2)
    self.assertNotIn(untyped1, untyped2)
    self.assertIn(1, untyped2)
    self.assertNotIn(t.UNASSIGNED, untyped2)

  def test_iterable_thing_typed_add(self):
    untyped = t.IterableThing(1, 'a')
    typed = t.IterableThing.typed(int, untyped, 2, [3], t.UNASSIGNED)
    self.assertIn(1, typed)
    self.assertIn(2, typed)
    self.assertIn(3, typed)
    self.assertNotIn(untyped, typed)
    self.assertNotIn('a', typed)
    self.assertNotIn(t.UNASSIGNED, typed)

  def test_iterable_thing_item(self):
    iterable = t.IterableThing(0, 1, 2, 3)
    self.assertEqual(iterable.item(0), 0)
    self.assertEqual(iterable.item(3), 3)
    self.assertEqual(iterable.item(5), t.MISSING)
    self.assertEqual(iterable.item(-4), 0)
    self.assertIsNone(iterable.item(-5, None))

if __name__ == '__main__':
  absltest.main()
