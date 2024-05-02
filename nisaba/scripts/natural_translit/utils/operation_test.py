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

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import operation as op

_OPS = op.Operation.COMMON


class OperationTest(absltest.TestCase):

  def test_operation(self):
    self.assertEqual(_OPS.alignable.index, 101)
    self.assertEqual(_OPS.index_lookup(101), _OPS.alignable)
    self.assertEqual(_OPS.alignable.base_cost, 0)

  def test_partial(self):
    self.assertEqual(_OPS.alignable.partial, _OPS.partial_alignable)
    self.assertEqual(_OPS.partial_alignable.index, 102)
    self.assertEqual(_OPS.partial_alignable.match, _OPS.alignable)
    self.assertEqual(_OPS.partial_alignable.base_cost, _OPS.alignable.base_cost)

  def test_unexpected(self):
    self.assertEqual(_OPS.alignable.unexpected, _OPS.unexpected_alignable)
    self.assertEqual(_OPS.unexpected_alignable.index, 103)
    self.assertEqual(_OPS.unexpected_alignable.match, _OPS.alignable)
    self.assertEqual(
        _OPS.unexpected_alignable.base_cost,
        _OPS.alignable.base_cost + op.Operation.UNEXPECTED_PENALTY,
    )
    self.assertEqual(_OPS.unexpected_alignable.match, _OPS.alignable)
    self.assertEqual(
        _OPS.unexpected_alignable.partial, _OPS.unexpected_partial_alignable
    )
    self.assertEqual(
        _OPS.partial_alignable.unexpected, _OPS.unexpected_partial_alignable
    )

  def test_assigned(self):
    self.assertTrue(_OPS.alignable.is_assigned())
    self.assertFalse(_OPS.unassigned.is_assigned())
    self.assertFalse(_OPS.error.is_assigned())

  def test_cost_free(self):
    self.assertTrue(_OPS.alignable.is_free())
    self.assertFalse(_OPS.unassigned.is_free())

  def test_is_cheaper(self):
    self.assertTrue(_OPS.alignable.is_cheaper_than(_OPS.interchangeable))

  def test_inventory(self):
    self.assertEqual(_OPS.alignable.inventory, _OPS)
    self.assertEqual(_OPS.index_lookup(101), _OPS.alignable)
    self.assertEqual(_OPS.index_lookup(120), _OPS.error)

  def test_add_operations(self):
    test = op.Operation('test', 1)
    _OPS.add_operations(test)
    self.assertIn(test, _OPS)
    self.assertFalse(test.inventory, _OPS)


if __name__ == '__main__':
  absltest.main()
