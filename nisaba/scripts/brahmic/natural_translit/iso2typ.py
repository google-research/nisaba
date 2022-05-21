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

"""ISO to typeable string conversion."""

import pynini as p
from pynini.export import multi_grm
from pynini.lib import byte

sigma_star = byte.BYTE.star


def _iso_to_decomposed_typ() -> p.Fst:
  """ISO to typable fst."""

  iso_to_typ_vowel = (p.cross('a', '(a)') |
                      p.cross('ā', '(aa)') |
                      p.cross('æ', '(ac)') |
                      p.cross('e', '(e)') |
                      p.cross('ē', '(ee)') |
                      p.cross('ê', '(ec)') |
                      p.cross('i', '(i)') |
                      p.cross('ī', '(ii)') |
                      p.cross('o', '(o)') |
                      p.cross('ō', '(oo)') |
                      p.cross('ô', '(oc)') |
                      p.cross('õ', '(ot)') |
                      p.cross('u', '(u)') |
                      p.cross('ū', '(uu)'))

  iso_to_typ_consonant = (p.cross('b', '(b)') |
                          p.cross('c', '(c)') |
                          p.cross('d', '(d)') |
                          p.cross('ḍ', '(dd)') |
                          p.cross('f', '(f)') |
                          p.cross('g', '(g)') |
                          p.cross('ġ', '(gg)') |
                          p.cross('h', '(h)') |
                          p.cross('j', '(j)') |
                          p.cross('k', '(k)') |
                          p.cross('l', '(l)') |
                          p.cross('ḷ', '(ll)') |
                          p.cross('ḻ', '(lr)') |
                          p.cross('m', '(m)') |
                          p.cross('n', '(n)') |
                          p.cross('ñ', '(ny)') |
                          p.cross('ṅ', '(ng)') |
                          p.cross('ṇ', '(nn)') |
                          p.cross('ṉ', '(na)') |
                          p.cross('p', '(p)') |
                          p.cross('q', '(q)') |
                          p.cross('r', '(r)') |
                          p.cross('ṛ', '(rd)') |
                          p.cross('ṟ', '(rr)') |
                          p.cross('s', '(s)') |
                          p.cross('ś', '(sh)') |
                          p.cross('ṣ', '(ss)') |
                          p.cross('t', '(t)') |
                          p.cross('ṭ', '(tt)') |
                          p.cross('ṯ', '(ta)') |
                          p.cross('v', '(v)') |
                          p.cross('x', '(x)') |
                          p.cross('y', '(y)') |
                          p.cross('ẏ', '(yy)') |
                          p.cross('z', '(z)'))

  iso_to_typ_coda = (p.cross('’', '(avg)') |  # avagraha
                     p.cross('ˑ', '(nkt)') |  # nukta
                     p.cross('ḥ', '(vis)') |  # visarga
                     p.cross('ṁ', '(ans)') |  # anusvara
                     p.cross('̐', '(candra)') |  # candrabindu
                     p.cross('ḫ', '(upadh)') |  # upadhmaniya
                     p.cross('ẖ', '(jihva)'))  # jihvamuliya

  iso_to_typ_modifier = (p.cross('ʰ', '(asp)') |  # aspiration
                         p.cross('̥', '(vocal)') |  # vocalic
                         p.cross('̄', '(long)') |
                         p.cross('ⸯ', '(chl)') |  # chillu
                         p.cross('̆', '(eye)'))  # eyelash

  iso_to_typ_symbol = (p.cross('.', '(ind)') |  # independent vowel
                       p.cross('+', '(zwj)') |  # zero width joiner
                       p.cross('|', '(zwn)'))  # zero width non-joiner

  iso_to_decomposed_typ_aux = (iso_to_typ_vowel |
                               iso_to_typ_consonant |
                               iso_to_typ_coda |
                               iso_to_typ_modifier |
                               iso_to_typ_symbol)

  return iso_to_decomposed_typ_aux.star.optimize()


