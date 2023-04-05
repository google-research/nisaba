# Copyright 2023 Nisaba Authors.
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
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/iso.far \
 --rules=FROM_BRAHMIC \
 < /tmp/words.txt
```

To create input - output tsv:

```sh
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/iso.far \
 --rules=FROM_BRAHMIC \
 < /tmp/words.txt \
 | sed 's/Output string: //' \
 | paste /tmp/words.txt - \
 > /tmp/iso.tsv
```
"""

import os
from typing import Tuple

import pynini as p
from pynini.export import multi_grm
from pynini.lib import pynutil as pu
from nisaba.scripts.brahmic import util as u
from nisaba.scripts.utils import file as f
from nisaba.scripts.utils import rewrite as rw



# Public version of does not accept type subscript on os.PathLike, yet.
def brahmic_to_iso(consonant_file: os.PathLike,
                   inherent_vowel_file: os.PathLike,
                   vowel_sign_file: os.PathLike,
                   vowel_file: os.PathLike,
                   vowel_length_sign_file: os.PathLike,
                   coda_file: os.PathLike,
                   dead_consonant_file: os.PathLike,
                   standalone_file: os.PathLike,
                   subjoined_consonant_file: os.PathLike,
                   virama_file: os.PathLike) -> p.Fst:

  """Creates an FST that transduces a Brahmic script to ISO 15919.

  Args:
    consonant_file: Path relative to the runfiles directory of a StringFile containing a
      native--latin consonant mapping.
    inherent_vowel_file: Path relative to depot of a StringFile containing the
      inherent vowel.
    vowel_sign_file: Path relative to depot of a StringFile containing a
      native--latin vowel matra mapping.
    vowel_file: Path relative to depot of a StringFile containing a
      native--latin independent vowel mapping.
    vowel_length_sign_file: Path relative to depot of a StringFile containing a
      native--latin vowel length sign mapping.
    coda_file: Path relative to depot of a StringFile containing a
      native--latin coda mapping.
    dead_consonant_file: Path relative to depot of a StringFile containing a
      native--latin dead consonant mapping.
    standalone_file: Path relative to depot of a StringFile containing a
      native--latin standalone string mapping.
    subjoined_consonant_file: Path relative to depot of a StringFile containing
      a native--latin subjoined consonant mapping.
    virama_file: Path relative to depot of a StringFile containing the virama
      for the script.

  Returns:
    Brahmic script to ISO FST.
  """
  core_consonant = f.StringFile(consonant_file)
  inherent_vowel = f.StringFile(inherent_vowel_file)
  vowel_sign = f.StringFile(vowel_sign_file)
  vowel = f.StringFile(vowel_file)
  vowel_length_sign = f.StringFile(vowel_length_sign_file)
  coda = f.StringFile(coda_file)
  dead_consonant = f.StringFile(dead_consonant_file)
  standalone = f.StringFile(standalone_file)
  subjoined_consonant = f.StringFile(subjoined_consonant_file)
  virama = f.StringFile(virama_file)

  common_symbol = f.StringFile(u.SCRIPT_DIR / 'symbol.tsv')

  ins_inherent = pu.insert(inherent_vowel)
  ins_dash = pu.insert('-')
  ins_dot = pu.insert('.')
  del_virama = pu.delete(virama)
  virama_mark = p.cross(virama, '˘')

  low_priority_epsilon = p.accep('', weight=1)
  consonant = core_consonant + f.QuesSafe(subjoined_consonant)
  convert_to_iso = p.union(
      consonant + vowel_sign,
      consonant + ins_inherent + low_priority_epsilon,
      consonant + del_virama + low_priority_epsilon,
      vowel + low_priority_epsilon,
      coda,
      dead_consonant,
      vowel_length_sign,
      standalone,

      # Rare cases:
      # Dangling vowel signs.
      ins_dash + vowel_sign + (ins_dot + vowel).star + low_priority_epsilon,
      virama_mark + low_priority_epsilon,  # Explicit virama elsewhere.
      common_symbol,  # Joiners.

      # Independent vowel not as the first letter:
      vowel + (ins_dot + vowel).plus + low_priority_epsilon,
      consonant + vowel_sign + (ins_dot + vowel).plus,
      consonant + del_virama + (ins_dot + vowel).plus,
      consonant + ins_inherent + (ins_dot + vowel).plus)

  return p.optimize(convert_to_iso.star)


def _script_fsts(script: str, token_type: str) -> Tuple[p.Fst, p.Fst]:
  """Creates FSTs to convert between script and ISO."""
  from_script = brahmic_to_iso(
      u.SCRIPT_DIR / script / 'consonant.tsv',
      u.SCRIPT_DIR / script / 'inherent_vowel.tsv',
      u.SCRIPT_DIR / script / 'vowel_sign.tsv',
      u.SCRIPT_DIR / script / 'vowel.tsv',
      u.SCRIPT_DIR / script / 'vowel_length_sign.tsv',
      u.SCRIPT_DIR / script / 'coda.tsv',
      u.SCRIPT_DIR / script / 'dead_consonant.tsv',
      u.SCRIPT_DIR / script / 'standalone.tsv',
      u.SCRIPT_DIR / script / 'subjoined_consonant.tsv',
      u.SCRIPT_DIR / script / 'virama.tsv')
  to_script = p.invert(from_script)
  nfc = u.OpenFstFromBrahmicFar('nfc', script, token_type)
  from_script = rw.ComposeFsts([nfc, from_script])
  return (from_script, to_script)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generate FSTs for ISO conversion of various Brahmic scripts."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):
      exporter = exporter_map[token_type]
      from_script_fsts = []
      for script in u.SCRIPTS:
        from_script, to_script = _script_fsts(script, token_type)
        from_script_fsts += [from_script]
        script = script.upper()
        exporter[f'FROM_{script}'] = from_script
        exporter[f'TO_{script}'] = to_script
      exporter['FROM_BRAHMIC'] = rw.Rewrite(p.union(*from_script_fsts))


if __name__ == '__main__':
  multi_grm.run(generator_main)
