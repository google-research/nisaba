# Copyright 2021 Nisaba Authors.
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


r"""ISO 15919 2-way converstion rules for major Brahmic family of scripts.

Please refer to: https://en.wikipedia.org/wiki/ISO_15919 Also, please refer to
README for extensions to this scheme.
To try:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/iso.far \
 --rules=From_Brahmic \
 < /tmp/words.txt
```

To create input - output tsv:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/iso.far \
 --rules=From_Brahmic \
 < /tmp/words.txt \
 | sed 's/Output string: //' \
 | paste /tmp/words.txt - \
 > /tmp/iso.tsv
```
"""

import os
from typing import Dict

import pynini
from pynini.export import grm
from pynini.lib import pynutil
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.file as uf
import nisaba.scripts.utils.rewrite as ur


def brahmic_to_iso(consonant_file: os.PathLike, vowel_sign_file: os.PathLike,
                   vowel_file: os.PathLike, coda_file: os.PathLike,
                   standalone_file: os.PathLike,
                   virama_file: os.PathLike) -> pynini.Fst:
  """Creates an FST that transduces a Brahmic script to ISO 15919.

  Args:
    consonant_file: Path relative to the runfiles directory of a StringFile containing a
      native--latin consonant mapping.
    vowel_sign_file: Path relative to depot of a StringFile containing a
      native--latin vowel matra mapping.
    vowel_file: Path relative to depot of a StringFile containing a
      native--latin independent vowel mapping.
    coda_file: Path relative to depot of a StringFile containing a
      native--latin coda mapping.
    standalone_file: Path relative to depot of a StringFile containing a
      native--latin standalone string mapping.
    virama_file: Path relative to depot of a StringFile containing the virama
      for the script.

  Returns:
    Brahmic script to ISO FST.
  """

  consonant = uf.StringFile(consonant_file)
  vowel_sign = uf.StringFile(vowel_sign_file)
  vowel = uf.StringFile(vowel_file)
  coda = uf.StringFile(coda_file)
  standalone = uf.StringFile(standalone_file)
  virama = uf.StringFile(virama_file)
  common_symbol = uf.StringFile(u.DATA_DIR / 'common' / 'symbol.tsv')

  ins_a = pynutil.insert('a')
  ins_dash = pynutil.insert('-')
  ins_dot = pynutil.insert('.')
  del_virama = pynutil.delete(virama)
  virama_mark = pynini.cross(virama, '˘')

  low_priority_epsilon = pynini.accep('', weight=1)

  convert_to_iso = pynini.union(
      consonant + vowel_sign,
      consonant + del_virama + low_priority_epsilon,
      consonant + ins_a + low_priority_epsilon,
      vowel + low_priority_epsilon,
      coda,
      standalone,

      # Rare cases:
      # Dangling vowel signs.
      ins_dash + vowel_sign + (ins_dot + vowel).star + low_priority_epsilon,
      virama_mark + low_priority_epsilon,  # Explicit virama elsewhere.
      common_symbol,  # Joiners.

      # Independent vowel not as the first letter:
      vowel + (ins_dot + vowel).plus + low_priority_epsilon,
      consonant + ins_a + (ins_dot + vowel).plus,
      consonant + vowel_sign + (ins_dot + vowel).plus,
      consonant + del_virama + (ins_dot + vowel).plus)

  return pynini.optimize(convert_to_iso.star)


def _script_to_iso(script: str) -> pynini.Fst:
  return brahmic_to_iso(u.SCRIPT_DIR / script / 'consonant.tsv',
                        u.SCRIPT_DIR / script / 'vowel_sign.tsv',
                        u.SCRIPT_DIR / script / 'vowel.tsv',
                        u.SCRIPT_DIR / script / 'coda.tsv',
                        u.SCRIPT_DIR / script / 'standalone.tsv',
                        u.SCRIPT_DIR / script / 'virama.tsv')


def generator_main(exporter: grm.Exporter):
  """Generate FSTs for ISO conversion of various Brahmic scripts."""
  script_to_iso_dict: Dict[str, pynini.Fst] = {
      script: _script_to_iso(script) for script in u.SCRIPTS
  }
  for script, from_script in script_to_iso_dict.items():
    exporter[f'FROM_{script.upper()}'] = from_script
    exporter[f'TO_{script.upper()}'] = pynini.invert(from_script)
  exporter['FROM_BRAHMIC'] = ur.Rewrite(
      pynini.union(*script_to_iso_dict.values()))


if __name__ == '__main__':
  grm.run(generator_main)
