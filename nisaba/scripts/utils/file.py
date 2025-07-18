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

"""File access functions used in this package."""

import errno
import os
import pathlib

import pynini
from rules_python.python.runfiles import runfiles

EMPTY: pynini.Fst = pynini.intersect(
    pynini.accep("a"), pynini.accep("b")).optimize()
EPSILON: pynini.Fst = pynini.accep("").optimize()


def AsResourcePath(filename: os.PathLike[str]) -> os.PathLike[str]:
  filename = os.fspath(filename)
  return pathlib.Path(runfiles.Create().Rlocation(filename))


def IsFileExist(filename: os.PathLike[str]) -> bool:
  """Checks if a resource file exists."""
  try:
    if os.path.isfile(AsResourcePath(filename)):
      return True
  except IOError as ex:
    if ex.errno != errno.ENOENT:
      raise ex  # Reraise unknown error.
  return False


def OnEmpty(fst, return_if_empty=EMPTY):
  """If FST is empty returns `return_if_empty`; no-op otherwise."""
  return return_if_empty if fst.start() == pynini.NO_STATE_ID else fst


def StringFile(filename: os.PathLike[str],
               return_if_empty: pynini.Fst = EMPTY) -> pynini.Fst:
  """Reads FST from `filename`. If FST is empty returns `return_if_empty`."""
  return OnEmpty(pynini.string_file(AsResourcePath(filename)), return_if_empty)


def QuesSafe(fst: pynini.Fst) -> pynini.Fst:
  """Version of `.ques`, always returning EPSILON when closure count is 0."""
  return OnEmpty(fst, EPSILON).ques


def StarSafe(fst: pynini.Fst) -> pynini.Fst:
  """Version of `.star`, always returning EPSILON when closure count is 0."""
  return OnEmpty(fst, EPSILON).star


def OpenFar(
    far_dir: pathlib.Path, far_name: str, token_type: str
) -> pynini.Far:
  tt_suffix = {"byte": "", "utf8": "_utf8"}[token_type]
  far_path = far_dir / f"{far_name}{tt_suffix}.far"
  return pynini.Far(AsResourcePath(far_path), "r")


def OpenFstFromFar(
    far_dir: pathlib.Path, far_name: str, token_type: str, fst_name: str
) -> pynini.Fst:
  with OpenFar(far_dir, far_name, token_type) as far:
    return far[fst_name.upper()]


def OpenFstFromFarSafe(
    far_dir: pathlib.Path, far_name: str, token_type: str, fst_name: str,
    default: pynini.Fst) -> pynini.Fst:
  """Returns FST from a given FAR; returns default if FST is not found."""
  tt_suffix = {"byte": "", "utf8": "_utf8"}[token_type]
  far_path = far_dir / f"{far_name}{tt_suffix}.far"
  if not IsFileExist(far_path):
    return default
  with pynini.Far(AsResourcePath(far_path), "r") as far:
    try:
      return far[fst_name.upper()]
    except KeyError:
      return default
