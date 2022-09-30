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
bazel build -c opt nlp/grm/language:rewrite-tester \
                   nisaba/scripts/brahmic:reading_norm

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/reading_norm.far \
  --rules=MLYM < /tmp/mlym_words.txt
```
"""

import pathlib

from absl import flags

import pynini
from pynini.export import grm
import nisaba.scripts.brahmic.util as u
from nisaba.scripts.utils import file
from nisaba.scripts.utils import rewrite
from nisaba.scripts.utils import rule


FLAGS = flags.FLAGS
_SCRIPT = flags.DEFINE_string('script', '', 'ISO 15924 script tag.')
_LANG = flags.DEFINE_string('lang', '', 'ISO 639-2/3 language tag.')
_TOKEN_TYPE = flags.DEFINE_enum('token_type', '', ['byte', 'utf8'],
                                'Token type: utf8 or byte')


def _reading_norm_fst(path: pathlib.Path, sigma: pynini.Fst) -> pynini.Fst:
  default = rewrite.Rewrite('', sigma)
  filename = path / 'reading_norm.tsv'
  reading_rewrite_fst = (rule.fst_from_rule_file(filename, sigma)
                         if file.IsFileExist(filename) else default)
  return reading_rewrite_fst


def generator_main(exporter: grm.Exporter):
  """Generates FSTs for reading normalization of Brahmic scripts."""
  script = _SCRIPT.value
  lang = _LANG.value
  token_type = _TOKEN_TYPE.value
  with pynini.default_token_type(FLAGS.token_type):
    sigma = u.OpenSigma(script, token_type)
    script_reading_norm = _reading_norm_fst(u.SCRIPT_DIR / script, sigma)
    fsts = [script_reading_norm]
    if lang:
      lang_reading_norm = _reading_norm_fst(u.SCRIPT_DIR / script / lang, sigma)
      fsts += [lang_reading_norm]

    # TODO: Enable pre-processing with Visual Norm once the timeout issues
    # are resolved.
    # visual_norm = u.OpenFstFromBrahmicFar('visual_norm', script, token_type)
    # fsts = [visual_norm] + fsts
    name = lang if lang else script
    exporter[name.upper()] = rewrite.ComposeFsts(fsts)

if __name__ == '__main__':
  grm.run(generator_main)