def _composed_typ() -> p.Fst:
  """Maps multiple ISO characters to single native characters."""

  compose_diphthong_aux = (p.cross('(a)(i)', '(ai)') |
                           p.cross('(a)(u)', '(au)'))

  compose_diphthong = p.cdrewrite(compose_diphthong_aux,
                                  '', '', sigma_star).optimize()

  compose_vocalic_aux = (p.cross('(l)(vocal)', '(l_vocal)') |
                         p.cross('(r)(vocal)', '(r_vocal)'))

  compose_vocalic = p.cdrewrite(compose_vocalic_aux,
                                '', '', sigma_star).optimize()

  compose_retroflex_vocalic_aux = (p.cross('(l_vocal)(long)', '(ll_vocal)') |
                                   p.cross('(r_vocal)(long)', '(rr_vocal)'))

  compose_retroflex_vocalic = p.cdrewrite(compose_retroflex_vocalic_aux,
                                          '', '', sigma_star).optimize()

  compose_ind_vowel_aux = (p.cross('(ind)(a)', '(a_i)') |
                           p.cross('(ind)(aa)', '(aa_i)') |
                           p.cross('(ind)(ac)', '(ac_i)') |
                           p.cross('(ind)(e)', '(e_i)') |
                           p.cross('(ind)(ee)', '(ee_i)') |
                           p.cross('(ind)(ec)', '(ec_i)') |
                           p.cross('(ind)(i)', '(i_i)') |
                           p.cross('(ind)(ii)', '(ii_i)') |
                           p.cross('(ind)(o)', '(o_i)') |
                           p.cross('(ind)(oo)', '(oo_i)') |
                           p.cross('(ind)(oc)', '(oc_i)') |
                           p.cross('(ind)(u)', '(u_i)') |
                           p.cross('(ind)(uu)', '(uu_i)') |
                           p.cross('(ind)(ai)', '(ai_i)') |
                           p.cross('(ind)(au)', '(au_i)') |
                           p.cross('(ind)(l_vocal)', '(l_vocal_i)') |
                           p.cross('(ind)(ll_vocal)', '(ll_vocal_i)') |
                           p.cross('(ind)(r_vocal)', '(r_vocal_i)') |
                           p.cross('(ind)(rr_vocal)', '(rr_vocal_i)'))

  compose_ind_vowel = p.cdrewrite(compose_ind_vowel_aux,
                                  '', '', sigma_star).optimize()

  compose_aspiration_aux = (p.cross('(b)(asp)', '(bh)') |
                            p.cross('(c)(asp)', '(ch)') |
                            p.cross('(d)(asp)', '(dh)') |
                            p.cross('(dd)(asp)', '(ddh)') |
                            p.cross('(g)(asp)', '(gh)') |
                            p.cross('(j)(asp)', '(jh)') |
                            p.cross('(k)(asp)', '(kh)') |
                            p.cross('(p)(asp)', '(ph)') |
                            p.cross('(rd)(asp)', '(rdh)') |
                            p.cross('(t)(asp)', '(th)') |
                            p.cross('(tt)(asp)', '(tth)'))

  compose_aspiration = p.cdrewrite(compose_aspiration_aux,
                                   '', '', sigma_star).optimize()

  compose_candra = p.cdrewrite(p.cross('(m)(candra)', '(cnd)'),
                               '', '', sigma_star).optimize()

  # Malayalam chillu characters
  compose_chillu_aux = (p.cross('(k)(chl)', '(k_chl)') |
                        p.cross('(l)(chl)', '(l_chl)') |
                        p.cross('(ll)(chl)', '(ll_chl)') |
                        p.cross('(n)(chl)', '(n_chl)') |
                        p.cross('(nn)(chl)', '(nn_chl)') |
                        p.cross('(rr)(chl)', '(rr_chl)') |
                        p.cross('(r)(chl)', '(reph)'))

  compose_chillu = p.cdrewrite(compose_chillu_aux,
                               '', '', sigma_star).optimize()

  # Marathi eyelash ra
  compose_eyelash = p.cdrewrite(p.cross('(r)(eye)', '(reye)'),
                                '', '', sigma_star).optimize()

  compose_om = p.cdrewrite(p.cross('(ot)(m)', '(om)'),
                           '', '', sigma_star).optimize()

  return (compose_diphthong @
          compose_vocalic @
          compose_retroflex_vocalic @
          compose_ind_vowel @
          compose_aspiration @
          compose_candra @
          compose_chillu @
          compose_eyelash @
          compose_om).optimize()


# TODO: Convert to constant
def iso_to_typ() -> p.Fst:
  return (_iso_to_decomposed_typ() @ _composed_typ()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for language agnostic ISO to typeable string conversion."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_TYP_DECOMPOSED'] = _iso_to_decomposed_typ()
      exporter['ISO_TO_TYP'] = iso_to_typ()


if __name__ == '__main__':
  multi_grm.run(generator_main)
