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

from __future__ import annotations

from typing import Any, Callable, Iterable

import pynini as pyn
from nisaba.scripts.natural_translit.utils import type_op as ty
from nisaba.scripts.utils import rewrite


class FstList(ty.IterableThing):
  """An iterable Thing that holds a flat list of fsts."""

  def __init__(self, *fsts, alias: str = ''):
    super().__init__(alias=alias)
    self._item_type = pyn.Fst
    self.add(*fsts)

  @classmethod
  def accep(cls, *strings: str) -> FstList:
    """Creates an FstList from acceptors of strings."""
    return FstList([pyn.accep(s) for s in strings])

  @classmethod
  def make(
      cls, maker: Callable[..., pyn.Fst], *args: tuple[Any, ...]
  ) -> FstList:
    """Creates an FstList from a maker function and argument tuples.

    Args:
      maker: A function that returns an fst.
      *args: Argument tuples for the maker function.

    Returns:
      FstList.

    Following call:
    ```
    FstList.make(
        maker_function,
        [
            (arg1, arg2, arg3),
            (arg3, arg4),
            (arg5, arg6, arg7),
        ]
    )
    ```
    will return:
    ```
    FstList(
        maker_function(arg1, arg2, arg3),
        maker_function(arg3, arg4),
        maker_function(arg5, arg6, arg7),
    )
    ```
    """
    return FstList([maker(*arg) for arg in args])

  @classmethod
  def cross(cls, *cross_tuples: tuple[pyn.FstLike, pyn.FstLike]):
    """Shorthand for when the maker function is pyn.cross."""
    return cls.make(pyn.cross, *cross_tuples)

  def add(self, *args) -> FstList:
    """Adds fsts to self.

    Args:
      *args: If the arg is an fst, adds it to the list. If the arg is a string,
        adds the acceptor fst. If the args are iterable, flattens tree
        structures into a list and adds the fsts and the acceptors of strings.
        Ignores args and elements of args of other types.

    Returns:
      Self
    """
    for arg in args:
      if isinstance(arg, ty.FstLike):
        self._items.append(arg if isinstance(arg, pyn.Fst) else pyn.accep(arg))
      elif isinstance(arg, Iterable):
        self.add(*arg)
    return self

  def union(self) -> pyn.Fst:
    """Union all fsts in the list."""
    if not self:
      return pyn.Fst()
    if len(self) == 1:
      return self.item(0)
    else:
      return pyn.union(*self)

  def union_opt(self) -> pyn.Fst:
    """Optimized union all fsts in the list."""
    return self.union().optimize()

  def union_star(self) -> pyn.Fst:
    """Starred and optimized union of all fsts in the list."""
    return self.union().star.optimize()

  def concat(self) -> pyn.Fst:
    """Concatenates all fsts in the list."""
    final_fst = pyn.accep('')
    for fst in self:
      final_fst = final_fst + fst
    return final_fst

  def compose(self) -> pyn.Fst:
    """Composes all fsts in the list."""
    return rewrite.ComposeFsts(self)
