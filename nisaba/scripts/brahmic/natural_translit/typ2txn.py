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

"""South Asian multilingual phoneme assignment."""

import pynini as p
from pynini.export import multi_grm


def typ_to_txn() -> p.Fst:
  """Naive grapheme to phoneme assignment."""

  assign_phoneme = (p.cross('(a)', '(a=a)') |
                    p.cross('(aa)', '(aa=a_l)') |
                    p.cross('(ans)', '(ans=ni)') |
                    p.cross('(d)', '(d=di)') |
                    p.cross('(dd)', '(dd=dd)') |
                    p.cross('(h)', '(h=h)') |
                    p.cross('(i)', '(i=i)') |
                    p.cross('(ii)', '(ii=i_l)') |
                    p.cross('(n)', '(n=ni)') |
                    p.cross('(n_chl)', '(n_chl=ni)') |
                    p.cross('(t)', '(t=ti)') |
                    p.cross('(tt)', '(tt=tt)') |
                    p.cross('(y)', '(y=y)'))

  return assign_phoneme.star.optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for ISO char to PSA phoneme assignment."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['TYP_TO_TXN'] = typ_to_txn()


if __name__ == '__main__':
  multi_grm.run(generator_main)
