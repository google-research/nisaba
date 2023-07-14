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

from absl import logging  

import pynini
from absl.testing import absltest
from absl.testing import parameterized
from nisaba.scripts.abjad_alphabet import util as u
from nisaba.scripts.utils import file as uf
from nisaba.scripts.utils import test_util as ut


class FstRandgenTest(parameterized.TestCase, ut.FstRandgenTestCase):

  def test_romanization_roundtrip(self):
    far_path = u.FAR_DIR / 'reversible_roman.far'
    with pynini.Far(uf.AsResourcePath(far_path), 'r') as far:
      natv_to_latin = far['FROM_ARAB']
      latin_to_natv = far['TO_ARAB']
      round_trip = natv_to_latin @ latin_to_natv
      self.AssertFstProbablyFunctional(round_trip, token_type='byte')

  @parameterized.parameters(itertools.product(
      u.LANGS, ('visual_norm', 'reading_norm'), ('byte', 'utf8')))
  def test_visual_or_reading_norm(self, lang: str, far_name: str,
                                  token_type: str):
    fst = uf.OpenFstFromFar(u.FAR_DIR, far_name, token_type, lang)
    self.AssertFstProbablyFunctional(fst, token_type)

  @parameterized.parameters('byte', 'utf8')
  def test_nfc(self, token_type: str):
    fst = uf.OpenFstFromFar(u.FAR_DIR, 'nfc', token_type, 'ARAB')
    self.AssertFstProbablyFunctional(fst, token_type)


if __name__ == '__main__':
  absltest.main()
