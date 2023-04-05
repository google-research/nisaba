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

"""txn pronunciation romanization."""

from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph

tr = ltn.TRANSLIT_INVENTORY

MAP_VOWEL_DIPHTHONG = p.ls_translit_by_key(ph.DIPHTHONG, 'diph')

MAP_VOWEL_SHORT = p.ls_translit_base(ph.SHORT_VOWEL)

MAP_VOWEL_LONG = p.ls_translit_by_key(ph.LONG_VOWEL, 'long')

MAP_VOWEL_IGNORE_LENGTH = p.ls_translit_base(ph.LONG_VOWEL)

MAP_AFFRICATE = p.ls_translit_by_key(ph.AFFRICATE_PHON, 'affr')

MAP_CONSONANT = p.ls_translit_base(ph.CONSONANT_PHON)

MAP_FEATURE = p.ls_translit_base(ph.FEATURE)
