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

"""Pan-South Asian natural romanization."""

import pynini as p
from pynini.export import multi_grm
from pynini.lib import byte

sigma_star = byte.BYTE.star
left_bound = p.accep('(')
right_bound = p.accep(')')
assign = p.accep('=')
modifier = p.accep('_')


def romanize_fine() -> p.Fst:
  """Fine-grained Pan South Asian romanization."""
  romanize_aux = (p.cross('a_l', 'aa') |
                  p.cross('i_l', 'ii') |
                  p.cross('dd', 'd') |
                  p.cross('di', 'd') |
                  p.cross('ti', 't') |
                  p.cross('ni', 'n'))

  romanize = p.cdrewrite(romanize_aux,
                         assign,
                         right_bound,
                         sigma_star).optimize()

  return romanize


def romanize_coarse() -> p.Fst:
  """Coarse-grained Pan South Asian romanization."""

  romanize_aux = (p.cross('a_l', 'a') |
                  p.cross('i_l', 'i') |
                  p.cross('dd', 'd') |
                  p.cross('di', 'd') |
                  p.cross('ti', 't') |
                  p.cross('ni', 'n'))

  romanize = p.cdrewrite(romanize_aux,
                         assign,
                         right_bound,
                         sigma_star).optimize()

  return romanize


def remove_leftside() -> p.Fst:
  """Removes the left side of the assigment."""

  vowel = p.union('a', 'i')

  consonant = p.union('c', 'd', 'h', 'l', 'n', 's', 't', 'y')

  letter = (vowel | consonant)

  remove_graphemes = p.cdrewrite(p.cross((letter | modifier).star, ''),
                                 left_bound,
                                 assign,
                                 sigma_star).optimize()

  return remove_graphemes


def remove_formatting() -> p.Fst:
  """Removes the assigment and boundary markers."""

  remove_assignment = p.cdrewrite(p.cross(assign, ''),
                                  '',
                                  '',
                                  sigma_star).optimize()

  remove_bounds = p.cdrewrite(p.cross((left_bound | right_bound), ''),
                              '',
                              '',
                              sigma_star)

  return (remove_assignment @ remove_bounds).optimize()


def txn_to_psaf() -> p.Fst:
  return (romanize_fine() @
          remove_leftside() @
          remove_formatting()).optimize()


def txn_to_psac() -> p.Fst:
  return (romanize_coarse() @
          remove_leftside() @
          remove_formatting()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for character-phoneme assinment to natural translit."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['TXN_TO_PSAF'] = txn_to_psaf()
      exporter['TXN_TO_PSAC'] = txn_to_psac()

if __name__ == '__main__':
  multi_grm.run(generator_main)
