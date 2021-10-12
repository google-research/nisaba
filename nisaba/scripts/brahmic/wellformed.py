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


r"""Acceptor for well-formed strings from major modern Brahmic scripts.

To try:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
                   nisaba/scripts/brahmic:wellformed

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/brahmic/wellformed.far \
 --rules=DEVA \
 < /tmp/words_to_verify.txt
```
"""

import os

import pynini
from pynini.export import multi_grm
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.file as uf


def _input_string_file(filename: os.PathLike,
                       return_if_empty: pynini.Fst = uf.EMPTY) -> pynini.Fst:
  fst = uf.StringFile(filename, return_if_empty)
  return pynini.project(fst, 'input').rmepsilon()


def accept_well_formed(script_config_file: os.PathLike,
                       consonant_file: os.PathLike,
                       dead_consonant_file: os.PathLike,
                       subjoined_consonant_file: os.PathLike,
                       vowel_sign_file: os.PathLike,
                       vowel_file: os.PathLike,
                       vowel_length_sign_file: os.PathLike,
                       coda_file: os.PathLike,
                       standalone_file: os.PathLike,
                       virama_file: os.PathLike,
                       accept_file: os.PathLike,
                       preserve_file: os.PathLike) -> pynini.Fst:
  """Create an unweighted FSA to accept the well-formed strings in a script.

  Args:
    script_config_file: Script configuration protocol buffer in text format.
      This file is allowed to be missing.
    consonant_file: Path relative to depot of a StringFile containing a
      native--latin consonant mapping.
    dead_consonant_file: Path relative to the runfiles directory of a StringFile containing
      native--latin dead consonants.
    subjoined_consonant_file: Path relative to the runfiles directory of a StringFile
      containing native--latin subjoined consonants.
    vowel_sign_file: Path relative to depot of a StringFile containing a
      native--latin vowel matra mapping.
    vowel_file: Path relative to depot of a StringFile containing a
      native--latin independent vowel mapping.
    vowel_length_sign_file: Path relative to depot of a StringFile containing a
      native--latin vowel length sign mapping.
    coda_file: Path relative to depot of a StringFile containing a
      native--latin coda symbol mapping.
    standalone_file: Path relative to depot of a StringFile containing a
      native--latin standalone string mapping.
    virama_file: Path relative to depot of a StringFile containing the virama
      for the script.
    accept_file: Path relative to depot of a StringFile containing a list of
      legal codables that are exceptional to the other rules.
    preserve_file: Path relative to depot of a StringFile containing a
      native--special escape mapping of interconsonantal contexts that should
      maintain their zero width formatting characters.

  Returns:
    pynini.Fst: An unweighted FSA to accept this language.
  """
  script_config = u.MaybeLoadScriptConfig(script_config_file)
  core_consonant = _input_string_file(consonant_file)
  dead_consonant = _input_string_file(dead_consonant_file)
  subjoined_consonant = _input_string_file(subjoined_consonant_file)
  vowel_sign = _input_string_file(vowel_sign_file)
  independent_vowel = _input_string_file(vowel_file)
  vowel_length_sign = _input_string_file(vowel_length_sign_file)
  coda = _input_string_file(coda_file)
  standalone = _input_string_file(standalone_file)
  virama = _input_string_file(virama_file)
  accept = _input_string_file(accept_file)
  preserve = _input_string_file(preserve_file)

  consonant = core_consonant + uf.QuesSafe(subjoined_consonant)
  cluster = uf.StarSafe(consonant + pynini.union(virama, preserve)) + consonant
  cluster_and_virama = cluster + virama + uf.QuesSafe(dead_consonant)

  if script_config.no_inherent_vowel:
    # This case supports the category of scripts that always require the
    # dependent vowel to present after a consonant (e.g., Thaana).
    cluster_with_vowel = cluster + vowel_sign
  else:
    # Most of the Brahmic scripts.
    cluster_with_vowel = cluster + vowel_sign.ques

  cluster_or_vowel_with_coda = pynini.union(
      independent_vowel,
      cluster_with_vowel
  ) + (uf.QuesSafe(vowel_length_sign) +
       uf.QuesSafe(coda) +
       uf.QuesSafe(dead_consonant))
  akshara = pynini.union(
      cluster_or_vowel_with_coda,
      cluster_and_virama
  )
  return uf.StarSafe(pynini.union(akshara, standalone, accept)).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generate unweighted FSAs accepting the language of each Brahmic script."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      exporter = exporter_map[token_type]
      for script in u.SCRIPTS:
        exporter[script.upper()] = accept_well_formed(
            u.SCRIPT_DIR / script / 'script_config.textproto',
            u.SCRIPT_DIR / script / 'consonant.tsv',
            u.SCRIPT_DIR / script / 'dead_consonant.tsv',
            u.SCRIPT_DIR / script / 'subjoined_consonant.tsv',
            u.SCRIPT_DIR / script / 'vowel_sign.tsv',
            u.SCRIPT_DIR / script / 'vowel.tsv',
            u.SCRIPT_DIR / script / 'vowel_length_sign.tsv',
            u.SCRIPT_DIR / script / 'coda.tsv',
            u.SCRIPT_DIR / script / 'standalone.tsv',
            u.SCRIPT_DIR / script / 'virama.tsv',
            u.SCRIPT_DIR / script / 'accept.tsv',
            u.SCRIPT_DIR / script / 'preserve.tsv')


if __name__ == '__main__':
  multi_grm.run(generator_main)
