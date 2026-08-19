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
from nisaba.scripts.natural_translit.brahmic import derom_inventory
from nisaba.scripts.natural_translit.brahmic import deromanizer
from nisaba.scripts.natural_translit.language_params import ta as ta_params
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.utils import test_util

ta = ta_params.deromanize
drm = derom_inventory.DEROMANIZATION_INVENTORY


class DeromanizerTest(test_util.FstTestCase):

  def test_script(self):
    self.assertEqual(ta.script, 'taml')

  def test_add_to_groups(self):
    self.assertIn(drm.k, ta.consonant[1])  # rom len 1  # pyrefly: ignore[missing-attribute]
    self.assertIn(drm.ch, ta.consonant[2])  # rom len 2  # pyrefly: ignore[missing-attribute]
    self.assertIn(drm.zh_lr, ta.consonant[3])  # rom len 2 + priority 1  # pyrefly: ignore[missing-attribute]

  def test_default_rules(self):
    self.AssertEqualFstLike(
        fl.FstList('zha', ta.to_brahmic()).compose(), 'ழ'
    )

  def test_compose_rules(self):
    # Initiate empty deromanizer for Tamil script.
    ta2 = deromanizer.Deromanizer.params(
        script='taml',
    )
    # Compose existing ta rules without high_priority and cons_drop_asp
    ta2.rules(
        ta.cons_foreign,  # pyrefly: ignore[missing-attribute]
        ta.cons_gem_only,  # pyrefly: ignore[missing-attribute]
        ta.cons_base,  # pyrefly: ignore[missing-attribute]
        ta.mono_long,  # pyrefly: ignore[missing-attribute]
        ta.diph_base,  # pyrefly: ignore[missing-attribute]
        ta.mono_base_long,  # pyrefly: ignore[missing-attribute]
        ta.mono_base,  # pyrefly: ignore[missing-attribute]
    )
    self.AssertEqualFstLike(
        fl.FstList('zha', ta2.to_brahmic()).compose(), 'ஃஜ்ஹ'
    )
    self.AssertEqualFstLike(
        fl.FstList('kha', ta2.to_brahmic()).compose(), 'க்ஹ'
    )

if __name__ == '__main__':
  absltest.main()
