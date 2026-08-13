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
from nisaba.scripts.natural_translit.utils import feature as ft
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import test_op

_CTRL = sym.Symbol.CTRL  # pyrefly: ignore[missing-attribute]
_SYM_FTR = sym.Symbol.SYM_FEATURES
_TEST_FTR = ft.Feature.Inventory(
    'test_features',
    ft.Feature.Aspect(
        ft.Feature.equidistant(
            'case',
            ft.Feature('upper'),
            ft.Feature('lower'),
        )
    ),
    ft.Feature.Aspect(
        ft.Feature.equidistant(
            'sym_class',
            ft.Feature('digit'),
            ft.Feature('letter'),
        )
    ),
)


def _sym_inventory() -> sym.Symbol.Inventory:
  syms = sym.Symbol.Inventory(
      'test',
      sym.Symbol(
          'schwa',
          text='🜔',
          index=sym.Symbol.ReservedIndex.GRAPHEME_PREFIX + 1,
          name='SCHWA',
      ),
      sym.Symbol(
          'a_ind',
          text='अ',
          raw='अ',
          index=sym.Symbol.ReservedIndex.GRAPHEME_PREFIX + 2,
          name='A LETTER',
      ),
  )
  return syms


def _latn_inventory() -> sym.Symbol.Inventory:
  syms = sym.Symbol.Inventory(
      'test',
      sym.Symbol('a', text='a', raw='a', name='LETTER A'),
      sym.Symbol('b', text='b', raw='b', name='LETTER B'),
      sym.Symbol('i', text='i', raw='i', name='LETTER I'),
      sym.Symbol('i_uc', text='I', raw='I', name='UPPERCASE LETTER I'),
  )
  syms.make_iterable_suppl('letter', syms.a, syms.b, syms.i, syms.i_uc)  # pyrefly: ignore[missing-attribute]
  syms.add_symbols(
      sym.Symbol('digit_1', text='1', raw='1', name='DIGIT ONE'),
      sym.Symbol('digit_2', text='2', raw='2', name='DIGIT TWO'),
      list_alias='digit',
  )
  for symbol in syms:
    symbol.features.new_profile(ft.Feature.Profile(_TEST_FTR, 'new'))
  return syms


_SYM = _sym_inventory()
_DEVA = sym.Symbol.Inventory('deva', *_SYM)
_LATN = _latn_inventory()
_COMBINED = sym.Symbol.Inventory('combined', *_DEVA, *_LATN)


