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
from nisaba.scripts.natural_translit.utils import symbol as sym
from nisaba.scripts.natural_translit.utils import test_op


def _basic_sym(char):
  return sym.Symbol(alias=char, text=char, raw=char)


_SYM = sym.Symbol.Inventory(
    'symbol',
    sym.Symbol('nul', '◌', index=123, name='NULL'),
    _basic_sym('a'),
    _basic_sym('b'),
    _basic_sym('c'),
    _basic_sym('d'),
)


def _atomic_inventory() -> exp.Atomic.Inventory:
  atomics = exp.Atomic.Inventory('atomic')
  atomics.make_suppl('atm_sym', {exp.Atomic.read(sym): sym for sym in _SYM})
  atomics.add_symbols(*atomics.atm_sym)
  return atomics


_ATM = _atomic_inventory()


class ExpressionTest(test_op.TestCase):

  def test_atomic_read(self):
    self.assertIs(exp.Atomic.read(sym.Symbol.CTRL.eps), exp.Atomic.CTRL.eps)
    self.assertIs(exp.Atomic.read(exp.Atomic.CTRL.unk), exp.Atomic.CTRL.unk)
    self.assertIs(_ATM.a.symbol, _SYM.a)

  def test_constants(self):
    self.assertTrue(exp.Atomic.CTRL.unk.is_control())
    self.assertTrue(exp.Atomic.CTRL.eps.is_eps())
    self.assertTrue(exp.Atomic.CTRL.nor.is_nor())
    self.assertTrue(exp.Expression.ANY.is_any())
    self.AssertStrEqual(exp.Expression.ANY, '​🝓⋆​')

  def test_symbol_inventory_lookup(self):
    self.assertEqual(_ATM.lookup(_ATM.a, 'atm_sym'), _SYM.a)

  def test_atomic_from_symbol(self):
    self.AssertStrEqual(_ATM.nul, _SYM.nul)
    self.assertEmpty(_ATM.nul.raw)
    self.assertIn(_ATM.nul, _ATM.nul)
    self.assertIs(_ATM.nul.symbol, _SYM.nul)
    self.assertEqual(_ATM.nul.index, _SYM.nul.index)
    self.assertIn(sym.Symbol.SYM_FEATURES.type.abst, _ATM.nul.features)
    self.assertEqual(
        _ATM.nul.description(show_features=True),
        'alias: nul  index: 123  text: ◌  name: NULL\n    features: {abstract}',
    )

  def test_atomic_from_atomic(self):
    atm_nul2 = exp.Atomic.read(_ATM.nul)
    self.AssertStrEqual(atm_nul2, _SYM.nul)
    self.assertEmpty(atm_nul2.raw)
    self.assertIn(atm_nul2, atm_nul2)
    self.assertNotIn(_ATM.nul, atm_nul2)
    self.assertIs(atm_nul2.symbol, _SYM.nul)
    self.assertEqual(atm_nul2.index, _SYM.nul.index)
    self.assertEqual(
        atm_nul2.description(),
        'alias: nul  index: 123  text: ◌  name: NULL',
    )
    _ATM.nul.add(atm_nul2)
    self.AssertEqualItems(_ATM.nul, [_ATM.nul])

  def test_cat_empty(self):
    empty_cat = exp.Cat()
    self.assertEmpty(empty_cat)
    self.AssertStrEqual(empty_cat, '​ℰ​')

  def test_cat_control(self):
    eps_cat = exp.Cat(exp.Atomic.CTRL.eps)
    self.assertEmpty(eps_cat)
    self.AssertStrEqual(eps_cat, '​ℰ​')

  def test_cat_items(self):
    cat = exp.Cat(_ATM.a, _ATM.b, _ATM.a)
    self.assertLen(cat, 3)
    self.AssertStrEqual(cat, '(a b a)')
    self.assertIsNot(cat.item(0), cat.item(2))
    self.AssertEquivalent(cat.item(0), (cat.item(2)))
    self.assertTrue(exp.Cat(exp.Expression.ANY).is_any())

  def test_cat_nested(self):
    cat1 = exp.Cat(_ATM.a, _ATM.b)
    cat2 = exp.Cat(cat1, _ATM.c)
    or1 = exp.Or(_ATM.a)
    or2 = exp.Or(_ATM.b, _ATM.c)
    cat3 = exp.Cat(or1, or2)
    self.assertLen(cat2, 3)
    self.AssertStrEqual(cat2, '(a b c)')
    self.AssertStrEqual(exp.Cat(exp.Or()), '(​◎​)')
    self.AssertStrEqual(cat3, '(a (b | c))')

  def test_repeat(self):
    self.assertEmpty(_ATM.a.repeat(0))
    self.AssertStrEqual(_ATM.a.repeat(), '(a a)')
    self.AssertStrEqual(_ATM.a.repeat(3), '(a a a)')
    self.AssertStrEqual(exp.Cat(_ATM.a, _ATM.b).repeat(), '(a b a b)')

  def test_or_no_alternative(self):
    or_eps = exp.Or(exp.Atomic.CTRL.eps)
    or0 = exp.Or()
    or1 = exp.Or(_ATM.a)
    self.assertEmpty(or_eps)
    self.assertEmpty(or0)
    self.assertLen(or1, 1)
    self.AssertStrEqual(or_eps, '​◎​')
    self.AssertStrEqual(or0, '​◎​')
    self.AssertStrEqual(or1, '(a | ​◎​)')

  def test_or_items(self):
    or1 = exp.Or(_ATM.a)
    or2 = exp.Or(_ATM.b, _ATM.c)
    or3 = exp.Or(or1, or2)
    or4 = exp.Or(_ATM.a, _ATM.b, _ATM.a)
    or5 = or1.copy().add(exp.Expression.ANY)
    self.AssertStrEqual(or2, '(b | c)')
    self.AssertStrEqual(or3, '(a | b | c)')
    self.AssertStrEqual(or4, '(a | b)')
    self.assertLen(or4, 2)
    self.assertNotIn(_ATM.a, or5)
    self.AssertAccepts(or5, _ATM.a)

  def test_or_nested(self):
    cat1 = exp.Cat(_ATM.a)
    cat2 = exp.Cat(_ATM.b, _ATM.c)
    cat3 = exp.Cat(_ATM.a, exp.Or(_ATM.b, _ATM.c))
    or4 = exp.Or(cat1, cat2)
    or5 = exp.Or(cat3).add(exp.Cat(_ATM.a, _ATM.b))
    or6 = exp.Or(cat3).add(exp.Cat(_ATM.a, exp.Or(_ATM.b, _ATM.c, _ATM.d)))
    self.AssertStrEqual(exp.Or(exp.Cat()), '(​ℰ​ | ​◎​)')
    self.AssertStrEqual(or4, '(a | (b c))')
    self.AssertStrEqual(or5, '((a (b | c)) | ​◎​)')
    self.AssertStrEqual(or6, '((a (b | c | d)) | ​◎​)')

  def test_copy(self):
    exp1 = exp.Expression('new_exp')
    exp1_copy = exp1.copy()
    cat1 = exp.Cat(_ATM.a, _ATM.b)
    cat1_copy = cat1.copy()
    self.assertIs(exp.Expression.ANY.copy(), exp.Expression.ANY)
    self.assertIsNot(exp1, exp1_copy)
    self.assertIs(exp.Atomic.CTRL.eps.copy(), exp.Atomic.CTRL.eps)
    self.assertIsNot(_ATM.a.copy(), _ATM.a)
    self.AssertEquivalent(_ATM.a.copy(), _ATM.a)
    self.assertIsNot(cat1.item(0), cat1_copy.item(0))
    self.AssertEquivalent(cat1, cat1_copy)

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
        '  [​ℰ​]\n'
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
    self.AssertEquivalent(exp.Atomic.CTRL.eps, sym.Symbol.CTRL.eps)
    self.AssertEquivalent(exp.Expression.ANY, exp.Expression.ANY)
    self.AssertNotEquivalent(exp.Expression.ANY, exp.Atomic.CTRL.eps)
    self.AssertEquivalent(exp.Cat(), exp.Atomic.CTRL.eps)
    self.AssertEquivalent(exp.Cat(), exp.Cat())
    self.AssertNotEquivalent(or0, exp.Atomic.CTRL.nor)
    self.AssertNotEquivalent(or0, or0)
    self.AssertEquivalent(exp.Cat(_ATM.a), _ATM.a)
    self.AssertEquivalent(
        exp.Cat(_ATM.a, _ATM.b, exp.Or(_ATM.c, _ATM.d)),
        exp.Or(
            exp.Cat(_ATM.a, _ATM.b, _ATM.c), exp.Cat(_ATM.a, _ATM.b, _ATM.d)
        ),
    )

  def test_contains_controls(self):
    eps = exp.Atomic.CTRL.eps
    nor = exp.Atomic.CTRL.nor
    any_exp = exp.Expression.ANY
    self.AssertContains(eps, eps)
    self.AssertContains(nor, eps)
    self.AssertNotContains(nor, any_exp)
    self.AssertNotContains(eps, nor)
    self.AssertNotContains(nor, nor)
    self.AssertNotContains(any_exp, nor)

  def test_contains_expressions(self):
    cat_abc = _ATM.a + _ATM.b + _ATM.c
    any_exp = exp.Expression.ANY
    self.AssertContains(any_exp, _ATM.a)
    self.AssertContains(_ATM.a, any_exp)
    self.AssertContains(any_exp, cat_abc)
    self.AssertContains(cat_abc, any_exp)
    self.AssertContains(cat_abc, exp.Cat())
    self.AssertNotContains(cat_abc, exp.Or())
    self.AssertContains(cat_abc, exp.Or(exp.Cat()))
    self.AssertNotContains(cat_abc, exp.Cat(exp.Or()))
    self.AssertContains(cat_abc, _ATM.b)
    self.AssertNotContains(_ATM.b, cat_abc)
    self.assertTrue(exp.Cat().is_contained(_SYM.a))
    self.assertFalse(exp.Or().is_contained(_SYM.a))
    self.assertTrue(_ATM.b.is_contained(cat_abc))
    self.assertTrue(_ATM.a.is_contained(_SYM.a))

  def test_matches(self):
    abc_or_cd = (_ATM.a + _ATM.b + _ATM.c) | (_ATM.c + _ATM.d)
    a_or_c_b_or_d = (_ATM.a | _ATM.c) + (_ATM.b | _ATM.d)
    any_exp = exp.Expression.ANY
    self.AssertMatches(any_exp, a_or_c_b_or_d)
    self.AssertMatches(a_or_c_b_or_d, any_exp)
    self.AssertMatches(abc_or_cd, a_or_c_b_or_d)
    self.AssertNotMatches(abc_or_cd, _ATM.a + _ATM.b + _ATM.d)
    self.assertTrue(any_exp.is_prefix(abc_or_cd))
    self.assertTrue(any_exp.is_suffix(abc_or_cd))
    self.assertTrue(abc_or_cd.is_prefix(any_exp))
    self.assertTrue(abc_or_cd.is_suffix(any_exp))
    self.assertTrue(exp.Cat().is_prefix(exp.Cat()))
    self.assertTrue(exp.Cat().is_suffix(exp.Cat()))
    self.assertFalse(exp.Cat().is_prefix(abc_or_cd))
    self.assertFalse(exp.Cat().is_suffix(abc_or_cd))
    self.assertTrue(_ATM.c.is_prefix(abc_or_cd))
    self.assertTrue(_ATM.c.is_prefix(abc_or_cd))
    self.assertTrue((_ATM.a | (_ATM.b + _ATM.c)).is_prefix(_SYM.a))
    self.assertTrue((_ATM.a + _ATM.d).is_suffix(a_or_c_b_or_d))
    self.assertTrue(_ATM.a.is_prefix(_SYM.a))
    self.assertTrue(_ATM.a.is_suffix(_SYM.a))

  def test_operator_add(self):
    self.AssertEquivalent(
        _ATM.a + _ATM.b + _ATM.c, exp.Cat(_ATM.a, _ATM.b, _ATM.c)
    )

  def test_operator_or(self):
    self.AssertEquivalent(
        _ATM.a | _ATM.b | _ATM.c, exp.Or(_ATM.a, _ATM.b, _ATM.c)
    )

if __name__ == '__main__':
  absltest.main()
