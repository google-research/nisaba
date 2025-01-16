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
from nisaba.scripts.natural_translit.script import grapheme as g
from nisaba.scripts.natural_translit.utils import test_op

_UND_GRAPHEMES = g.Grapheme.Inventory(g.Grapheme.GR_FEATURES.script.und)


class GraphemeTest(test_op.TestCase):

  def test_script_iso(self):
    self.AssertStrEqual(
        g.Grapheme.GR_FEATURES.script.latn,
        'alias: latn text: Latin numeric: 215',
    )

  def test_script_custom(self):
    self.AssertStrEqual(
        g.Grapheme.GR_FEATURES.script.br,
        'alias: br text: Brahmic Parent numeric: 801',
    )

  def test_from_char_index(self):
    self.assertEqual(
        g.Grapheme.from_char('a').index,
        g.Grapheme.ReservedIndex.GRAPHEME_PREFIX + 97,
    )

  def test_from_char_name(self):
    self.assertEqual(g.Grapheme.from_char('🐱').name, 'CAT FACE U+0X1F431')

  def test_from_char_name_error(self):
    self.assertEqual(
        g.Grapheme.from_char(chr(0xE027)).name, 'GRAPHEME U+0XE027'
    )

  def test_from_char_alias_explicit(self):
    self.assertEqual(g.Grapheme.from_char('ç', 'c_ced').alias, 'c_ced')

  def test_from_char_alias_default(self):
    self.assertEqual(g.Grapheme.from_char('ç').alias, 'u_0xe7')

  def test_from_char_has_feature(self):
    self.assertIn(
        g.Grapheme.SYM_FEATURES.type.raw, g.Grapheme.from_char('a').features
    )

  def test_from_char_add_feature(self):
    self.assertIn(
        g.Grapheme.GR_FEATURES.ph_class.cons,
        g.Grapheme.from_char(
            'n', features=g.Grapheme.GR_FEATURES.ph_class.cons
        ).features,
    )

  def test_control_index(self):
    self.assertEqual(
        _UND_GRAPHEMES.CTRL.eps.index, g.Grapheme.ReservedIndex.CONTROL_PREFIX
    )

  def test_control_in_text_dict(self):
    self.assertIn(g.Grapheme.CTRL.unk.text, _UND_GRAPHEMES.text_dict)

  def test_control_not_in_raw_dict(self):
    self.assertNotIn(g.Grapheme.CTRL.unk.text, _UND_GRAPHEMES.raw_dict)

  def test_control_in_index_dict(self):
    self.assertIn(g.Grapheme.CTRL.oos.index, _UND_GRAPHEMES.index_dict)

  def test_inventory(self):
    self.assertEqual(_UND_GRAPHEMES.alias, 'und')
    self.assertEqual(_UND_GRAPHEMES.prefix, 2_800_000)

  def test_add_grapheme_in_dicts(self):
    char = 'ß'
    _UND_GRAPHEMES.add_graphemes(g.Grapheme.from_char(char, alias='ss'))
    self.assertEqual(_UND_GRAPHEMES.raw_lookup(char), _UND_GRAPHEMES.ss)
    self.assertEqual(_UND_GRAPHEMES.text_lookup(char), _UND_GRAPHEMES.ss)
    self.assertEqual(
        _UND_GRAPHEMES.index_lookup(
            g.Grapheme.ReservedIndex.GRAPHEME_PREFIX + ord(char)
        ),
        _UND_GRAPHEMES.ss,
    )
    self.assertNotEqual(_UND_GRAPHEMES.atomics.ss, _UND_GRAPHEMES.ss)
    self.AssertEquivalent(_UND_GRAPHEMES.atomics.ss, _UND_GRAPHEMES.ss)

  def test_add_grapheme_recurring_alias(self):
    _UND_GRAPHEMES.add_graphemes(g.Grapheme.from_char('œ', alias='oe'))
    self.assertFalse(
        _UND_GRAPHEMES.add_graphemes(g.Grapheme.from_char('Œ', alias='oe'))
    )

  def test_add_grapheme_wrong_type(self):
    self.assertFalse(_UND_GRAPHEMES._add_symbol(g.Grapheme.CTRL.eps))

  def test_add_graphemes(self):
    _UND_GRAPHEMES.add_graphemes(
        g.Grapheme.from_char('(', 'prl'),
        g.Grapheme.from_char(')', 'prr'),
        list_alias='parentheses',
    )
    self.assertIn(_UND_GRAPHEMES.prl, _UND_GRAPHEMES)
    self.assertIn(_UND_GRAPHEMES.prl, _UND_GRAPHEMES.parentheses)

  def test_get_grapheme_in_inventory(self):
    _UND_GRAPHEMES.add_graphemes(g.Grapheme.from_char('æ', alias='ae'))
    self.assertEqual(_UND_GRAPHEMES.text_lookup('æ'), _UND_GRAPHEMES.ae)

  def test_get_grapheme_out_of_inventory_char(self):
    self.assertEqual(_UND_GRAPHEMES.text_lookup('🐱'), _UND_GRAPHEMES.CTRL.unk)

  def test_parse(self):
    self.assertIn(_UND_GRAPHEMES.raw_from_unknown('ç'), _UND_GRAPHEMES)
    # Adding the same grapheme again fails and returns CTRL.nor
    self.assertIs(_UND_GRAPHEMES.raw_from_unknown('ç'), _UND_GRAPHEMES.CTRL.nor)
    self.assertEqual(
        _UND_GRAPHEMES.parse('ş'), [_UND_GRAPHEMES.get('u_' + hex(ord('ş')))]
    )
    self.assertIn(
        g.Grapheme.ReservedIndex.GRAPHEME_PREFIX + ord('ş'),
        _UND_GRAPHEMES.index_dict,
    )


if __name__ == '__main__':
  absltest.main()
