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

r"""Acyclic acceptor accepting characters from Brahmic scripts."""

from typing import Iterable, Set

import unicodedata

import pynini
from pynini.lib import pynutil
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.char as uc
import nisaba.scripts.utils.rewrite as ur


def script_chars(script: str) -> Set[str]:
  """Creates the set of characters in a script."""
  return uc.derive_chars(
      input_side=[
          u.SCRIPT_DIR / script / "accept.tsv",
          u.SCRIPT_DIR / script / "coda.tsv",
          u.SCRIPT_DIR / script / "consonant.tsv",
          u.SCRIPT_DIR / script / "dead_consonant.tsv",
          u.SCRIPT_DIR / script / "standalone.tsv",
          u.SCRIPT_DIR / script / "subjoined_consonant.tsv",
          u.SCRIPT_DIR / script / "virama.tsv",
          u.SCRIPT_DIR / script / "vowel.tsv",
          u.SCRIPT_DIR / script / "vowel_length_sign.tsv",
          u.SCRIPT_DIR / script / "vowel_sign.tsv",
      ],
      both_sides=[
          u.SCRIPT_DIR / script / "nfc.tsv",
          u.SCRIPT_DIR / script / "visual_rewrite.tsv",
      ])


def consonants(script: str) -> Set[str]:
  """Returns the set of consonants in a script."""
  return uc.derive_chars(input_side=[u.SCRIPT_DIR / script / "consonant.tsv"])


def _dedup_chars(chars: Iterable[str], sigma: pynini.Fst) -> pynini.Fst:
  """Creates an FST to de-dup the specified characters."""
  char_fsts = (ur.Rewrite(pynutil.delete(c), sigma, left=c)
               for c in chars)
  return ur.ComposeFsts(char_fsts).optimize()


def mark_chars(script: str) -> Set[str]:
  """Returns a set of non-spacing marks of a script and joiners."""

  chars = script_chars(script)
  marks = {uc.ZWS, uc.ZWNJ, uc.ZWJ}
  # 'Mn' is the category value for Nonspacing Marks:
  # See: http://www.unicode.org/reports/tr44/#General_Category_Values
  marks.update(c for c in chars if unicodedata.category(c) == "Mn")
  return marks


def dedup_marks_fst(script: str, sigma: pynini.Fst) -> pynini.Fst:
  """Creates an FST to de-dup non-spacing marks of a script and joiners."""

  return _dedup_chars(mark_chars(script), sigma)
