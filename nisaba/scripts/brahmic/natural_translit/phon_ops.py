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

sigma_star = byte.BYTE.star

# TODO: Grapheme inventory
letter = p.union('a', 'c', 'd', 'h', 'i', 'l', 'n', 's', 't', 'y')
left_bound = p.accep('(')
right_bound = p.accep(')')
assign = p.accep('=')
grapheme = left_bound + letter.star + assign

# TODO: Phonological model
vowel = p.union('a', 'i')
nasal = p.accep('ni')
approximant = p.accep('y')
sonorant = vowel | nasal | approximant


def intersonorant_voicing() -> p.Fst:
  """Voicing between vowels, approximants, and nasals."""
  voicing_aux = p.cross('(t=ti)', '(t=di)')

  # TODO: add test to cover voicing with substring assignments
  voicing = p.cdrewrite(
      voicing_aux,
      (sonorant + right_bound),
      (grapheme + sonorant),
      sigma_star).optimize()

  return voicing


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for multilingual phonological operations."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['VOICING'] = intersonorant_voicing()


if __name__ == '__main__':
  multi_grm.run(generator_main)
