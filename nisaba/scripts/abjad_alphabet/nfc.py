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

r"""NFC grammar for abjad / alphabet script languages.

To try for Urdu:

```sh
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/abjad_alphabet:nfc

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/abjad_alphabet/nfc.far \
 --rules=ARAB \
 < /tmp/arab_word_list.txt
```
"""

import pynini
from pynini.export import multi_grm
import nisaba.scripts.abjad_alphabet.util as u
import nisaba.scripts.utils.rule as rule


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for language-agnostic NFC normalization of abjad / alphabet script text."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      sigma = u.sigma_from_common_data_files()
      mapping_file = u.LANG_DIR / 'nfc.tsv'
      mapping = rule.fst_from_rule_file(mapping_file, sigma)
      exporter = exporter_map[token_type]
      exporter[u.SCRIPT_NAME.upper()] = mapping


if __name__ == '__main__':
  multi_grm.run(generator_main)
