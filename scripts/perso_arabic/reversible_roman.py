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


r"""Reversible romanization rules for Perso-Arabic family of language scripts.

To try for Urdu:

```shell
PERSO_ARABIC_DIR=nisaba/scripts/perso_arabic
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  ${PERSO_ARABIC_DIR}:reversible_roman

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
 --far=blaze-genfiles/${PERSO_ARABIC_DIR}/reversible_roman.far \
 --rules=FROM_UR \
 < /tmp/urdu_word_list.txt
```
"""

import pynini
from pynini.export import grm
from pynini.lib import byte
import nisaba.scripts.perso_arabic.util as u
import nisaba.scripts.utils.file as f
import nisaba.scripts.utils.rule as rule


def generator_main(exporter: grm.Exporter):
  """FSTs for language-agnostic reversible romanization of Perso-Arabic text."""
  # Construct NFC transducer - it is different from the standalone FST
  # transducer in that it allows non-Perso-Arabic letters.
  nfc_file = u.LANG_DIR / 'nfc.tsv'
  nfc_fst = rule.fst_from_rule_file(nfc_file, byte.BYTE)

  # Build language-agnostic visual normalization transducer.
  visual_norm_file = u.LANG_DIR / 'common' / 'visual_norm.tsv'
  visual_norm_fst = rule.fst_from_rule_file(visual_norm_file, byte.BYTE)

  # Compile romanisation transducer. In the Latin direction we apply NFC and
  # visual normalization first. No visual normalization is required in the
  # opposite direction.
  roman_mapping_file = u.LANG_DIR / 'reversible_roman.tsv'
  roman_fst = rule.fst_from_rule_file(roman_mapping_file, byte.BYTE)
  exporter['FROM_ARAB'] = pynini.optimize(
      nfc_fst @ visual_norm_fst @ roman_fst)

  # Transforming Latin to native is simpler.
  roman_strings = f.StringFile(roman_mapping_file)
  roman_inv_fst = pynini.invert(roman_strings).star
  exporter['TO_ARAB'] = roman_inv_fst.optimize()


if __name__ == '__main__':
  grm.run(generator_main)
