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

"""Tests for txn2ipa."""

from absl.testing import absltest

from nisaba.scripts.natural_translit.phonology import txn2ipa
from nisaba.scripts.utils import test_util

_TEST_CASES = [
    (txn2ipa.txn_to_ipa, [
        ('<a>={ec}', 'ə'),
        ('<a>={a}', 'a'),
        ('<aa>={a}{:h}', 'aː'),
        ('<ac>={ae}', 'æ'),
        ('<e>={e}', 'e'),
        ('<ee>={e}{:h}', 'eː'),
        ('<ac>={eh}', 'ɛ'),
        ('<i>={i}', 'i'),
        ('<ii>={i}{:h}', 'iː'),
        ('<o>={o}', 'o'),
        ('<oo>={o}{:h}', 'oː'),
        ('<oc>={oh}', 'ɔ'),
        ('<u>={u}', 'u'),
        ('<uu>={u}{:h}', 'uː'),
        ('<b>={b}', 'b'),
        ('<c>={t}{+}{sh}', 't͡ʃ'),
        ('<d>={di}', 'd̪'),
        ('<dd>={dd}', 'ɖ'),
        ('<f>={f}', 'f'),
        ('<g>={g}', 'ɡ'),
        ('<gg>={gh}', 'ɣ'),
        ('<h>={h}', 'h'),
        ('<j>={d}{+}{zh}', 'd͡ʒ'),
        ('<k>={k}', 'k'),
        ('<l>={l}', 'l'),
        ('<ll>={ll}', 'ɭ'),
        ('<lr>={rru}', 'ɻ'),
        ('<m>={m}', 'm'),
        ('<n>={ni}', 'n̪'),
        ('<ny>={ny}', 'ɲ'),
        ('<ng>={ng}', 'ŋ'),
        ('<nn>={nn}', 'ɳ'),
        ('<na>={n}', 'n'),
        ('<p>={p}', 'p'),
        ('<q>={q}', 'q'),
        ('<r>={rt}', 'ɾ'),
        ('<rd>={rd}', 'ɽ'),
        ('<rr>={r}', 'r'),
        ('<s>={s}', 's'),
        ('<sh>={sh}', 'ʃ'),
        ('<ss>={ss}', 'ʂ'),
        ('<t>={ti}', 't̪'),
        ('<tt>={tt}', 'ʈ'),
        ('<ta>={t}', 't'),
        ('<v>={vu}', 'ʋ'),
        ('<x>={kh}', 'x'),
        ('<y>={y}', 'j'),
        ('<z>={z}', 'z'),
        ('<kh>={k}{H}', 'kʰ'),
        ('<ans>={N}', '~'),
        ('<om>={o}{:h}{m}', 'oːm'),
        ('<rv>={r}{S}', 'r̍'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i}{:h}', 'hin̪d̪iː'),
        ('{a}{^h}{&r}{*h}', 'á̌ˈ'),
        ('{a}{.}{i}{!k}', 'a.i|'),
    ]),
]


class Txn2IpaTest(test_util.FstTestCase):

  def test_all(self):
    self.AssertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
