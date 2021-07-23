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

import collections
from typing import Callable, Iterator, List

import pynini
from pynini.lib import utf8
from absl.testing import absltest

# Number of random test strings to generate for each FST type and token type.
NUM_TEST_SAMPLES = 5

# Maximum length of test string.
_MAX_SAMPLE_LENGTH = 5


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


def verify_if_single_path(input_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Do nothing if a string FST has only one path; throws otherwise.

  If there is more than one path in the FST, then string() method on the FST
  will throw FstOpError. That exception is converted to AssertError with
  relevant error message.

  Args:
    input_str_fsa: Input string FSA used to create the FST.
                   Used in the exception message.
    fst: An FST to verify if is single path.

  Raises:
    AssertionError: If the FST is found to have more than one path.
  """
  try:
    fst.string()
  except pynini.FstOpError as e:
    raise AssertionError(
        "Expected FST to be functional but input string `{input}`"
        " produced output strings: {outputs}".format(
            input=input_str_fsa.string(),
            outputs=", ".join(
                f"`{ostring}`" for ostring in
                fst.optimize().paths().ostrings()))) from e


def verify_identity(input_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Verifies if FST produces only the input string at its minimum weight path.

  If there is more than one path in the FST with mininum weight or if this only
  path outputs string different from the input string, then throws AssertError
  with a detailed error message; otherwise do nothing.

  Args:
    input_str_fsa: Input string FSA used to create the FST.
    fst: An FST to verify if its minimum weight path is the given input string.

  Raises:
    AssertionError: If the FST is found to have more than one path.
  """
  input_str = input_str_fsa.string()
  out_weights = collections.defaultdict(set)
  for _, out, weight in fst.optimize().paths().items():
    out_weights[int(str(weight))].add(out)
  outstrs = out_weights[min(out_weights)]

  if outstrs - {input_str}:
    raise AssertionError(
        f'Expected FST to be idenity but input `{input_str}`'
        f' produced output string(s): `{", ".join(outstrs)}`')


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
    """Assert that an FST is likely funcional by sampling.

    This samples from an Fst's input projection in order to verify that all the
    samples produce exactly one output when composed with the FST. This is used
    in lieu of statically verifying that an FST is functional as that isn't easy
    to answer for non-deterministic Fsts. If token_type is set to "byte", then
    the input projection of the FST is intersected with the definition of the
    closure over valid UTF-8 characters to ensure all samples are valid UTF-8
    strings that Python can handle. The maximum length of a sample is set to 100
    labels.

    Args:
      fst: An FST to verify if is functional.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If the FST is found to have a non-functional input sample.
    """
    self._assert_fst_property(fst, token_type, samples, verify_if_single_path)

  def assertFstProbablyIdentity(self, fst: pynini.Fst,
                                token_type: pynini.TokenType,
                                samples: int) -> None:
    """Assert that an FST likely generates an identity by sampling.

    This samples from an Fst's input projection in order to verify that all the
    samples produce idenity in its minimum weighted output, when composed with
    the FST. This is statically verifying that an FST is identity to check for
    reversibility/round-tripping. If token_type is set to "byte", then
    the input projection of the FST is intersected with the definition of the
    closure over valid UTF-8 characters to ensure all samples are valid UTF-8
    strings that Python can handle. The maximum length of a sample is set to 100
    labels.

    Args:
      fst: An FST to verify if is idenity at its minimum weighted path.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If the FST is found to have a non-functional input sample.
    """
    self._assert_fst_property(fst, token_type, samples, verify_identity)

  def _assert_fst_property(
      self, fst: pynini.Fst,
      token_type: pynini.TokenType,
      samples: int,
      verify_function: Callable[[pynini.Fst, pynini.Fst], None]) -> None:
    """Assert that an FST is likely follow a property by sampling.

    This samples from an Fst's input projection in order to verify that all the
    samples produce the output being verified. This is used in lieu of
    statically verifying that an FST has a specific property as that isn't easy
    to answer for non-deterministic Fsts. If token_type is set to "byte", then
    the input projection of the FST is intersected with the definition of the
    closure over valid UTF-8 characters to ensure all samples are valid UTF-8
    strings that Python can handle. The maximum length of a sample is set to 100
    labels.

    Args:
      fst: An FST to verify if it obeys the property specified in the function.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.
      verify_function: Verification function taking the input string FSA and
          output FSA.

    Raises:
      AssertionError: If the FST is found to have a non-functional input sample.
    """
    input_language = pynini.project(fst, "input")
    if token_type == "byte":
      # NOTE: Randgenning directly from the byte machine is bound to lead to
      # trouble since it can generate things that aren't well-formed UTF-8
      # sequences and thus cannot be put into a Python str type.
      input_language = pynini.intersect(input_language,
                                        utf8.VALID_UTF8_CHAR.star)
    input_samples = pynini.randgen(
        input_language, npath=samples, max_length=_MAX_SAMPLE_LENGTH)
    with pynini.default_token_type(token_type):
      for ilabels in _olabels_iter(input_samples):
        input_str_fsa = _label_list_to_string_fsa(ilabels)
        output_fst = input_str_fsa @ fst
        verify_function(input_str_fsa, output_fst)
