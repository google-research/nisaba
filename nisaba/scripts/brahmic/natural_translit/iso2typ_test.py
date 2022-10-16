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


_TEST_CASES = [
    (iso2typ._iso_to_decomposed_typ, [
        ('a', '<a>'),
        ('ā', '<aa>'),
        ('æ', '<ac>'),
        ('e', '<e>'),
        ('ē', '<ee>'),
        ('ê', '<ec>'),
        ('i', '<i>'),
        ('ī', '<ii>'),
        ('o', '<o>'),
        ('ō', '<oo>'),
        ('ô', '<oc>'),
        ('õ', '<ot>'),
        ('u', '<u>'),
        ('ū', '<uu>'),
        ('b', '<b>'),
        ('c', '<c>'),
        ('d', '<d>'),
        ('ḍ', '<dd>'),
        ('f', '<f>'),
        ('g', '<g>'),
        ('ġ', '<gg>'),
        ('h', '<h>'),
        ('j', '<j>'),
        ('k', '<k>'),
        ('l', '<l>'),
        ('ḷ', '<ll>'),
        ('ḻ', '<lr>'),
        ('m', '<m>'),
        ('n', '<n>'),
        ('ñ', '<ny>'),
        ('ṅ', '<ng>'),
        ('ṇ', '<nn>'),
        ('ṉ', '<na>'),
        ('p', '<p>'),
        ('q', '<q>'),
        ('r', '<r>'),
        ('ṛ', '<rd>'),
        ('ṟ', '<rr>'),
        ('s', '<s>'),
        ('ś', '<sh>'),
        ('ṣ', '<ss>'),
        ('t', '<t>'),
        ('ṭ', '<tt>'),
        ('ṯ', '<ta>'),
        ('v', '<v>'),
        ('x', '<x>'),
        ('y', '<y>'),
        ('ẏ', '<yy>'),
        ('z', '<z>'),
        ('’', '<avg>'),
        ('ˑ', '<nkt>'),
        ('ḥ', '<vis>'),
        ('ṁ', '<ans>'),
        ('̐', '<cnd_dia>'),
        ('ḫ', '<upadh>'),
        ('ẖ', '<jihva>'),
        ('ʰ', '<asp>'),
        ('̥', '<vcl>'),
        ('̄', '<long>'),
        ('ⸯ', '<chl>'),
        ('̆', '<eye>'),
        ('hiṁdī', '<h><i><ans><d><ii>'),
        ('hindī', '<h><i><n><d><ii>'),
        ('hindi', '<h><i><n><d><i>'),
        ('iṁḍiyā', '<i><ans><dd><i><y><aa>'),
        ('intya', '<i><n><t><y><a>'),
        ('inⸯḍya', '<i><n><chl><dd><y><a>'),
    ]),
    (iso2typ.iso_to_typ, [
        ('ba', '<b><a>'),
        ('ai', '<ai>'),
        ('au', '<au>'),
        ('l̥', '<l_vcl>'),
        ('r̥', '<r_vcl>'),
        ('l̥̄', '<ll_vcl>'),
        ('r̥̄', '<rr_vcl>'),
        ('a', '<a_i>'),
        ('.a', '<a_i>'),
        ('.ā', '<aa_i>'),
        ('.æ', '<ac_i>'),
        ('.e', '<e_i>'),
        ('.ē', '<ee_i>'),
        ('.ê', '<ec_i>'),
        ('.i', '<i_i>'),
        ('.ī', '<ii_i>'),
        ('.o', '<o_i>'),
        ('.ō', '<oo_i>'),
        ('.ô', '<oc_i>'),
        ('.u', '<u_i>'),
        ('.ū', '<uu_i>'),
        ('.ai', '<ai_i>'),
        ('.au', '<au_i>'),
        ('.l̥', '<l_vcl_i>'),
        ('.r̥', '<r_vcl_i>'),
        ('.l̥̄', '<ll_vcl_i>'),
        ('.r̥̄', '<rr_vcl_i>'),
        ('bʰ', '<bh>'),
        ('cʰ', '<ch>'),
        ('dʰ', '<dh>'),
        ('ḍʰ', '<ddh>'),
        ('gʰ', '<gh>'),
        ('jʰ', '<jh>'),
        ('kʰ', '<kh>'),
        ('pʰ', '<ph>'),
        ('ṛʰ', '<rdh>'),
        ('tʰ', '<th>'),
        ('ṭʰ', '<tth>'),
        ('m̐', '<cnd>'),
        ('kⸯ', '<k_chl>'),
        ('lⸯ', '<l_chl>'),
        ('ḷⸯ', '<ll_chl>'),
        ('nⸯ', '<n_chl>'),
        ('ṇⸯ', '<nn_chl>'),
        ('ṟⸯ', '<rr_chl>'),
        ('rⸯ', '<reph>'),
        ('r̆', '<r_eye>'),
        ('õm', '<om>'),
    ]),
]


class Iso2TypTest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
