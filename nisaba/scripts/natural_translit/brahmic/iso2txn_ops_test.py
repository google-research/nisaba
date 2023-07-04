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

"""Tests for iso2txn_ops."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (lambda: iso2txn_ops.AI_TO_EH_LONG, [
        ('{a}{+}{i}', '{eh}{:h}'),
    ]),
    (lambda: iso2txn_ops.vocalic('{i}', '{i}{:h}'), [
        ('{S}', '{i}'),
        ('{S}{:h}', '{i}{:h}'),
    ]),
    (lambda: iso2txn_ops.default_schwa('{a}'), [
        ('{_}', '{a}'),
        ('{V}', '{a}'),
    ]),
    (iso2txn_ops.vocal_schwa, [
        ('{_}', '{V}'),
    ]),
    (iso2txn_ops.silent_schwa, [
        ('{_}', '{sil}'),
    ]),
    (lambda: iso2txn_ops.schwa_eow('{r}{t}'), [
        ('{a}{r}{t}{_}', '{a}{r}{t}{sil}'),
        ('{a}{p}{t}{_}', '{a}{p}{t}{_}'),
    ]),
    (lambda: iso2txn_ops.schwa_between_syllables('{s}{p}', '{r}{t}'), [
        ('{a}{r}{t}{_}{s}{p}{a}', '{a}{r}{t}{sil}{s}{p}{a}'),
        ('{a}{p}{t}{_}{s}{p}{a}', '{a}{p}{t}{_}{s}{p}{a}'),
        ('{a}{r}{t}{_}{k}{p}{a}', '{a}{r}{t}{_}{k}{p}{a}'),
    ]),
    (lambda: iso2txn_ops.assign_anusvara('{m}'), [
        ('<a>={a}<ans>={N}<b>={b}<aa>={a}{:h}',
         '<a>={a}<ans>={m}<b>={b}<aa>={a}{:h}'),
        ('<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}',
         '<a>={a}<ans>={m}<s>={s}<aa>={a}{:h}'),
    ]),
    (lambda: iso2txn_ops.assign_anusvara('{ng}', '{g}'), [
        ('<a>={a}<ans>={N}<g>={g}<aa>={a}{:h}',
         '<a>={a}<ans>={ng}<g>={g}<aa>={a}{:h}'),
        ('<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}',
         '<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}'),
    ]),
    (lambda: iso2txn_ops.rewrite_jny('{g}', '{y}'), [
        ('<j>={d}{+}{zh}<ny>={ny}', '<j>={g}<ny>={y}'),
    ]),
]


class Iso2TxnOpsTest(test_util.FstTestCase):

  def test_all(self):
    self.AssertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
