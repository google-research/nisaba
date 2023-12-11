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

"""A library for making unit tests that verify FST properties."""

import collections
from typing import Callable, Iterator, List, Optional, Tuple

import pynini
from pynini.lib import utf8
from absl.testing import absltest
from nisaba.scripts.utils import rewrite

# Number of random test strings to generate for each FST type and token type.
# TODO: As of this writing, the time it takes for `randgen_test` in
# `abjad_alphabet` is around 4 times longer than that of `brahmic`. If the
# current number of samples and sample lengths are not catching the relevant
# errors in `brahmic`, consider using separate and higher numbers of samples
# and sample lengths for `brahmic`.
NUM_TEST_SAMPLES = 5

# Maximum length of test string.
_MAX_SAMPLE_LENGTH = 5


def _OlabelsIter(f: pynini.Fst) -> Iterator[List[int]]:
  it = f.paths()
  while not it.done():
    yield it.olabels()
    it.next()


def _LabelListToStringFsa(labels: List[int]) -> pynini.Fst:
  fst = pynini.Fst()
  fst.add_states(len(labels) + 1)
  fst.set_start(0)
  fst.set_final(len(labels))
  for i, lbl in enumerate(labels):
    fst.add_arc(i, pynini.Arc(lbl, lbl, pynini.Weight.one("tropical"), i + 1))
  return fst.optimize()


def AssertFstFunctional(fst: pynini.Fst,
                        token_type: pynini.TokenType,
                        string_fsa: pynini.Fst) -> None:
  """Assert that an FST is functional for the given string FSA.

  Args:
    fst: An FST to verify if is functional.
    token_type: The token_type used to derive the Fst.
    string_fsa: The string FSA to verify functional behavior.

  Raises:
    AssertionError: If the FST is found to have a non-functional.
  """
  with pynini.default_token_type(token_type):
    AssertIfSinglePath(string_fsa, string_fsa @ fst)


def AssertIfSinglePath(log_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Does nothing if given string FST has only one path; throws otherwise.

  If there is more than one path in the FST, then string() method on the FST
  will throw FstOpError. That exception is converted to AssertError with
  relevant error message with input string from the given string FSA.

  Args:
    log_str_fsa: Input string FSA specific to the FST. Used in the
        exception message.
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
            input=log_str_fsa.string(),
            outputs=", ".join(
                f"`{ostring}`" for ostring in
                fst.optimize().paths().ostrings()))) from e


def _VerifyIfSingleShortestPath(input_str_fsa: pynini.Fst, fst: pynini.Fst):
  """Throws if given string FST has multiple shorest paths; pass otherwise.

  Args:
    input_str_fsa: Input string FSA specific to the FST. Used in the
        exception message.
    fst: FST to be verified if it has only a single path.

  Raises:
    AssertionError: If the FST is found to have more than one shortest path.
  """
  input_str = input_str_fsa.string()
  out_weights = collections.defaultdict(set)
  for _, out, weight in fst.optimize().paths().items():
    out_weights[int(str(weight))].add(out)
  outstrs = out_weights[min(out_weights)]

  if len(outstrs) > 1:
    raise AssertionError(
        f"Expected FST to produce single best output for input `{input_str}`;"
        f" however, produced multiple: `{', '.join(outstrs)}`")


def AssertIdentity(input_str_fsa: pynini.Fst, fst: pynini.Fst):
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

  if not out_weights:
    raise AssertionError(
        f"Expected FST identical to `{input_str}`, but it is empty.")

  outstrs = out_weights[min(out_weights)]
  if outstrs - {input_str}:
    raise AssertionError(
        f"Expected FST to be idenity but input `{input_str}`"
        f" produced output string(s): `{', '.join(outstrs)}`")


class FstPropertiesTestCase(absltest.TestCase):

  def AssertFstCompliesWithProperties(
      self, fst: pynini.Fst, expected_props: pynini.FstProperties) -> None:
    if fst.properties(expected_props, True) != expected_props:
      raise AssertionError(
          "Expected {actual} to contain the property {expected}".format(
              expected=expected_props,
              actual=fst.properties(pynini.FST_PROPERTIES, True)))


