# Copyright 2022 Nisaba Authors.
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

"""Tests for phon_ops."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import phon_ops
from nisaba.scripts.utils import test_util


class PhonOpsTest(test_util.FstTestCase):

  def test_jny_to_gny(self):
    self.assertFstStrIO(phon_ops.JNY_TO_GNY, '(j=jh)(ny=ny)', '(j,ny=g,ny)')

if __name__ == '__main__':
  absltest.main()
