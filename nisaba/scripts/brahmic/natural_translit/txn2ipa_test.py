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

"""Tests for txn2ipa."""

from absl.testing import absltest

from nisaba.scripts.brahmic.natural_translit import txn2ipa
from nisaba.scripts.utils import test_util

_TEST_CASES = [
    (txn2ipa.txn_to_ipa, [
        ('<a>={ec}', 'ə'),
        ('<a>={a}', 'a'),
        ('<aa>={a_l}', 'aː'),
        ('<ac>={ae}', 'æ'),
        ('<e>={e}', 'e'),
        ('<ee>={e_l}', 'eː'),
        ('<ac>={eh}', 'ɛ'),
        ('<i>={i}', 'i'),
        ('<ii>={i_l}', 'iː'),
        ('<o>={o}', 'o'),
        ('<oo>={o_l}', 'oː'),
        ('<oc>={oh}', 'ɔ'),
        ('<u>={u}', 'u'),
        ('<uu>={u_l}', 'uː'),
        ('<b>={b}', 'b'),
        ('<c>={ch}', 't͡ʃ'),
        ('<d>={di}', 'd̪'),
        ('<dd>={dd}', 'ɖ'),
        ('<f>={f}', 'f'),
        ('<g>={g}', 'ɡ'),
        ('<gg>={xa}', 'ɣ'),
        ('<h>={h}', 'h'),
        ('<j>={jh}', 'd͡ʒ'),
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
        ('<rd>={rrt}', 'ɽ'),
        ('<rr>={r}', 'r'),
        ('<s>={s}', 's'),
        ('<sh>={sh}', 'ʃ'),
        ('<ss>={ss}', 'ʂ'),
        ('<t>={ti}', 't̪'),
        ('<tt>={tt}', 'ʈ'),
        ('<ta>={t}', 't'),
        ('<v>={vu}', 'ʋ'),
        ('<x>={x}', 'x'),
        ('<y>={y}', 'j'),
        ('<z>={z}', 'z'),
        ('<kh>={k}{asp}', 'kʰ'),
        ('<ans>={nsl}', '~'),
        ('<om>={o_l}{m}', 'oːm'),
        ('<r_vcl>={rt}{vcl}', 'ɾ̍'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i_l}', 'hin̪d̪iː'),
    ]),
]


class Txn2IpaTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
