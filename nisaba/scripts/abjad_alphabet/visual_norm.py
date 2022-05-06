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

r"""Visual normalization grammar for abjad / alphabet script languages.

To try for Urdu:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  nisaba/scripts/abjad_alphabet:visual_norm

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far \
    bazel-bin/nisaba/scripts/abjad_alphabet/visual_norm.far \
  --rules=UR \
  < /tmp/urdu_word_list.txt
```
"""
import pynini
from pynini.export import multi_grm
import nisaba.scripts.abjad_alphabet.util as u
from nisaba.scripts.utils import rewrite
from nisaba.scripts.utils import rule
import nisaba.scripts.utils.file as uf


def _open_nfc(script_or_lang_code: str, token_type: str) -> pynini.Fst:
  return u.open_fst_from_far('nfc', script_or_lang_code.upper(), token_type)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for visual normalization of abjad / alphabet script languages."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      sigma = u.sigma_from_common_data_files()
      presentation_forms_rewrite = rule.fst_from_rule_file(
          u.LANG_DIR / 'presentation_forms.tsv', sigma)
      nfc_rewrite = rule.fst_from_rule_file(u.LANG_DIR / 'nfc.tsv', sigma)

      exporter = exporter_map[token_type]
      for lang in u.LANGS:
        anywhere_rewrite = rule.fst_from_rule_file(
            u.LANG_DIR / lang / 'visual_norm.tsv', sigma)

        nonfinal_file = u.LANG_DIR / lang / 'visual_norm_nonfinal.tsv'
        nonfinal_rule = uf.StringFile(nonfinal_file, return_if_empty=uf.EPSILON)
        nonfinal_rewrite = rewrite.Rewrite(nonfinal_rule, sigma, right=sigma)

        final_isolated_file = (u.LANG_DIR / lang /
                               'visual_norm_final_isolated.tsv')
        final_isolated_rule = uf.StringFile(final_isolated_file,
                                            return_if_empty=uf.EPSILON)
        final_rewrite = rewrite.Rewrite(final_isolated_rule, sigma,
                                        left=sigma, right='[EOS]')

        isolated_file = u.LANG_DIR / lang / 'visual_norm_isolated.tsv'
        isolated_rule = uf.StringFile(isolated_file, return_if_empty=uf.EPSILON)
        isolated_rewrite = rewrite.Rewrite(
            pynini.union(final_isolated_rule, isolated_rule), sigma,
            left='[BOS]', right='[EOS]')

        exporter[lang.upper()] = rewrite.ComposeFsts([
            presentation_forms_rewrite,
            nfc_rewrite,
            anywhere_rewrite,
            nonfinal_rewrite,
            final_rewrite,
            isolated_rewrite,
        ])


if __name__ == '__main__':
  multi_grm.run(generator_main)
