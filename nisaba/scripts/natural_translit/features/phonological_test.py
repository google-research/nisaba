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
from nisaba.scripts.natural_translit.features import phonological

_ar = phonological.articulatory
_ss = phonological.suprasegmental


class PhonologicalTest(absltest.TestCase):

  def test_feature_voiced(self):
    self.assertEqual(_ar.voiced.alias, 'voiced')
    self.assertEqual(_ar.voiced.category, 'articulatory')
    self.assertEqual(_ar.voiced.group, 'voicing')

  def test_group_voicing(self):
    self.assertIn(_ar.voiced, _ar.voicing)

  def test_feature_set_vcd_stop(self):
    self.assertIn(_ar.voiced, _ar.vcd_stop)

  def test_suprasegmental(self):
    self.assertIn(_ss.duration, _ss)

if __name__ == '__main__':
  absltest.main()
