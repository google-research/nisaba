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

"""Syllable structure."""

import pynini as pyn
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import list_op as ls


def legal_onset(
    nucleic: pyn.FstLike,
    non_nucleic: pyn.FstLike,
    onset_cl: pyn.FstLike
) -> pyn.Fst:
  """Legal onset.

  A syllable can start with a consonant, a permitted consonant cluster followed
  by a vowel, or just a vowel. Since in native words, schwa is pronounced before
  an independent vowel, the vowel onset has been left out of this function.

  Args:
    nucleic: Phonemes that can be the nucleus of a syllable.
    non_nucleic: Single non-nucleic phonemes allowed at onset.
    onset_cl: Non-nucleic clusters allowed at onset.

  Returns:
    Rewrite fst.

  Following call:
  ```
  _legal_onset(cc.concat_r(ph.STOP, ph.RHOTIC))
  ```
  will return:
  ```
  pyn.union(
      '{b}{a}',
      '{b}gr.GRAPHEMES{a}',
      ...
      '{b}{r}{a}',
      '{b}gr.GRAPHEMES{r}{a}'
      '{b}gr.GRAPHEMES{r}gr.GRAPHEMES{a}'
      ...
  )
  ```
  """
  return cc.concat_r(ls.union_opt(non_nucleic, onset_cl), nucleic)


def legal_coda(
    nucleic: pyn.FstLike,
    non_nucleic: pyn.FstLike,
    coda_cl: pyn.FstLike
) -> pyn.Fst:
  """Legal coda.

  A syllable can end with a just a vowel, or a vowel followed by a consonant or
  a permitted consonant cluster.

  Args:
    nucleic: Phonemes that can be the nucleus of a syllable.
    non_nucleic: Single non-nucleic phonemes allowed at coda.
    coda_cl: Non-nucleic clusters allowed at coda.

  Returns:
    Rewrite fst.

  Following call:
  ```
  _legal_coda(cc.concat_r(ph.RHOTIC, ph.STOP))
  ```
  will return:
  ```
  pyn.union(
      '{a}',
      '{a}{:h}',
      ...
      '{a}gr.GRAPHEMES{b}',
      ...
      '{a}gr.GRAPHEMES{r}gr.GRAPHEMES{b}'
      ...
  )
  ```
  """
  return cc.concat_r(nucleic, ls.union_opt(non_nucleic, coda_cl).ques)
