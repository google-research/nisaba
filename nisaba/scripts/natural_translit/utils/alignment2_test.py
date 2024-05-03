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

  def test_simple(self):
    simple = alg.Alignment.simple(_SYM.a, _ATM.b + _ATM.c)
    self.assertIsInstance(simple.left, exp.Atomic)
    self.AssertStrEqual(simple, '(a:(b c))')

  def test_constants(self):
    self.assertTrue(alg.Alignment.ANY.is_any())
    self.AssertStrEqual(alg.Alignment.ANY, '(⍙*:⍙*)')
    self.assertTrue(alg.Alignment.ANY.preceding.is_any())
    self.assertEqual(alg.Alignment.ANY.source, alg.Alignment.Source.CONSTANT)
    self.assertTrue(alg.Alignment.EPSILON.is_eps())
    self.AssertStrEqual(alg.Alignment.EPSILON, '(⍷:⍷)')
    self.assertTrue(alg.Alignment.ERROR.is_nor())
    self.AssertStrEqual(alg.Alignment.ERROR, '(⍜:⍜)')
    self.assertEqual(alg.Alignment.ERROR.operation, op.Operation.COMMON.error)

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
    self.AssertStrEqual(rule, '([c:⍙*] a:b [⍙*:d], alignable (0.000))')
    self.AssertStrEqual(rule.tsv_row(), 'test	a	b	alignable (0.000)	0.1')

  def test_copy(self):
    rule1 = alg.Alignment.rule(
        'test',
        _ATM.a,
        _ATM.b,
        preceding_left=_ATM.c,
        applied_cost=0.1,
    )
    rule2 = rule1.copy()
    self.AssertStrEqual(rule1, rule2)
    self.assertIs(rule2.following, alg.Alignment.ANY)
    self.assertEqual(rule1.applied_cost, rule2.applied_cost)
    self.assertEqual(rule1.source, rule2.source)

  def test_deletion(self):
    rule = alg.Alignment.deletion(
        'a_deletion',
        _ATM.a,
        preceding_right=_ATM.b,
        from_bos=True,
    )
    self.AssertStrEqual(rule, '([^⍙*:b] a:⍷, deletion (1.000))')

  def test_insertion(self):
    rule = alg.Alignment.insertion(
        'a_insertion',
        _ATM.a,
        following_right=_ATM.b,
        to_eos=True,
    )
    self.AssertStrEqual(rule, '(⍷:a [⍙*:b$], insertion (1.000))')

  def test_interchangeable(self):
    rule1, rule2 = alg.Alignment.interchangeable('a_b', _ATM.a, _ATM.b)
    self.AssertStrEqual(rule1, '(a:b, interchangeable (0.100))')
    self.AssertStrEqual(rule2, '(b:a, interchangeable (0.100))')

if __name__ == '__main__':
  absltest.main()
