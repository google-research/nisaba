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
import nisaba.scripts.brahmic.natural_translit.constants as c


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
                  p.cross('ng', 'ng') |
                  p.cross('ni', 'n') |
                  p.cross('nn', 'n') |
                  p.cross('ny', 'ny') |
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
                               c.ASSIGN,
                               c.SEP | c.R_BOUND,
                               c.SIGMA_STAR).optimize()

  romanize_final = p.cdrewrite(romanize_aux,
                               c.ASSIGN + c.SEQUENCE + c.SEP,
                               c.SEP | c.R_BOUND,
                               c.SIGMA_STAR).optimize()

  return (romanize_first @
          romanize_final).optimize()

_ROMANIZE_FINE = _romanize_fine()


def _romanize_coarse() -> p.Fst:
  """Coarse-grained Pan South Asian romanization."""

  coarse_aux = (p.cross('aa', 'a') |
                p.cross('ee', 'e') |
                p.cross('ii', 'i') |
                p.cross('oo', 'o') |
                p.cross('uu', 'u'))

  coarse = p.cdrewrite(coarse_aux,
                       c.ASSIGN,
                       c.R_BOUND,
                       c.SIGMA_STAR).optimize()

  return coarse

_ROMANIZE_COARSE = _romanize_coarse()


def _remove_graphemes() -> p.Fst:
  """Removes the left side of the assigment."""

  remove_sequence = p.cdrewrite(p.cross(c.SEQUENCE.star, ''),
                                c.L_BOUND,
                                c.ASSIGN,
                                c.SIGMA_STAR).optimize()

  return remove_sequence


def _remove_markers() -> p.Fst:
  """Removes the assigment and boundary markers."""

  signs = c.SEP | c.ASSIGN | c.L_BOUND | c.R_BOUND

  remove_signs = p.cdrewrite(p.cross(signs, ''),
                             '',
                             '',
                             c.SIGMA_STAR).optimize()

  return remove_signs

_REMOVE_FORMATTING = (_remove_graphemes() @ _remove_markers()).optimize()


def _txn_to_psaf() -> p.Fst:
  return (_ROMANIZE_FINE @
          _REMOVE_FORMATTING).optimize()

TXN_TO_PSAF = _txn_to_psaf()


def _txn_to_psac() -> p.Fst:
  return (_ROMANIZE_FINE @
          _ROMANIZE_COARSE @
          _REMOVE_FORMATTING).optimize()

TXN_TO_PSAC = _txn_to_psac()
