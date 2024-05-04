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
from nisaba.scripts.natural_translit.utils import alignment2 as alg
from nisaba.scripts.natural_translit.utils import expression as exp
from nisaba.scripts.natural_translit.utils import operation as op
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


class AlignmentTest(test_op.TestCase):

  def test_alignment(self):
    alignment = alg.Alignment('test')
    self.assertEqual(alignment.left, exp.Expression.ANY)
    self.assertFalse(alignment.from_bos)
    self.assertFalse(alignment.to_eos)
    self.assertEqual(alignment.operation, op.Operation.COMMON.unassigned)

  def test_simple(self):
    simple = alg.Alignment.simple(_SYM.a, _ATM.b + _ATM.c)
    self.assertIsInstance(simple.left, exp.Atomic)
    self.AssertStrEqual(simple, '(a∶(b c))')

  def test_constants(self):
    self.assertTrue(alg.Alignment.ANY.is_any())
    self.AssertStrEqual(alg.Alignment.ANY, '(​🝓⋆​∶​🝓⋆​)')
    self.assertTrue(alg.Alignment.ANY.preceding.is_any())
    self.assertEqual(alg.Alignment.ANY.source, alg.Alignment.CONSTANT)
    self.assertTrue(alg.Alignment.EPS.is_eps())
    self.AssertStrEqual(alg.Alignment.EPS, '(​ℰ​∶​ℰ​)')
    self.assertTrue(alg.Alignment.NOR.is_nor())
    self.AssertStrEqual(alg.Alignment.NOR, '(​◎​∶​◎​)')
    self.assertEqual(alg.Alignment.NOR.operation, op.Operation.COMMON.error)

  def test_rule(self):
    rule = alg.Alignment.rule(
        'test',
        _ATM.a,
        _ATM.b,
        preceding_left=_ATM.c,
        following_right=_ATM.d,
        applied_cost=0.1,
    )
    self.AssertEquivalent(rule.left, _ATM.a)
    self.AssertEquivalent(rule.right, _ATM.b)
    self.assertEqual(rule.operation, op.Operation.COMMON.alignable)
    self.AssertStrEqual(rule, '(⌈c∶​🝓⋆​⌋ a∶b ⌈​🝓⋆​∶d⌋, alignable (0.000))')
    self.AssertStrEqual(rule.tsv_row(), 'test	a	b	alignable (0.000)	0.1')

  def test_deletion(self):
    rule = alg.Alignment.deletion(
        'a_deletion',
        _ATM.a,
        preceding_right=_ATM.b,
        from_bos=True,
    )
    self.AssertStrEqual(rule, '(⌈​⊳​​🝓⋆​∶b⌋ a∶​ℰ​, deletion (1.000))')
    self.assertFalse(rule.is_any())

  def test_insertion(self):
    rule = alg.Alignment.insertion(
        'a_insertion',
        _ATM.a,
        following_right=_ATM.b,
        to_eos=True,
    )
    self.AssertStrEqual(rule, '(​ℰ​∶a ⌈​🝓⋆​∶b​⊲​⌋, insertion (1.000))')
    self.assertFalse(rule.is_any())

  def test_interchangeable(self):
    rule1, rule2 = alg.Alignment.interchangeable('a_b', _ATM.a, _ATM.b)
    self.AssertStrEqual(rule1, '(a∶b, interchangeable (0.100))')
    self.AssertStrEqual(rule2, '(b∶a, interchangeable (0.100))')

  def test_copy(self):
    rule1 = alg.Alignment.rule(
        'test',
        _ATM.a,
        _ATM.b,
        preceding_left=_ATM.c,
        applied_cost=0.1,
    )
    rule2 = rule1.copy()
    self.assertIs(alg.Alignment.NOR.copy(), alg.Alignment.NOR)
    self.assertIs(alg.Alignment().copy().preceding, alg.Alignment.ANY)
    self.assertIs(rule2.following, alg.Alignment.ANY)
    self.AssertStrEqual(rule1, rule2)
    self.assertEqual(rule1.applied_cost, rule2.applied_cost)
    self.assertEqual(rule1.source, rule2.source)


if __name__ == '__main__':
  absltest.main()
