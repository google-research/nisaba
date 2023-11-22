# Copyright 2023 Nisaba Authors.
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
"""Shorthands for functions that loop over lists of arguments."""

from typing import Any, Callable, List
import pynini as pyn
# from nisaba.scripts.
# natural_translit.utils import type_op as ty

# Shorthands for optimized union and star.


def star_opt(fst: pyn.Fst) -> pyn.Fst:
  return fst.star.optimize()


# TODO: Rename this union() to be consistent with the following functions.
def union_opt(*fsts) -> pyn.Fst:
  return pyn.union(*fsts).optimize()


def union_star(*fsts) -> pyn.Fst:
  return star_opt(pyn.union(*fsts))

# List, union_of and star over functions and argument lists.


def apply_foreach(
    func: Callable[..., Any],
    arg_list: List[List[Any]]
) -> List[Any]:
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
    func: Callable[..., pyn.FstLike],
    arg_list: List[List[Any]]
) -> pyn.Fst:
  return union_opt(*apply_foreach(func, arg_list))


def apply_union_star(
    func: Callable[..., pyn.FstLike],
    arg_list: List[List[Any]]
) -> pyn.Fst:
  return union_star(*apply_foreach(func, arg_list))

# Special cases where the function is a simple ty.pyn.cross(old, new)


def cross_union(
    arg_list: List[List[pyn.FstLike]]
) -> pyn.Fst:
  """Shorthand for pyn.union(pyn.cross(x, y), pyn.cross(y, z),...)"""
  return union_opt(*apply_foreach(pyn.cross, arg_list))


def cross_union_star(
    arg_list: List[List[pyn.FstLike]]
) -> pyn.Fst:
  return union_star(*apply_foreach(pyn.cross, arg_list))


# def attr_list(
#     things: list[Any],
#     attr: str,
#     attr_type: ty.TypeOrNothing = ty.UNSPECIFIED
# ) -> list[Any]:
#   """Makes a list from an attribute of a list of objects.

#   Args:
#     things: A list of objects.
#     attr: The attribute from which the new list is to be compiled. If the
#       object doesn't have the requested attribute, skips that object.
#     attr_type: If specified, only the results that are instances of this type
#       will be added to the list.

#   Returns:
#     if attr_type is specified:
#       [t.attr for t in things if isinstance(t.attr, attr_type)]
#     else:
#       [t.attr for t in things]
#   """
#   l = [ty.get_attribute(t, attr, want=attr_type) for t in things]
#   return list(filter(ty.is_found, l))


# def fst_attr_list(things: list[Any], attr: str) -> list[pyn.Fst]:
#   return attr_list(things, attr, ty.FstLike)


# def fst_attr_list_union(things: list[Any], attr: str) -> pyn.Fst:
#   return union_opt(*fst_attr_list(things, attr))


# def fst_attr_list_union_star(things: list[Any], attr: str) -> pyn.Fst:
#   return union_star(*fst_attr_list(things, attr))
