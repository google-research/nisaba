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

# Lint as: python3
"""Common constants and symbol and alignment forming functions."""

from typing import Callable, List, Tuple
import pynini as p

# Shorthands for optimized union and star.


def star_opt(fst: p.Fst) -> p.Fst:
  return fst.star.optimize()


def union_opt(*fsts) -> p.Fst:
  return p.union(*fsts).optimize()


def union_star(*fsts) -> p.Fst:
  return star_opt(p.union(*fsts))

# List, union_of and star over functions and argument lists.


def apply_foreach(
    func, arg_list: Tuple[Callable[[], p.Fst], List[List[p.Fst]]]
    ) -> List[p.Fst]:
  """Lists the returns of a function from a list of arguments.

  Args:
    func: A function that will apply to the list of arguments.
    arg_list: A list containing the arguments of the function in list form.

  Returns:
    List of fsts.

  Following call:
  ```
  apply_foreach(myfunction, [
      [arg1, arg2, arg3],
      [arg4, arg5],
      [arg6, arg7, arg8],
      ...
      ])
  ```
  will return:
  ```
  [myfunction(arg1, arg2, arg3),
   myfunction(arg4, arg5),
   myfunction(arg6, arg7, arg8),
   ...]
  ```
  """
  return [func(*args) for args in arg_list]


def apply_union(
    func, arg_list: Tuple[Callable[[], p.Fst], List[List[p.Fst]]]
    ) -> p.Fst:
  return union_opt(*apply_foreach(func, arg_list))


def apply_union_star(
    func, arg_list: Tuple[Callable[[], p.Fst], List[List[p.Fst]]]
    ) -> p.Fst:
  return star_opt(apply_union(func, arg_list))

# Special cases where the function is a simple p.cross(old, new)


def cross_union(
    arg_list: List[Tuple[p.Fst, p.Fst]]
    ) -> p.Fst:
  """Shorthand for p.union(p.cross(x, y), p.cross(y, z),...)"""
  return union_opt(*apply_foreach(p.cross, arg_list))


def cross_union_star(
    arg_list: List[Tuple[p.Fst, p.Fst]]
    ) -> p.Fst:
  return star_opt(cross_union(arg_list))
