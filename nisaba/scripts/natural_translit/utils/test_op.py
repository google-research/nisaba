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

from typing import Any, Iterable
from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import feature as ftr
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import type_op as ty


class TestCase(absltest.TestCase):
  """Collection of asserts for natural translit."""

  # Common asserts

  def AssertEqualValue(
      self,
      obj_1: ...,
      obj_2: ...,
  ):
    self.assertTrue(ty.is_equal(obj_1, obj_2))

  def AssertNotEqualValue(
      self,
      obj_1: ...,
      obj_2: ...,
  ):
    self.assertFalse(ty.is_equal(obj_1, obj_2))

  def AssertStrEqual(self, obj_1: ..., obj_2: ...):
    self.assertEqual(str(obj_1), str(obj_2))

  def AssertFileContentEndsWith(self, file_path: str, obj: ...):
    with open('nisaba/scripts/' + file_path, 'r') as f:
      self.assertTrue(f.read().strip().endswith(str(obj).strip()))

  # Expression asserts

  def AssertAccepts(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertTrue(expression_1.accepts(expression_2))

  def AssertNotAccepts(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertFalse(expression_1.accepts(expression_2))

  def AssertEquivalent(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertTrue(expression_1.is_equivalent(expression_2))

  def AssertNotEquivalent(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertFalse(expression_1.is_equivalent(expression_2))

  def AssertContains(
      self,
      expression_1: exp.Expression,
      expression_2: sym.Item,
      head: bool = False,
      tail: bool = False,
  ):
    return self.assertTrue(expression_1.contains(expression_2, head, tail))

  def AssertNotContains(
      self,
      expression_1: exp.Expression,
      expression_2: sym.Item,
      head: bool = False,
      tail: bool = False,
  ):
    return self.assertFalse(expression_1.contains(expression_2, head, tail))

  def AssertMatches(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertTrue(expression_1.matches(expression_2))

  def AssertNotMatches(
      self, expression_1: exp.Expression, expression_2: sym.Item
  ):
    return self.assertFalse(expression_1.matches(expression_2))

  # Feature asserts

  def AssertFeatureDistance(
      self,
      feature_1: ftr.Feature.ITERABLE,
      feature_2: ftr.Feature.ITERABLE,
      expected_distance: float,
  ):
    if hasattr(feature_1, 'distance'):
      distance = feature_1.distance(feature_2)
    else:
      distance = ftr.Feature.ERROR_DISTANCE
    self.assertEqual(distance, expected_distance)

  def AssertFeatureIn(self, value: ftr.Feature.Aspect.VALUES, obj: ...) -> None:
    self.assertTrue(ftr.value_in(value, obj))

  def AssertFeatureNotIn(
      self, value: ftr.Feature.Aspect.VALUES, obj: ...
  ) -> None:
    self.assertFalse(ftr.value_in(value, obj))

  def AssertHasFeature(
      self,
      obj: ...,
      value: ftr.Feature.Aspect.VALUES,
  ):
    self.assertTrue(ftr.value_in(value, obj))

  def AssertNotHasFeature(
      self,
      obj: ...,
      value: ftr.Feature.Aspect.VALUES,
  ):
    self.assertFalse(ftr.value_in(value, obj))

  # Iterable asserts

  def AssertEqualItems(
      self, iterable_1: Iterable[Any], iterable_2: Iterable[Any]
  ):
    self.assertEqual([*iterable_1], [*iterable_2])
