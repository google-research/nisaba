# Copyright 2024 Nisaba Authors.
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

from absl.testing import absltest
from nisaba.scripts.natural_translit.brahmic import en_spellout as en
from nisaba.scripts.natural_translit.utils import test_op

_A = en._SPELLOUTS.a
_HI_DEVA = en.speller(en.Language.HI, en.Script.DEVA)
_ML_MLYM = en.speller(en.Language.ML, en.Script.MLYM)
_UR_ARAB = en.speller(en.Language.UR, en.Script.ARAB)


class EnSpelloutTest(test_op.TestCase):

  def test_a(self):
    self.assertEqual(_A.text, 'a')
    self.assertEqual(_A.bn_beng, 'এ')
    self.assertEqual(_A.gu_gujr, 'એ')
    self.assertEqual(_A.hi_deva, 'ए')
    self.assertEqual(_A.kn_knda, 'ಎ')
    self.assertEqual(_A.ml_mlym, 'എ')
    self.assertEqual(_A.mr_deva, 'ए')
    self.assertEqual(_A.or_orya, 'ଏ')
    self.assertEqual(_A.pa_guru, 'ਏ')
    self.assertEqual(_A.sd_arab, 'اي')
    self.assertEqual(_A.si_sinh, 'ඒ')
    self.assertEqual(_A.ta_taml, 'ஏ')
    self.assertEqual(_A.te_telu, 'ఎ')
    self.assertEqual(_A.ur_arab, 'اے')

  def test_not_separated(self):
    self.AssertEqualValue('a' @ _HI_DEVA, 'ए')
    self.AssertEqualValue('A' @ _HI_DEVA, 'ए')
    self.AssertEqualValue('pdf' @ _HI_DEVA, 'पीडीएफ़')

  def test_zwnj(self):
    self.AssertEqualValue('a' @ _ML_MLYM, 'എ')
    self.AssertEqualValue('A' @ _ML_MLYM, 'എ')
    self.AssertEqualValue('pdf' @ _ML_MLYM, 'പിഡിഎഫ്')

  def test_space_separated(self):
    self.AssertEqualValue('a' @ _UR_ARAB, 'اے')
    self.AssertEqualValue('A' @ _UR_ARAB, 'اے')
    self.AssertEqualValue('pdf' @ _UR_ARAB, 'پی ڈی ایف')


if __name__ == '__main__':
  absltest.main()
