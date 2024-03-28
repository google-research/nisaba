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
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso


class IsoInventoryTest(absltest.TestCase):

  def test_get_brh(self):
    self.assertEqual(iso.get_brh('a_i', iso.DEVA), 'अ')

  def test_get_brh_missing(self):
    self.assertEqual(iso.get_brh('kh', iso.TAML), '')

  def test_ls_tr2brh(self):
    self.assertIn(('`a_i`', 'अ'), iso.ls_tr2brh(iso.DEVA))

  def test_ls_tr2brh_missing(self):
    self.assertIn(('`kh`', ''), iso.ls_tr2brh(iso.TAML))

if __name__ == '__main__':
  absltest.main()
