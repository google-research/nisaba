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

import os
import pathlib
from typing import Iterable, Iterator, NamedTuple

import pandas as pd

import pynini
from pynini.lib import byte
import pathlib
import nisaba.utils.file as uf

Rule = NamedTuple("Rule", [("lhs", str), ("rhs", str)])


def Rewrite(rule: pynini.FstLike,
            left: pynini.FstLike = "",
            right: pynini.FstLike = "",
            *,
            sigma: pynini.Fst = byte.BYTE) -> pynini.Fst:
  return pynini.optimize(pynini.cdrewrite(rule, left, right, sigma.star))


def RulesFromStringFile(file: os.PathLike) -> Iterator[Rule]:
  """Yields string rules from a text resource with unweighted string maps."""
  return RulesFromStringPath(uf.AsResourcePath(file))


def RulesFromStringPath(file: os.PathLike) -> Iterator[Rule]:
  """Yields string rules from a text file with unweighted string maps."""
  with pathlib.Path(file).open("rt", encoding="utf8") as f:
    df = pd.read_csv(f, sep="\t", comment="#", escapechar="\\",
                     names=["lhs", "rhs"], na_filter=False)
    for row in df.itertuples(index=False, name="Rule"):
      if not row.lhs:
        raise ValueError("Rule expects an LHS: {}".format(row))
      yield row


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


def ComposeFsts(fsts: Iterable[pynini.Fst]) -> pynini.Fst:
  composed, *rest = fsts
  for fst in rest:
    composed @= fst
  return composed.optimize()


def RewriteAndComposeFsts(fsts: Iterable[pynini.Fst],
                          sigma: pynini.Fst) -> pynini.Fst:
  composed = sigma.star
  for fst in fsts:
    composed @= Rewrite(fst, sigma=sigma)
  return composed.optimize()


def OpenFstFromBrahmicFar(far_name: str, script: str, *,
                          token_type: str) -> pynini.Fst:
  tt_suffix = {"byte": "", "utf8": "_utf8"}[token_type]
  far_path = FAR_DIR / f"{far_name}{tt_suffix}.far"
  with pynini.Far(uf.AsResourcePath(far_path), "r") as far:
    return far[script.upper()]


def OpenFstFromBrahmicFarSafe(far_name: str, fst_name: str, token_type: str,
                              default: pynini.Fst) -> pynini.Fst:
  """Returns FST from a given FAR; returns default if FST is not found."""
  tt_suffix = {"byte": "", "utf8": "_utf8"}[token_type]
  far_path = FAR_DIR / f"{far_name}{tt_suffix}.far"
  if not uf.IsFileExist(far_path):
    return default
  with pynini.Far(uf.AsResourcePath(far_path), "r") as far:
    try:
      return far[fst_name.upper()]
    except KeyError:
      return default


def OpenSigma(script: str, *, token_type: str) -> pynini.Fst:
  # Returns the byte FSA if token_type is 'byte', otherwise opens the sigma FAR.
  if token_type == "byte":
    return byte.BYTE
  elif token_type == "utf8":
    return OpenFstFromBrahmicFar("sigma", script, token_type=token_type)
  else:
    raise ValueError(f"Received invalid token_type: {token_type}")


ZWNJ = "\u200C"  # Zero Width Non-Joiner
ZWJ = "\u200D"  # Zero Width Joiner
ZWS = "\u200B"  # Zero Width Space

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
    "as": "Beng",
    "bn": "Beng",
}

FIXED_RULE_SCRIPTS = ["Mlym"]

FAR_DIR = pathlib.Path("com_google_nisaba/nisaba/brahmic")
DATA_DIR = FAR_DIR / "data"
SCRIPT_DIR = DATA_DIR / "script"
LANG_DIR = DATA_DIR / "lang"
