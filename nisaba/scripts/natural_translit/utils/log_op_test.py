# Copyright 2023 Nisaba Authors.
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

import collections
from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as t

# Test objects

D = collections.namedtuple('D', ['k'])
_D1 = D('v')
_T1 = t.Thing.with_alias('T1')
_T3 = t.Thing.with_alias_and_value('', _T1)
_T5 = t.Thing.with_alias_and_value('T5', t.pyn.accep(''))


class LoggingTest(absltest.TestCase):

  def test_class_of_thing(self):
    self.assertEqual(log.class_of(_T1), 'Thing')

  def test_class_of_int(self):
    self.assertEqual(log.class_of(1), 'int')

  def test_text_of_thing(self):
    self.assertEqual(log.text_of(_T1), 'Thing_T1')

  def test_text_of_thing_empty(self):
    self.assertEqual(log.text_of(_T5), 'Thing_T5:Fst_<no_text>')

  def test_text_of_str(self):
    self.assertEqual(log.text_of('abc'), 'abc')

  def test_text_of_fst(self):
    self.assertEqual(log.text_of(t.pyn.accep('abc')), 'abc')

  def test_text_of_fst_non_string(self):
    self.assertEqual(log.text_of(t.pyn.union('a', 'b')), '<non_string_fst>')

  def test_text_of_namedtuple(self):
    self.assertEqual(log.text_of(_D1), 'D(k=\'v\')')

  def test_text_of_int(self):
    self.assertEqual(log.text_of('0'), '0')

  def test_text_of_none(self):
    self.assertEqual(log.text_of(None), 'None')

  def test_text_of_nothing(self):
    self.assertEqual(log.text_of(t.UNSPECIFIED), 'Unspecified')

  def test_alias_of_thing(self):
    self.assertEqual(log.alias_of(_T1), 'T1')

  def test_alias_of_thing_empty(self):
    self.assertNotEmpty(log.alias_of(_T3))

  def test_alias_of_list(self):
    self.assertEqual(log.alias_of([0, 1]), '[0, 1]')

  def test_frame(self):
    self.assertEqual(log._add_caller('msg', 3), 'case.py/run: msg')

  def test_return_message(self):
    self.assertEqual(log._return_message(5, 'msg'), 'returns 5, detail: msg')

  def test_dbg_return(self):
    self.assertEqual(log.dbg_return(5), 5)

  def test_dbg_return_true(self):
    self.assertTrue(log.dbg_return_true())

  def test_dbg_return_false(self):
    self.assertFalse(log.dbg_return_false('msg'))

if __name__ == '__main__':
  absltest.main()
