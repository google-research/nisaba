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
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import test_op


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


_SYM = _sym_inventory()


class SymbolTest(test_op.TestCase):

  def test_symbol_abstract(self):
    self.AssertStrEqual(_SYM.schwa, '🜔')
    self.assertEmpty(_SYM.schwa.raw)
    self.assertEqual(
        _SYM.schwa.description(show_features=True),
        'alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}',
    )

  def test_symbol_raw(self):
    self.assertEqual(
        _SYM.a_ind.description(show_features=True),
        'alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}',
    )

  def test_control(self):
    self.assertTrue(sym.Symbol.CTRL.eps.is_control())

  def test_symbol_inventory_assignment(self):
    self.assertTrue(_SYM.a_ind.inventory, _SYM)
    self.assertEqual(_SYM.CTRL.unk.inventory, sym.Symbol.Inventory.EMPTY)

  def test_recurring_alias(self):
    syms1 = [sym.Symbol(alias='schwa'), sym.Symbol(alias='a_ind')]
    syms2 = [sym.Symbol(alias='schwa'), sym.Symbol(alias='a_ind')]
    inventory = sym.Symbol.Inventory('recurring')
    self.assertEqual(inventory.add_symbols(*syms1), syms1)
    self.assertNotEqual(inventory.add_symbols(*syms2), syms2)

  def test_symbol_inventory_lookup(self):
    self.assertEqual(_SYM.index_lookup(2000001), _SYM.schwa)
    self.assertEqual(_SYM.raw_lookup('अ'), _SYM.a_ind)
    self.assertEqual(_SYM.text_lookup('🜔'), _SYM.schwa)
    self.assertEqual(_SYM.raw_lookup('🜔'), _SYM.CTRL.unk)

  def test_controls(self):
    self.assertEqual(
        sym.Symbol.descriptions(*sym.Symbol.CTRL),
        'symbols:\n'
        '  alias: eps  index: 1000000  text: ​ℰ​  name: EPSILON\n'
        '  alias: unk  index: 1000001  text: ​␦​  name: UNKNOWN SYMBOL\n'
        '  alias: bos  index: 1000002  text: ​⊳​  name: BEGINNING OF SEQUENCE\n'
        '  alias: eos  index: 1000003  text: ​⊲​  name: END OF SEQUENCE\n'
        '  alias: oos  index: 1000004  text: ​⊽​  name: OUT OF SEQUENCE\n'
        '  alias: nor  index: 1000005  text: ​◎​  name: NO ALTERNATIVE\n',
    )

  def test_symbol_inventory_str(self):
    self.AssertStrEqual(
        _SYM,
        'test inventory:\n\n'
        '  alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n\n'
        '  alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n\n',
    )

  def test_symbol_inventory_description(self):
    self.assertEqual(
        _SYM.description(show_features=True, show_control=True),
        'test inventory:\n\n'
        '  alias: eps  index: 1000000  text: ​ℰ​  name: EPSILON\n'
        '    features: {abstract, control}\n\n'
        '  alias: unk  index: 1000001  text: ​␦​  name: UNKNOWN SYMBOL\n'
        '    features: {abstract, control}\n\n'
        '  alias: bos  index: 1000002  text: ​⊳​  name: BEGINNING OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: eos  index: 1000003  text: ​⊲​  name: END OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: oos  index: 1000004  text: ​⊽​  name: OUT OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: nor  index: 1000005  text: ​◎​  name: NO ALTERNATIVE\n'
        '    features: {abstract, control}\n\n'
        '  alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}\n\n'
        '  alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}\n\n',
    )


if __name__ == '__main__':
  absltest.main()
