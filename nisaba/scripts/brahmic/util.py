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


"""Utility functions and definitions used in this package."""

import pathlib

import pynini
from pynini.lib import byte
import nisaba.scripts.utils.file as uf


def BuildSigmaFstFromSymbolTable(syms: pynini.SymbolTableView) -> pynini.Fst:
  f = pynini.Fst()
  start_state = f.add_state()
  f.set_start(start_state)
  final_state = f.add_state()
  f.set_final(final_state)
  for lbl, _ in syms:
    f.add_arc(start_state,
              pynini.Arc(lbl, lbl, pynini.Weight.one("tropical"), final_state))
  return f


def OpenFstFromBrahmicFar(far_name: str, fst_name: str, *,
                          token_type: str) -> pynini.Fst:
  return uf.OpenFstFromFar(FAR_DIR, far_name, token_type, fst_name)


def OpenFstFromBrahmicFarSafe(far_name: str, fst_name: str, token_type: str,
                              default: pynini.Fst) -> pynini.Fst:
  """Returns FST from a given FAR; returns default if FST is not found."""
  return uf.OpenFstFromFarSafe(FAR_DIR, far_name, token_type, fst_name, default)


def OpenSigma(script: str, *, token_type: str) -> pynini.Fst:
  # Returns the byte FSA if token_type is 'byte', otherwise opens the sigma FAR.
  if token_type == "byte":
    return byte.BYTE
  elif token_type == "utf8":
    return OpenFstFromBrahmicFar("sigma", script, token_type=token_type)
  else:
    raise ValueError(f"Received invalid token_type: {token_type}")


# Scripts supported by the brahmic library.
# Script and language codes are used as per IANA registry:
# https://www.iana.org/assignments/language-subtag-registry
SCRIPTS = [
    "Beng",
    "Deva",
    "Gujr",
    "Guru",
    "Knda",
    "Mlym",
    "Mtei",
    "Orya",
    "Sinh",
    "Taml",
    "Telu",
    "Tglg",
]

LANG_SCRIPT_MAP = {
    "Beng": ["as", "bn"]
}

FIXED_RULE_SCRIPTS = ["Mlym"]

FAR_DIR = pathlib.Path("com_google_nisaba/nisaba/scripts/brahmic")
DATA_DIR = FAR_DIR / "data"
SCRIPT_DIR = DATA_DIR / "script"
