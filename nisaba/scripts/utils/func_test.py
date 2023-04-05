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

"""Tests for third_party.nisaba.scripts.utils.func."""

from nisaba.scripts.utils import func
from absl.testing import absltest


class FuncTest(absltest.TestCase):

  def test_ComposeFn1(self):
    incr = lambda n: n + 1
    double = lambda n: n * 2
    third = lambda n: n // 3

    fn = func.ComposeFn1(double, incr, third)
    self.assertEqual(5, fn(7))  # (7*2 + 1)/3


if __name__ == '__main__':
  absltest.main()
