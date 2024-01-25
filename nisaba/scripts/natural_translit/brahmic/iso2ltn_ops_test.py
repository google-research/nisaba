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

"""Tests for iso2ltn_ops."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (lambda: iso2ltn_ops.SIBV_TO_SIBW, [
        ('<sh>={sh}<v>={vu}', '<sh>={sh}<v>=`w`'),
        ]),
    (lambda: iso2ltn_ops.NON_LABIAL_ANUSVARA, [
        ('<ans>={ny}', '<ans>=`n`'),
        ]),
    (lambda: iso2ltn_ops.VOCALIC_TR_I, [
        ('<rv>={r}{u}', '<rv>={r}`i`'),
        ('<llv_i>={l}{S}{:h}', '<llv_i>={l}`s_ii`'),
        ]),
    (lambda: iso2ltn_ops.DIPHTHONG_GR, [
        ('<ai>={eh}{:h}', '<ai>=`s_ai`'),
        ]),
    (lambda: iso2ltn_ops.CC_TO_CCH, [
        ('<c>=`s_ch`<c>=`s_ch`', '<c><c>=`c``s_ch`'),
        ]),
    (lambda: iso2ltn_ops.CCH_TO_CHH, [
        ('<c>=`s_ch`<ch>=`s_ch``h`', '<c><ch>=`s_ch``h`'),
        ]),
    (lambda: iso2ltn_ops.TRANSLIT_BY_PSA, [
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i}{:h}',
         '<h>=`h`<i>=`i`<ans>=`n`<d>=`d`<ii>=`i``DEL`'),
        ]),
    (lambda: iso2ltn_ops.TRANSLIT_LONG, [
        ('{i}{:h}', '`s_ii`'),
        ]),
    (lambda: iso2ltn_ops.IGNORE_LONG, [
        ('{i}{:h}', '{i}'),
        ]),
    (lambda: iso2ltn_ops.REMOVE_REPEATED_LTN, [
        ('kk', 'k'),
        ('kkk', 'kk'),
        ('kkkk', 'kk'),
        ('rdrd', 'rd'),
        ]),
]


class Iso2LtnOpsTest(test_util.FstTestCase):

  def test_all(self):
    self.AssertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
