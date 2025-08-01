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

"""Python APIs for Brahmic grammars."""

import functools
import pathlib
import re
import string

import pynini
from nisaba.scripts.brahmic import util as u
from nisaba.scripts.utils import far

SCRIPTS = u.SCRIPTS

# Language-specific visual normalization. The language-agnostic visual
# normalization grammars are available through `SCRIPTS` above.
VISUAL_NORM_LANGS = u.VISUAL_NORM_LANGS


class _FarStore(object):
  """Manages loading of FAR archives, implementing lazy loading.

  This class is intended to be used as a singleton instance (_FARS).
  FAR files are loaded only when first accessed via the corresponding property
  (e.g., _FARS.iso) or method (e.g., _FARS.Natural('lang')). Subsequent accesses
  use the cached instance, preventing redundant FAR file loading.
  """

  def __init__(self) -> None:
    self._natural = {}

  @functools.cached_property
  def iso(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'iso.far')

  @functools.cached_property
  def nfc(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'nfc.far')

  @functools.cached_property
  def visual_norm(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'visual_norm.far')

  @functools.cached_property
  def wellformed(self) -> far.Far:
    return far.Far(u.FAR_DIR / 'wellformed.far')


_FARS = _FarStore()


def ToIso() -> far.Far.FstWrapper:
  return _FARS.iso.Fst('FROM_BRAHMIC')


def IsoTo(script: str) -> far.Far.FstWrapper:
  return _FARS.iso.Fst('TO_' + script.upper())


def Nfc() -> far.Far.FstWrapper:
  return _FARS.nfc.Fst('BRAHMIC')


def VisualNorm(script: str) -> far.Far.FstWrapper:
  return _FARS.visual_norm.Fst(script.upper())


def WellFormed(script: str) -> far.Far.FstWrapper:
  return _FARS.wellformed.Fst(script.upper())


class ScriptError(ValueError):
  pass


class IllFormedError(ValueError):
  pass


class NormalizingAcceptor(object):
  """Visual Norm a string while rejecting it, if it is not well-formed."""

  def __init__(self, script: str, ignore: str = string.whitespace) -> None:
    try:
      self._visual_norm = VisualNorm(script)
      self._wellformed = WellFormed(script)
    except KeyError as e:
      raise ScriptError('Unsupported language script: {}'.format(e)) from e
    else:
      self.accept_pat = re.compile(r'[^{}]+'.format(re.escape(ignore)))

  def ApplyOnWord(self, word: str) -> str:
    """Normalize or reject a entire word."""
    norm_word = self._visual_norm.ApplyOnText(word)
    if not self._wellformed.AcceptText(norm_word):
      raise IllFormedError
    return norm_word

  def ApplyOnText(self, line: str) -> str:
    """Normalize or reject a line of formed of words."""
    return self.accept_pat.sub(lambda m: self.ApplyOnWord(m.group(0)), line)
