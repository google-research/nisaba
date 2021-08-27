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
from nisaba.scripts.utils import rewrite

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


def assert_fst_functional(fst: pynini.Fst,
                          token_type: pynini.TokenType,
                          string_fsa: pynini.Fst) -> None:
  """Assert that an FST is funcional for the given string FSA.

  Args:
    fst: An FST to verify if is functional.
    token_type: The token_type used to derive the Fst.
    string_fsa: The string FSA to verify functional behavior.

  Raises:
    AssertionError: If the FST is found to have a non-functional.
  """
  with pynini.default_token_type(token_type):
    verify_if_single_path(string_fsa, string_fsa @ fst)


def verify_if_single_path(input_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Does nothing if given string FST has only one path; throws otherwise.

  If there is more than one path in the FST, then string() method on the FST
  will throw FstOpError. That exception is converted to AssertError with
  relevant error message with input string from the given string FSA.

  Args:
    input_str_fsa: Input string FSA specific to the FST. Used in the exception
      message.
    fst: FST to be verified if it has only a single path.

  Raises:
    AssertionError: If the FST is found to have more than one path.
  """
  try:
    fst.string()
  except pynini.FstOpError as e:
    raise AssertionError(
        "Expected FST to be functional but input string `{input}`"
        " produced multiple output strings: {outputs}".format(
            input=input_str_fsa.string(),
            outputs=", ".join(
                f"`{ostring}`"
                for ostring in fst.optimize().paths().ostrings()))) from e


def verify_identity(input_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Verifies if FST produces only the input string at its minimum weight path.

  Throws AssertError with a detailed error message on verification failure;
  otherwise do nothing.

  Args:
    input_str_fsa: Input string FSA to be compared with the minimum weight path
      in the FST.
    fst: FST to be verified.

  Raises:
    AssertionError: If the verification has failed; that is, if the given FST
    produces anything other than the input string at its minimum weight path.
  """
  input_str = input_str_fsa.string()
  out_weights = collections.defaultdict(set)
  for _, out, weight in fst.optimize().paths().items():
    out_weights[int(str(weight))].add(out)
  outstrs = out_weights[min(out_weights)]

  if outstrs - {input_str}:
    raise AssertionError(f"Expected FST to be idenity but input `{input_str}`"
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
    """Asserts that an FST is likely funcional by sampling.

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
    self._assert_fst_sampled_behavior([fst], token_type, samples,
                                      verify_if_single_path)

  def assertFstProbablyIdentity(self, fsts: List[pynini.Fst],
                                token_type: pynini.TokenType,
                                samples: int) -> None:
    """Asserts that FSTs composed on samples behaves as an identity.

    This samples from first FST's input projection in order to verify that all
    the samples produce idenity in its minimum weighted output, when composed
    with given FSTs. This is approximately verifying that FSTs together behave
    as an identity to check for reversibility/round-tripping. If token_type is
    set to "byte", then the input projection of the FST is intersected with the
    definition of the closure over valid UTF-8 characters to ensure all samples
    are valid UTF-8 strings that Python can handle. The maximum length of a
    sample is set to 100 labels.

    Args:
      fsts: List of FSTs to be applied on a sample to verify if the resultant
        FST generates sample itself at its minimum weighted path.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If, for any sample, the FSTs composed on it produces
          anything other than the sample itself at its minimum weight path.
    """
    self._assert_fst_sampled_behavior(fsts, token_type, samples,
                                      verify_identity)

  def _assert_fst_sampled_behavior(
      self, fsts: List[pynini.Fst], token_type: pynini.TokenType, samples: int,
      assert_function: Callable[[pynini.Fst, pynini.Fst], None]) -> None:
    """Asserts that FST composed on samples is follow a specific behavior.

    This samples from first FST's input projection in order to assert a
    behavior when composed with the FSTs. This is used in lieu of statically
    verifying that this composition has a specific property as that isn't easy
    to answer for non-deterministic FSTs. If token_type is set to "byte", then
    the input projection of the FST is intersected with the definition of the
    closure over valid UTF-8 characters to ensure all samples are valid UTF-8
    strings that Python can handle. The maximum length of a sample is set to 100
    labels.

    Args:
      fsts: List of FSTs to be applied on a sample to verify if the resultant
        FST obeys the property specified in the function.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.
      assert_function: An assert function with  input string FSA and output FST
        as parameters. This function is run in `pynini.default_token_type`
        environment. This function raises AssertionError on assert failure.
    """
    input_language = pynini.project(fsts[0], "input")
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
        output_fst = rewrite.ComposeFsts([input_str_fsa] + fsts)
        assert_function(input_str_fsa, output_fst)
