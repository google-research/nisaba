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
from nisaba.scripts.natural_translit.phonology import phonological_symbol as po
from nisaba.scripts.natural_translit.utils import test_op


def _test_inventory() -> po.Phon.Inventory:
  """Multilingual Phon inventory."""
  phf = po.Phon.DESCRIPTIVE_FEATURES
  ph_inv = po.Phon.Inventory()
  vowels = [
      ('a', 'a', 'open front unrounded vowel'),
      ('e', 'e', 'close_mid front unrounded vowel'),
      ('i', 'i', 'close front unrounded vowel'),
  ]
  ph_inv.add_phonemes(
      *(
          po.Phon(alias=alias, ipa=ipa, name=name, features=phf.vowel)
          for ipa, alias, name in vowels
      ),
      list_alias='vowel',
  )
  # Default heights from IPA vowel table.
  ph_inv.a.update_descriptives(
      phf.height.open, phf.backness.front, phf.labialization.unrounded
  )
  ph_inv.e.update_descriptives(
      phf.height.close_mid, phf.backness.front, phf.labialization.unrounded
  )
  ph_inv.i.update_descriptives(
      phf.height.close, phf.backness.front, phf.labialization.unrounded
  )
  ph_inv.make_iterable_suppl('close_like', ph_inv.e)
  ph_inv.or_from_suppl(ph_inv.close_like)
  ph_inv.close_like.add(ph_inv.i)
  return ph_inv.sync_atomics([ph_inv.vowel, ph_inv.close_like])


_TEST = _test_inventory()


class PhonologicalSymbolTest(test_op.TestCase):

  def test_phon_inventory(self):
    self.assertEqual(_TEST.alias, 'x_mul')
    self.assertIn(_TEST.a, _TEST.vowel)

  def test_phon_description(self):
    self.assertEqual(
        _TEST.a.description(show_features=True),
        'alias: a\tipa: a\tname: open front unrounded vowel\n'
        '  a features:\n\n'
        '| aspects          | values         |\n'
        '|------------------|----------------|\n'
        '| **sym_features** |                |\n'
        '| type             | abstract       |\n'
        '| **descriptive**  |                |\n'
        '| ph_class         | vowel          |\n'
        '| airstream        | pulmonic       |\n'
        '| manner           | not_applicable |\n'
        '| place            | not_applicable |\n'
        '| articulator      | not_applicable |\n'
        '| height           | open           |\n'
        '| backness         | front          |\n'
        '| breathiness      | none           |\n'
        '| voicing          | voiced         |\n'
        '| labialization    | unrounded      |\n'
        '| lateralization   | not_applicable |\n'
        '| nasalization     | none           |\n'
        '| palatalization   | none           |\n'
        '| rhoticization    | none           |\n'
        '| duration         | any            |\n'
        '| syllabicity      | syllabic       |\n',
    )

  def test_has_feature(self):
    self.AssertHasFeature(
        _TEST.i, po.Phon.DESCRIPTIVE_FEATURES.ph_class.vowel
    )

  def test_phon_copy(self):
    self.assertEqual(
        _TEST.a.copy(alias='a_copy').description(show_features=True),
        'alias: a_copy\tipa: a\tname: open front unrounded vowel\n'
        '  a_copy features:\n\n'
        '| aspects          | values         |\n'
        '|------------------|----------------|\n'
        '| **sym_features** |                |\n'
        '| type             | abstract       |\n'
        '| **descriptive**  |                |\n'
        '| ph_class         | vowel          |\n'
        '| airstream        | pulmonic       |\n'
        '| manner           | not_applicable |\n'
        '| place            | not_applicable |\n'
        '| articulator      | not_applicable |\n'
        '| height           | open           |\n'
        '| backness         | front          |\n'
        '| breathiness      | none           |\n'
        '| voicing          | voiced         |\n'
        '| labialization    | unrounded      |\n'
        '| lateralization   | not_applicable |\n'
        '| nasalization     | none           |\n'
        '| palatalization   | none           |\n'
        '| rhoticization    | none           |\n'
        '| duration         | any            |\n'
        '| syllabicity      | syllabic       |\n',
    )

  def test_phon_update_descriptives(self):
    self.assertEqual(
        _TEST.e.copy(alias='ee', ipa='e̞')
        .update_descriptives(po.Phon.DESCRIPTIVE_FEATURES.height.mid)
        .description(show_features=True),
        'alias: ee\tipa: e̞\tname: close_mid front unrounded vowel\n'
        '  ee features:\n\n'
        '| aspects          | values         |\n'
        '|------------------|----------------|\n'
        '| **sym_features** |                |\n'
        '| type             | abstract       |\n'
        '| **descriptive**  |                |\n'
        '| ph_class         | vowel          |\n'
        '| airstream        | pulmonic       |\n'
        '| manner           | not_applicable |\n'
        '| place            | not_applicable |\n'
        '| articulator      | not_applicable |\n'
        '| height           | mid            |\n'
        '| backness         | front          |\n'
        '| breathiness      | none           |\n'
        '| voicing          | voiced         |\n'
        '| labialization    | unrounded      |\n'
        '| lateralization   | not_applicable |\n'
        '| nasalization     | none           |\n'
        '| palatalization   | none           |\n'
        '| rhoticization    | none           |\n'
        '| duration         | any            |\n'
        '| syllabicity      | syllabic       |\n',
    )

  def test_sync_atomics(self):
    self.AssertStrEqual(_TEST.atomics.a.features, _TEST.a.features)
    self.AssertStrEqual(_TEST.atomics.vowel, '(a | e | i)')
    self.AssertStrEqual(_TEST.atomics.close_like, '(e | i)')

if __name__ == '__main__':
  absltest.main()