class FstRandgenTestCase(absltest.TestCase):
  """Tests using sampling to verify properties of an FST."""

  def AssertFstProbablyFunctional(self, fst: pynini.Fst,
                                  token_type: pynini.TokenType,
                                  samples: int = NUM_TEST_SAMPLES) -> None:
    """Asserts that an FST is likely functional by sampling.

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
    self._AssertFstSampledBehavior(
        [fst], token_type, samples, AssertIfSinglePath)

  def AssertFstSingleShortestPath(self, fst: pynini.Fst,
                                  token_type: pynini.TokenType,
                                  samples: int = NUM_TEST_SAMPLES) -> None:
    """Empirically asserts an FST produces a unique shortest path for the input.

    This samples from an FST's input projection to verify that all the samples
    produce unique best output when composed with the FST. This is used in lieu
    of statically verifying that an FST is functional as that isn't easy to
    answer for non-deterministic weighted Fsts. If token_type is set to "byte",
    then the input projection of the FST is intersected with the definition of
    the closure over valid UTF-8 characters to ensure all samples are valid
    UTF-8 strings that Python can handle. The maximum length of a sample is set
    to 100 labels.


    Args:
      fst: An FST to verify if it produces single best output.
      token_type: The token_type used to derive the FST.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If the FST is found to have a non-functional input sample.
    """
    self._AssertFstSampledBehavior(
        [fst], token_type, samples, _VerifyIfSingleShortestPath)

  def AssertFstProbablyIdentity(self, fsts: List[pynini.Fst],
                                token_type: pynini.TokenType,
                                norm_fst: pynini.Fst,
                                samples: int = NUM_TEST_SAMPLES) -> None:
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
      norm_fst: The FST to normalize the randomly generated string; usually
            NFC or Visual Norm.
      samples: The number of input samples to take to verify functionality.

    Raises:
      AssertionError: If, for any sample, the FSTs composed on it produces
          anything other than the sample itself at its minimum weight path.
    """
    self._AssertFstSampledBehavior(
        fsts, token_type, samples, AssertIdentity, norm_fst)

  def _AssertFstSampledBehavior(
      self, fsts: List[pynini.Fst],
      token_type: pynini.TokenType,
      samples: int,
      assert_function: Callable[[pynini.Fst, pynini.Fst], None],
      norm_fst: Optional[pynini.Fst] = None) -> None:
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
      norm_fst: The FST to normalize the randomly generated string; usually
          NFC or Visual Norm.
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
      for ilabels in _OlabelsIter(input_samples):
        input_str_fsa = _LabelListToStringFsa(ilabels)
        output_str = rewrite.ComposeFsts([input_str_fsa] + fsts)

        # Please note that `norm` is not idempotent if it is Arabic NFC which
        # cannot handle the reordering of a large number of SHADDA, FATHA,
        # FATHATAN, KASRA, etc.. Even though this is only a theoretical
        # possibility, for randgen test, the number of NFCs in the round trip
        # should be the same as the count of NFCs applied to the input before
        # the assert function.
        if norm_fst:
          input_str_fsa = rewrite.ComposeFsts([input_str_fsa, norm_fst])
        assert_function(input_str_fsa, output_str)


class FstTestCase(absltest.TestCase):
  """Collection of asserts related to string FSTs."""

  def AssertFstStrIO(self, fst: pynini.Fst,
                     input_str: str, expected_str: str) -> None:
    """Asserts that given FST produces expeted_str for the given input_str.

    Args:
      fst: FST being tested.
      input_str: Input string to be suppled to the FST.
      expected_str: Expected string output from the FST on input_str.
    """

    input_str_fsa = pynini.accep(input_str)
    output_fst = rewrite.ComposeFsts([input_str_fsa, fst])
    actual_output = output_fst.string()
    self.assertEqual(actual_output, expected_str)

  def AssertFstStrIoTestCases(
      self,
      test_cases:
      List[Tuple[Callable[[], pynini.Fst], List[Tuple[str, str]]]]) -> None:
    """Asserts on every test in a list of FST input-ouput testcases.

    Args:
      test_cases: It is a list of tuples which carry an FST builder function
      and a list of input / output test string tuples. Example:
          ```
          [
              (ISO_TO_TYP_DECOMPOSED_FST_BUILDER_FUNCION, [
                  ('a', '(a)'),
                  ('ā', '(aa)'),
              ]),
              (ISO_TO_TYP_FST_BUILDER_FUNCION, [
                  ('ai', '(ai)'),
                  ('au', '(au)'),
              ]),
          ]
          ```
    """

    for fst_builder, test_pairs in test_cases:
      for token_type in ("utf8", "byte"):
        with pynini.default_token_type(token_type):
          for test_pair in test_pairs:
            self.AssertFstStrIO(fst_builder(), *test_pair)

  def _FstLikeString(self, fstlike: pynini.FstLike) -> str:
    return fstlike.string() if isinstance(fstlike, pynini.Fst) else fstlike

  def AssertEqualFstLike(self, fstlike: pynini.FstLike,
                         expected_fstlike: str) -> None:
    """Asserts that given FstLike is equal to expected_str.

    Args:
      fstlike : FST or string being tested.
      expected_fstlike: Expected Fst or string output.
    """
    self.assertEqual(
        self._FstLikeString(fstlike),
        self._FstLikeString(expected_fstlike))

  def AssertEqualFstLikeTestCases(
      self,
      test_cases:
      List[Tuple[Callable[[str], pynini.Fst], List[Tuple[List[str], str]]]],
  ) -> None:
    """Asserts on every test in a list of FstLike input-ouput testcases.

    Args:
      test_cases: It is a list of tuples which carry an FST builder function
      and a list of input / output test string tuples. Example:
          ```
          [
              (enclose_function, [
                  (['a', '(', ')'], '(a)'),
                  (['a', '<', '>'], '<a>'),
              ]),
              (enclose_phoneme_function, [
                  (['a'], '{a}'),
                  ...
              ]),
          ]
          ```
    """

    for fst_builder, test_pairs in test_cases:
      for token_type in ("utf8", "byte"):
        with pynini.default_token_type(token_type):
          for args, expected_str in test_pairs:
            self.AssertEqualFstLike(fst_builder(*args), expected_str)
