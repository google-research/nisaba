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

import pynini as pyn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.natural_translit.utils import type_op as ty


class Char(ty.Thing):
  """See README for Char attributes."""

  def __init__(
      self,
      typ: str,
      glyph: str,
      ph: pyn.Fst = al.EPSILON,
      alias: str = '',
      cmp: ty.FstIterable = ty.UNSPECIFIED
  ):
    """Makes a Char with the default alias as typ in uppercase.

    Args:
      typ: The typ of the Char.
      glyph: The glyph of the character in the source script.
      ph: The default phoneme assignment of the character.
      alias: The alias of the character that will be used in grammars.
      cmp: The concatenation of the gr fields of the components of a composite
        character.

    Returns:
      Char

    Following call:
    ```
    Char('aa', 'ā', ph.A + ph.DURH)
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
        cmp=None
    )
    ```
    """
    super().__init__(alias if alias else typ.upper(), glyph)
    self.typ = typ
    self.gr = al.enclose_grapheme(typ)
    self.tr = al.enclose_translit(typ)
    self.glyph = glyph
    self.ph = ph
    self.cmp = cmp


def uppercase_list(char_list: list[Char]) -> list[Char]:
  """Returns a list of uppercase Chars from a Char list."""
  return [
      Char(char.typ.upper() + '_uc', char.glyph.upper(), char.ph)
      for char in char_list
  ]


# TODO: Convert substrings to composite Chars.
def make_substring(substring: str) -> Char:
  """Makes a substring Char with 's_' prefix."""
  return Char('s_' + substring, substring)


def double_substring(char: Char) -> Char:
  """Makes a substring Char by repeating the glyph of the arg Char."""
  return Char('s_' + char.typ + char.typ, char.glyph + char.glyph)


def ls_double_substring(
    chars: list[Char],
) -> tuple[list[Char], dict[str, pyn.Fst]]:
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
    double_dict |= {char.tr.string(): double.tr}
  return doubles, double_dict


def make_composite_char(
    chars: list[Char], typ: str, ph: pyn.Fst = al.EPSILON, alias: str = ''
) -> Char:
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
  return Char(
      typ,
      ''.join([c.glyph for c in chars]),
      ph,
      alias,
      fl.FstList(*[c.gr for c in chars]).concat(),
  )


def compose_from_gr(char_list: list[Char]) -> pyn.Fst:
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
  return rw.rewrite_ls([(char.cmp, char.gr) for char in char_list])

# Functions for listing the .gr or .tr fields of a list of Chars.


def gr_list(char_list: list[Char]) -> list[pyn.Fst]:
  return [char.gr for char in char_list]


def tr_list(char_list: list[Char]) -> list[pyn.Fst]:
  return [char.tr for char in char_list]

# Functions for storing lists of fields for functions like
# `for coda in CODA_LIST:`


def thing_gr_list(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=gr_list(char_list))


def thing_tr_list(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=tr_list(char_list))

# Functions for storing union of fields for rules like
# `schwa_before_coda(vocal_schwa(), following=gr.CODA)`


def thing_gr_union(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=fl.FstList(gr_list(char_list)).union_opt())


def thing_gr_star(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=fl.FstList(gr_list(char_list)).union_star())


def thing_tr_union(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=fl.FstList(tr_list(char_list)).union_opt())


def thing_tr_star(alias: str, char_list: list[Char]) -> ty.Thing:
  return ty.Thing(alias, value_from=fl.FstList(tr_list(char_list)).union_star())

# Functions for building grapheme and translit inventories from a list of
# Chars and Stores.


def char_inventory(
    char_list: list[Char], suppl_list: ty.ListOrNothing = ty.UNSPECIFIED
) -> i.Inventory:
  return i.Inventory.from_list(char_list, suppls=suppl_list)


def gr_inventory(
    char_list: list[Char], suppl_list: ty.ListOrNothing = ty.UNSPECIFIED
) -> i.Inventory:
  return i.Inventory.from_list(char_list, attr='gr', suppls=suppl_list)


def tr_inventory(
    char_list: list[Char], suppl_list: ty.ListOrNothing = ty.UNSPECIFIED
) -> i.Inventory:
  return i.Inventory.from_list(char_list, attr='tr', suppls=suppl_list)

# Functions for reading and printing glyphs


def read_glyph(char_list: list[Char]) -> pyn.Fst:
  return fl.FstList.cross(
      *[(char.glyph, char.gr) for char in char_list]
  ).union_star()


def print_glyph(char_list: list[Char]) -> pyn.Fst:
  return fl.FstList.cross(
      *[(char.tr, char.glyph) for char in char_list]
  ).union_star()


def print_only_glyph(char_list: list[Char]) -> pyn.Fst:
  return (rw.EXTRACT_RIGHT_SIDE @ print_glyph(char_list)).optimize()


def remove_repeated_glyph(char_list: list[Char]) -> pyn.Fst:
  return rw.rewrite_ls(
      [(char.glyph + char.glyph, char.glyph) for char in char_list]
  )
