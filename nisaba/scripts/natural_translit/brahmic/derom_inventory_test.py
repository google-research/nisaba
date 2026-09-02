# Copyright 2026 Nisaba Authors.
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
from nisaba.scripts.natural_translit.brahmic import derom_inventory as dm
from nisaba.scripts.natural_translit.brahmic import grapheme_inventory
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.utils import test_op
from nisaba.scripts.natural_translit.utils import type_op as ty


ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = grapheme_inventory.TRANSLIT_INVENTORY
drm = dm.DEROMANIZATION_INVENTORY


class DeromInventoryTest(test_op.TestCase):

  def test_independent_vowel(self):
    self.AssertEqualValue(dm._independent_vowel(iso.AA), iso.AA_I)  # pyrefly: ignore[missing-attribute]

  def test_long_vowel(self):
    self.AssertEqualValue(dm._long_vowel(iso.I), iso.II)  # pyrefly: ignore[missing-attribute]

  def test_long_independent_vwl(self):
    self.AssertEqualValue(
        dm._independent_vowel(dm._long_vowel(iso.U)), iso.UU_I  # pyrefly: ignore[bad-argument-type, missing-attribute]
    )

  def test_aspirated_consonant(self):
    self.AssertEqualValue(dm._aspirated_consonant(iso.C), iso.CH)  # pyrefly: ignore[missing-attribute]

  def test_get(self):
    self.AssertEqualValue(drm.f.get('frg'), iso.F)  # pyrefly: ignore[missing-attribute]

  def test_as_list(self):
    self.assertEqual(
        dm.DeromMapping.as_list(drm.a, [drm.b, drm.c]),  # pyrefly: ignore[missing-attribute]
        [drm.a, drm.b, drm.c],  # pyrefly: ignore[missing-attribute]
    )

  def test_as_list_nothing(self):
    self.assertEmpty(dm.DeromMapping.as_list(ty.UNSPECIFIED))

  def test_vowel_fields(self):
    self.AssertEqualValue(drm.i.rom, ltn.I)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.i.rom_l, ltn.I + ltn.I)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.i.brh, iso.I)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.i.brh_i, iso.I_I)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.i.brh_l, iso.II)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.i.brh_l_i, iso.II_I)  # pyrefly: ignore[missing-attribute]

  def test_vowel_field_missing(self):
    self.assertFalse(hasattr(drm.ai, 'brh_l'))  # pyrefly: ignore[missing-attribute]

  def test_cons_fields(self):
    self.AssertEqualValue(drm.p.rom, ltn.P)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.rom_l, ltn.P + ltn.P)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.rom_l_h, ltn.P + ltn.P + ltn.H)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.rom_h_l, ltn.P + ltn.H + ltn.P + ltn.H)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh, iso.P)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_v, iso.P + iso.VIR)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_l, iso.P + iso.VIR + iso.P)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_l_v, iso.P + iso.VIR + iso.P + iso.VIR)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_asp, iso.PH)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_asp_v, iso.PH + iso.VIR)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_l_asp, iso.P + iso.VIR + iso.PH)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_l_asp_v, iso.P + iso.VIR + iso.PH + iso.VIR)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(drm.p.brh_asp_l, iso.PH + iso.VIR + iso.PH)  # pyrefly: ignore[missing-attribute]
    self.AssertEqualValue(
        drm.p.brh_asp_l_v, iso.PH + iso.VIR + iso.PH + iso.VIR  # pyrefly: ignore[missing-attribute]
    )

  def test_cons_field_missing(self):
    self.assertFalse(hasattr(drm.sh, 'brh_asp'))  # pyrefly: ignore[missing-attribute]

  def test_high_priority(self):
    self.assertTrue(drm.zh_lr.high_priority())  # pyrefly: ignore[missing-attribute]

  def test_high_priority_false(self):
    self.assertFalse(drm.z.high_priority())  # pyrefly: ignore[missing-attribute]


if __name__ == '__main__':
  absltest.main()
