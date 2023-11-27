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

from absl.testing import absltest
from nisaba.scripts.natural_translit.phonology import feature

_f = feature.FEATURE_INVENTORY


class FeatureTest(absltest.TestCase):

  def test_str_voiced(self):
    self.assertEqual(_f.voiced, 'voiced')

  def test_str_vcd_stop(self):
    self.assertIn('voiced', _f.vcd_stop)

if __name__ == '__main__':
  absltest.main()
