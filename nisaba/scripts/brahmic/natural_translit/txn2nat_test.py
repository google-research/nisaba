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

"""Tests for txn2nat."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import txn2nat
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (lambda: txn2nat.TXN_TO_PSAF, [
        ('<a>={a}', 'a'),
        ('<aa>={a_l}', 'aa'),
        ('<ac>={ae}', 'ae'),
        ('<ai>={ae}', 'ae'),
        ('<au>={o_l}', 'oo'),
        ('<e>={e}', 'e'),
        ('<ee>={e_l}', 'ee'),
        ('<ec>={ae}', 'ae'),
        ('<i>={i}', 'i'),
        ('<ii>={i_l}', 'ii'),
        ('<o>={o}', 'o'),
        ('<oo>={o_l}', 'oo'),
        ('<oc>={o_l}', 'oo'),
        ('<u>={u}', 'u'),
        ('<uu>={u_l}', 'uu'),
        ('<a_i>={a}', 'a'),
        ('<aa_i>={a_l}', 'aa'),
        ('<ac_i>={ae}', 'ae'),
        ('<ai_i>={ae}', 'ae'),
        ('<au_i>={o_l}', 'oo'),
        ('<e_i>={e}', 'e'),
        ('<ee_i>={e_l}', 'ee'),
        ('<ec_i>={ae}', 'ae'),
        ('<i_i>={i}', 'i'),
        ('<ii_i>={i_l}', 'ii'),
        ('<o_i>={o}', 'o'),
        ('<oo_i>={o_l}', 'oo'),
        ('<oc_i>={o_l}', 'oo'),
        ('<u_i>={u}', 'u'),
        ('<uu_i>={u_l}', 'uu'),
        ('<l_vcl>={l}{u}', 'lu'),
        ('<l_vcl>={l}{u}', 'lu'),
        ('<ll_vcl>={ll}{u}', 'lu'),
        ('<r_vcl>={rt}{u}', 'ru'),
        ('<rr_vcl_i>={r}{u}', 'ru'),
        ('<l_vcl_i>={l}{u}', 'lu'),
        ('<ll_vcl_i>={ll}{u}', 'lu'),
        ('<r_vcl_i>={rt}{u}', 'ru'),
        ('<rr_vcl_i>={r}{u}', 'ru'),
        ('<b>={b}', 'b'),
        ('<c>={ch}', 'ch'),
        ('<d>={di}', 'd'),
        ('<dd>={dd}', 'd'),
        ('<f>={f}', 'f'),
        ('<g>={g}', 'g'),
        ('<gg>={xa}', 'g'),
        ('<h>={h}', 'h'),
        ('<j>={jh}', 'j'),
        ('<k>={k}', 'k'),
        ('<l>={l}', 'l'),
        ('<ll>={l}', 'l'),
        ('<lr>={rru}', 'zh'),
        ('<m>={m}', 'm'),
        ('<n>={ni}', 'n'),
        ('<ny>={ny}', 'ny'),
        ('<ng>={ng}', 'ng'),
        ('<nn>={nn}', 'n'),
        ('<na>={n}', 'n'),
        ('<p>={p}', 'p'),
        ('<q>={q}', 'k'),
        ('<r>={rt}', 'r'),
        ('<rd>={rrt}', 'rd'),
        ('<rr>={r}', 'r'),
        ('<s>={s}', 's'),
        ('<sh>={sh}', 'sh'),
        ('<ss>={ss}', 'sh'),
        ('<t>={ti}', 't'),
        ('<tt>={tt}', 't'),
        ('<ta>={t}', 't'),
        ('<v>={vu}', 'v'),
        ('<x>={x}', 'kh'),
        ('<y>={y}', 'y'),
        ('<z>={z}', 'z'),
        ('<k_chl>={k}', 'k'),
        ('<l_chl>={l}', 'l'),
        ('<ll_chl>={ll}', 'l'),
        ('<n_chl>={ni}', 'n'),
        ('<nn_chl>={nn}', 'n'),
        ('<rr_chl>={rt}', 'r'),
        ('<reph>={rt}', 'r'),
        ('<r_eye>={rt}', 'r'),
        ('<yy>={y}{asp}', 'yh'),
        ('<bh>={b}{asp}', 'bh'),
        ('<ch>={ch}{asp}', 'chh'),
        ('<dh>={di}{asp}', 'dh'),
        ('<ddh>={dd}{asp}', 'dh'),
        ('<gh>={g}{asp}', 'gh'),
        ('<jh>={jh}{asp}', 'jh'),
        ('<kh>={k}{asp}', 'kh'),
        ('<ph>={p}{asp}', 'ph'),
        ('<rdh>={rrt}{asp}', 'rdh'),
        ('<th>={ti}{asp}', 'th'),
        ('<tth>={tt}{asp}', 'th'),
        ('<vis>={h}', 'h'),
        ('<ans>={m}', 'm'),
        ('<ans>={ni}', 'n'),
        ('<ans>={ny}', 'n'),
        ('<ans>={ng}', 'n'),
        ('<ans>={nn}', 'n'),
        ('<cnd>={ni}', 'n'),
        ('<upadh>={h}', 'h'),
        ('<jihva>={h}', 'h'),
        ('<avg><y><a><ans>={sil}{y}{a}{ni}', 'yan'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i_l}', 'hindii'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i_l}', 'hindii'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<i>={i}', 'hindi'),
        ('<i>={i}<n>={ni}<dd>={dd}<i>={i}<y>={y}<aa>={a_l}',
         'indiyaa'),
        ('<i>={i}<n>={ni}<t>={di}<y>={y}<a>={a}', 'indya'),
        ('<i>={i}<n_chl>={ni}<dd>={dd}<y>={y}<a>={a}', 'indya'),
        ]),
    (lambda: txn2nat.TXN_TO_PSAC, [
        ('<aa>={a_l}', 'a'),
        ('<ee>={e_l}', 'e'),
        ('<ii>={i_l}', 'i'),
        ('<oo>={o_l}', 'o'),
        ('<uu>={u_l}', 'u'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i_l}', 'hindi'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i_l}', 'hindi'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<i>={i}', 'hindi'),
        ('<i>={i}<n>={ni}<dd>={dd}<i>={i}<y>={y}<aa>={a_l}',
         'indiya'),
        ('<i>={i}<n>={ni}<t>={di}<y>={y}<a>={a}', 'indya'),
        ('<i>={i}<n_chl>={ni}<dd>={dd}<y>={y}<a>={a}', 'indya'),
        ]),
]


class Txn2NatTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
