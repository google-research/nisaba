# Copyright 2025 Nisaba Authors.
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

# Latin script characters


def make_ascii_char(glyph: str) -> c.Char:
  return c.Char(glyph, glyph)


ASCII_VOWEL = [make_ascii_char(vowel) for vowel in [
    'a', 'e', 'i', 'o', 'u'
]]

ASCII_CONS = [make_ascii_char(cons) for cons in [
    'b', 'c', 'd', 'f', 'g', 'h', 'j',
    'k', 'l', 'm', 'n', 'p', 'q', 'r',
    's', 't', 'v', 'w', 'x', 'y', 'z',
]]

ASCII_LC = ASCII_VOWEL + ASCII_CONS
ASCII_UC = c.uppercase_list(ASCII_LC)

DOUBLE_SUBSTRING, DOUBLE_DICT = c.ls_double_substring(ASCII_LC)


def double_substring_tr(tr: pyn.Fst) -> pyn.Fst:
  return DOUBLE_DICT.get(tr.string(), tr)

OTHER_SUBSTRING = [c.make_substring(sub) for sub in [
    'ae', 'ai', 'au', 'ch', 'dh', 'kh',
    'ng', 'ny', 'rd', 'sh', 'th', 'zh',
]]

SUBSTRING = DOUBLE_SUBSTRING + OTHER_SUBSTRING

DEL = [c.Char('DEL', '')]

EN_LETTERS = c.thing_tr_star('EN_LETTERS', ASCII_UC)

VOWEL_GR = c.thing_gr_union('VOWEL', ASCII_VOWEL)
CONS_GR = c.thing_gr_union('CONS', ASCII_CONS)

CHARS = ASCII_LC + ASCII_UC + SUBSTRING + DEL
GRAPHEME_INVENTORY = c.gr_inventory(CHARS, [VOWEL_GR, CONS_GR])
TRANSLIT_INVENTORY = c.tr_inventory(CHARS, [EN_LETTERS])

DEL_REPEATED_LOWER = c.remove_repeated_glyph(ASCII_LC)
DEL_REPEATED_SUBSTRING = c.remove_repeated_glyph(OTHER_SUBSTRING)


def print_only_ltn() -> pyn.Fst:
  return c.print_only_glyph(CHARS)
