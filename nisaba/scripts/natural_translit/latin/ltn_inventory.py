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
"""Latin inventory.

Currently only ASCII characters are used in grammars, therefore the typ and
glyph of the Chars are identical.

"""

import pynini as pyn
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import list_op as ls

# Latin script characters


def make_ascii_char(glyph: str) -> c.Char:
  return c.make_char(glyph, glyph)


ASCII_VOWEL = ls.apply_foreach(make_ascii_char, [
    ['a'], ['e'], ['i'], ['o'], ['u']
])

ASCII_CONS = ls.apply_foreach(make_ascii_char, [
    ['b'], ['c'], ['d'], ['f'], ['g'], ['h'], ['j'],
    ['k'], ['l'], ['m'], ['n'], ['p'], ['q'], ['r'],
    ['s'], ['t'], ['v'], ['w'], ['x'], ['y'], ['z'],
])

ASCII_LC = ASCII_VOWEL + ASCII_CONS
ASCII_UC = c.uppercase_list(ASCII_LC)

DOUBLE_SUBSTRING, DOUBLE_DICT = c.ls_double_substring(ASCII_LC)


def double_substring_tr(tr: pyn.Fst) -> pyn.Fst:
  return DOUBLE_DICT.get(tr.string(), tr)

OTHER_SUBSTRING = ls.apply_foreach(c.make_substring, [
    ['ae'], ['ai'], ['au'], ['ch'], ['dh'], ['kh'],
    ['ng'], ['ny'], ['rd'], ['sh'], ['th'], ['zh'],
])

SUBSTRING = DOUBLE_SUBSTRING + OTHER_SUBSTRING

DEL = [c.make_char('DEL', '')]

EN_LETTERS = c.store_tr_star('EN_LETTERS', ASCII_UC)

VOWEL_GR = c.store_gr_union('VOWEL', ASCII_VOWEL)
CONS_GR = c.store_gr_union('CONS', ASCII_CONS)

CHARS = ASCII_LC + ASCII_UC + SUBSTRING + DEL
GRAPHEME_INVENTORY = c.gr_inventory(CHARS, [VOWEL_GR, CONS_GR])
TRANSLIT_INVENTORY = c.tr_inventory(CHARS, [EN_LETTERS])


def print_only_ltn() -> pyn.Fst:
  return c.print_only_glyph(CHARS)
