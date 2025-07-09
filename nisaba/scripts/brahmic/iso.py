# Copyright 2025 Nisaba Authors.
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
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/iso.far \
 --rules=FROM_BRAHMIC \
 < /tmp/words.txt
```

To create input - output tsv:

```sh
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
  nisaba/scripts/brahmic:iso

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
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


def brahmic_to_iso(
    consonant_file: os.PathLike[str],
    inherent_vowel_file: os.PathLike[str],
    vowel_sign_file: os.PathLike[str],
    vowel_file: os.PathLike[str],
    vowel_length_sign_file: os.PathLike[str],
    coda_file: os.PathLike[str],
    dead_consonant_file: os.PathLike[str],
    standalone_file: os.PathLike[str],
    subjoined_consonant_file: os.PathLike[str],
    virama_file: os.PathLike[str],
) -> p.Fst:
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
    coda_file: Path relative to depot of a StringFile containing a native--latin
      coda mapping.
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
  very_low_priority_epsilon = p.accep('', weight=2)
  consonant = core_consonant + f.QuesSafe(subjoined_consonant)
  convert_to_iso = p.union(
      consonant + vowel_sign,
      consonant + ins_inherent + low_priority_epsilon,
      consonant + del_virama + low_priority_epsilon,
      vowel + low_priority_epsilon,
      coda + low_priority_epsilon,
      dead_consonant,
      vowel_length_sign,
      standalone + low_priority_epsilon,
      # Rare cases:
      # Dangling vowel signs.
      ins_dash + vowel_sign + (ins_dot + vowel).star + low_priority_epsilon,
      virama_mark + very_low_priority_epsilon,  # Explicit virama elsewhere.
      common_symbol,  # Joiners.
      # Independent vowel not as the first letter:
      vowel + (ins_dot + vowel).plus + low_priority_epsilon,
      consonant + vowel_sign + (ins_dot + vowel).plus,
      consonant + del_virama + (ins_dot + vowel).plus,
      consonant + ins_inherent + (ins_dot + vowel).plus,
  )

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
      u.SCRIPT_DIR / script / 'virama.tsv',
  )
  to_script = p.invert(from_script)

  # TODO: Ideally, this should be Visual-Normalized with NFC. However,
  # this makes the following compositions too slow, causing the build to time
  # out.
  nfc = u.OpenFstFromBrahmicFar('nfc', script, token_type)
  from_nfced_script = rw.ComposeFsts([nfc, from_script])

  # TODO: The NFC form of Gurmukhi SHA is <SA, NUKTA>, which currently has
  # the same romanization defined in the Guru/consonant. So NFC on TO_GURU is
  # required currently. However that need not be the case. We could consider
  # moving the SHA from common consonant mapping to script specific files
  # without adding that to Gurmukhi. That would then align this code with
  # Arabic, which does not do NFC on TO_ARAB.
  to_nfced_script = rw.ComposeFsts([to_script, nfc])
  return (from_nfced_script, to_nfced_script)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generate FSTs for ISO conversion of various Brahmic scripts."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):
      exporter = exporter_map[token_type]
      from_script_fsts = []
      sigma_fsts = []
      for script in u.SCRIPTS:
        sigma = u.OpenSigma(script, token_type)
        sigma_fsts += [sigma]
        from_script, to_script = _script_fsts(script, token_type)
        from_script_fsts += [from_script]
        script = script.upper()
        exporter[f'FROM_{script}'] = from_script
        exporter[f'TO_{script}'] = to_script
      # TODO: The utf8 version of `FROM_BRAHMIC` transducer is
      # failing to rewrite any native script inputs.
      exporter['FROM_BRAHMIC'] = rw.Rewrite(
          p.union(*from_script_fsts).optimize(),
          sigma=p.union(*sigma_fsts).optimize()
      )


if __name__ == '__main__':
  multi_grm.run(generator_main)
