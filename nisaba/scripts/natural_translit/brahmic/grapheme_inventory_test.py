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
from nisaba.scripts.natural_translit.brahmic import grapheme_inventory as iso
from nisaba.scripts.natural_translit.utils import test_op


class IsoInventoryTest(test_op.TestCase):

  def test_to_typ(self):
    self.AssertEqualValue(iso.to_typ('a'), '<a_i>')
    self.AssertEqualValue(iso.to_typ('.a'), '<a_i>')
    self.AssertEqualValue(iso.to_typ('ạ̄'), '<aan>')
    self.AssertEqualValue(iso.to_typ('ba'), '<b><a>')
    self.AssertEqualValue(iso.to_typ('ba.i'), '<b><a><i_i>')
    self.AssertEqualValue(iso.to_typ('bai'), '<b><ai>')
    self.AssertEqualValue(iso.to_typ('bʰ'), '<bh>')
    self.AssertEqualValue(iso.to_typ('l̥'), '<lv_i>')
    self.AssertEqualValue(iso.to_typ('l̥̄'), '<llv_i>')
    self.AssertEqualValue(iso.to_typ('m̐'), '<cnd>')
    self.AssertEqualValue(iso.to_typ('mô'), '<m><oc>')
    self.AssertEqualValue(iso.to_typ('õm'), '<om>')
    self.AssertEqualValue(iso.to_typ('r̆'), '<r_eye>')
    self.AssertEqualValue(iso.to_typ('rⸯ'), '<reph>')
    self.AssertEqualValue(iso.to_typ('ṟⸯ'), '<rr_chl>')

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
