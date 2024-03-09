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

"""A library for making unit tests for natural translit."""

from typing import Any

from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import feature as ftr
from nisaba.scripts.natural_translit.utils import type_op as ty
from nisaba.scripts.utils import test_util


class TestCase(test_util.FstTestCase):
  """Collection of asserts for natural translit."""

  def AssertStrEqual(self, obj1: ..., obj2: ...):
    self.assertEqual(str(obj1), str(obj2))

  def AssertEqualValue(
      self,
      a: ...,
      b: ...,
      empty: bool = False,
      epsilon: bool = False,
      zero: bool = True,
  ):
    self.assertTrue(ty.is_equal(a, b, empty, epsilon, zero))

  def AssertNotEqualValue(
      self,
      a: ...,
      b: ...,
      empty: bool = False,
      epsilon: bool = False,
      zero: bool = True,
  ):
    self.assertTrue(ty.not_equal(a, b, empty, epsilon, zero))

  def AssertEqualItems(
      self, iterable_thing: ty.IterableThing, expected: list[Any]
  ):
    self.assertEqual([*iterable_thing], expected)

  def AssertFeatureDistance(
      self,
      feature1: ftr.Feature.ITERABLE,
      feature2: ftr.Feature.ITERABLE,
      expected_distance: float,
  ):
    if hasattr(feature1, 'distance'):
      distance = feature1.distance(feature2)
    else:
      distance = ftr.Feature.ERROR_DISTANCE
    self.assertEqual(distance, expected_distance)

  def AssertAccepts(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertTrue(expression.accepts(other))

  def AssertNotAccepts(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertFalse(expression.accepts(other))

  def AssertEquivalent(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertTrue(expression.is_equivalent(other))

  def AssertNotEquivalent(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertFalse(expression.is_equivalent(other))
