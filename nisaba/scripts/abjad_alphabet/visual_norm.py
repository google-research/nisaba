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


r"""Visual normalization grammar for abjad / alphabet script languages.

To try for Urdu:

```sh
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/abjad_alphabet:visual_norm_byte

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far \
    bazel-bin/nisaba/scripts/abjad_alphabet/visual_norm_byte.far \
  --rules=UR \
  < /tmp/urdu_word_list.txt
```
"""

from typing import List

from absl import flags
import pynini
from pynini.export import grm
from nisaba.scripts.abjad_alphabet import visual_norm_common
import nisaba.scripts.abjad_alphabet.util as u
from nisaba.scripts.utils import rewrite
from nisaba.scripts.utils import rule
import nisaba.scripts.utils.file as uf

FLAGS = flags.FLAGS
_LANG = flags.DEFINE_string('lang', '', 'ISO 639-2/3 language tag.')
_TOKEN_TYPE = flags.DEFINE_enum('token_type', '', ['byte', 'utf8'],
                                'Token type: utf8 or byte')


def lang_fsts(lang: str, sigma: pynini.Fst) -> List[pynini.Fst]:
  """FSTs for visual normalization of abjad / alphabet script languages."""
  anywhere_rewrite = rule.fst_from_rule_file(
      u.LANG_DIR / lang / 'visual_norm.tsv', sigma)

  nonfinal_file = u.LANG_DIR / lang / 'visual_norm_nonfinal.tsv'
  nonfinal_rule = uf.StringFile(nonfinal_file, return_if_empty=uf.EPSILON)
  nonfinal_rewrite = rewrite.Rewrite(nonfinal_rule, sigma, right=sigma)

  final_isolated_file = (u.LANG_DIR / lang / 'visual_norm_final_isolated.tsv')
  final_isolated_rule = uf.StringFile(final_isolated_file,
                                      return_if_empty=uf.EPSILON)
  final_rewrite = rewrite.Rewrite(final_isolated_rule, sigma,
                                  left=sigma, right='[EOS]')

  isolated_file = u.LANG_DIR / lang / 'visual_norm_isolated.tsv'
  isolated_rule = uf.StringFile(isolated_file, return_if_empty=uf.EPSILON)
  isolated_rewrite = rewrite.Rewrite(
      pynini.union(final_isolated_rule, isolated_rule), sigma,
      left='[BOS]', right='[EOS]')

  return [
      anywhere_rewrite,
      nonfinal_rewrite,
      final_rewrite,
      isolated_rewrite,
  ]


def generator_main(exporter: grm.Exporter):
  """FSTs for visual normalization of abjad / alphabet script languages."""
  lang = _LANG.value
  token_type = _TOKEN_TYPE.value
  with pynini.default_token_type(token_type):  # pytype: disable=wrong-arg-types
    sigma = u.sigma_from_common_data_files()
    common_fsts = visual_norm_common.script_common_fsts(
        sigma, prefix=('presentation_forms',))
    per_lang_fsts = lang_fsts(lang, sigma)
    exporter[lang.upper()] = rewrite.ComposeFsts(common_fsts + per_lang_fsts)


if __name__ == '__main__':
  grm.run(generator_main)
