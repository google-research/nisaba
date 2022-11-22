# Copyright 2022 Nisaba Authors.
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

"""Multilingual phonological operations."""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw


def legal_onset(onset_cl: p.FstLike) -> p.Fst:
  """Legal onset.

  A syllable can start with a consonant, a permitted consonant cluster followed
  by a vowel, or just a vowel. Since in native words, schwa is pronounced before
  an independent vowel, the vowel onset has been left out of this function.

  Args:
    onset_cl: Permitted onset consonant clusters for the language.

  Returns:
    Following call:
  ```
  _legal_onset(rw.concat(ph.STOP, ph.RHOTIC))

  ```
  would return:
  ```
  p.union(
      '{b}{a}',
      '{b}gr.GRAPHEMES{a}',
      ...
      '{b}{r}{a}',
      '{b}gr.GRAPHEMES{r}{a}'
      '{b}gr.GRAPHEMES{r}gr.GRAPHEMES{a}'
      ...
  )
  """
  return rw.concat_r(p.union(ph.CONSONANT, onset_cl).optimize(), ph.VOWEL)


def legal_coda(coda_cl: p.FstLike) -> p.Fst:
  """Legal coda.

  A syllable can end with a just a vowel, or a vowel followed by a consonant or
  a permitted consonant cluster.

  Args:
    coda_cl: Permitted coda consonant clusters for the language.

  Returns:
    Following call:
  ```
  _legal_coda(rw.concat(ph.RHOTIC, ph.STOP))

  ```
  would return:
  ```
  p.union(
      '{a}',
      '{a_l}',
      ...
      '{a}gr.GRAPHEMES{b}',
      ...
      '{a}gr.GRAPHEMES{r}gr.GRAPHEMES{b}'
      ...
  )
  """
  return rw.concat_r(ph.VOWEL, p.union(ph.CONSONANT, coda_cl).optimize().ques)

# Voicing

VOICING_OP = p.union(
    p.cross(ph.CH, ph.JH),
    p.cross(ph.K, ph.G),
    p.cross(ph.P, ph.B),
    p.cross(ph.T, ph.D),
    p.cross(ph.TI, ph.DI),
    p.cross(ph.TT, ph.DD)).optimize()


def voicing(
    preceding: p.FstLike,
    following: p.FstLike) -> p.Fst:
  """Voicing. See rewrite_by_operation for argument details."""
  return rw.rewrite_operation_by_context(
      VOICING_OP,
      preceding,
      following)

