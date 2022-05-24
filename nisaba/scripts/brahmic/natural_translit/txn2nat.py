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

import nisaba.scripts.brahmic.natural_translit.constants as c

sigma_star = byte.BYTE.star
sep = c.SEPARATOR
sequence = c.SYMBOL_SEQUENCE
l_bound = c.LEFT_BOUNDARY
r_bound = c.RIGHT_BOUNDARY
asgn = c.ASSIGNMENT_SIGN


def _romanize_fine() -> p.Fst:
  """Fine-grained Pan South Asian romanization."""
  romanize_aux = (p.cross('a', 'a') |
                  p.cross('a_l', 'aa') |
                  p.cross('ae', 'ae') |
                  p.cross('b', 'b') |
                  p.cross('ch', 'ch') |
                  p.cross('dd', 'd') |
                  p.cross('di', 'd') |
                  p.cross('e', 'e') |
                  p.cross('e_l', 'ee') |
                  p.cross('f', 'f') |
                  p.cross('g', 'g') |
                  p.cross('h', 'h') |
                  p.cross('i', 'i') |
                  p.cross('i_l', 'ii') |
                  p.cross('jh', 'j') |
                  p.cross('k', 'k') |
                  p.cross('l', 'l') |
                  p.cross('ll', 'l') |
                  p.cross('m', 'm') |
                  p.cross('n', 'n') |
                  p.cross('ng', 'n') |
                  p.cross('ni', 'n') |
                  p.cross('nn', 'n') |
                  p.cross('ny', 'n') |
                  p.cross('o', 'o') |
                  p.cross('o_l', 'oo') |
                  p.cross('p', 'p') |
                  p.cross('q', 'k') |
                  p.cross('r', 'r') |
                  p.cross('rrt', 'rd') |
                  p.cross('rru', 'zh') |
                  p.cross('rt', 'r') |
                  p.cross('s', 's') |
                  p.cross('sh', 'sh') |
                  p.cross('ss', 'sh') |
                  p.cross('t', 't') |
                  p.cross('ti', 't') |
                  p.cross('tt', 't') |
                  p.cross('u', 'u') |
                  p.cross('u_l', 'uu') |
                  p.cross('vu', 'v') |
                  p.cross('x', 'kh') |
                  p.cross('xa', 'g') |
                  p.cross('y', 'y') |
                  p.cross('z', 'z') |
                  p.cross('asp', 'h') |
                  p.cross('nsl', 'n') |
                  p.cross('sil', ''))

  romanize_first = p.cdrewrite(romanize_aux,
                               asgn,
                               sep | r_bound,
                               sigma_star).optimize()

  romanize_final = p.cdrewrite(romanize_aux,
                               asgn + sequence + sep,
                               sep | r_bound,
                               sigma_star).optimize()

  return (romanize_first @
          romanize_final).optimize()

ROMANIZE_FINE = _romanize_fine()


def _romanize_coarse() -> p.Fst:
  """Coarse-grained Pan South Asian romanization."""

  coarse_aux = (p.cross('aa', 'a') |
                p.cross('ee', 'e') |
                p.cross('ii', 'i') |
                p.cross('oo', 'o') |
                p.cross('uu', 'u'))

  coarse = p.cdrewrite(coarse_aux,
                       asgn,
                       r_bound,
                       sigma_star).optimize()

  return coarse

ROMANIZE_COARSE = _romanize_coarse()


def _remove_graphemes() -> p.Fst:
  """Removes the left side of the assigment."""

  remove_sequence = p.cdrewrite(p.cross(sequence.star, ''),
                                l_bound,
                                asgn,
                                sigma_star).optimize()

  return remove_sequence


def _remove_markers() -> p.Fst:
  """Removes the assigment and boundary markers."""

  signs = sep | asgn | l_bound | r_bound

  remove_signs = p.cdrewrite(p.cross(signs, ''),
                             '',
                             '',
                             sigma_star).optimize()

  return remove_signs

REMOVE_FORMATTING = (_remove_graphemes() @ _remove_markers()).optimize()


def _txn_to_psaf() -> p.Fst:
  return (ROMANIZE_FINE @
          REMOVE_FORMATTING).optimize()

TXN_TO_PSAF = _txn_to_psaf()


def _txn_to_psac() -> p.Fst:
  return (ROMANIZE_FINE @
          ROMANIZE_COARSE @
          REMOVE_FORMATTING).optimize()

TXN_TO_PSAC = _txn_to_psac()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for character-phoneme assinment to natural translit."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['TXN_TO_PSAF'] = TXN_TO_PSAF
      exporter['TXN_TO_PSAC'] = TXN_TO_PSAC

if __name__ == '__main__':
  multi_grm.run(generator_main)
