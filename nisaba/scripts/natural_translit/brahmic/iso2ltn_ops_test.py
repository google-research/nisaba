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

"""Tests for iso2ltn_ops."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (lambda: iso2ltn_ops.TXN_TO_PSAF, [
        ('<a>={a}', 'a'),
        ('<aa>={a_l}', 'aa'),
        ('<ac>={ae}', 'ae'),
        ('<ai>={ae}', 'ae'),
        ('<au>={o_l}', 'oo'),
        ('<an>={a}', 'a'),
        ('<aan>={a_l}', 'aa'),
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
        ('<lv>={l}{u}', 'lu'),
        ('<llv>={l}{u_l}', 'luu'),
        ('<rv>={r}{u}', 'ru'),
        ('<rrv>={r}{u_l}', 'ruu'),
        ('<lv_i>={l}{u}', 'lu'),
        ('<llv_i>={l}{u_l}', 'luu'),
        ('<rv_i>={r}{u}', 'ru'),
        ('<rrv_i>={r}{u_l}', 'ruu'),
        ('<b>={b}', 'b'),
        ('<c>={t}{+}{sh}', 'ch'),
        ('<d>={di}', 'd'),
        ('<dd>={dd}', 'd'),
        ('<f>={f}', 'f'),
        ('<g>={g}', 'g'),
        ('<gg>={gh}', 'g'),
        ('<h>={h}', 'h'),
        ('<j>={d}{+}{zh}', 'j'),
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
        ('<x>={kh}', 'kh'),
        ('<y>={y}', 'y'),
        ('<z>={z}', 'z'),
        ('<k_chl>={k}', 'k'),
        ('<l_chl>={l}', 'l'),
        ('<ll_chl>={ll}', 'l'),
        ('<n_chl>={n}', 'n'),
        ('<nn_chl>={nn}', 'n'),
        ('<rr_chl>={rt}', 'r'),
        ('<reph>={rt}', 'r'),
        ('<r_eye>={rt}', 'r'),
        ('<yy>={y}{H}', 'yh'),
        ('<bh>={b}{H}', 'bh'),
        ('<ch>={t}{+}{sh}{H}', 'chh'),
        ('<dh>={di}{H}', 'dh'),
        ('<ddh>={dd}{H}', 'dh'),
        ('<gh>={g}{H}', 'gh'),
        ('<jh>={d}{+}{zh}{H}', 'jh'),
        ('<kh>={k}{H}', 'kh'),
        ('<ph>={p}{H}', 'ph'),
        ('<rdh>={rrt}{H}', 'rdh'),
        ('<th>={ti}{H}', 'th'),
        ('<tth>={tt}{H}', 'th'),
        ('<vis>={h}', 'h'),
        ('<ans>={m}', 'm'),
        ('<ans>={ni}', 'n'),
        ('<ans>={ny}', 'n'),
        ('<ans>={ng}', 'n'),
        ('<ans>={nn}', 'n'),
        ('<cnd>={ni}', 'n'),
        ('<upadh>={h}', 'h'),
        ('<jihva>={h}', 'h'),
        ('<rv>={r}{V}', 'ri'),
        ('<avg><y><a><ans>={sil}{y}{a}{ni}', 'yan'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i_l}', 'hindii'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i_l}', 'hindii'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<i>={i}', 'hindi'),
        ('<i>={i}<n>={ni}<dd>={dd}<i>={i}<y>={y}<aa>={a_l}',
         'indiyaa'),
        ('<i>={i}<n>={ni}<t>={di}<y>={y}<a>={a}', 'indya'),
        ('<i>={i}<n_chl>={n}<dd>={dd}<y>={y}<a>={a}', 'indya'),
        ]),
    (lambda: iso2ltn_ops.TXN_TO_PSAC, [
        ('<aa>={a_l}', 'a'),
        ('<ee>={e_l}', 'e'),
        ('<ii>={i_l}', 'i'),
        ('<oo>={o_l}', 'o'),
        ('<uu>={u_l}', 'u'),
        ('<c>={t}{+}{sh}<c>={t}{+}{sh}', 'ch'),
        ('<c>={t}{+}{sh}<ch>={t}{+}{sh}{H}', 'ch'),
        ('<ss>={ss}<ss>={ss}', 'sh'),
        ('<sh>={sh}<sh>={sh}', 'sh'),
        ('<h>={h}<i>={i}<ans>={ni}<d>={di}<ii>={i_l}', 'hindi'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i_l}', 'hindi'),
        ('<h>={h}<i>={i}<n>={ni}<d>={di}<i>={i}', 'hindi'),
        ('<i>={i}<n>={ni}<dd>={dd}<i>={i}<y>={y}<aa>={a_l}',
         'indiya'),
        ('<i>={i}<n>={ni}<t>={di}<y>={y}<a>={a}', 'indya'),
        ('<i>={i}<n_chl>={n}<dd>={dd}<y>={y}<a>={a}', 'indya'),
        ]),
]


class Iso2LtnOpsTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
