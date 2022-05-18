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

"""South Asian multilingual phoneme assignment."""

import pynini as p
from pynini.export import multi_grm


def typ_to_txn() -> p.Fst:
  """Naive grapheme to phoneme assignment."""

  assign_phoneme_vowel = (p.cross('(a)', '(a=a)') |
                          p.cross('(aa)', '(aa=a_l)') |
                          p.cross('(ac)', '(ac=ae)') |
                          p.cross('(ai)', '(ai=ae)') |
                          p.cross('(au)', '(au=o_l)') |
                          p.cross('(e)', '(e=e)') |
                          p.cross('(ee)', '(ee=e_l)') |
                          p.cross('(ec)', '(ec=ae)') |
                          p.cross('(i)', '(i=i)') |
                          p.cross('(ii)', '(ii=i_l)') |
                          p.cross('(o)', '(o=o)') |
                          p.cross('(oo)', '(oo=o_l)') |
                          p.cross('(oc)', '(oc=o_l)') |
                          p.cross('(u)', '(u=u)') |
                          p.cross('(uu)', '(uu=u_l)') |
                          p.cross('(a_i)', '(a_i=a)') |
                          p.cross('(aa_i)', '(aa_i=a_l)') |
                          p.cross('(ac_i)', '(ac_i=ae)') |
                          p.cross('(ai_i)', '(ai_i=ae)') |
                          p.cross('(au_i)', '(au_i=o_l)') |
                          p.cross('(e_i)', '(e_i=e)') |
                          p.cross('(ee_i)', '(ee_i=e_l)') |
                          p.cross('(ec_i)', '(ec_i=ae)') |
                          p.cross('(i_i)', '(i_i=i)') |
                          p.cross('(ii_i)', '(ii_i=i_l)') |
                          p.cross('(o_i)', '(o_i=o)') |
                          p.cross('(oo_i)', '(oo_i=o_l)') |
                          p.cross('(oc_i)', '(oc_i=o_l)') |
                          p.cross('(u_i)', '(u_i=u)') |
                          p.cross('(uu_i)', '(uu_i=u_l)'))

  # Vocalic characters are assigned a consonant followed by a vowel
  assign_phoneme_vocalic = (p.cross('(l_vocal)', '(l_vocal=l,u)') |
                            p.cross('(ll_vocal)', '(ll_vocal=ll,u)') |
                            p.cross('(r_vocal)', '(r_vocal=r,u)') |
                            p.cross('(rr_vocal)', '(rr_vocal_i=rr,u)') |
                            p.cross('(l_vocal_i)', '(l_vocal_i=l,u)') |
                            p.cross('(ll_vocal_i)', '(ll_vocal_i=ll,u)') |
                            p.cross('(r_vocal_i)', '(r_vocal_i=r,u)') |
                            p.cross('(rr_vocal_i)', '(rr_vocal_i=rr,u)'))

  assign_phoneme_consonant = (p.cross('(b)', '(b=b)') |
                              p.cross('(c)', '(c=ch)') |
                              p.cross('(d)', '(d=di)') |
                              p.cross('(dd)', '(dd=dd)') |
                              p.cross('(f)', '(f=f)') |
                              p.cross('(g)', '(g=g)') |
                              p.cross('(gg)', '(gg=xa)') |
                              p.cross('(h)', '(h=h)') |
                              p.cross('(j)', '(j=jh)') |
                              p.cross('(k)', '(k=k)') |
                              p.cross('(l)', '(l=l)') |
                              p.cross('(ll)', '(ll=l)') |
                              p.cross('(lr)', '(lr=rru)') |
                              p.cross('(m)', '(m=m)') |
                              p.cross('(n)', '(n=ni)') |
                              p.cross('(ny)', '(ny=ny)') |
                              p.cross('(ng)', '(ng=ng)') |
                              p.cross('(nn)', '(nn=nn)') |
                              p.cross('(na)', '(na=n)') |
                              p.cross('(p)', '(p=p)') |
                              p.cross('(q)', '(q=q)') |
                              p.cross('(r)', '(r=rt)') |
                              p.cross('(rd)', '(rd=rrt)') |
                              p.cross('(rr)', '(rr=r)') |
                              p.cross('(s)', '(s=s)') |
                              p.cross('(sh)', '(sh=sh)') |
                              p.cross('(ss)', '(ss=ss)') |
                              p.cross('(t)', '(t=ti)') |
                              p.cross('(tt)', '(tt=tt)') |
                              p.cross('(ta)', '(ta=t)') |
                              p.cross('(v)', '(v=vu)') |
                              p.cross('(x)', '(x=x)') |
                              p.cross('(y)', '(y=y)') |
                              p.cross('(z)', '(z=z)') |
                              p.cross('(k_chl)', '(k_chl=k)') |
                              p.cross('(l_chl)', '(l_chl=l)') |
                              p.cross('(ll_chl)', '(ll_chl=ll)') |
                              p.cross('(n_chl)', '(n_chl=ni)') |
                              p.cross('(nn_chl)', '(nn_chl=nn)') |
                              p.cross('(rr_chl)', '(rr_chl=rt)') |
                              p.cross('(reph)', '(reph=rt)') |
                              p.cross('(reye)', '(reye=rt)'))

  # Aspirated consonants are featurised into a consonant
  # followed by an aspirated release.
  assign_phoneme_aspirated = (p.cross('(bh)', '(bh=b,asp)') |
                              p.cross('(ch)', '(ch=ch,asp)') |
                              p.cross('(dh)', '(dh=di,asp)') |
                              p.cross('(ddh)', '(ddh=dd,asp)') |
                              p.cross('(gh)', '(gh=g,asp)') |
                              p.cross('(jh)', '(jh=jh,asp)') |
                              p.cross('(kh)', '(kh=k,asp)') |
                              p.cross('(ph)', '(ph=p,asp)') |
                              p.cross('(rdh)', '(rdh=rrt,asp)') |
                              p.cross('(th)', '(th=ti,asp)') |
                              p.cross('(tth)', '(tth=tt,asp)') |
                              p.cross('(yy)', '(yy=y,asp)'))

  assign_phoneme_coda = (p.cross('(avg)', '(avg=sil)') |  # sil = silent
                         p.cross('(vis)', '(vis=h)') |
                         p.cross('(ans)', '(ans=ni)') |
                         p.cross('(cnd)', '(cnd=ni)') |
                         p.cross('(upadh)', '(upadh=h)') |
                         p.cross('(jihva)', '(jihva=h)'))

  assign_phoneme_om = p.cross('(om)', '(om=o_l,m)')

  return (assign_phoneme_vowel |
          assign_phoneme_vocalic |
          assign_phoneme_consonant |
          assign_phoneme_aspirated |
          assign_phoneme_coda |
          assign_phoneme_om).star.optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for ISO char to PSA phoneme assignment."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['TYP_TO_TXN'] = typ_to_txn()


if __name__ == '__main__':
  multi_grm.run(generator_main)