class SymbolTest(test_op.TestCase):

  def test_item(self):
    item = sym.Item('alias', 'text', 1)
    self.assertEqual(item.alias, 'alias')
    self.assertEqual(item.text, 'text')
    self.assertEqual(item.index, 1)
    self.assertEqual(
        item.symbols_str(),
        '[\n'
        ']\n'
    )

  def test_symbol_abstract(self):
    self.AssertStrEqual(_SYM.schwa, '🜔')  # pyrefly: ignore[missing-attribute]
    self.assertEmpty(_SYM.schwa.raw)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(
        _SYM.schwa.description(show_features=True),  # pyrefly: ignore[missing-attribute]
        'alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}',
    )

  def test_symbol_raw(self):
    self.assertEqual(
        _SYM.a_ind.description(show_features=True),  # pyrefly: ignore[missing-attribute]
        'alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}',
    )

  def test_control(self):
    self.assertTrue(_CTRL.eps.is_control())

  def test_symbol_inventory_assignment(self):
    self.assertTrue(_SYM.a_ind.inventory, _SYM)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_CTRL.unk.inventory, sym.Symbol.Inventory.EMPTY)  # pyrefly: ignore[missing-attribute]

  def test_recurring_alias(self):
    syms1 = [sym.Symbol(alias='schwa'), sym.Symbol(alias='a_ind')]
    syms2 = [sym.Symbol(alias='schwa'), sym.Symbol(alias='a_ind')]
    inventory = sym.Symbol.Inventory('recurring')
    self.assertEqual(inventory.add_symbols(*syms1), syms1)
    self.assertNotEqual(inventory.add_symbols(*syms2), syms2)

  def test_symbol_inventory_lookup(self):
    self.assertEqual(_SYM.index_lookup(2000001), _SYM.schwa)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_SYM.raw_lookup('अ'), _SYM.a_ind)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_SYM.text_lookup('🜔'), _SYM.schwa)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_SYM.raw_lookup('🜔'), _CTRL.unk)

  def test_symbol_inventory_iterable_suppl(self):
    self.assertEqual(_LATN.letter.alias, 'letter')  # pyrefly: ignore[missing-attribute]
    self.assertIn(_LATN.a, _LATN.letter)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.digit.alias, 'digit')  # pyrefly: ignore[missing-attribute]
    self.assertIn(_LATN.digit_1, _LATN.digit)  # pyrefly: ignore[missing-attribute]

  def test_controls(self):
    self.assertEqual(
        sym.Symbol.descriptions(*_CTRL),
        'symbols:\n'
        '  alias: eps  index: 1000000  text: ​ℰ​  name: EPSILON\n'
        '  alias: unk  index: 1000001  text: ​␦​  name: UNKNOWN SYMBOL\n'
        '  alias: bos  index: 1000002  text: ​⊳​  name: BEGINNING OF SEQUENCE\n'
        '  alias: eos  index: 1000003  text: ​⊲​  name: END OF SEQUENCE\n'
        '  alias: oos  index: 1000004  text: ​⊽​  name: OUT OF SEQUENCE\n'
        '  alias: nor  index: 1000005  text: ​◎​  name: NO ALTERNATIVE\n'
        '  alias: nos  index: 1000006  text: ​⨱​  name: NO SYMBOL\n',
    )

  def test_symbol_inventory_str(self):
    self.assertEqual(
        _SYM.description(show_features=False),
        '## Inventory: test\n\n'
        '### alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '### alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n',
    )

  def test_symbol_inventory_description(self):
    self.assertEqual(
        _SYM.description(show_features=True, show_control=True),
        '## Inventory: test\n\n'
        '### alias: eps  index: 1000000  text: ​ℰ​  name: EPSILON\n'
        '    features: {abstract, control}\n'
        '### alias: unk  index: 1000001  text: ​␦​  name: UNKNOWN SYMBOL\n'
        '    features: {abstract, control}\n'
        '### alias: bos  index: 1000002  text: ​⊳​  name: BEGINNING OF SEQUENCE\n'
        '    features: {abstract, control}\n'
        '### alias: eos  index: 1000003  text: ​⊲​  name: END OF SEQUENCE\n'
        '    features: {abstract, control}\n'
        '### alias: oos  index: 1000004  text: ​⊽​  name: OUT OF SEQUENCE\n'
        '    features: {abstract, control}\n'
        '### alias: nor  index: 1000005  text: ​◎​  name: NO ALTERNATIVE\n'
        '    features: {abstract, control}\n'
        '### alias: nos  index: 1000006  text: ​⨱​  name: NO SYMBOL\n'
        '    features: {abstract, control}\n'
        '### alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}\n'
        '### alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}\n',
    )

  def test_raw_from_unknown(self):
    _LATN.raw_from_unknown('c')
    self.assertEqual(
        _LATN.from_unk_1.description(),  # pyrefly: ignore[missing-attribute]
        'alias: from_unk_1  index: 9000001  raw: c  text: <from_unk_1_c>'
        '  name: from_unk_1_c',
    )

  def test_str_to_raw_symbols(self):
    self.assertEqual(
        _DEVA.str_to_raw_symbols('अ🐱'), [_DEVA.a_ind, _DEVA.from_unk_1]  # pyrefly: ignore[missing-attribute]
    )
    self.assertEqual(
        _SYM.str_to_raw_symbols('अ🐶', _DEVA),
        [_DEVA.a_ind, _DEVA.from_unk_2],  # pyrefly: ignore[missing-attribute]
    )
    self.assertEqual(_SYM.raw_lookup('🐶'), _CTRL.unk)

  def test_parse(self):
    self.assertEqual(_DEVA.parse('अa', _COMBINED), [_DEVA.a_ind, _LATN.a])  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_DEVA.parse('🦄', _COMBINED), [_COMBINED.from_unk_1])  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.parse('🦄', _COMBINED), [_COMBINED.from_unk_1])  # pyrefly: ignore[missing-attribute]

  def test_has_feature(self):
    x = sym.Symbol('x', 'x')
    x.add_features(_SYM_FTR.type.imp)  # pyrefly: ignore[missing-attribute]
    self.AssertHasFeature(x, _SYM_FTR.type.imp)  # pyrefly: ignore[missing-attribute]
    self.AssertHasFeature(x, _SYM_FTR.type.abst)  # pyrefly: ignore[missing-attribute]
    self.AssertNotHasFeature(x, _SYM_FTR.type.raw)  # pyrefly: ignore[missing-attribute]

  def test_set_attribute(self):
    _LATN.digit_2.set_attribute(  # pyrefly: ignore[missing-attribute]
        'numeric', 2, features_to_add=_TEST_FTR.sym_class.digit  # pyrefly: ignore[missing-attribute]
    )
    self.assertEqual(_LATN.digit_2.numeric, 2)  # pyrefly: ignore[missing-attribute]
    self.AssertHasFeature(_LATN.digit_2, _TEST_FTR.sym_class.digit)  # pyrefly: ignore[missing-attribute]

  def test_set_attribute_control(self):
    _CTRL.eps.set_attribute(
        'numeric', 2, features_to_add=_TEST_FTR.sym_class.digit  # pyrefly: ignore[missing-attribute]
    )
    self.assertRaises(AttributeError, getattr, _CTRL.eps, 'numeric')
    self.AssertNotHasFeature(_CTRL.eps, _TEST_FTR.sym_class.digit)  # pyrefly: ignore[missing-attribute]

  def test_feature_pair_add_true(self):
    _LATN.i.feature_pair(_LATN.i_uc, _TEST_FTR.case.lower, _TEST_FTR.case.upper)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i.case, _TEST_FTR.case.lower)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i.upper, _LATN.i_uc)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i.lower, _LATN.i)  # pyrefly: ignore[missing-attribute]
    self.AssertHasFeature(_LATN.i, _TEST_FTR.case.lower)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i_uc.case, _TEST_FTR.case.upper)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i_uc.lower, _LATN.i)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i_uc.upper, _LATN.i_uc)  # pyrefly: ignore[missing-attribute]
    self.AssertHasFeature(_LATN.i_uc, _TEST_FTR.case.upper)  # pyrefly: ignore[missing-attribute]

  def test_feature_pair_add_false(self):
    _LATN.digit_1.feature_pair(  # pyrefly: ignore[missing-attribute]
        _LATN.i_uc,  # pyrefly: ignore[missing-attribute]
        _TEST_FTR.sym_class.digit,  # pyrefly: ignore[missing-attribute]
        _TEST_FTR.sym_class.letter,  # pyrefly: ignore[missing-attribute]
        add_aspect=False,
        add_features=False,
    )
    self.assertEqual(_LATN.digit_1.letter, _LATN.i_uc)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.i_uc.digit, _LATN.digit_1)  # pyrefly: ignore[missing-attribute]
    self.assertRaises(AttributeError, getattr, _LATN.digit_1, 'sym_class')  # pyrefly: ignore[missing-attribute]
    self.assertRaises(AttributeError, getattr, _LATN.i_uc, 'sym_class')  # pyrefly: ignore[missing-attribute]
    self.AssertNotHasFeature(_LATN.digit_1, _TEST_FTR.sym_class.digit)  # pyrefly: ignore[missing-attribute]
    self.AssertNotHasFeature(_LATN.i_uc, _TEST_FTR.sym_class.letter)  # pyrefly: ignore[missing-attribute]

  def test_feature_pair_with_control(self):
    _LATN.digit_2.feature_pair(  # pyrefly: ignore[missing-attribute]
        _CTRL.nor, _TEST_FTR.sym_class.digit, _TEST_FTR.sym_class.letter  # pyrefly: ignore[missing-attribute]
    )
    self.assertEqual(_LATN.digit_2.letter, _CTRL.nos)  # pyrefly: ignore[missing-attribute]
    self.assertEqual(_LATN.digit_2.sym_class, _TEST_FTR.sym_class.digit)  # pyrefly: ignore[missing-attribute]
    self.assertRaises(AttributeError, getattr, _CTRL.nor, 'digit')
    self.assertRaises(AttributeError, getattr, _CTRL.nor, 'sym_class')
    self.AssertHasFeature(_LATN.digit_2, _TEST_FTR.sym_class.digit)  # pyrefly: ignore[missing-attribute]
    self.AssertNotHasFeature(_CTRL.nor, _TEST_FTR.sym_class.letter)  # pyrefly: ignore[missing-attribute]


if __name__ == '__main__':
  absltest.main()
