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

"""Script-specific visual normalization for abjad/alphabet script languages."""
from typing import List

import pynini
from nisaba.scripts.abjad_alphabet import util
from nisaba.scripts.utils import rule


def script_common_fsts(sigma: pynini.Fst, prefix=()) -> List[pynini.Fst]:
  return [rule.fst_from_rule_file(util.LANG_DIR / (component + '.tsv'), sigma)
          for component in prefix + ('nfc', 'visual_norm')]
