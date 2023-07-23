# Copyright 2023 Nisaba Authors.
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

"""Tests that employ pynini.randgen to verify abjad / alphabet transducers."""

import itertools

from absl.testing import absltest
from absl.testing import parameterized
from nisaba.scripts.abjad_alphabet import util as u
from nisaba.scripts.utils import test_util


class FstRandgenTest(parameterized.TestCase, test_util.FstRandgenTestCase):

  @parameterized.parameters('byte', 'utf8')
  def test_romanization_roundtrip(self, token_type: str):
    nfc = u.open_fst_from_far('nfc', 'ARAB', token_type)
    far = u.open_far('reversible_roman', token_type)
    natv_to_latin = far['FROM_ARAB']
    latin_to_natv = far['TO_ARAB']
    self.AssertFstProbablyIdentity(
        [natv_to_latin, latin_to_natv], token_type, nfc)

  @parameterized.parameters(itertools.product(
      ('visual_norm', 'reading_norm'), u.LANGS, ('byte', 'utf8')))
  def test_visual_or_reading_norm(self, far_name: str, lang: str,
                                  token_type: str):
    fst = u.open_fst_from_far(far_name, lang, token_type)
    self.AssertFstProbablyFunctional(fst, token_type)

  @parameterized.parameters('byte', 'utf8')
  def test_nfc(self, token_type: str):
    fst = u.open_fst_from_far('nfc', 'ARAB', token_type)
    self.AssertFstProbablyFunctional(fst, token_type)


if __name__ == '__main__':
  absltest.main()
