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

r"""Reversible romanization rules for abjad/alphabet family of language scripts.

To try for Urdu:

```shell
ABJAD_ALPHABET_DIR=nisaba/scripts/abjad_alphabet
bazel build -c opt nlp/grm/language:rewrite-tester \
  ${ABJAD_ALPHABET_DIR}:reversible_roman

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=blaze-genfiles/${ABJAD_ALPHABET_DIR}/reversible_roman.far \
 --rules=FROM_UR \
 < /tmp/urdu_word_list.txt
```
"""

import pynini
from pynini.export import multi_grm
from pynini.lib import byte
from nisaba.scripts.abjad_alphabet import util
from nisaba.scripts.abjad_alphabet import visual_norm_common
from nisaba.scripts.utils import file
from nisaba.scripts.utils import rewrite
from nisaba.scripts.utils import rule


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for language-agnostic reversible romanization of abjad/alphabets."""
  # Compile romanisation transducer. In the direction to Latin, NFC and then
  # visual normalization are applied. They are not required in the opposite
  # direction.
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      exporter = exporter_map[token_type]
      sigma = byte.BYTE
      if token_type == 'utf8':
        sigma = util.sigma_from_common_data_files()

      # TODO: Currently, `prefix=(‘presentation_forms’,)` takes too long
      # to process, so it is not specified in `script_common_fsts()` even though
      # it should be included.
      script_common_fsts = visual_norm_common.script_common_fsts(sigma)
      roman_mapping_file = util.LANG_DIR / 'reversible_roman.tsv'
      roman_fst = rule.fst_from_rule_file(roman_mapping_file, sigma)
      fsts = script_common_fsts + [roman_fst]
      exporter['FROM_ARAB'] = rewrite.ComposeFsts(fsts, sigma)

      # Transforming Latin to native is simpler.
      roman_strings = file.StringFile(roman_mapping_file)
      roman_inv_fst = pynini.invert(roman_strings).star
      exporter['TO_ARAB'] = roman_inv_fst.optimize()


if __name__ == '__main__':
  multi_grm.run(generator_main)
