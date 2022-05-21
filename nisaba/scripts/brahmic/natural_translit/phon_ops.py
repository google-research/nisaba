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

"""Multilingual phonological operations."""

import pynini as p
from pynini.export import multi_grm
from pynini.lib import byte

LETTERS = p.union('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                  'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                  's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_')
SEPARATOR = p.accep(',')
SYMBOL_SEQUENCE = p.union(LETTERS.star, SEPARATOR.star).star
LEFT_BOUNDARY = p.accep('(')
RIGHT_BOUNDARY = p.accep(')')
ASSIGNMENT_SIGN = p.accep('=')
LEFT_SIDE = LEFT_BOUNDARY + SYMBOL_SEQUENCE + ASSIGNMENT_SIGN

# TODO: Grapheme inventory
sigma_star = byte.BYTE.star
r_bound = RIGHT_BOUNDARY
l_side = LEFT_SIDE

# TODO: Phonological model
vowel = p.union('a', 'i')
nasal = p.accep('ni')
approximant = p.accep('y')
sonorant = p.union(vowel, nasal, approximant)


def _intersonorant_voicing() -> p.Fst:
  """Voicing between vowels, approximants, and nasals."""
  voicing_aux = p.cross('(t=ti)', '(t=di)')

  # TODO: add test to cover voicing with substring assignments
  voicing = p.cdrewrite(
      voicing_aux,
      (sonorant + r_bound),
      (l_side + sonorant),
      sigma_star).optimize()

  return voicing

INTERSONORANT_VOICING = _intersonorant_voicing()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for multilingual phonological operations."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['VOICING'] = INTERSONORANT_VOICING


if __name__ == '__main__':
  multi_grm.run(generator_main)
