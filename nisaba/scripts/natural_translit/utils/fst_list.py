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

"""Class for holding and handling lists of fsts."""

from typing import Iterable
import pynini as pyn
from nisaba.scripts.natural_translit.utils import type_op as ty
from nisaba.scripts.utils import rewrite


class FstList(ty.IterableThing):
  """An iterable Thing that holds a flat list of fsts."""

  def __init__(self, *fsts, alias: str = ''):
    super().__init__(alias=alias)
    self._item_type = pyn.Fst
    self.add(*fsts)

  def add(self, *args) -> 'FstList':
    """Adds fsts to self.

    Args:
      *args: If the arg is an fst, adds it to the list. If the arg is a string,
      adds the acceptor fst.
      If the args are iterable, flattens tree structures into a list and adds
      the fsts and the acceptors of strings.
      Ignores args and elements of args of other types.

    Returns:
      Self

    """
    for arg in args:
      if isinstance(arg, str):
        self._items.append(pyn.accep(arg))
      elif isinstance(arg, pyn.Fst):
        self._items.append(arg)
      elif isinstance(arg, Iterable):
        self.add(*arg)
    return self

  def concat(self) -> pyn.Fst:
    """Concatenates all fsts in the list."""
    final_fst = pyn.accep('')
    for fst in self:
      final_fst = final_fst + fst
    return final_fst

  def compose(self) -> pyn.Fst:
    """Composes all fsts in the list."""
    return rewrite.ComposeFsts(self)
