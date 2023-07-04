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

"""Tests that the generated FST has the expected set of FST properties."""

import itertools

import pynini
from absl.testing import absltest
from absl.testing import parameterized
from nisaba.scripts.abjad_alphabet import util as u
from nisaba.scripts.utils import file as uf
from nisaba.scripts.utils import test_util as ut


class FstPropertiesTest(parameterized.TestCase, ut.FstPropertiesTestCase):

  @parameterized.parameters(
      itertools.product(('TO', 'FROM'),
                        (pynini.ACCESSIBLE,
                         pynini.COACCESSIBLE,
                         pynini.CYCLIC,
                         pynini.NO_EPSILONS,
                         pynini.UNWEIGHTED)))
  def test_reversible_roman(self, direction: str, prop: pynini.FstProperties):
    fst = uf.OpenFstFromFar(u.FAR_DIR, 'reversible_roman', 'byte',
                            f'{direction}_ARAB')
    self.AssertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(u.LANGS,
                        ('visual_norm', 'reading_norm'),
                        ('byte', 'utf8'),
                        (pynini.ACCESSIBLE,
                         pynini.COACCESSIBLE,
                         pynini.CYCLIC,
                         pynini.NO_EPSILONS,
                         pynini.UNWEIGHTED)))
  def test_visual_or_reading_norm(self, lang: str, far_name: str,
                                  token_type: str, prop: pynini.FstProperties):
    fst = uf.OpenFstFromFar(u.FAR_DIR, far_name, token_type, lang)
    self.AssertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(('byte', 'utf8'),
                        (pynini.ACCESSIBLE,
                         pynini.COACCESSIBLE,
                         pynini.CYCLIC,
                         pynini.NO_EPSILONS,
                         pynini.UNWEIGHTED)))
  def test_nfc(self, token_type: str, prop: pynini.FstProperties):
    fst = uf.OpenFstFromFar(u.FAR_DIR, 'nfc', token_type, 'ARAB')
    self.AssertFstCompliesWithProperties(fst, prop)


if __name__ == '__main__':
  absltest.main()
