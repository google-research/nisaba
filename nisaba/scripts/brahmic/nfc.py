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

r"""Grammar to convert texts in Brahmic family of scripts to their NFC form.

Please refer to: http://unicode.org/charts/normalization/
To try each rule:

```sh
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/brahmic:nfc

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/nfc.far \
  --rules=DEVA < /tmp/deva_words.txt
```
"""

import pynini
from pynini.export import multi_grm
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.rule as r


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FSTs for NFC normalizing Brahmic scripts."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      exporter = exporter_map[token_type]
      all_rules = []
      all_sigmas = []
      for script in u.SCRIPTS:
        sigma = u.OpenSigma(script, token_type)
        rules = list(
            r.rules_from_string_file(u.SCRIPT_DIR / script / 'nfc.tsv'))
        fst = r.fst_from_rules(rules, sigma)
        exporter[script.upper()] = fst
        all_rules += rules
        all_sigmas += [sigma]
      # Exports the pan-brahmic NFC FST.
      brahmic_sigma = pynini.union(*all_sigmas)
      brahmic_fst = r.fst_from_rules(all_rules, brahmic_sigma)
      exporter['BRAHMIC'] = brahmic_fst


if __name__ == '__main__':
  multi_grm.run(generator_main)
