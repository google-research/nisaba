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

"""IPA pronunciation output."""

import pynini as pyn
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph


def txn_to_ipa() -> pyn.Fst:
  """Converts txn to IPA and outputs only transcription strings."""
  return p.print_only_ipa(ph.PHONEMES + [ph.MOD_INVENTORY.DURH])
