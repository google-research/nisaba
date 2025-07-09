# Copyright 2025 Nisaba Authors.
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

"""Tests for g2p."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import g2p
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (
        lambda: g2p.TYP_TO_TXN,
        [
            ('<a>', '<a>={_}'),
            ('<aa>', '<aa>={a}{:h}'),
            ('<ai>', '<ai>={a}{+}{i}'),
            ('<a_i>', '<a_i>={a}'),
            ('<rv>', '<rv>={r}{S}'),
            ('<rrv>', '<rrv>={r}{S}{:h}'),
            ('<b>', '<b>={b}'),
            ('<bh>', '<bh>={b}{H}'),
            ('<c>', '<c>={t}{+}{sh}'),
            ('<ch>', '<ch>={t}{+}{sh}{H}'),
            ('<k_chl>', '<k_chl>={k}'),
            ('<reph>', '<reph>={rt}'),
            ('<r_eye>', '<r_eye>={rt}'),
            ('<yy>', '<yy>={y}{H}'),
            ('<avg>', '<avg>={sil}'),
            ('<vis>', '<vis>={h}'),
            ('<ans>', '<ans>={N}'),
            ('<om>', '<om>={o}{:h}{m}'),
            (
                '<h><i><ans><d><ii>',
                '<h>={h}<i>={i}<ans>={N}<d>={di}<ii>={i}{:h}',
            ),
            ('<h><i><n><d><ii>', '<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i}{:h}'),
        ],
    ),
    (lambda: g2p.AI_TO_EH_LONG, [('{a}{+}{i}', '{eh}{:h}')]),
    (
        lambda: g2p.vocalic('{i}', '{i}{:h}'),
        [('{S}', '{i}'), ('{S}{:h}', '{i}{:h}')],
    ),
    (
        lambda: g2p.default_schwa('{a}'),
        [('{_}', '{a}'), ('{V}', '{a}')],
    ),
    (g2p.vocal_schwa, [('{_}', '{V}')]),
    (g2p.silent_schwa, [('{_}', '{sil}')]),
    (
        lambda: g2p.schwa_eow('{r}{t}'),
        [('{a}{r}{t}{_}', '{a}{r}{t}{sil}'), ('{a}{p}{t}{_}', '{a}{p}{t}{_}')],
    ),
    (
        lambda: g2p.schwa_between_syllables('{s}{p}', '{r}{t}'),
        [
            ('{a}{r}{t}{_}{s}{p}{a}', '{a}{r}{t}{sil}{s}{p}{a}'),
            ('{a}{p}{t}{_}{s}{p}{a}', '{a}{p}{t}{_}{s}{p}{a}'),
            ('{a}{r}{t}{_}{k}{p}{a}', '{a}{r}{t}{_}{k}{p}{a}'),
        ],
    ),
    (
        lambda: g2p.assign_nasal('<ans>', '{m}'),
        [
            (
                '<a>={a}<ans>={N}<b>={b}<aa>={a}{:h}',
                '<a>={a}<ans>={m}<b>={b}<aa>={a}{:h}',
            ),
            (
                '<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}',
                '<a>={a}<ans>={m}<s>={s}<aa>={a}{:h}',
            ),
        ],
    ),
    (
        lambda: g2p.assign_nasal('<ans>', '{ng}', '{g}'),
        [
            (
                '<a>={a}<ans>={N}<g>={g}<aa>={a}{:h}',
                '<a>={a}<ans>={ng}<g>={g}<aa>={a}{:h}',
            ),
            (
                '<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}',
                '<a>={a}<ans>={N}<s>={s}<aa>={a}{:h}',
            ),
        ],
    ),
    (
        lambda: g2p.rewrite_jny('{g}', '{y}'),
        [('<j>={d}{+}{zh}<ny>={ny}', '<j>={g}<ny>={y}')],
    ),
]


class Iso2TxnOpsTest(test_util.FstTestCase):

  def test_all(self):
    self.AssertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
