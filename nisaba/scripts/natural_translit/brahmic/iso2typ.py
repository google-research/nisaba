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

"""ISO to typeable string conversion."""

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

gr = iso.GRAPHEME_INVENTORY


def _iso_to_decomposed_typ() -> p.Fst:
  """ISO to typable fst."""
  return c.read_glyph(iso.SINGLE_POINT)

_COMPOSE_THREE_POINT_SIGN = c.compose_from_gr(iso.RETROFLEX_VOCALIC)

_COMPOSE_TWO_POINT_SIGN = c.compose_from_gr(iso.TWO_POINT_SIGN)

# Word initial vowels are independent vowels but they are not marked with an
# independent sign in ISO.
_WORD_INITIAL_VOWEL = rw.rewrite_word_initial(
    al.EPSILON,
    gr.IND,
    gr.VOWEL_S - gr.AAN)

_COMPOSE_INDEPENDENT_VOWEL = c.compose_from_gr(iso.INDEPENDENT_VOWEL)

_COMPOSE_CONSONANT = c.compose_from_gr(iso.COMPOSITE_CONSONANT)

_COMPOSE_MISC = c.compose_from_gr(iso.OM + iso.CND)

_COMPOSE_TYP = (
    _COMPOSE_THREE_POINT_SIGN @
    _COMPOSE_TWO_POINT_SIGN @
    _WORD_INITIAL_VOWEL @
    _COMPOSE_INDEPENDENT_VOWEL @
    _COMPOSE_CONSONANT @
    _COMPOSE_MISC
).optimize()


def iso_to_typ() -> p.Fst:
  return (_iso_to_decomposed_typ() @ _COMPOSE_TYP).optimize()
