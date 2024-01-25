# Copyright 2024 Nisaba Authors.
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
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

tr = ltn.TRANSLIT_INVENTORY

TRANSLIT_DIPHTHONG = p.ls_translit_by_key(ph.DIPHTHONG, 'diphthong')
TRANSLIT_AFFRICATE = p.ls_translit_by_key(ph.AFFRICATE, 'affricate')
TRANSLIT_BASE = p.ls_translit_base(ph.PHONEMES)
IGNORE_MODIFIERS = rw.rewrite_ls(
    [mod.ph, tr.DEL] for mod in ph.COMBINING_MODIFIERS
)
DEL_REPEATED_SUBSTRING = rw.rewrite_ls(
    [char.tr + char.tr, char.tr] for char in ltn.OTHER_SUBSTRING
)
