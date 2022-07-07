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

"""Tests for iso2typ."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import iso2typ
from nisaba.scripts.utils import test_util


class Iso2TypTest(test_util.FstTestCase):

  def test_typ_a(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'a',
        '(a)')

  def test_typ_aa(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ā',
        '(aa)')

  def test_typ_ac(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'æ',
        '(ac)')

  def test_typ_e(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'e',
        '(e)')

  def test_typ_ee(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ē',
        '(ee)')

  def test_typ_ec(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ê',
        '(ec)')

  def test_typ_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'i',
        '(i)')

  def test_typ_ii(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ī',
        '(ii)')

  def test_typ_o(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'o',
        '(o)')

  def test_typ_oo(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ō',
        '(oo)')

  def test_typ_oc(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ô',
        '(oc)')

  def test_typ_ot(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'õ',
        '(ot)')

  def test_typ_u(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'u',
        '(u)')

  def test_typ_uu(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ū',
        '(uu)')

  def test_typ_b(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'b',
        '(b)')

  def test_typ_c(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'c',
        '(c)')

  def test_typ_d(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'd',
        '(d)')

  def test_typ_dd(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ḍ',
        '(dd)')

  def test_typ_f(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'f',
        '(f)')

  def test_typ_g(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'g',
        '(g)')

  def test_typ_gg(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ġ',
        '(gg)')

  def test_typ_h(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'h',
        '(h)')

  def test_typ_j(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'j',
        '(j)')

  def test_typ_k(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'k',
        '(k)')

  def test_typ_l(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'l',
        '(l)')

  def test_typ_ll(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ḷ',
        '(ll)')

  def test_typ_lr(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ḻ',
        '(lr)')

  def test_typ_m(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'm',
        '(m)')

  def test_typ_n(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'n',
        '(n)')

  def test_typ_ny(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ñ',
        '(ny)')

  def test_typ_ng(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṅ',
        '(ng)')

  def test_typ_nn(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṇ',
        '(nn)')

  def test_typ_na(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṉ',
        '(na)')

  def test_typ_p(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'p',
        '(p)')

  def test_typ_q(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'q',
        '(q)')

  def test_typ_r(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'r',
        '(r)')

  def test_typ_rd(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṛ',
        '(rd)')

  def test_typ_rr(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṟ',
        '(rr)')

  def test_typ_s(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        's',
        '(s)')

  def test_typ_sh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ś',
        '(sh)')

  def test_typ_ss(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṣ',
        '(ss)')

  def test_typ_t(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        't',
        '(t)')

  def test_typ_tt(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṭ',
        '(tt)')

  def test_typ_ta(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṯ',
        '(ta)')

  def test_typ_v(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'v',
        '(v)')

  def test_typ_x(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'x',
        '(x)')

  def test_typ_y(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'y',
        '(y)')

  def test_typ_yy(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ẏ',
        '(yy)')

  def test_typ_z(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'z',
        '(z)')

  def test_typ_avg(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        '’',
        '(avg)')

  def test_typ_nkt(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ˑ',
        '(nkt)')

  def test_typ_vis(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ḥ',
        '(vis)')

  def test_typ_ans(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ṁ',
        '(ans)')

  def test_typ_candra(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        '̐',
        '(candra)')

  def test_typ_upadh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ḫ',
        '(upadh)')

  def test_typ_jihva(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ẖ',
        '(jihva)')

  def test_typ_asp(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ʰ',
        '(asp)')

  def test_typ_vocal(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        '̥',
        '(vocal)')

  def test_typ_long(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        '̄',
        '(long)')

  def test_typ_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'ⸯ',
        '(chl)')

  def test_typ_eye(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        '̆',
        '(eye)')

  def test_typ_hindi_anusvara(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'hiṁdī',
        '(h)(i)(ans)(d)(ii)')

  def test_typ_hindi_long_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'hindī',
        '(h)(i)(n)(d)(ii)')

  def test_typ_hindi_short_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'hindi',
        '(h)(i)(n)(d)(i)')

  def test_typ_indiya_anusvara(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'iṁḍiyā',
        '(i)(ans)(dd)(i)(y)(aa)')

  def test_typ_intya(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'intya',
        '(i)(n)(t)(y)(a)')

  def test_typ_indya_chillu(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP_DECOMPOSED,
        'inⸯḍya',
        '(i)(n)(chl)(dd)(y)(a)')

  def test_typ_ai(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ai',
        '(ai)')

  def test_typ_au(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'au',
        '(au)')

  def test_typ_l_vocal(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'l̥',
        '(l_vocal)')

  def test_typ_r_vocal(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'r̥',
        '(r_vocal)')

  def test_typ_ll_vocal(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'l̥̄',
        '(ll_vocal)')

  def test_typ_rr_vocal(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'r̥̄',
        '(rr_vocal)')

  def test_typ_a_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.a',
        '(a_i)')

  def test_typ_aa_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ā',
        '(aa_i)')

  def test_typ_ac_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.æ',
        '(ac_i)')

  def test_typ_e_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.e',
        '(e_i)')

  def test_typ_ee_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ē',
        '(ee_i)')

  def test_typ_ec_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ê',
        '(ec_i)')

  def test_typ_i_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.i',
        '(i_i)')

  def test_typ_ii_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ī',
        '(ii_i)')

  def test_typ_o_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.o',
        '(o_i)')

  def test_typ_oo_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ō',
        '(oo_i)')

  def test_typ_oc_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ô',
        '(oc_i)')

  def test_typ_u_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.u',
        '(u_i)')

  def test_typ_uu_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ū',
        '(uu_i)')

  def test_typ_ai_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.ai',
        '(ai_i)')

  def test_typ_au_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.au',
        '(au_i)')

  def test_typ_l_vocal_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.l̥',
        '(l_vocal_i)')

  def test_typ_r_vocal_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.r̥',
        '(r_vocal_i)')

  def test_typ_ll_vocal_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.l̥̄',
        '(ll_vocal_i)')

  def test_typ_rr_vocal_i(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        '.r̥̄',
        '(rr_vocal_i)')

  def test_typ_bh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'bʰ',
        '(bh)')

  def test_typ_ch(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'cʰ',
        '(ch)')

  def test_typ_dh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'dʰ',
        '(dh)')

  def test_typ_ddh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ḍʰ',
        '(ddh)')

  def test_typ_gh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'gʰ',
        '(gh)')

  def test_typ_jh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'jʰ',
        '(jh)')

  def test_typ_kh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'kʰ',
        '(kh)')

  def test_typ_ph(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'pʰ',
        '(ph)')

  def test_typ_rdh(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ṛʰ',
        '(rdh)')

  def test_typ_th(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'tʰ',
        '(th)')

  def test_typ_tth(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ṭʰ',
        '(tth)')

  def test_typ_cnd(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'm̐',
        '(cnd)')

  def test_typ_k_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'kⸯ',
        '(k_chl)')

  def test_typ_l_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'lⸯ',
        '(l_chl)')

  def test_typ_ll_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ḷⸯ',
        '(ll_chl)')

  def test_typ_n_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'nⸯ',
        '(n_chl)')

  def test_typ_nn_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ṇⸯ',
        '(nn_chl)')

  def test_typ_rr_chl(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'ṟⸯ',
        '(rr_chl)')

  def test_typ_reph(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'rⸯ',
        '(reph)')

  def test_typ_r_eyelash(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'r̆',
        '(reye)')

  def test_typ_om(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'õm',
        '(om)')

  def test_typ_indya_chillu_composed(self):
    self.assertFstStrIO(
        iso2typ.ISO_TO_TYP,
        'inⸯḍya',
        '(i)(n_chl)(dd)(y)(a)')


if __name__ == '__main__':
  absltest.main()
