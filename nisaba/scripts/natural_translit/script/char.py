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

"""Char building functions."""

import collections
import pynini as pyn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

# See README for Char tuple details.
Char = collections.namedtuple(
    'Char', ['alias', 'typ', 'gr', 'tr', 'glyph', 'ph', 'cmp'])


def make_char(
    typ: str,
    glyph: str,
    ph: pyn.Fst = al.EPSILON,
    alias: str = al.EMPTY_STR,
    cmp: pyn.Fst = None) -> Char:
  """Makes a Char with the default alias typ in uppercase.

  Args:
    typ: The typ of the Char.
    glyph: The glyph of the character in the source script.
    ph: The default phoneme assignment of the character.
    alias: The alias of the character that will be used in grammars.
    cmp: The components of a composite character.

  Returns:
    Char

  Following call:
  ```
  make_char('aa', 'ā', ph.A + ph.DURH)
  ```
  will return:
  ```
  Char(
      alias='AA',
      typ='aa',
      gr=<aa>,
      tr=`aa`,
      glyph='ā',
      ph=ph.A + ph.DURH,
      cmp=None)
  ```
  """
  if alias == al.EMPTY_STR:
    char_alias = typ.upper()
  else:
    char_alias = alias
  return Char(
      char_alias,
      typ,
      al.enclose_grapheme(typ),
      al.enclose_translit(typ),
      glyph,
      ph,
      cmp)


def uppercase_list(char_list: [Char]) -> [Char]:
  """Returns a list of uppercase Chars from a Char list."""
  upper_list = []
  for char in char_list:
    upper = make_char(
        char.typ.upper() + '_uc',
        char.glyph.upper(),
        char.ph)
    upper_list.append(upper)
  return upper_list


# TODO: Convert substrings to composite Chars.
def make_substring(substring: str) -> Char:
  """Makes a substring Char with 's_' prefix."""
  typ = 's_' + substring
  return make_char(typ, substring)


def double_substring(char: Char) -> Char:
  """Makes a substring Char by repeating the glyph of the arg Char."""
  new_typ = 's_' + char.typ + char.typ
  new_glyph = char.glyph + char.glyph
  return make_char(new_typ, new_glyph)


def ls_double_substring(chars: [Char]) -> ([Char], dict[str, pyn.Fst]):
  """Makes a list of double substring Chars from a list of Chars.

  Also makes a dictionary of corresponding tr fields.

  Args:
    chars: List of Chars

  Returns:
    A list of Chars, a dictionary of {tr: double_substring_tr}

  Given
  ```
  Char(alias='A', typ='a', gr=<a>, tr=`a`, glyph='a',...)
  ```
  Following call:
  ```
  ls_double_substring([ltn.A])
  ```
  will return:
  ```
  Char(alias='S_AA', typ='s_aa', gr=<s_aa>, tr=`s_aa`, glyph='aa',...)
  ```
  and
  ```
  {`a`: `s_aa`}
  ```
  """
  doubles = []
  double_dict = {}
  for char in chars:
    double = double_substring(char)
    doubles.append(double)
    double_dict.update({char.tr.string(): double.tr})
  return doubles, double_dict


def make_composite_char(
    chars: [Char],
    typ: str,
    ph: pyn.Fst = al.EPSILON,
    alias: str = al.EMPTY_STR) -> Char:
  """Makes a new Char from a list of Chars and keeps their grs in the cmp.

  Args:
    chars: The components of the composite character.
    typ: typ of the new character.
    ph: phoneme assignment for the new character.
    alias: alias of the new character.

  Returns:
    Char

  Following call:
  ```
  make_composite_char([iso.L, iso.VCL], 'lv', ph.L + ph.SYL)
  ```
  will return:
  ```
  Char('LV', 'lv', <lv>, `lv`, 'l̥', ph.L + ph.SYL, <l><vcl>)
  ```
  """
  glyph = al.EMPTY_STR
  gr = al.EPSILON
  for char in chars:
    glyph = glyph + char.glyph
    gr = gr + char.gr
  return make_char(typ, glyph, ph, alias, gr)


def compose_from_gr(char_list: [Char]) -> pyn.Fst:
  """Composes a list of Chars from the graphemes of their components.

  Args:
    char_list: A list of composite characters to be read.

  Returns:
    Rewrite fst.

  Following call:
  ```
  compose_from_gr([iso.LV, iso.RV])
  ```
  will return:
  ```
  pyn.cdrewrite(
      pyn.union(
          pyn.cross('<l><vcl>', '<lv>'),
          pyn.cross('<r><vcl>', '<rv>')
      )
  )
  ```
  """
  cross_list = [pyn.cross(char.cmp, char.gr) for char in char_list]
  return rw.rewrite_op(ls.union_opt(*cross_list))

# Functions for listing the .gr or .tr fields of a list of Chars.


def gr_list(char_list: [Char]) -> [pyn.Fst]:
  return [char.gr for char in char_list]


def tr_list(char_list: [Char]) -> [pyn.Fst]:
  return [char.tr for char in char_list]

# Functions for storing lists of fields for functions like
# `for coda in CODA_LIST:`


def store_gr_list(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, gr_list(char_list))


def store_tr_list(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, tr_list(char_list))

# Functions for storing union of fields for rules like
# `schwa_before_coda(vocal_schwa(), following=gr.CODA)`


def store_gr_union(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, ls.union_opt(*gr_list(char_list)))


def store_gr_star(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, ls.union_star(*gr_list(char_list)))


def store_tr_union(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, ls.union_opt(*tr_list(char_list)))


def store_tr_star(alias: str, char_list: [Char]) -> i.Store:
  return i.store_as(alias, ls.union_star(*tr_list(char_list)))

# Functions for building grapheme and translit inventories from a list of
# Chars and Stores.


def char_inventory(
    char_list: [Char],
    store_list: [i.Store] = None) -> collections.namedtuple:
  return i.make_inventory(char_list, char_list, store_list)


def gr_inventory(
    char_list: [Char],
    store_list: [i.Store] = None) -> collections.namedtuple:
  fst_list = gr_list(char_list)
  return i.make_inventory(fst_list, char_list, store_list)


def tr_inventory(
    char_list: [Char],
    store_list: [i.Store] = None) -> collections.namedtuple:
  fst_list = tr_list(char_list)
  return i.make_inventory(fst_list, char_list, store_list)

# Functions for reading and printing glyphs


def read_glyph(char_list: [Char]) -> pyn.Fst:
  glyph_to_gr = [pyn.cross(char.glyph, char.gr) for char in char_list]
  return ls.union_star(*glyph_to_gr)


def print_glyph(char_list: [Char]) -> pyn.Fst:
  tr_to_glyph = [pyn.cross(char.tr, char.glyph) for char in char_list]
  return ls.union_star(*tr_to_glyph)


def print_only_glyph(char_list: [Char]) -> pyn.Fst:
  return (rw.EXTRACT_RIGHT_SIDE @ print_glyph(char_list)).optimize()
