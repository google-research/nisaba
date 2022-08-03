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

_TEST_CASES = [
    (typ2txn._typ_to_txn, [
        ('(a)', '(a=a)'),
        ('(aa)', '(aa=a_l)'),
        ('(ac)', '(ac=ae)'),
        ('(ai)', '(ai=ae)'),
        ('(au)', '(au=o_l)'),
        ('(e)', '(e=e)'),
        ('(ee)', '(ee=e_l)'),
        ('(ec)', '(ec=ae)'),
        ('(i)', '(i=i)'),
        ('(ii)', '(ii=i_l)'),
        ('(o)', '(o=o)'),
        ('(oo)', '(oo=o_l)'),
        ('(oc)', '(oc=o_l)'),
        ('(u)', '(u=u)'),
        ('(uu)', '(uu=u_l)'),
        ('(a_i)', '(a_i=a)'),
        ('(aa_i)', '(aa_i=a_l)'),
        ('(ac_i)', '(ac_i=ae)'),
        ('(ai_i)', '(ai_i=ae)'),
        ('(au_i)', '(au_i=o_l)'),
        ('(e_i)', '(e_i=e)'),
        ('(ee_i)', '(ee_i=e_l)'),
        ('(ec_i)', '(ec_i=ae)'),
        ('(i_i)', '(i_i=i)'),
        ('(ii_i)', '(ii_i=i_l)'),
        ('(o_i)', '(o_i=o)'),
        ('(oo_i)', '(oo_i=o_l)'),
        ('(oc_i)', '(oc_i=o_l)'),
        ('(u_i)', '(u_i=u)'),
        ('(uu_i)', '(uu_i=u_l)'),
        ('(l_vocal)', '(l_vocal=l,u)'),
        ('(ll_vocal)', '(ll_vocal=ll,u)'),
        ('(r_vocal)', '(r_vocal=rt,u)'),
        ('(rr_vocal)', '(rr_vocal=r,u)'),
        ('(l_vocal_i)', '(l_vocal_i=l,u)'),
        ('(ll_vocal_i)', '(ll_vocal_i=ll,u)'),
        ('(r_vocal_i)', '(r_vocal_i=rt,u)'),
        ('(rr_vocal_i)', '(rr_vocal_i=r,u)'),
        ('(b)', '(b=b)'),
        ('(c)', '(c=ch)'),
        ('(d)', '(d=di)'),
        ('(dd)', '(dd=dd)'),
        ('(f)', '(f=f)'),
        ('(g)', '(g=g)'),
        ('(gg)', '(gg=xa)'),
        ('(h)', '(h=h)'),
        ('(j)', '(j=jh)'),
        ('(k)', '(k=k)'),
        ('(l)', '(l=l)'),
        ('(ll)', '(ll=l)'),
        ('(lr)', '(lr=rru)'),
        ('(m)', '(m=m)'),
        ('(n)', '(n=ni)'),
        ('(ny)', '(ny=ny)'),
        ('(ng)', '(ng=ng)'),
        ('(nn)', '(nn=nn)'),
        ('(na)', '(na=n)'),
        ('(p)', '(p=p)'),
        ('(q)', '(q=q)'),
        ('(r)', '(r=rt)'),
        ('(rd)', '(rd=rrt)'),
        ('(rr)', '(rr=r)'),
        ('(s)', '(s=s)'),
        ('(sh)', '(sh=sh)'),
        ('(ss)', '(ss=ss)'),
        ('(t)', '(t=ti)'),
        ('(tt)', '(tt=tt)'),
        ('(ta)', '(ta=t)'),
        ('(v)', '(v=vu)'),
        ('(x)', '(x=x)'),
        ('(y)', '(y=y)'),
        ('(z)', '(z=z)'),
        ('(k_chl)', '(k_chl=k)'),
        ('(l_chl)', '(l_chl=l)'),
        ('(ll_chl)', '(ll_chl=ll)'),
        ('(n_chl)', '(n_chl=ni)'),
        ('(nn_chl)', '(nn_chl=nn)'),
        ('(rr_chl)', '(rr_chl=rt)'),
        ('(reph)', '(reph=rt)'),
        ('(reye)', '(reye=rt)'),
        ('(bh)', '(bh=b,asp)'),
        ('(ch)', '(ch=ch,asp)'),
        ('(dh)', '(dh=di,asp)'),
        ('(ddh)', '(ddh=dd,asp)'),
        ('(gh)', '(gh=g,asp)'),
        ('(jh)', '(jh=jh,asp)'),
        ('(kh)', '(kh=k,asp)'),
        ('(ph)', '(ph=p,asp)'),
        ('(rdh)', '(rdh=rrt,asp)'),
        ('(th)', '(th=ti,asp)'),
        ('(tth)', '(tth=tt,asp)'),
        ('(yy)', '(yy=y,asp)'),
        ('(avg)', '(avg=sil)'),
        ('(vis)', '(vis=h)'),
        ('(ans)', '(ans=nsl)'),
        ('(cnd)', '(cnd=nsl)'),
        ('(upadh)', '(upadh=h)'),
        ('(jihva)', '(jihva=h)'),
        ('(om)', '(om=o_l,m)'),
        ('(h)(i)(ans)(d)(ii)', '(h=h)(i=i)(ans=nsl)(d=di)(ii=i_l)'),
        ('(h)(i)(n)(d)(ii)', '(h=h)(i=i)(n=ni)(d=di)(ii=i_l)'),
        ('(h)(i)(n)(d)(i)', '(h=h)(i=i)(n=ni)(d=di)(i=i)'),
        ('(i)(ans)(dd)(i)(y)(aa)', '(i=i)(ans=nsl)(dd=dd)(i=i)(y=y)(aa=a_l)'),
        ('(i)(n)(t)(y)(a)', '(i=i)(n=ni)(t=ti)(y=y)(a=a)'),
        ('(i)(n_chl)(dd)(y)(a)', '(i=i)(n_chl=ni)(dd=dd)(y=y)(a=a)'),
    ]),
]


class Typ2TxnTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
