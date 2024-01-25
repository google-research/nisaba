# Copyright 2024 Nisaba Authors.
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

"""Library to load a .far file and transduce a string with an FST from that."""

import os
import warnings

import pynini
import functools
import nisaba.scripts.utils.file as uf


class FstInputError(ValueError):
  pass


class Far:
  """Far object created from a .far file.

  This .far file is usually generated in the runfiles directory and provided through the data
  field of the BUILD target as a resource.
  """

  class FstWrapper:
    """An FST object wrapper retrieved from a Far object."""

    def __init__(self, fst: pynini.Fst) -> None:
      self._fst = fst

    def ApplyOnText(self, text: str) -> str:
      """Transduce the given string using the FST.

      Args:
        text: Input string to be transduced.

      Returns:
        Transduced string output.

      Raises:
        ValueError on Pynini string compilation exceptions.

      This operation involves pre-composing the input string with the FST and
      then finding the shortest path to output a resultant string.
      """
      try:
        # Square brackets and backslash carry special meaning in Pynini.
        # So they need to be escaped for unmanaged strings.
        return pynini.shortestpath(pynini.escape(text) @ self._fst).string()
      except pynini.FstOpError as error:
        raise FstInputError(
            f'{error} on the string (between quotes): `{text}`') from error

    def AcceptText(self, text: str) -> bool:
      """Accept or reject the given string using the FST.

      Args:
        text: Input string to be accepted.

      Returns:
        Boolean indicating if the string is accepted or not.

      Raises:
        RuntimeWarning: If the underlying FST is not an acceptor.

      This operation involves pre-composing the input string with the FST,
      connects the result, and returns true iff the result is non-empty.
      """
      if not self._fst.properties(pynini.ACCEPTOR, True):
        warnings.warn('Underlying WFST is not an acceptor.', RuntimeWarning)
      lattice = text @ self._fst
      return lattice.start() != pynini.NO_STATE_ID

  def __init__(self, path_to_far: os.PathLike[str]) -> None:
    # This member variable can be used for debugging info.
    self.path_to_far = path_to_far

  # NOTE: Due to a pytype inconvenience with memoize.Memoize, this users of this
  # and the following function actually have no type information checked
  # ().
  @functools.lru_cache(maxsize=None)
  def _LoadFar(self) -> pynini.Far:
    return pynini.Far(uf.AsResourcePath(self.path_to_far))

  @functools.lru_cache(maxsize=None)
  def Fst(self, rule_name: str) -> 'FstWrapper':
    far = self._LoadFar()
    return self.FstWrapper(far[rule_name])
