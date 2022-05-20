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

import nisaba.scripts.brahmic.natural_translit.phon_ops as ph

sigma_star = byte.BYTE.star


def romanize_fine() -> p.Fst:
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
                               ph.asgn(),
                               ph.sep() | ph.r_bound(),
                               sigma_star).optimize()

  romanize_final = p.cdrewrite(romanize_aux,
                               ph.asgn() + ph.sequence() + ph.sep(),
                               ph.sep() | ph.r_bound(),
                               sigma_star).optimize()

  return (romanize_first @
          romanize_final).optimize()


def romanize_coarse() -> p.Fst:
  """Coarse-grained Pan South Asian romanization."""

  coarse_aux = (p.cross('aa', 'a') |
                p.cross('ee', 'e') |
                p.cross('ii', 'i') |
                p.cross('oo', 'o') |
                p.cross('uu', 'u'))

  coarse = p.cdrewrite(coarse_aux,
                       ph.asgn(),
                       ph.r_bound(),
                       sigma_star).optimize()

  return coarse


def remove_leftside() -> p.Fst:
  """Removes the left side of the assigment."""

  remove_graphemes = p.cdrewrite(p.cross(ph.sequence().star, ''),
                                 ph.l_bound(),
                                 ph.asgn(),
                                 sigma_star).optimize()

  return remove_graphemes


def remove_formatting() -> p.Fst:
  """Removes the assigment and boundary markers."""

  markers = ph.sep() | ph.asgn() | ph.l_bound() | ph.r_bound()

  remove_markers = p.cdrewrite(p.cross(markers, ''),
                               '',
                               '',
                               sigma_star).optimize()

  return remove_markers


def txn_to_psaf() -> p.Fst:
  return (romanize_fine() @
          remove_leftside() @
          remove_formatting()).optimize()


def txn_to_psac() -> p.Fst:
  return (romanize_fine() @
          romanize_coarse() @
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
