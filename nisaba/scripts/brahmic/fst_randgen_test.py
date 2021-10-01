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
from nisaba.scripts.utils import file
from nisaba.scripts.utils import test_util


class FstRandgenTest(parameterized.TestCase, test_util.FstRandgenTestCase):

  @parameterized.parameters(
      itertools.product(u.SCRIPTS + ['brahmic'], ('byte', 'utf8')))
  def test_nfc(self, script: str, token_type: str):
    fst = u.OpenFstFromBrahmicFar('nfc', script, token_type=token_type)
    self.assertFstProbablyFunctional(fst, token_type=token_type, samples=1e6)

  @parameterized.parameters(itertools.product(u.SCRIPTS, ('byte', 'utf8')))
  def test_visual_norm(self, script: str, token_type: str):
    fst = u.OpenFstFromBrahmicFar('visual_norm', script, token_type=token_type)
    self.assertFstProbablyFunctional(fst, token_type=token_type,
                                     samples=test_util.NUM_TEST_SAMPLES)

  @parameterized.parameters(u.SCRIPTS)
  def test_iso_roundtrip(self, tag: str):
    tag = tag.upper()
    far_path = u.FAR_DIR / 'iso.far'
    with pynini.Far(file.AsResourcePath(far_path), 'r') as far:
      natv_to_iso = far[f'FROM_{tag}']
      iso_to_natv = far[f'TO_{tag}']
      self.assertFstProbablyIdentity([natv_to_iso, iso_to_natv],
                                     token_type='byte',
                                     samples=test_util.NUM_TEST_SAMPLES)

  @parameterized.parameters(
      itertools.product(u.FIXED_RULE_SCRIPTS, ('byte', 'utf8')))
  def test_fixed(self, script: str, token_type: str):
    fst = u.OpenFstFromBrahmicFar('fixed', script, token_type=token_type)
    self.assertFstProbablyFunctional(fst, token_type=token_type, samples=1e6)


if __name__ == '__main__':
  absltest.main()
