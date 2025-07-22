# Copyright 2025 Nisaba Authors.
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

"""Python APIs for abjad / alphabet grammars."""

# TODO: This library currently only supports `byte` tokens. Consider
# supporting `utf8` tokens too.

import functools
import pathlib
import re
import string

import pynini
from nisaba.scripts.abjad_alphabet import util as u
from nisaba.scripts.utils import far
from nisaba.scripts.utils import rewrite


class _FarStore(object):
  """Manages loading of FAR archives, implementing lazy loading.

  This class is intended to be used as a singleton instance (_FARS).
  FAR files are loaded only when first accessed via the corresponding property
  (e.g., _FARS.nfc). Subsequent accesses use the cached instance, preventing
  redundant FAR file loading.
  """

  @functools.cached_property
  def reversible_roman(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'reversible_roman.far')

  @functools.cached_property
  def nfc(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'nfc.far')

  @functools.cached_property
  def reading_norm(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'reading_norm.far')

  @functools.cached_property
  def visual_norm(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'visual_norm.far')


_FARS = _FarStore()


def ToReversibleRoman() -> far.Far.FstWrapper:
  fst = u.open_fst_from_far('reversible_roman', 'FROM_ARAB', 'byte')
  # Allows out of script characters to pass through.
  return far.Far.FstWrapper(rewrite.Rewrite(fst))


def FromReversibleRoman() -> far.Far.FstWrapper:
  return _FARS.reversible_roman.Fst('TO_ARAB')


def Nfc() -> far.Far.FstWrapper:
  return _FARS.nfc.Fst('ARAB')


def VisualNorm(tag: str = 'ur') -> far.Far.FstWrapper:
  return _FARS.visual_norm.Fst(tag.upper())


def ReadingNorm(tag: str = 'ur') -> far.Far.FstWrapper:
  return _FARS.reading_norm.Fst(tag.upper())


class TagError(ValueError):
  pass


class Normalizer(object):
  """Visual Norm a given abjad / alphabet string."""

  def __init__(self, tag: str = 'ur', ignore: str = string.whitespace) -> None:
    try:
      self._nfc = Nfc()
      self._visual_norm = VisualNorm(tag)
    except KeyError as error:
      raise TagError(f'Unsupported language/script: {tag}') from error
    else:
      self.accept_pat = re.compile(r'[^{}]+'.format(re.escape(ignore)))

  def ApplyOnWord(self, word: str) -> str:
    """Normalize a entire word."""
    return self._visual_norm.ApplyOnText(self._nfc.ApplyOnText(word))

  def ApplyOnText(self, line: str) -> str:
    """Normalize a line formed of words."""
    return self.accept_pat.sub(lambda m: self.ApplyOnWord(m.group(0)), line)
