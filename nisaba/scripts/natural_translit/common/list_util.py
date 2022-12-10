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

"""Utility functions that operate on lists of fsts."""

from typing import Callable, List, Tuple, TypeVar
import pynini as p

# Generic type
_T = TypeVar('_T')


def unite(items: [p.FstLike]) -> p.Fst:
  if len(items) == 1:
    return items[0]
  else:
    return p.union(*items).optimize()


def ques(items: [p.FstLike]) -> p.Fst:
  return [unite(items).ques]


def returns(
    function: Callable[[], _T],
    args_list: List[_T]) -> List[_T]:
  """The list of returns of a function.

  Args:
    function: Callable that will apply to the list of arguments.
    args_list: List of arguments for the function.

  Returns:
    A list of results.

  Following call

  ```
  return_list(myfunction, [
          [arga, argb, argc],
          [argd, arge],
          [argf, argg, argh],
          ...
          ])
  ```

  will return

  ```
  [myfunction(arga, argb, argc),
   myfunction(argd, arge),
   myfunction(argf, argg, argh),
   ...]
  ```
  """
  return [function(*args) for args in args_list]


def unite_returns(
    function: Callable[[], _T],
    args_list: List[_T]) -> List[_T]:
  return unite(returns(function, args_list))


def pcross(
    old: [p.Fst],
    new: p.Fst) -> p.Fst:
  """Shorthand for p.cross(p.union(fsts), fst).

  Args:
    old: list of items that will be the input for p.cross.
    new: the output of p.cross.

  Returns:
      Following call

  ```
  cross_from_list([a, b, c], d)
  ```
  will return:

  ```
  p.cross(p.union(a, b, c), d)
  ```
  """
  return p.cross(unite(old), new)


def unite_pcross(crlist: List[Tuple[List[p.Fst], p.FstLike]]) -> p.Fst:
  """Shorthand for p.union(p.cross(x, y), p.cross(y, z),...)"""
  return unite([pcross(old, new) for [old, new] in crlist])


def compose(
    op: Callable[[], p.Fst],
    args_list: List[List[p.Fst]]) -> p.Fst:
  composed_fst = op(*args_list[0])
  for args in args_list[1:]:
    composed_fst = p.compose(composed_fst, op(*args)).optimize()
  return composed_fst


