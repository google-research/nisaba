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
from nisaba.scripts.natural_translit.phonology import descriptive_features
from nisaba.scripts.natural_translit.utils import inventory
from nisaba.scripts.natural_translit.utils import test_op


def _profiles() -> inventory.Inventory:
  f = descriptive_features.FEATURES
  profiles = inventory.Inventory.from_list([
      f.consonant.copy_and_update(
          'p',
          f.manner.stop,
          f.bilabial,
          f.voicing.voiceless,
      ),
      f.consonant.copy_and_update(
          'f',
          f.manner.non_sibilant,
          f.labiodental,
          f.voicing.voiceless,
      ),
      f.consonant.copy_and_update(
          's',
          f.manner.sibilant,
          f.para_alveolar,
          f.voicing.voiceless,
      ),
  ])
  profiles.add_item(
      profiles.s.copy_and_update('s_low_amplitude', f.manner.non_sibilant)
  )
  return profiles


_P = _profiles()


class DescriptiveFeaturesTest(test_op.TestCase):

  def test_profile_p(self):
    self.AssertStrEqual(
        _P.p,
        'Profile: {\n'
        '    ph_class: {consonant}\n'
        '    airstream: {pulmonic}\n'
        '    manner: {stop}\n'
        '    place: {labial}\n'
        '    articulator: {labial}\n'
        '    height: {not_applicable}\n'
        '    backness: {not_applicable}\n'
        '    breathiness: {any}\n'
        '    voicing: {voiceless}\n'
        '    labialization: {labialized}\n'
        '    lateralization: {none}\n'
        '    nasalization: {none}\n'
        '    palatalization: {none}\n'
        '    rhoticization: {none}\n'
        '    duration: {any}\n'
        '    syllabicity: {none}\n'
        '}\n',
    )

  def test_compare_p_f_verbose(self):
    self.assertEqual(
        _P.p.comparison_table(_P.f, verbose=True),
        'phonology_descriptive comparison (max distance = 23.50):\n\n'
        '| aspect         | p              | f              |   distance |\n'
        '|----------------|----------------|----------------|------------|\n'
        '| ph_class       | consonant      | consonant      |      0     |\n'
        '| airstream      | pulmonic       | pulmonic       |      0     |\n'
        '| manner         | stop           | non_sibilant   |      1     |\n'
        '| place          | labial         | dental         |      0.5   |\n'
        '| articulator    | labial         | labial         |      0     |\n'
        '| height         | not_applicable | not_applicable |      0     |\n'
        '| backness       | not_applicable | not_applicable |      0     |\n'
        '| breathiness    | any            | any            |      0     |\n'
        '| voicing        | voiceless      | voiceless      |      0     |\n'
        '| labialization  | labialized     | labialized     |      0     |\n'
        '| lateralization | none           | none           |      0     |\n'
        '| nasalization   | none           | none           |      0     |\n'
        '| palatalization | none           | none           |      0     |\n'
        '| rhoticization  | none           | none           |      0     |\n'
        '| duration       | any            | any            |      0     |\n'
        '| syllabicity    | none           | none           |      0     |\n'
        '| Total distance |                |                |      1.5   |\n'
        '| Similarity     |                |                |      0.936 |\n',
    )

  def test_compare_p_f(self):
    self.assertEqual(
        _P.p.comparison_table(_P.f),
        'phonology_descriptive comparison (max distance = 23.50):\n\n'
        '| aspect         | p      | f            |   distance |\n'
        '|----------------|--------|--------------|------------|\n'
        '| manner         | stop   | non_sibilant |      1     |\n'
        '| place          | labial | dental       |      0.5   |\n'
        '| Total distance |        |              |      1.5   |\n'
        '| Similarity     |        |              |      0.936 |\n',
    )

  def test_compare_f_s(self):
    self.assertEqual(
        _P.f.comparison_table(_P.s),
        'phonology_descriptive comparison (max distance = 23.50):\n\n'
        '| aspect         | f            | s               |   distance |\n'
        '|----------------|--------------|-----------------|------------|\n'
        '| manner         | non_sibilant | sibilant        |      0.5   |\n'
        '| articulator    | labial       | apical, laminal |      0.5   |\n'
        '| labialization  | labialized   | none            |      1     |\n'
        '| Total distance |              |                 |      2     |\n'
        '| Similarity     |              |                 |      0.915 |\n',
    )

  def test_compare_f_s_low_amplitude(self):
    self.assertEqual(
        _P.f.comparison_table(_P.s_low_amplitude),
        'phonology_descriptive comparison (max distance = 23.50):\n\n'
        '| aspect         | f          | s_low_amplitude   |   distance |\n'
        '|----------------|------------|-------------------|------------|\n'
        '| articulator    | labial     | apical, laminal   |      0.5   |\n'
        '| labialization  | labialized | none              |      1     |\n'
        '| Total distance |            |                   |      1.5   |\n'
        '| Similarity     |            |                   |      0.936 |\n',
    )

if __name__ == '__main__':
  absltest.main()
