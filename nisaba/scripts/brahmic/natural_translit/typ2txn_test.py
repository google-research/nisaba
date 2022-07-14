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
from nisaba.scripts.brahmic.natural_translit import typ2txn
from nisaba.scripts.utils import test_util


class Typ2TxnTest(test_util.FstTestCase):

  def test_typ_a_to_a(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(a)',
        '(a=a)')

  def test_typ_aa_to_a_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(aa)',
        '(aa=a_l)')

  def test_typ_ac_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ac)',
        '(ac=ae)')

  def test_typ_ai_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ai)',
        '(ai=ae)')

  def test_typ_au_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(au)',
        '(au=o_l)')

  def test_typ_e_to_e(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(e)',
        '(e=e)')

  def test_typ_ee_to_e_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ee)',
        '(ee=e_l)')

  def test_typ_ec_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ec)',
        '(ec=ae)')

  def test_typ_i_to_i(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(i)',
        '(i=i)')

  def test_typ_ii_to_i_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ii)',
        '(ii=i_l)')

  def test_typ_o_to_o(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(o)',
        '(o=o)')

  def test_typ_oo_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(oo)',
        '(oo=o_l)')

  def test_typ_oc_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(oc)',
        '(oc=o_l)')

  def test_typ_u_to_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(u)',
        '(u=u)')

  def test_typ_uu_to_u_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(uu)',
        '(uu=u_l)')

  def test_typ_a_i_to_a(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(a_i)',
        '(a_i=a)')

  def test_typ_aa_i_to_a_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(aa_i)',
        '(aa_i=a_l)')

  def test_typ_ac_i_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ac_i)',
        '(ac_i=ae)')

  def test_typ_ai_i_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ai_i)',
        '(ai_i=ae)')

  def test_typ_au_i_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(au_i)',
        '(au_i=o_l)')

  def test_typ_e_i_to_e(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(e_i)',
        '(e_i=e)')

  def test_typ_ee_i_to_e_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ee_i)',
        '(ee_i=e_l)')

  def test_typ_ec_i_to_ae(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ec_i)',
        '(ec_i=ae)')

  def test_typ_i_i_to_i(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(i_i)',
        '(i_i=i)')

  def test_typ_ii_i_to_i_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ii_i)',
        '(ii_i=i_l)')

  def test_typ_o_i_to_o(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(o_i)',
        '(o_i=o)')

  def test_typ_oo_i_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(oo_i)',
        '(oo_i=o_l)')

  def test_typ_oc_i_to_o_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(oc_i)',
        '(oc_i=o_l)')

  def test_typ_u_i_to_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(u_i)',
        '(u_i=u)')

  def test_typ_uu_i_to_u_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(uu_i)',
        '(uu_i=u_l)')

  def test_typ_l_vocal_to_l_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(l_vocal)',
        '(l_vocal=l,u)')

  def test_typ_ll_vocal_to_ll_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ll_vocal)',
        '(ll_vocal=ll,u)')

  def test_typ_r_vocal_to_rt_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(r_vocal)',
        '(r_vocal=rt,u)')

  def test_typ_rr_vocal_to_r_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rr_vocal)',
        '(rr_vocal=r,u)')

  def test_typ_l_vocal_i_to_l_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(l_vocal_i)',
        '(l_vocal_i=l,u)')

  def test_typ_ll_vocal_i_to_ll_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ll_vocal_i)',
        '(ll_vocal_i=ll,u)')

  def test_typ_r_vocal_i_to_rt_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(r_vocal_i)',
        '(r_vocal_i=rt,u)')

  def test_typ_rr_vocal_i_to_r_u(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rr_vocal_i)',
        '(rr_vocal_i=r,u)')

  def test_typ_b_to_b(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(b)',
        '(b=b)')

  def test_typ_c_to_ch(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(c)',
        '(c=ch)')

  def test_typ_d_to_di(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(d)',
        '(d=di)')

  def test_typ_dd_to_dd(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(dd)',
        '(dd=dd)')

  def test_typ_f_to_f(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(f)',
        '(f=f)')

  def test_typ_g_to_g(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(g)',
        '(g=g)')

  def test_typ_gg_to_xa(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(gg)',
        '(gg=xa)')

  def test_typ_h_to_h(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(h)',
        '(h=h)')

  def test_typ_j_to_jh(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(j)',
        '(j=jh)')

  def test_typ_k_to_k(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(k)',
        '(k=k)')

  def test_typ_l_to_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(l)',
        '(l=l)')

  def test_typ_ll_to_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ll)',
        '(ll=l)')

  def test_typ_lr_to_rru(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(lr)',
        '(lr=rru)')

  def test_typ_m_to_m(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(m)',
        '(m=m)')

  def test_typ_n_to_ni(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(n)',
        '(n=ni)')

  def test_typ_ny_to_ny(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ny)',
        '(ny=ny)')

  def test_typ_ng_to_ng(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ng)',
        '(ng=ng)')

  def test_typ_nn_to_nn(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(nn)',
        '(nn=nn)')

  def test_typ_na_to_n(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(na)',
        '(na=n)')

  def test_typ_p_to_p(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(p)',
        '(p=p)')

  def test_typ_q_to_q(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(q)',
        '(q=q)')

  def test_typ_r_to_rt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(r)',
        '(r=rt)')

  def test_typ_rd_to_rrt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rd)',
        '(rd=rrt)')

  def test_typ_rr_to_r(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rr)',
        '(rr=r)')

  def test_typ_s_to_s(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(s)',
        '(s=s)')

  def test_typ_sh_to_sh(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(sh)',
        '(sh=sh)')

  def test_typ_ss_to_ss(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ss)',
        '(ss=ss)')

  def test_typ_t_to_ti(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(t)',
        '(t=ti)')

  def test_typ_tt_to_tt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(tt)',
        '(tt=tt)')

  def test_typ_ta_to_t(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ta)',
        '(ta=t)')

  def test_typ_v_to_vu(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(v)',
        '(v=vu)')

  def test_typ_x_to_x(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(x)',
        '(x=x)')

  def test_typ_y_to_y(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(y)',
        '(y=y)')

  def test_typ_z_to_z(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(z)',
        '(z=z)')

  def test_typ_k_chl_to_k(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(k_chl)',
        '(k_chl=k)')

  def test_typ_l_chl_to_l(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(l_chl)',
        '(l_chl=l)')

  def test_typ_ll_chl_to_ll(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ll_chl)',
        '(ll_chl=ll)')

  def test_typ_n_chl_to_ni(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(n_chl)',
        '(n_chl=ni)')

  def test_typ_nn_chl_to_nn(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(nn_chl)',
        '(nn_chl=nn)')

  def test_typ_rr_chl_to_rt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rr_chl)',
        '(rr_chl=rt)')

  def test_typ_reph_to_rt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(reph)',
        '(reph=rt)')

  def test_typ_reye_to_rt(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(reye)',
        '(reye=rt)')

  def test_typ_bh_to_b_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(bh)',
        '(bh=b,asp)')

  def test_typ_ch_to_ch_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ch)',
        '(ch=ch,asp)')

  def test_typ_dh_to_di_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(dh)',
        '(dh=di,asp)')

  def test_typ_ddh_to_dd_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ddh)',
        '(ddh=dd,asp)')

  def test_typ_gh_to_g_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(gh)',
        '(gh=g,asp)')

  def test_typ_jh_to_jh_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(jh)',
        '(jh=jh,asp)')

  def test_typ_kh_to_k_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(kh)',
        '(kh=k,asp)')

  def test_typ_ph_to_p_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ph)',
        '(ph=p,asp)')

  def test_typ_rdh_to_rrt_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(rdh)',
        '(rdh=rrt,asp)')

  def test_typ_th_to_ti_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(th)',
        '(th=ti,asp)')

  def test_typ_tth_to_tt_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(tth)',
        '(tth=tt,asp)')

  def test_typ_yy_to_y_asp(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(yy)',
        '(yy=y,asp)')

  def test_typ_avg_to_sil(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(avg)',
        '(avg=sil)')

  def test_typ_vis_to_h(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(vis)',
        '(vis=h)')

  def test_typ_ans_to_nsl(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(ans)',
        '(ans=nsl)')

  def test_typ_cnd_to_nsl(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(cnd)',
        '(cnd=nsl)')

  def test_typ_upadh_to_h(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(upadh)',
        '(upadh=h)')

  def test_typ_jihva_to_h(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(jihva)',
        '(jihva=h)')

  def test_typ_om_to_o_l_m(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(om)',
        '(om=o_l,m)')

  def test_typ_hindi_anusvara(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(h)(i)(ans)(d)(ii)',
        '(h=h)(i=i)(ans=nsl)(d=di)(ii=i_l)')

  def test_typ_hindi_long_i(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(h)(i)(n)(d)(ii)',
        '(h=h)(i=i)(n=ni)(d=di)(ii=i_l)')

  def test_typ_hindi_short_i(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(h)(i)(n)(d)(i)',
        '(h=h)(i=i)(n=ni)(d=di)(i=i)')

  def test_typ_indiya_anusvara(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(i)(ans)(dd)(i)(y)(aa)',
        '(i=i)(ans=nsl)(dd=dd)(i=i)(y=y)(aa=a_l)')

  def test_typ_intya(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(i)(n)(t)(y)(a)',
        '(i=i)(n=ni)(t=ti)(y=y)(a=a)')

  def test_typ_indya_chillu(self):
    self.assertFstStrIO(
        typ2txn.TYP_TO_TXN,
        '(i)(n_chl)(dd)(y)(a)',
        '(i=i)(n_chl=ni)(dd=dd)(y=y)(a=a)')

if __name__ == '__main__':
  absltest.main()
