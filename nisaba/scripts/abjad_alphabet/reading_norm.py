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

r"""Reading normalization grammar for abjad / alphabet script languages.

To try for Urdu:

```sh
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
  nisaba/scripts/abjad_alphabet:reading_norm

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
  --far \
    bazel-bin/nisaba/scripts/abjad_alphabet/reading_norm.far \
  --rules=UR \
  < /tmp/urdu_word_list.txt
```
"""

from absl import flags

import pynini
from pynini.export import grm
import nisaba.scripts.abjad_alphabet.util as u
from nisaba.scripts.utils import rule

_LANG = flags.DEFINE_string('lang', '', 'ISO 639-2/3 language tag.')
_TOKEN_TYPE = flags.DEFINE_enum('token_type', '', ['byte', 'utf8'],
                                'Token type: utf8 or byte')


def generator_main(exporter: grm.Exporter):
  """FSTs for reading normalization of abjad / alphabet script languages."""
  lang = _LANG.value
  token_type = _TOKEN_TYPE.value
  with pynini.default_token_type(token_type):  # pytype: disable=wrong-arg-types
    sigma = u.sigma_from_common_data_files()
    reading_norm_file = u.LANG_DIR / lang / 'reading_norm.tsv'
    reading_norm_fst = rule.fst_from_rule_file(reading_norm_file, sigma)
    lang = lang.upper()
    exporter[lang] = reading_norm_fst

if __name__ == '__main__':
  grm.run(generator_main)
