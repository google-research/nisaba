# Copyright 2021 Nisaba Authors.
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


"""Tests that the sigma FST has the expected set of FST properties."""

import itertools

import pynini
from absl.testing import absltest
from absl.testing import parameterized
from nisaba.scripts.brahmic import util as u
from nisaba.scripts.utils import test_util


class FstPropertiesTest(parameterized.TestCase,
                        test_util.FstPropertiesTestCase):

  @parameterized.parameters(
      itertools.product(
          u.SCRIPTS,
          (pynini.ACYCLIC, pynini.UNWEIGHTED, pynini.I_DETERMINISTIC,
           pynini.NO_EPSILONS, pynini.ACCESSIBLE, pynini.COACCESSIBLE,
           pynini.ACCEPTOR)))
  def test_sigma_utf8(self, script: str, prop: pynini.FstProperties):
    fst = u.OpenFstFromBrahmicFar('sigma', script, token_type='utf8')
    self.assertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(
          u.SCRIPTS,
          (pynini.CYCLIC, pynini.UNWEIGHTED, pynini.I_DETERMINISTIC,
           pynini.NO_EPSILONS, pynini.ACCESSIBLE, pynini.COACCESSIBLE,
           pynini.ACCEPTOR), ('byte', 'utf8')))
  def test_wellformed(self, script: str, prop: pynini.FstProperties,
                      token_type: str):
    fst = u.OpenFstFromBrahmicFar('wellformed', script, token_type=token_type)
    self.assertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(u.SCRIPTS + ['Brahmic'],
                        (pynini.UNWEIGHTED, pynini.NO_EPSILONS, pynini.CYCLIC,
                         pynini.ACCESSIBLE, pynini.COACCESSIBLE),
                        ('byte', 'utf8')))
  def test_nfc(self, script: str, prop: pynini.FstProperties, token_type: str):
    fst = u.OpenFstFromBrahmicFar('nfc', script, token_type=token_type)
    self.assertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(u.SCRIPTS,
                        (pynini.UNWEIGHTED, pynini.NO_EPSILONS, pynini.CYCLIC,
                         pynini.ACCESSIBLE, pynini.COACCESSIBLE),
                        ('byte', 'utf8')))
  def test_visual_norm(self, script: str, prop: pynini.FstProperties,
                       token_type: str):
    fst = u.OpenFstFromBrahmicFar('visual_norm', script, token_type=token_type)
    self.assertFstCompliesWithProperties(fst, prop)

  @parameterized.parameters(
      itertools.product(u.FIXED_RULE_SCRIPTS,
                        (pynini.ACCESSIBLE,
                         pynini.COACCESSIBLE,
                         pynini.CYCLIC,
                         # TODO: Investigate why it is not deterministic
                         # pynini.I_DETERMINISTIC,
                         pynini.NO_EPSILONS,
                         pynini.UNWEIGHTED),
                        ('byte', 'utf8')))
  def test_fixed(self,
                 script: str,
                 prop: pynini.FstProperties,
                 token_type: str):
    fst = u.OpenFstFromBrahmicFar('fixed', script, token_type=token_type)
    self.assertFstCompliesWithProperties(fst, prop)


if __name__ == '__main__':
  absltest.main()
