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


"""File access functions used in this package."""

import errno
import os

import pynini
from rules_python.python.runfiles import runfiles


def AsResourcePath(filename: os.PathLike) -> os.PathLike:
  filename = os.fspath(filename)
  return runfiles.Create().Rlocation(filename)


def IsFileExist(filename: os.PathLike) -> bool:
  """Checks if a resource file exists."""
  try:
    filename = AsResourcePath(filename)
    if os.path.isfile(filename):
      return True
  except IOError as ex:
    if ex.errno != errno.ENOENT:
      raise ex  # Reraise unknown error.
  return False


def StringFile(filename: os.PathLike) -> pynini.Fst:
  return pynini.string_file(AsResourcePath(filename))


def StringFileSafe(filename: os.PathLike) -> pynini.Fst:
  return StringFile(filename) if IsFileExist(filename) else pynini.accep("")
