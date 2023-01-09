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

"""South Asian multilingual phoneme assignment."""

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso2typ
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

TYP_TO_TXN = ls.union_star(*[al.assign(char.gr, char.ph) for char in iso.CHAR])


def iso_to_txn() -> p.Fst:
  """ISO graphemes to txn pronunciation."""
  return (iso2typ.iso_to_typ() @ TYP_TO_TXN).optimize()
