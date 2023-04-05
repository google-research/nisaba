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

r"""Acyclic acceptor accepting characters from Brahmic scripts."""

import os
import pathlib
from typing import Iterable, Set

import pynini
import pathlib
import nisaba.scripts.utils.file as uf

ZWNJ = "\u200C"  # Zero Width Non-Joiner
ZWJ = "\u200D"  # Zero Width Joiner
ZWS = "\u200B"  # Zero Width Space


def _read_string_file_chars_to_set(files: Iterable[os.PathLike],
                                   relevant_fields: int) -> Set[str]:
  """Reads the characters under some selection from some file paths into a set.

  Arguments:
    files: An Iterable of filepaths
    relevant_fields: The number of tab-delimited fields from the beginning in a
      StringFile to process. Must be a positive integer.

  Returns:
    Set[str] -- The set of all characters, under the selection in the files.
  """
  chars = set()
  for fname in files:
    with pathlib.Path(uf.AsResourcePath(pathlib.Path(fname))).open("rt", encoding="utf8") as f:
      for line in f:
        if line.startswith("#"):
          continue
        fields = line.strip().split("\t")[0:relevant_fields]
        for field in fields:
          chars.update(field)
  return chars


def derive_chars(both_sides: Iterable[os.PathLike] = (),
                 input_side: Iterable[os.PathLike] = ()) -> Set[str]:
  """Create the set of characters in a script from StringFiles.

  Args:
    both_sides: Iterable of Paths relative to depot of a StringFile, both of
      whose sides contain in-script characters.
    input_side: Iterable of Paths relative to depot of a StringFile whose input
      side contains in-script characters.

  Returns:
    The set of characters in a script.
  """

  all_chars = _read_string_file_chars_to_set(both_sides, relevant_fields=2)
  all_chars.update(
      _read_string_file_chars_to_set(input_side, relevant_fields=1))

  return all_chars


def derive_sigma(chars: Set[str]) -> pynini.Fst:
  """Creates an unweighted FSA over the given set of characters and joiners.

  Args:
    chars: Set of all characters.

  Returns:
    pynini.Fst: An unweighted FSA that accepts this finite sigma language.
  """

  sigma = pynini.string_map(zip(chars))
  sigma.project("output")  # Project in-place
  sigma.union(ZWNJ, ZWJ, ZWS)
  return sigma.optimize()
