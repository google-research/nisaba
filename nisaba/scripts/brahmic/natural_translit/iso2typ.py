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
from pynini.export import multi_grm
from pynini.lib import byte

sigma_star = byte.BYTE.star


def iso_to_decomposed_typ() -> p.Fst:
  """ISO to typable fst."""

  iso_to_typ_vowel = (p.cross('a', '(a)') |
                      p.cross('i', '(i)') |
                      p.cross('ā', '(aa)') |
                      p.cross('ī', '(ii)'))

  iso_to_typ_consonant = (p.cross('ṭ', '(tt)') |
                          p.cross('ḍ', '(dd)') |
                          p.cross('h', '(h)') |
                          p.cross('t', '(t)') |
                          p.cross('d', '(d)') |
                          p.cross('n', '(n)') |
                          p.cross('y', '(y)'))

  iso_to_typ_symbol = (p.cross('ṁ', '(ans)') |
                       p.cross('ⸯ', '(chl)'))

  iso_to_decomposed_typ_aux = (iso_to_typ_vowel |
                               iso_to_typ_consonant |
                               iso_to_typ_symbol)

  return iso_to_decomposed_typ_aux.star.optimize()


def composed_typ() -> p.Fst:
  """Maps multiple ISO characters to single native characters."""

  combine_chillu = p.cdrewrite(p.cross('(n)(chl)', '(n_chl)'),
                               '', '', sigma_star).optimize()
  return combine_chillu


def iso_to_typ() -> p.Fst:
  return (iso_to_decomposed_typ() @ composed_typ()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for language agnostic ISO to typeable string conversion."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_TYP_DECOMPOSED'] = iso_to_decomposed_typ()
      exporter['ISO_TO_TYP'] = iso_to_typ()


if __name__ == '__main__':
  multi_grm.run(generator_main)
