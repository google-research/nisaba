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

_test = g.Grapheme.Inventory(g.Grapheme.GR_FEATURES.script.und)


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
    self.assertEqual(g.Grapheme.from_char(chr(0xcf3)).name, 'GRAPHEME U+0XCF3')

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
        _test.CTRL.eps.index, g.Grapheme.ReservedIndex.CONTROL_PREFIX
    )

  def test_control_in_text_dict(self):
    self.assertIn(g.Grapheme.CTRL.unk.text, _test.text_dict)

  def test_control_not_in_raw_dict(self):
    self.assertNotIn(g.Grapheme.CTRL.unk.text, _test.raw_dict)

  def test_control_in_index_dict(self):
    self.assertIn(g.Grapheme.CTRL.oos.index, _test.index_dict)

  def test_add_grapheme_in_dicts(self):
    char = 'ß'
    _test.add_symbols(g.Grapheme.from_char(char, alias='ss'))
    self.assertEqual(_test.raw_lookup(char), _test.ss)
    self.assertEqual(_test.text_lookup(char), _test.ss)
    self.assertEqual(
        _test.index_lookup(
            g.Grapheme.ReservedIndex.GRAPHEME_PREFIX + ord(char)
        ),
        _test.ss,
    )

  def test_add_grapheme_recurring_alias(self):
    _test.add_symbols(g.Grapheme.from_char('œ', alias='oe'))
    self.assertFalse(_test.add_symbols(g.Grapheme.from_char('Œ', alias='oe')))

  def test_add_grapheme_wrong_type(self):
    self.assertFalse(_test._add_symbol(g.Grapheme.CTRL.eps))

  def test_add_graphemes(self):
    _test.add_symbols(
        g.Grapheme.from_char('(', 'prl'),
        g.Grapheme.from_char(')', 'prr'),
        list_alias='parentheses',
    )
    self.assertIn(_test.prl, _test)
    self.assertIn(_test.prl, _test.parentheses)

  def test_get_grapheme_in_inventory(self):
    _test.add_symbols(g.Grapheme.from_char('æ', alias='ae'))
    self.assertEqual(_test.text_lookup('æ'), _test.ae)

  def test_get_grapheme_out_of_inventory_char(self):
    self.assertEqual(_test.text_lookup('🐱'), _test.CTRL.unk)

if __name__ == '__main__':
  absltest.main()
