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


"""A library for making unit tests that verify FST properties."""

from typing import Iterator, List

import pynini
from pynini.lib import utf8
from absl.testing import absltest


def _olabels_iter(f: pynini.Fst) -> Iterator[List[int]]:
  it = f.paths()
  while not it.done():
    yield it.olabels()
    it.next()


def _label_list_to_string_fsa(labels: List[int]) -> pynini.Fst:
  fst = pynini.Fst()
  fst.add_states(len(labels) + 1)
  fst.set_start(0)
  fst.set_final(len(labels))
  for i, lbl in enumerate(labels):
    fst.add_arc(i, pynini.Arc(lbl, lbl, pynini.Weight.one("tropical"), i + 1))
  return fst


class FstPropertiesTestCase(absltest.TestCase):

  def assertFstCompliesWithProperties(
      self, fst: pynini.Fst, expected_props: pynini.FstProperties) -> None:
    if fst.properties(expected_props, True) != expected_props:
      raise AssertionError(
          "Expected {actual} to contain the property {expected}".format(
              expected=expected_props,
              actual=fst.properties(pynini.FST_PROPERTIES, True)))


class FstRandgenTestCase(absltest.TestCase):

  def assertFstProbablyFunctional(self, fst: pynini.Fst,
                                  token_type: pynini.TokenType,
                                  samples: int) -> None:
    """Assert that an Fst is likely funcional by sampling.

    This samples from an Fst's input projection in order to verify that all the
    samples produce exactly one output when composed with the Fst. This is used
    in lieu of statically verifying that an Fst is functional as that isn't easy
    to answer for non-deterministic Fsts. If token_type is set to "byte", then
    the input projection of the FST is intersected with the definition of the
    closure over valid UTF-8 characters to ensure all samples are valid UTF-8
    strings that Python can handle. The maximum length of a sample is set to 100
    labels.

    Args:
      fst: An Fst to verify if is functional.
      token_type: The token_type used to derive the Fst.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If the Fst is found to have a non-functional input sample.
    """
    input_language = pynini.project(fst, "input")
    if token_type == "byte":
      # NOTE: Randgenning directly from the byte machine is bound to lead to
      # trouble since it can generate things that aren't well-formed UTF-8
      # sequences and thus cannot be put into a Python str type.
      input_language = pynini.intersect(input_language,
                                        utf8.VALID_UTF8_CHAR.star)
    input_samples = pynini.randgen(
        input_language, npath=samples, max_length=100)
    with pynini.default_token_type(token_type):
      for olabels in _olabels_iter(input_samples):
        string_fsa = _label_list_to_string_fsa(olabels)
        cascade = string_fsa @ fst
        try:
          cascade.string()
        except pynini.FstOpError as e:
          raise AssertionError(
              "Expected Fst to be functional but input string `{input}`"
              " produced output strings: {outputs}".format(
                  input=string_fsa.string(),
                  outputs=", ".join(
                      f"`{ostring}`" for ostring in
                      cascade.optimize().paths().ostrings()))) from e
