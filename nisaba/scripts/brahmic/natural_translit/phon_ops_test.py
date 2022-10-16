# Copyright 2022 Nisaba Authors.
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

"""Tests for phon_ops."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import phon_ops
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (lambda: phon_ops.ANUSVARA_ASSIMILATION, [
        ('<a>={a}<ans>={nsl}<b>={b}<aa>={a_l}',
         '<a>={a}<ans>={m}<b>={b}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<d>={di}<aa>={a_l}',
         '<a>={a}<ans>={ni}<d>={di}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<d>={d}<aa>={a_l}',
         '<a>={a}<ans>={n}<d>={d}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<y>={y}<aa>={a_l}',
         '<a>={a}<ans>={ny}<y>={y}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<dd>={dd}<aa>={a_l}',
         '<a>={a}<ans>={nn}<dd>={dd}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<g>={g}<aa>={a_l}',
         '<a>={a}<ans>={ng}<g>={g}<aa>={a_l}'),
        ('<a>={a}<ans>={nsl}<s>={s}<aa>={a_l}',
         '<a>={a}<ans>={nsl}<s>={s}<aa>={a_l}'),
    ]),
    (lambda: phon_ops.DEFAULT_ANUSVARA_LABIAL, [
        ('<a>={a}<ans>={nsl}<s>={s}<aa>={a_l}',
         '<a>={a}<ans>={m}<s>={s}<aa>={a_l}'),
    ]),
    (lambda: phon_ops.DEFAULT_ANUSVARA_DENTAL, [
        ('<a>={a}<ans>={nsl}<s>={s}<aa>={a_l}',
         '<a>={a}<ans>={ni}<s>={s}<aa>={a_l}'),
    ]),
    (lambda: phon_ops.JNY_TO_GNY, [
        ('<j>={jh}<ny>={ny}', '<j>={g}<ny>={ny}'),
    ]),
    (lambda: phon_ops.JNY_TO_GY, [
        ('<j>={jh}<ny>={ny}', '<j>={g}<ny>={y}'),
    ]),
    (lambda: phon_ops.JNY_TO_NY, [
        ('<j>={jh}<ny>={ny}', '<j>={sil}<ny>={ny}'),
    ]),
]


class PhonOpsTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
