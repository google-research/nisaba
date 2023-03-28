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

# Lint as: python3
"""End-to-end natural transliteration for Telugu."""

import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import iso2ltn_ops
from nisaba.scripts.natural_translit.brahmic import iso2txn
from nisaba.scripts.natural_translit.brahmic import iso2txn_ops
from nisaba.scripts.natural_translit.phonology import txn2ipa


def _iso_to_txn() -> pyn.Fst:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return (iso2txn.iso_to_txn() @
          iso2txn_ops.VOCALIC_U @
          iso2txn_ops.SCHWA_A @
          iso2txn_ops.ANUSVARA_ASSIMILATION @
          iso2txn_ops.DEFAULT_ANUSVARA_LABIAL @
          iso2txn_ops.JNY_TO_GNY).optimize()


def iso_to_psaf() -> pyn.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAF).optimize()


def iso_to_psac() -> pyn.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (_iso_to_txn() @ iso2ltn_ops.TXN_TO_PSAC).optimize()


def iso_to_ipa() -> pyn.Fst:
  """Pronunciation in IPA."""
  return (_iso_to_txn() @ txn2ipa.txn_to_ipa()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration for Telugu."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_IPA'] = iso_to_ipa()


if __name__ == '__main__':
  multi_grm.run(generator_main)
