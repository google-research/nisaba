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

# Lint as: python3
"""End-to-end natural transliteration for Kannada."""

import pynini as p
from pynini.export import multi_grm
import nisaba.scripts.brahmic.natural_translit.iso2typ as iso
import nisaba.scripts.brahmic.natural_translit.phon_ops as ops
import nisaba.scripts.brahmic.natural_translit.txn2ipa as ipa
import nisaba.scripts.brahmic.natural_translit.txn2nat as txn
import nisaba.scripts.brahmic.natural_translit.typ2txn as typ


def _iso_to_txn() -> p.Fst:
  """Composes the fsts from ISO characters to final txn pronunciation."""
  return (iso.iso_to_typ() @
          typ.TYP_TO_TXN @
          typ.TAP_TO_TRILL @
          ops.DEFAULT_SCHWA_A @
          ops.ANUSVARA_ASSIMILATION @
          ops.DEFAULT_ANUSVARA_LABIAL @
          ops.JNY_TO_GNY).optimize()


def iso_to_psaf() -> p.Fst:
  """Pan-South Asian fine grained transliteration."""
  return (_iso_to_txn() @ txn.TXN_TO_PSAF).optimize()


def iso_to_psac() -> p.Fst:
  """Pan-South Asian coarse grained transliteration."""
  return (_iso_to_txn() @ txn.TXN_TO_PSAC).optimize()


def iso_to_ipa() -> p.Fst:
  """Pronunciation in IPA."""
  return (_iso_to_txn() @ ipa.txn_to_ipa()).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration for Kannada."""
  for token_type in ('byte', 'utf8'):
    with p.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['ISO_TO_PSAF'] = iso_to_psaf()
      exporter['ISO_TO_PSAC'] = iso_to_psac()
      exporter['ISO_TO_IPA'] = iso_to_ipa()


if __name__ == '__main__':
  multi_grm.run(generator_main)
