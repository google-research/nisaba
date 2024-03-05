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
from nisaba.scripts.natural_translit.utils import expression as exp


def _sym_inventory() -> exp.Symbol.Inventory:
  syms = exp.Symbol.Inventory(
      'test',
      exp.Symbol(
          'schwa',
          text='🜔',
          index=exp.Symbol.ReservedIndex.GRAPHEME_PREFIX + 1,
          name='SCHWA',
      ),
      exp.Symbol(
          'a_ind',
          text='अ',
          raw='अ',
          index=exp.Symbol.ReservedIndex.GRAPHEME_PREFIX + 2,
          name='A LETTER',
      ),
  )
  syms.make_supl('atm_sym', {exp.Atomic(sym): sym for sym in syms})
  syms.add_supl(
      exp.Symbol.Inventory('atm', *syms.atm_sym)
  )
  return syms
_SYM = _sym_inventory()


class ExpressionTest(absltest.TestCase):

  def test_symbol_abstract(self):
    self.assertEqual(str(_SYM.schwa), '🜔')
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

  def test_symbol_atomic(self):
    self.assertIs(exp.Atomic.read(_SYM.schwa).symbol, _SYM.schwa)
    self.assertIs(exp.Atomic.read(exp.Symbol.CTRL.eps), exp.Atomic.CTRL.eps)
    self.assertIs(exp.Atomic.read(exp.Atomic.CTRL.unk), exp.Atomic.CTRL.unk)

  def test_control(self):
    self.assertTrue(exp.Symbol.CTRL.eps.is_control())
    self.assertTrue(exp.Atomic.CTRL.unk.is_control())

  def test_symbol_equal(self):
    self.assertTrue(exp.Atomic.CTRL.eps.is_equal(exp.Symbol.CTRL.eps))

  def test_symbol_inventory_assignment(self):
    self.assertTrue(_SYM.a_ind.inventory, _SYM)
    self.assertEqual(_SYM.CTRL.unk.inventory, exp.Symbol.Inventory.EMPTY)

  def test_recurring_alias(self):
    syms1 = [exp.Symbol(alias='schwa'), exp.Symbol(alias='a_ind')]
    syms2 = [exp.Symbol(alias='schwa'), exp.Symbol(alias='a_ind')]
    inventory = exp.Symbol.Inventory('recurring')
    self.assertEqual(inventory.add_symbols(*syms1), syms1)
    self.assertNotEqual(inventory.add_symbols(*syms2), syms2)

  def test_symbol_inventory_lookup(self):
    self.assertEqual(_SYM.index_lookup(2000001), _SYM.schwa)
    self.assertEqual(_SYM.raw_lookup('अ'), _SYM.a_ind)
    self.assertEqual(_SYM.text_lookup('🜔'), _SYM.schwa)
    self.assertEqual(_SYM.raw_lookup('🜔'), _SYM.CTRL.unk)
    self.assertEqual(_SYM.lookup(_SYM.atm.schwa, 'atm_sym'), _SYM.schwa)

  def test_atomic_from_symbol(self):
    self.assertEqual(str(_SYM.atm.schwa), str(_SYM.schwa))
    self.assertEmpty(_SYM.atm.schwa.raw)
    self.assertIn(_SYM.atm.schwa, _SYM.atm.schwa)
    self.assertIs(_SYM.atm.schwa.symbol, _SYM.schwa)
    self.assertEqual(_SYM.atm.schwa.index, _SYM.schwa.index)
    self.assertIn(exp.Symbol.SYM_FEATURES.type.abst, _SYM.atm.schwa.features)
    self.assertEqual(
        _SYM.atm.schwa.description(show_features=True),
        'alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}',
    )

  def test_atomic_from_atomic(self):
    atm_schwa2 = exp.Atomic.read(_SYM.atm.schwa)
    self.assertEqual(str(atm_schwa2), str(_SYM.schwa))
    self.assertEmpty(atm_schwa2.raw)
    self.assertIn(atm_schwa2, atm_schwa2)
    self.assertNotIn(_SYM.atm.schwa, atm_schwa2)
    self.assertIs(atm_schwa2.symbol, _SYM.schwa)
    self.assertEqual(atm_schwa2.index, _SYM.schwa.index)
    self.assertEqual(
        atm_schwa2.description(),
        'alias: schwa  index: 2000001  text: 🜔  name: SCHWA',
    )
    _SYM.atm.schwa.add(atm_schwa2)
    self.assertEqual(_SYM.atm.schwa._items, [_SYM.atm.schwa])

  def test_controls(self):
    self.assertEqual(
        exp.Symbol.descriptions(*exp.Symbol.CTRL),
        'symbols:\n'
        '  alias: eps  index: 1000000  text: ⍷  name: EPSILON\n'
        '  alias: unk  index: 1000001  text: ⍰  name: UNKNOWN SYMBOL\n'
        '  alias: bos  index: 1000002  text: ⍄  name: BEGINNING OF SEQUENCE\n'
        '  alias: eos  index: 1000003  text: ⍃  name: END OF SEQUENCE\n'
        '  alias: oos  index: 1000004  text: ⍔  name: OUT OF SEQUENCE\n',
    )

  def test_symbol_inventory_str(self):
    self.assertEqual(
        str(_SYM),
        'test inventory:\n\n'
        '  alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n\n'
        '  alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n\n'
    )

  def test_symbol_inventory_description(self):
    self.assertEqual(
        _SYM.description(show_features=True, show_control=True),
        'test inventory:\n\n'
        '  alias: eps  index: 1000000  text: ⍷  name: EPSILON\n'
        '    features: {abstract, control}\n\n'
        '  alias: unk  index: 1000001  text: ⍰  name: UNKNOWN SYMBOL\n'
        '    features: {abstract, control}\n\n'
        '  alias: bos  index: 1000002  text: ⍄  name: BEGINNING OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: eos  index: 1000003  text: ⍃  name: END OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: oos  index: 1000004  text: ⍔  name: OUT OF SEQUENCE\n'
        '    features: {abstract, control}\n\n'
        '  alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}\n\n'
        '  alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}\n\n'
    )

if __name__ == '__main__':
  absltest.main()
