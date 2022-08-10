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

r"""Grammar for Reading Norm of major Brahmic language script texts.

To try each rule:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
                   nisaba/scripts/brahmic:reading_norm

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/reading_norm.far \
  --rules=MLYM < /tmp/mlym_words.txt
```
"""

import pathlib

import pynini
from pynini.export import multi_grm
import nisaba.scripts.brahmic.util as u
from nisaba.scripts.utils import file
from nisaba.scripts.utils import rewrite
from nisaba.scripts.utils import rule


def _reading_norm_fst(
    path: pathlib.Path, tag: str, sigma: pynini.Fst) -> pynini.Fst:
  default = rewrite.Rewrite('', sigma)
  filename = path / tag / 'reading_norm.tsv'
  reading_rewrite_fst = (rule.fst_from_rule_file(filename, sigma)
                         if file.IsFileExist(filename) else default)
  return reading_rewrite_fst


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FSTs for reading normalization of Brahmic scripts."""
  for token_type in ('byte', 'utf8'):
    rewrite_map = {}
    with pynini.default_token_type(token_type):
      sigma_map = {}
      scripts = set(u.READING_NORM_SCRIPTS)
      scripts.update(u.READING_NORM_LANG_SCRIPT_MAP)
      for script in scripts:
        sigma = u.OpenSigma(script, token_type)
        sigma_map[script] = sigma
        visual_norm = u.OpenFstFromBrahmicFar('visual_norm', script, token_type)
        reading_norm = _reading_norm_fst(u.SCRIPT_DIR, script, sigma)
        rewrite_map[script] = rewrite.ComposeFsts([visual_norm, reading_norm])

      for script, langs in u.READING_NORM_LANG_SCRIPT_MAP.items():
        for lang in langs:
          sigma = sigma_map[script]
          rewrite_map[lang] = rewrite.ComposeFsts([
              rewrite_map[script],
              _reading_norm_fst(u.SCRIPT_DIR / script, lang, sigma),
          ])

      exporter = exporter_map[token_type]
      for name, fst in rewrite_map.items():
        exporter[name.upper()] = fst

if __name__ == '__main__':
  multi_grm.run(generator_main)
