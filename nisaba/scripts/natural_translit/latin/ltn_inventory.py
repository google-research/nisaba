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
"""Latin inventory.

Currently only ASCII characters are used in grammars, therefore the typ and
glyph of the Chars are identical.

"""

import pynini as p
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import list_op as ls

# Latin script characters


def make_ascii_char(glyph: str) -> c.Char:
  return c.make_char(glyph, glyph)


ASCII_CHAR = ls.apply_foreach(make_ascii_char, [
    ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'],
    ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'],
    ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z'],
])

ASCII_UC_CASE = c.uppercase_list(ASCII_CHAR)


SUBSTRING = ls.apply_foreach(c.make_substring, [
    ['aa'], ['ae'], ['ch'], ['ee'], ['ii'], ['kh'], ['ng'],
    ['ny'], ['oo'], ['rd'], ['sh'], ['th'], ['uu'], ['zh'],
])

DEL = [c.make_char('', '', alias='DEL')]

EN_LETTERS = c.store_tr_star('EN_LETTERS', ASCII_UC_CASE)

CHARS = ASCII_CHAR + ASCII_UC_CASE + SUBSTRING + DEL
TRANSLIT_INVENTORY = c.tr_inventory(CHARS, [EN_LETTERS])


def print_only_ltn() -> p.Fst:
  return c.print_only_glyph(CHARS)


