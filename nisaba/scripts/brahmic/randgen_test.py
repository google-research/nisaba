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

"""Tests that the sigma FST has the expected set of FST properties."""

import itertools

import pynini
from absl.testing import absltest
from absl.testing import parameterized
from nisaba.scripts.brahmic import util as u
from nisaba.scripts.utils import test_util as tu


class FstRandgenTest(parameterized.TestCase, tu.FstRandgenTestCase):

  @parameterized.parameters(
      itertools.product(u.SCRIPTS + ['brahmic'], ('byte', 'utf8'))
  )
  def test_nfc(self, script: str, token_type: pynini.TokenType):
    fst = u.OpenFstFromBrahmicFar('nfc', script, token_type)
    self.AssertFstProbablyFunctional(fst, token_type, samples=1_000_000)

  @parameterized.parameters(itertools.product(u.SCRIPTS, ('byte', 'utf8')))
  def test_visual_norm(self, script: str, token_type: pynini.TokenType):
    fst = u.OpenFstFromBrahmicFar('visual_norm', script, token_type)
    self.AssertFstProbablyFunctional(fst, token_type)

  @parameterized.parameters(
      itertools.product(u.READING_NORM_LANGS, ('byte', 'utf8'))
  )
  def test_reading_norm(self, script_lang: str, token_type: pynini.TokenType):
    script, lang = script_lang
    tag = lang if lang else script
    fst = u.OpenFstFromBrahmicFar('reading_norm', tag, token_type)
    self.AssertFstProbablyFunctional(fst, token_type)

  @parameterized.parameters(itertools.product(u.SCRIPTS, ('byte', 'utf8')))
  def test_from_iso_to_native_single_best(
      self, script: str, token_type: pynini.TokenType
  ):
    fst = u.OpenFstFromBrahmicFar('iso', f'TO_{script}', token_type)
    self.AssertFstSingleShortestPath(fst, token_type)

  @parameterized.parameters(itertools.product(u.SCRIPTS, ('byte', 'utf8')))
  def test_from_native_to_iso_single_best(
      self, script: str, token_type: pynini.TokenType
  ):
    fst = u.OpenFstFromBrahmicFar('iso', f'FROM_{script}', token_type)
    self.AssertFstSingleShortestPath(fst, token_type)

  @parameterized.parameters(itertools.product(u.SCRIPTS, ('byte', 'utf8')))
  def test_iso_roundtrip(self, script: str, token_type: pynini.TokenType):
    natv_to_iso = u.OpenFstFromBrahmicFar('iso', f'FROM_{script}', token_type)
    iso_to_natv = u.OpenFstFromBrahmicFar('iso', f'TO_{script}', token_type)
    nfc = u.OpenFstFromBrahmicFar('nfc', script, token_type)
    self.AssertFstProbablyIdentity([natv_to_iso, iso_to_natv], token_type, nfc)

  @parameterized.parameters(
      itertools.product(u.FIXED_RULE_SCRIPTS, ('byte', 'utf8'))
  )
  def test_fixed(self, script: str, token_type: pynini.TokenType):
    fst = u.OpenFstFromBrahmicFar('fixed', script, token_type)
    self.AssertFstSingleShortestPath(fst, token_type)


if __name__ == '__main__':
  absltest.main()
