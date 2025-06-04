# Copyright 2025 Nisaba Authors.
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

"""Grammar parameters for Te."""

from nisaba.scripts.natural_translit.brahmic import g2p
from nisaba.scripts.natural_translit.brahmic import romanizer
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import transcriptor
from nisaba.scripts.natural_translit.utils import fst_list as fl


def _iso_to_txn() -> fl.FstList:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return fl.FstList(
      g2p.iso_to_txn(),
      g2p.VOCALIC_U,
      g2p.SCHWA_A,
      g2p.ANUSVARA_ASSIMILATION,
      g2p.DEFAULT_ANUSVARA_LABIAL,
      g2p.JNY_TO_GNY,
  )


def iso_to_psaf() -> fl.FstList:
  """Pan-South Asian fine grained transliteration."""
  return fl.FstList(_iso_to_txn(), romanizer.TXN_TO_PSAF)


def iso_to_psac() -> fl.FstList:
  """Pan-South Asian coarse grained transliteration."""
  return fl.FstList(_iso_to_txn(), romanizer.TXN_TO_PSAC)


def iso_to_nat() -> fl.FstList:
  """Telugu natural transliteration."""
  return fl.FstList(
      _iso_to_txn(),
      romanizer.TXN_TO_PSA_COMMON,
      romanizer.TRANSLIT_BY_PSA,
      ltn.print_only_ltn(),
  )


def iso_to_ipa() -> fl.FstList:
  """Pronunciation in IPA."""
  return fl.FstList(_iso_to_txn(), transcriptor.txn_to_ipa())
