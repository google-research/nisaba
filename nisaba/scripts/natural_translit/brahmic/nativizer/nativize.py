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
"""End-to-end natural transliteration for Hindi."""

import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic.nativizer import ltn2iso

HI = (
    ltn2iso.LTN_GR
    @ ltn2iso.ASPIRATION
    @ ltn2iso.BASE_TWO
    @ ltn2iso.NUKTA
    @ ltn2iso.BASE_ONE
    @ ltn2iso.LONG_VOWEL
    @ ltn2iso.HI_VOWEL
    @ ltn2iso.SHORT_VOWEL
    @ ltn2iso.SCHWA_INSERTION
    @ ltn2iso.ISO_TR
).optimize()


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):

      exporter = exporter_map[token_type]
      exporter['HI'] = HI


if __name__ == '__main__':
  multi_grm.run(generator_main)
