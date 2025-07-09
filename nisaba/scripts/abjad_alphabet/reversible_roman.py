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

r"""Reversible romanization rules for abjad/alphabet family of language scripts.

To try for Urdu:

```shell
ABJAD_ALPHABET_DIR=nisaba/scripts/abjad_alphabet
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
  ${ABJAD_ALPHABET_DIR}:reversible_roman

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
 --far=blaze-genfiles/${ABJAD_ALPHABET_DIR}/reversible_roman.far \
 --rules=FROM_UR \
 < /tmp/urdu_word_list.txt
```
"""

import pynini
from pynini.export import multi_grm
from nisaba.scripts.abjad_alphabet import util
from nisaba.scripts.utils import file
from nisaba.scripts.utils import rewrite


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for language-agnostic reversible romanization of abjad/alphabets."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      nfc = util.open_fst_from_far('nfc', 'ARAB', token_type)

      roman_tsv = util.LANG_DIR / 'reversible_roman.tsv'
      roman = file.StringFile(roman_tsv).star.optimize()

      exporter = exporter_map[token_type]
      # NFC is used for romanization, not de-romanization.
      exporter['FROM_ARAB'] = rewrite.ComposeFsts([nfc, roman])
      exporter['TO_ARAB'] = roman.invert()


if __name__ == '__main__':
  multi_grm.run(generator_main)
