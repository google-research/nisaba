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


r"""Visual normalization grammar for Perso-Arabic script languages.

To try for Urdu:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  nisaba/scripts/perso_arabic:visual_norm

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=bazel-bin/nisaba/scripts/perso_arabic/visual_norm.far \
 --rules=UR \
 < /tmp/urdu_word_list.txt
```
"""

import pynini
from pynini.export import multi_grm
import nisaba.scripts.perso_arabic.util as u
import nisaba.scripts.utils.rule as rule


def _open_nfc(script_or_lang_code: str, token_type: str) -> pynini.Fst:
  return u.open_fst_from_far('nfc', script_or_lang_code.upper(),
                             token_type=token_type)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for visual normalization of Perso-Arabic script languages."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      sigma = u.derive_sigma_from_romanizer()
      nfc = _open_nfc(u.SCRIPT_NAME, token_type=token_type)
      exporter = exporter_map[token_type]
      for lang in u.LANGS:
        mapping_file = u.LANG_DIR / lang / 'visual_norm.tsv'
        mapping = rule.fst_from_rule_file(mapping_file, sigma)
        lang = lang.upper()
        exporter[lang] = (nfc @ mapping).optimize()


if __name__ == '__main__':
  multi_grm.run(generator_main)
