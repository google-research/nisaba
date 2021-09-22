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
from typing import Iterable

import pynini
from pynini.export import multi_grm
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.file as uf


def _input_string_files(filenames: Iterable[os.PathLike]) -> pynini.Fst:
  return pynini.project(uf.StringFilesSafe(filenames), 'input').rmepsilon()


def _accept_well_formed_fst(consonant: pynini.Fst,
                            dead_consonant: pynini.Fst,
                            vowel_sign: pynini.Fst,
                            independent_vowel: pynini.Fst,
                            coda: pynini.Fst,
                            standalone: pynini.Fst,
                            virama: pynini.Fst,
                            accept: pynini.Fst,
                            preserve: pynini.Fst) -> pynini.Fst:
  """Create an unweighted FSA to accept the well-formed strings in a script.

  Args:
    consonant: native--latin consonant mapping.
    dead_consonant: native--latin dead consonants.
    vowel_sign: native--latin vowel matra mapping.
    independent_vowel: native--latin independent vowel mapping.
    coda: native--latin coda symbol mapping.
    standalone: native--latin standalone string mapping.
    virama: Virama for the script.
    accept: A list of legal codables that are exceptional to the other rules.
    preserve: native--special escape mapping of interconsonantal contexts that
      should maintain their zero width formatting characters.

  Returns:
    pynini.Fst: An unweighted FSA to accept this language.
  """
  cluster = (consonant + pynini.union(virama, preserve)).star + consonant
  codable = pynini.union(
      independent_vowel,
      cluster + vowel_sign.ques
  ) + coda.ques
  akshara = pynini.union(
      codable,
      cluster + virama + dead_consonant.ques
  )
  return pynini.union(akshara, standalone, accept).plus.optimize()


def _accept_well_formed(consonant_files: Iterable[os.PathLike],
                        dead_consonant_files: Iterable[os.PathLike],
                        vowel_sign_files: Iterable[os.PathLike],
                        vowel_files: Iterable[os.PathLike],
                        coda_files: Iterable[os.PathLike],
                        standalone_files: Iterable[os.PathLike],
                        virama_files: Iterable[os.PathLike],
                        accept_files: Iterable[os.PathLike],
                        preserve_files: Iterable[os.PathLike]) -> pynini.Fst:
  """Create an unweighted FSA to accept the well-formed strings in a script.

  Args:
    consonant_files: Paths relative to depot of a StringFile containing a
      native--latin consonant mapping.
    dead_consonant_files: Paths relative to the runfiles directory of a StringFile containing a
      native--latin dead consonants.
    vowel_sign_files: Paths relative to depot of a StringFile containing a
      native--latin vowel matra mapping.
    vowel_files: Paths relative to depot of a StringFile containing a
      native--latin independent vowel mapping.
    coda_files: Paths relative to depot of a StringFile containing a
      native--latin coda symbol mapping.
    standalone_files: Paths relative to depot of a StringFile containing a
      native--latin standalone string mapping.
    virama_files: Paths relative to depot of a StringFile containing the virama
      for the script.
    accept_files: Paths relative to depot of a StringFile containing a list of
      legal codables that are exceptional to the other rules.
    preserve_files: Paths relative to depot of a StringFile containing a
      native--special escape mapping of interconsonantal contexts that should
      maintain their zero width formatting characters.

  Returns:
    pynini.Fst: An unweighted FSA to accept this language.
  """
  consonant = _input_string_files(consonant_files)
  dead_consonant = _input_string_files(dead_consonant_files)
  independent_vowel = _input_string_files(vowel_files)
  vowel_sign = _input_string_files(vowel_sign_files)
  coda = _input_string_files(coda_files)
  virama = _input_string_files(virama_files)
  standalone = _input_string_files(standalone_files)
  preserve = _input_string_files(preserve_files)
  accept = _input_string_files(accept_files)
  return _accept_well_formed_fst(consonant, dead_consonant, vowel_sign,
                                 independent_vowel, coda, standalone, virama,
                                 accept, preserve)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generate unweighted FSAs accepting the language of each Brahmic script."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      exporter = exporter_map[token_type]
      for script in u.SCRIPTS:
        exporter[script.upper()] = _accept_well_formed(
            [u.SCRIPT_DIR / script / 'consonant.tsv'],
            [u.SCRIPT_DIR / script / 'dead_consonant.tsv'],
            [u.SCRIPT_DIR / script / 'vowel_sign.tsv'],
            u.AllScriptAndLangFiles(script, 'vowel.tsv'),
            [u.SCRIPT_DIR / script / 'coda.tsv'],
            [u.SCRIPT_DIR / script / 'standalone.tsv'],
            [u.SCRIPT_DIR / script / 'virama.tsv'],
            [u.SCRIPT_DIR / script / 'accept.tsv'],
            [u.SCRIPT_DIR / script / 'preserve.tsv'])


if __name__ == '__main__':
  multi_grm.run(generator_main)
