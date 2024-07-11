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

  def test_compare_p_f(self):
    self.assertEqual(
        _P.p.comparison(_P.f),
        'p - f phonology_descriptive comparison:\n'
        '    ph_class: {consonant} vs ph_class: {consonant} = 0.00\n'
        '    airstream: {pulmonic} vs airstream: {pulmonic} = 0.00\n'
        '    manner: {stop} vs manner: {non_sibilant} = 1.00\n'
        '    place: {labial} vs place: {dental} = 0.50\n'
        '    articulator: {labial} vs articulator: {labial} = 0.00\n'
        '    height: {not_applicable} vs height: {not_applicable} = 0.00\n'
        '    backness: {not_applicable} vs backness: {not_applicable} = 0.00\n'
        '    breathiness: {any} vs breathiness: {any} = 0.00\n'
        '    voicing: {voiceless} vs voicing: {voiceless} = 0.00\n'
        '    labialization: {labialized} vs labialization: {labialized} = 0.00'
        '\n'
        '    lateralization: {none} vs lateralization: {none} = 0.00\n'
        '    nasalization: {none} vs nasalization: {none} = 0.00\n'
        '    palatalization: {none} vs palatalization: {none} = 0.00\n'
        '    rhoticization: {none} vs rhoticization: {none} = 0.00\n'
        '    duration: {any} vs duration: {any} = 0.00\n'
        '    syllabicity: {none} vs syllabicity: {none} = 0.00\n'
        '    Total distance = 1.50/23.50\n'
        '    Similarity = 0.936\n',
    )

  def test_compare_f_s(self):
    self.assertEqual(
        _P.f.comparison(_P.s),
        'f - s phonology_descriptive comparison:\n'
        '    ph_class: {consonant} vs ph_class: {consonant} = 0.00\n'
        '    airstream: {pulmonic} vs airstream: {pulmonic} = 0.00\n'
        '    manner: {non_sibilant} vs manner: {sibilant} = 0.50\n'
        '    place: {dental} vs place: {alveolar, dental, postalveolar} = 0.00'
        '\n'
        '    articulator: {labial} vs articulator: {apical, laminal} = 0.50\n'
        '    height: {not_applicable} vs height: {not_applicable} = 0.00\n'
        '    backness: {not_applicable} vs backness: {not_applicable} = 0.00\n'
        '    breathiness: {any} vs breathiness: {any} = 0.00\n'
        '    voicing: {voiceless} vs voicing: {voiceless} = 0.00\n'
        '    labialization: {labialized} vs labialization: {none} = 1.00\n'
        '    lateralization: {none} vs lateralization: {none} = 0.00\n'
        '    nasalization: {none} vs nasalization: {none} = 0.00\n'
        '    palatalization: {none} vs palatalization: {none} = 0.00\n'
        '    rhoticization: {none} vs rhoticization: {none} = 0.00\n'
        '    duration: {any} vs duration: {any} = 0.00\n'
        '    syllabicity: {none} vs syllabicity: {none} = 0.00\n'
        '    Total distance = 2.00/23.50\n'
        '    Similarity = 0.915\n',
    )

  def test_compare_f_s_low_amplitude(self):
    self.assertEqual(
        _P.f.comparison(_P.s_low_amplitude),
        'f - s_low_amplitude phonology_descriptive comparison:\n'
        '    ph_class: {consonant} vs ph_class: {consonant} = 0.00\n'
        '    airstream: {pulmonic} vs airstream: {pulmonic} = 0.00\n'
        '    manner: {non_sibilant} vs manner: {non_sibilant} = 0.00\n'
        '    place: {dental} vs place: {alveolar, dental, postalveolar} = 0.00'
        '\n'
        '    articulator: {labial} vs articulator: {apical, laminal} = 0.50\n'
        '    height: {not_applicable} vs height: {not_applicable} = 0.00\n'
        '    backness: {not_applicable} vs backness: {not_applicable} = 0.00\n'
        '    breathiness: {any} vs breathiness: {any} = 0.00\n'
        '    voicing: {voiceless} vs voicing: {voiceless} = 0.00\n'
        '    labialization: {labialized} vs labialization: {none} = 1.00\n'
        '    lateralization: {none} vs lateralization: {none} = 0.00\n'
        '    nasalization: {none} vs nasalization: {none} = 0.00\n'
        '    palatalization: {none} vs palatalization: {none} = 0.00\n'
        '    rhoticization: {none} vs rhoticization: {none} = 0.00\n'
        '    duration: {any} vs duration: {any} = 0.00\n'
        '    syllabicity: {none} vs syllabicity: {none} = 0.00\n'
        '    Total distance = 1.50/23.50\n'
        '    Similarity = 0.936\n',
    )

if __name__ == '__main__':
  absltest.main()
