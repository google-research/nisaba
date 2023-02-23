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

"""Tests for typ2txn."""

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.utils import test_util

_TEST_CASES = [
    (lambda: iso2txn.TYP_TO_TXN, [
        ('<a>', '<a>={sch}'),
        ('<aa>', '<aa>={a_l}'),
        ('<ac>', '<ac>={ae}'),
        ('<ai>', '<ai>={a}{+}{i}'),
        ('<au>', '<au>={a}{+}{u}'),
        ('<an>', '<an>={a}'),
        ('<aan>', '<aan>={a_l}'),
        ('<e>', '<e>={e}'),
        ('<ee>', '<ee>={e_l}'),
        ('<ec>', '<ec>={ae}'),
        ('<i>', '<i>={i}'),
        ('<ii>', '<ii>={i_l}'),
        ('<o>', '<o>={o}'),
        ('<oo>', '<oo>={o_l}'),
        ('<oc>', '<oc>={oh}'),
        ('<u>', '<u>={u}'),
        ('<uu>', '<uu>={u_l}'),
        ('<a_i>', '<a_i>={a}'),
        ('<aa_i>', '<aa_i>={a_l}'),
        ('<ac_i>', '<ac_i>={ae}'),
        ('<ai_i>', '<ai_i>={a}{+}{i}'),
        ('<au_i>', '<au_i>={a}{+}{u}'),
        ('<e_i>', '<e_i>={e}'),
        ('<ee_i>', '<ee_i>={e_l}'),
        ('<ec_i>', '<ec_i>={ae}'),
        ('<i_i>', '<i_i>={i}'),
        ('<ii_i>', '<ii_i>={i_l}'),
        ('<o_i>', '<o_i>={o}'),
        ('<oo_i>', '<oo_i>={o_l}'),
        ('<oc_i>', '<oc_i>={oh}'),
        ('<u_i>', '<u_i>={u}'),
        ('<uu_i>', '<uu_i>={u_l}'),
        ('<lv>', '<lv>={l}{V}'),
        ('<llv>', '<llv>={l}{V_l}'),
        ('<rv>', '<rv>={r}{V}'),
        ('<rrv>', '<rrv>={r}{V_l}'),
        ('<lv_i>', '<lv_i>={l}{V}'),
        ('<llv_i>', '<llv_i>={l}{V_l}'),
        ('<rv_i>', '<rv_i>={r}{V}'),
        ('<rrv_i>', '<rrv_i>={r}{V_l}'),
        ('<b>', '<b>={b}'),
        ('<c>', '<c>={t}{+}{sh}'),
        ('<d>', '<d>={di}'),
        ('<dd>', '<dd>={dd}'),
        ('<f>', '<f>={f}'),
        ('<g>', '<g>={g}'),
        ('<gg>', '<gg>={gh}'),
        ('<h>', '<h>={h}'),
        ('<j>', '<j>={d}{+}{zh}'),
        ('<k>', '<k>={k}'),
        ('<l>', '<l>={l}'),
        ('<ll>', '<ll>={ll}'),
        ('<lr>', '<lr>={rru}'),
        ('<m>', '<m>={m}'),
        ('<n>', '<n>={ni}'),
        ('<ny>', '<ny>={ny}'),
        ('<ng>', '<ng>={ng}'),
        ('<nn>', '<nn>={nn}'),
        ('<na>', '<na>={n}'),
        ('<p>', '<p>={p}'),
        ('<q>', '<q>={q}'),
        ('<r>', '<r>={rt}'),
        ('<rd>', '<rd>={rrt}'),
        ('<rr>', '<rr>={r}'),
        ('<s>', '<s>={s}'),
        ('<sh>', '<sh>={sh}'),
        ('<ss>', '<ss>={ss}'),
        ('<t>', '<t>={ti}'),
        ('<tt>', '<tt>={tt}'),
        ('<ta>', '<ta>={t}'),
        ('<v>', '<v>={vu}'),
        ('<x>', '<x>={kh}'),
        ('<y>', '<y>={y}'),
        ('<z>', '<z>={z}'),
        ('<k_chl>', '<k_chl>={k}'),
        ('<l_chl>', '<l_chl>={l}'),
        ('<ll_chl>', '<ll_chl>={ll}'),
        ('<n_chl>', '<n_chl>={n}'),
        ('<nn_chl>', '<nn_chl>={nn}'),
        ('<rr_chl>', '<rr_chl>={r}'),
        ('<reph>', '<reph>={rt}'),
        ('<r_eye>', '<r_eye>={rt}'),
        ('<bh>', '<bh>={b}{H}'),
        ('<ch>', '<ch>={t}{+}{sh}{H}'),
        ('<dh>', '<dh>={di}{H}'),
        ('<ddh>', '<ddh>={dd}{H}'),
        ('<gh>', '<gh>={g}{H}'),
        ('<jh>', '<jh>={d}{+}{zh}{H}'),
        ('<kh>', '<kh>={k}{H}'),
        ('<ph>', '<ph>={p}{H}'),
        ('<rdh>', '<rdh>={rrt}{H}'),
        ('<th>', '<th>={ti}{H}'),
        ('<tth>', '<tth>={tt}{H}'),
        ('<yy>', '<yy>={y}{H}'),
        ('<avg>', '<avg>={sil}'),
        ('<vis>', '<vis>={h}'),
        ('<ans>', '<ans>={N}'),
        ('<cnd>', '<cnd>={N}'),
        ('<upadh>', '<upadh>={h}'),
        ('<jihva>', '<jihva>={h}'),
        ('<om>', '<om>={o_l}{m}'),
        ('<h><i><ans><d><ii>',
         '<h>={h}<i>={i}<ans>={N}<d>={di}<ii>={i_l}'),
        ('<h><i><n><d><ii>',
         '<h>={h}<i>={i}<n>={ni}<d>={di}<ii>={i_l}'),
        ('<h><i><n><d><i>',
         '<h>={h}<i>={i}<n>={ni}<d>={di}<i>={i}'),
        ('<i><ans><dd><i><y><aa>',
         '<i>={i}<ans>={N}<dd>={dd}<i>={i}<y>={y}<aa>={a_l}'),
        ('<i><n><t><y><a>',
         '<i>={i}<n>={ni}<t>={ti}<y>={y}<a>={sch}'),
        ('<i><n_chl><dd><y><a>',
         '<i>={i}<n_chl>={n}<dd>={dd}<y>={y}<a>={sch}'),
    ]),
]


class Typ2TxnTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
