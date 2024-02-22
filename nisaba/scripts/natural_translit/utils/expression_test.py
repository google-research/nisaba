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

str_schwa = 'schwa'
str_salt = '🜔'  # Alchemical symbol for salt.

sym_schwa = exp.Symbol(str_schwa, text=str_salt)
atm_schwa = exp.Atomic(sym_schwa)
atm_schwa2 = exp.Atomic(atm_schwa)


class ExpressionTest(absltest.TestCase):

  def test_symbol_str(self):
    self.assertEqual(str(sym_schwa), str_salt)
    self.assertEmpty(sym_schwa.raw)

  def test_atomic_from_symbol(self):
    self.assertEqual(str(atm_schwa), str_salt)
    self.assertEmpty(atm_schwa.raw)
    self.assertIn(atm_schwa, atm_schwa)
    self.assertIs(atm_schwa.symbol, sym_schwa)
    self.assertEqual(atm_schwa.index, sym_schwa.index)

  def test_atomic_from_atomic(self):
    self.assertEqual(str(atm_schwa2), str_salt)
    self.assertEmpty(atm_schwa2.raw)
    self.assertIn(atm_schwa2, atm_schwa2)
    self.assertNotIn(atm_schwa, atm_schwa2)
    self.assertIs(atm_schwa2.symbol, sym_schwa)
    self.assertEqual(atm_schwa2.index, sym_schwa.index)

  def test_atomic_add(self):
    atm_schwa.add(atm_schwa2)
    self.assertEqual(atm_schwa._items, [atm_schwa])

if __name__ == '__main__':
  absltest.main()
