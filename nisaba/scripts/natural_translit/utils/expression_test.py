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


def _basic_atm(char):
  return exp.Atomic(exp.Symbol(alias=char, text=char, raw=char))

_ATM = exp.Symbol.Inventory(
    'atomic_test',
    _basic_atm('a'), _basic_atm('b'), _basic_atm('c'), _basic_atm('d'),
)


class ExpressionTest(absltest.TestCase):

  def assertStrEqual(self, obj1: ..., obj2: ...):
    return self.assertEqual(str(obj1), str(obj2))

  def assertAccepts(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertTrue(expression.accepts(other))

  def assertNotAccepts(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertFalse(expression.accepts(other))

  def assertEquivalent(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertTrue(expression.is_equivalent(other))

  def assertNotEquivalent(
      self, expression: exp.Expression, other: exp.Expression.OR_SYMBOL
  ):
    return self.assertFalse(expression.is_equivalent(other))

  def test_symbol_abstract(self):
    self.assertStrEqual(_SYM.schwa, '🜔')
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
    self.assertStrEqual(_SYM.atm.schwa, _SYM.schwa)
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
    self.assertStrEqual(atm_schwa2, _SYM.schwa)
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
        '  alias: oos  index: 1000004  text: ⍔  name: OUT OF SEQUENCE\n'
        '  alias: nor  index: 1000005  text: ⍜  name: NO ALTERNATIVE\n'
    )

  def test_symbol_inventory_str(self):
    self.assertStrEqual(
        _SYM,
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
        '  alias: nor  index: 1000005  text: ⍜  name: NO ALTERNATIVE\n'
        '    features: {abstract, control}\n\n'
        '  alias: schwa  index: 2000001  text: 🜔  name: SCHWA\n'
        '    features: {abstract}\n\n'
        '  alias: a_ind  index: 2000002  raw: अ  text: अ  name: A LETTER\n'
        '    features: {raw}\n\n'
    )

  def test_cat_empty(self):
    empty_cat = exp.Cat()
    self.assertEmpty(empty_cat)
    self.assertStrEqual(empty_cat, '⍷')

  def test_cat_control(self):
    eps_cat = exp.Cat(exp.Atomic.CTRL.eps)
    self.assertEmpty(eps_cat)
    self.assertStrEqual(eps_cat, '⍷')

  def test_cat_items(self):
    cat = exp.Cat(_ATM.a, _ATM.b, _ATM.a)
    self.assertLen(cat, 3)
    self.assertStrEqual(cat, '(a b a)')
    self.assertIsNot(cat.item(0), cat.item(2))
    self.assertEquivalent(cat.item(0), (cat.item(2)))

  def test_cat_nested(self):
    cat1 = exp.Cat(_ATM.a, _ATM.b)
    cat2 = exp.Cat(cat1, _ATM.c)
    or1 = exp.Or(_ATM.a)
    or2 = exp.Or(_ATM.b, _ATM.c)
    cat3 = exp.Cat(or1, or2)
    self.assertLen(cat2, 3)
    self.assertStrEqual(cat2, '(a b c)')
    self.assertStrEqual(exp.Cat(exp.Or()), '(⍜)')
    self.assertStrEqual(cat3, '(a (b | c))')

  def test_repeat(self):
    self.assertEmpty(_ATM.a.repeat(0))
    self.assertStrEqual(_ATM.a.repeat(), '(a a)')
    self.assertStrEqual(_ATM.a.repeat(3), '(a a a)')
    self.assertStrEqual(exp.Cat(_ATM.a, _ATM.b).repeat(), '(a b a b)')

  def test_or_no_alternative(self):
    or_eps = exp.Or(exp.Atomic.CTRL.eps)
    or0 = exp.Or()
    or1 = exp.Or(_ATM.a)
    self.assertEmpty(or_eps)
    self.assertEmpty(or0)
    self.assertLen(or1, 1)
    self.assertStrEqual(or_eps, '⍜')
    self.assertStrEqual(or0, '⍜')
    self.assertStrEqual(or1, '(a | ⍜)')

  def test_or_items(self):
    or1 = exp.Or(_ATM.a)
    or2 = exp.Or(_ATM.b, _ATM.c)
    or3 = exp.Or(or1, or2)
    or4 = exp.Or(_ATM.a, _ATM.b, _ATM.a)
    self.assertStrEqual(or2, '(b | c)')
    self.assertStrEqual(or3, '(a | b | c)')
    self.assertStrEqual(or4, '(a | b)')
    self.assertLen(or4, 2)

  def test_or_nested(self):
    cat1 = exp.Cat(_ATM.a)
    cat2 = exp.Cat(_ATM.b, _ATM.c)
    cat3 = exp.Cat(_ATM.a, exp.Or(_ATM.b, _ATM.c))
    or4 = exp.Or(cat1, cat2)
    or5 = exp.Or(cat3).add(exp.Cat(_ATM.a, _ATM.b))
    or6 = exp.Or(cat3).add(exp.Cat(_ATM.a, exp.Or(_ATM.b, _ATM.c, _ATM.d)))
    self.assertStrEqual(exp.Or(exp.Cat()), '(⍷ | ⍜)')
    self.assertStrEqual(or4, '(a | (b c))')
    self.assertStrEqual(or5, '((a (b | c)) | ⍜)')
    self.assertStrEqual(or6, '((a (b | c | d)) | ⍜)')

  def test_copy(self):
    exp1 = exp.Expression('new_exp')
    exp1_copy = exp1.copy()
    cat1 = exp.Cat(_ATM.a, _ATM.b)
    cat1_copy = cat1.copy()
    self.assertIsNot(exp1, exp1_copy)
    self.assertIs(exp.Atomic.CTRL.eps.copy(), exp.Atomic.CTRL.eps)
    self.assertIsNot(_ATM.a.copy(), _ATM.a)
    self.assertEquivalent(_ATM.a.copy(), _ATM.a)
    self.assertIsNot(cat1.item(0), cat1_copy.item(0))
    self.assertEquivalent(cat1, cat1_copy)

  def test_symbols(self):
    cat = exp.Cat(_ATM.a, _ATM.b, exp.Or(_ATM.c, _ATM.d))
    or1 = exp.Or(_ATM.a, _ATM.b, exp.Cat(_ATM.c, _ATM.d))
    self.assertEqual(
        exp.Expression().symbols_str(),
        '[\n'
        ']\n'
    )
    self.assertEqual(
        exp.Atomic.CTRL.eps.symbols_str(),
        '[\n'
        '  [⍷]\n'
        ']\n'
    )
    self.assertEqual(
        _ATM.a.symbols_str(),
        '[\n'
        '  [a]\n'
        ']\n'
    )
    self.assertEqual(
        cat.symbols_str(),
        '[\n'
        '  [a, b, c]\n'
        '  [a, b, d]\n'
        ']\n'
    )
    self.assertEqual(
        or1.symbols_str(),
        '[\n'
        '  [a]\n'
        '  [b]\n'
        '  [c, d]\n'
        ']\n'
    )

  def test_state_count(self):
    or1 = exp.Or(
        exp.Cat(_ATM.a, _ATM.b, _ATM.c), exp.Cat(_ATM.a, _ATM.b, _ATM.d)
    )
    or1_copy = or1.copy()
    cat = exp.Cat(_ATM.a, _ATM.b, exp.Or(_ATM.c, _ATM.d))
    self.assertEqual(exp.Atomic.CTRL.eps.state_count(), 1)
    self.assertEqual(_ATM.a.state_count(), 1)
    self.assertEqual(exp.Cat().state_count(), 0)
    self.assertEqual(cat.state_count(), 4)
    self.assertEqual(exp.Or().state_count(), 0)
    self.assertEqual(or1.state_count(), 6)
    self.assertEqual(or1_copy.add(cat).state_count(), 4)

  def test_equivalent(self):
    or0 = exp.Or()
    self.assertEquivalent(exp.Atomic.CTRL.eps, exp.Symbol.CTRL.eps)
    self.assertEquivalent(exp.Cat(), exp.Atomic.CTRL.eps)
    self.assertEquivalent(exp.Cat(), exp.Cat())
    self.assertNotEquivalent(or0, exp.Atomic.CTRL.nor)
    self.assertNotEquivalent(or0, or0)
    self.assertEquivalent(exp.Cat(_ATM.a), _ATM.a)
    self.assertEquivalent(
        exp.Cat(_ATM.a, _ATM.b, exp.Or(_ATM.c, _ATM.d)),
        exp.Or(
            exp.Cat(_ATM.a, _ATM.b, _ATM.c), exp.Cat(_ATM.a, _ATM.b, _ATM.d)
        ),
    )

if __name__ == '__main__':
  absltest.main()
