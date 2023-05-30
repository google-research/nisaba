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

"""Tests for type_op."""

import collections

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import type_op as t

# Test objects

D = collections.namedtuple('D', ['k'])
_D1 = D('v')
_T0 = t.make_thing(alias='T0', text='t0', value=0)
_T1 = t.make_thing(alias='T1', text='t1', value=t.UNSPECIFIED)
_T2 = t.make_thing(alias='T2', text='', value=_T0)
_T3 = t.make_thing(alias='', text='t3', value=_T1)
_T4 = t.make_thing(alias='T4', text='t4', value=_T1)


class TypeOpTest(absltest.TestCase):

  def assertEqualTypeOp(
      self, a: t.Valid, b: t.Valid,
      empty: bool = False, epsilon: bool = False, zero: bool = True
  ):
    self.assertTrue(t.is_equal(a, b, empty, epsilon, zero))

  def assertNotEqualTypeOp(
      self, a: t.Valid, b: t.Valid,
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

  def test_not_instance_invalid_type(self):
    self.assertTrue(t.not_instance(1, 'int'))

  def test_make_thing(self):
    self.assertEqual(_T0.value, 0)

  def test_make_thing_default_value(self):
    self.assertEqual(_T1.value, _T1)

  def test_make_thing_inherit_value(self):
    self.assertEqual(_T2.value, 0)

  def test_enforce_thing_thing(self):
    self.assertEqual(t.enforce_thing(_T1), _T1)

  def test_enforce_thing_int(self):
    self.assertEqual(t.enforce_thing(0).value, 0)

  def test_has_attribute(self):
    self.assertTrue(t.has_attribute(complex(1, 2), 'real'))

  def test_has_attribute_false(self):
    self.assertFalse(t.has_attribute(complex(1, 2), 'rea'))

  def test_has_attribute_none(self):
    self.assertFalse(t.has_attribute(None, 'real'))

  def test_has_attribute_type(self):
    self.assertTrue(t.has_attribute(complex(1, 2), 'real', want=float))

  def test_has_attribute_type_false(self):
    self.assertFalse(t.has_attribute(complex(1, 2), 'real', want=str))

  def test_get_attribute(self):
    self.assertEqual(t.get_attribute(complex(1, 2), 'real'), 1.0)

  def test_get_attribute_default(self):
    self.assertEqual(t.get_attribute(complex(1, 2), 'rea', default=0), 0)

  def test_get_attribute_type(self):
    self.assertEqual(
        t.get_attribute(complex(1, 2), 'real', want=int, default=-1), -1
    )

  def test_text_of_thing(self):
    self.assertEqual(t.text_of(_T1), 't1')

  def test_text_of_thing_empty(self):
    self.assertEqual(t.text_of(_T2), 'Textless Thing')

  def test_text_of_str(self):
    self.assertEqual(t.text_of('abc'), 'abc')

  def test_text_of_fst(self):
    self.assertEqual(t.text_of(t.pyn.accep('abc')), 'abc')

  def test_text_of_namedtuple(self):
    self.assertEqual(t.text_of(_D1), 'D(k=\'v\')')

  def test_text_of_int(self):
    self.assertEqual(t.text_of('0'), '0')

  def test_text_of_none(self):
    self.assertEqual(t.text_of(None), 'None')

  def test_text_of_nothing(self):
    self.assertEqual(t.text_of(t.UNSPECIFIED), 'Unspecified')

  def test_alias_of_thing(self):
    self.assertEqual(t.alias_of(_T1), 'T1')

  def test_alias_of_thing_empty(self):
    self.assertEqual(t.alias_of(_T3), 't3')

  def test_alias_of_list(self):
    self.assertEqual(t.alias_of([0, 1]), '[0, 1]')

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

  def test_not_empty_list(self):
    self.assertTrue(t.not_empty([1]))

  def test_is_empty_range(self):
    self.assertTrue(t.is_empty(range(0)))

  def test_is_empty_set(self):
    self.assertTrue(t.is_empty(set()))

  def test_not_empty_non_iterable(self):
    self.assertTrue(t.not_empty(_T1))

  def test_not_empty_zero(self):
    self.assertTrue(t.not_empty(0))

  def test_is_empty_unassigned(self):
    self.assertTrue(t.is_empty(t.UNASSIGNED))

  def test_is_empty_none(self):
    self.assertTrue(t.is_empty(None))

  def test_not_empty_allow_none(self):
    self.assertTrue(t.not_empty(None, allow_none=True))

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

  def test_enforce_range_1(self):
    self.assertEqual(t.enforce_range(3), range(3))

  def test_enforce_range_2(self):
    self.assertEqual(t.enforce_range(1, 3), range(1, 3))

  def test_enforce_range_3(self):
    self.assertEqual(t.enforce_range(1, 3, 2), range(1, 3, 2))

  def test_enforce_range_none(self):
    self.assertEqual(t.enforce_range(1, None), range(0))

  def test_enforce_range_none_def_stop(self):
    self.assertEqual(
        t.enforce_range(1, None, def_stop=len([0, 1, 2])),
        range(1, 3)
    )

  def test_enforce_range_none_def_start(self):
    self.assertEqual(
        t.enforce_range(None, 3, def_start=1),
        range(1, 3)
    )

  def test_enforce_range_tuple(self):
    self.assertEqual(t.enforce_range((1, 3)), range(1, 3))

  def test_enforce_range_tuple_none(self):
    self.assertEqual(t.enforce_range((1, None)), range(0))

  def test_enforce_range_tuple_none_def_stop(self):
    self.assertEqual(t.enforce_range((1, None), def_stop=3), range(1, 3))

  def test_enforce_range_tuple_step_in(self):
    self.assertEqual(t.enforce_range((1, 3, 2)), range(1, 3, 2))

  def test_enforce_range_tuple_step_out(self):
    self.assertEqual(t.enforce_range((1, 3), 2), range(1, 3, 2))

  def test_enforce_range_tuple_too_long(self):
    self.assertEqual(t.enforce_range((1, 3, 2, 2)), range(0))

  def test_enforce_range_tuple_step_in_and_out(self):
    self.assertEqual(t.enforce_range((1, 3, 2), 2), range(0))

  def test_enforce_range_bad_start(self):
    self.assertEqual(t.enforce_range(_T1, 3), range(0))

  def test_enforce_range_bad_stop(self):
    self.assertEqual(t.enforce_range(1, '3'), range(0))

  def test_enforce_range_bad_step(self):
    self.assertEqual(t.enforce_range(1, 3, [1]), range(0))

  def test_in_range(self):
    self.assertTrue(t.in_range(1, 0, 5))

  def test_in_range_step_false(self):
    self.assertFalse(t.in_range(1, 0, 5, 2))

  def test_in_range_tuple(self):
    self.assertTrue(t.in_range(1, (0, 5)))

  def test_enforce_list(self):
    self.assertEqual(t.enforce_list([0, 1]), [0, 1])

  def test_enforce_list_dict(self):
    self.assertEqual(t.enforce_list({'k': 'v'}), ['v'])

  def test_enforce_list_enf_dict_false(self):
    self.assertEqual(
        t.enforce_list({'k': 'v'}, enf_dict=False), [{'k': 'v'}]
    )

  def test_enforce_list_iter(self):
    self.assertEqual(t.enforce_list({'k': 'v'}.values()), ['v'])

  def test_enforce_list_range(self):
    self.assertEqual(t.enforce_list(range(0, 5, 2)), [0, 2, 4])

  def test_enforce_list_none(self):
    self.assertEqual(t.enforce_list(None), [])

  def test_enforce_list_none_true(self):
    self.assertEqual(
        t.enforce_list(None, allow_none=True), [None]
    )

  def test_in_list(self):
    self.assertTrue(t.in_list(3, range(1, 5)))

  def test_enforce_dict(self):
    self.assertEqual(t.enforce_dict({'k': 'v'}), {'k': 'v'})

  def test_enforce_dict_namedtuple(self):
    self.assertEqual(t.enforce_dict(_D1), {'k': 'v'})

  def test_enforce_dict_thing(self):
    self.assertEqual(
        t.enforce_dict(_T1), {'alias': 'T1', 'text': 't1', 'value': _T1}
    )

  def test_enforce_dict_no_key(self):
    self.assertEqual(t.enforce_dict('v'), {'default': 'v'})

  def test_enforce_dict_with_key(self):
    self.assertEqual(t.enforce_dict('v', add_key='k'), {'k': 'v'})

  def test_enforce_dict_none(self):
    self.assertEqual(t.enforce_dict(None), {})

  def test_enforce_dict_none_true(self):
    self.assertEqual(
        t.enforce_dict(None, allow_none=True), {'default': None}
    )

  def test_dict_get(self):
    self.assertEqual(t.dict_get('v'), 'v')

  def test_dict_get_with_key(self):
    self.assertTrue(t.not_found(t.dict_get('v', key='k')))

  def test_dict_get_with_key_unhashable(self):
    self.assertTrue(t.not_found(t.dict_get('v', key=['a'])))

  def test_dict_get_with_default(self):
    self.assertEqual(t.dict_get('v', key='k', default=[]), [])

  def test_in_dict(self):
    self.assertTrue(t.in_dict('v', {'k': ['v', 'v2']}))

  def test_in_dict_with_keys(self):
    self.assertTrue(t.in_dict('v', {'k': ['v', 'v2']}, keys='k'))

  def test_enforce_set(self):
    self.assertEqual(t.enforce_set({1, 2, 3}), {1, 2, 3})

  def test_enforce_set_int(self):
    self.assertEqual(t.enforce_set(1), {1})

  def test_enforce_set_list(self):
    self.assertEqual(t.enforce_set([1, 2, 3, 3]), {1, 2, 3})

  def test_enforce_set_empty_list(self):
    self.assertEqual(t.enforce_set([]), set())

  def test_enforce_set_dict(self):
    self.assertEqual(t.enforce_set({'k1': 'v1', 'k2': 'v2'}), {'v1', 'v2'})

  def test_enforce_set_dict_false(self):
    self.assertEqual(
        t.enforce_set({'k1': 'v1', 'k2': 'v2'}, enf_dict=False),
        {('k1', 'v1'), ('k2', 'v2')},
    )

  def test_enforce_set_list_of_unhashable(self):
    self.assertIsNotNone(t.enforce_set([[1], [2], [3]]))

  def test_enforce_set_str(self):
    self.assertEqual(t.enforce_set({'abc'}), {('abc')})

  def test_enforce_set_none(self):
    self.assertEqual(t.enforce_set(None), set())

  def test_enforce_set_allow_none(self):
    self.assertEqual(t.enforce_set(None, allow_none=True), {None})

  def test_in_set(self):
    self.assertTrue(t.in_set(1, {1, 2, 3}))

  def test_in_set_int(self):
    self.assertTrue(t.in_set(1, 1))

  def test_in_enforced_key_non_dict(self):
    self.assertFalse(t.in_enforced('v', ['k', 'v'], keys='k', enf_dict=False))

  def test_in_attribute(self):
    self.assertTrue(t.in_attribute(1.0, complex(1, 2), 'real'))


if __name__ == '__main__':
  absltest.main()
