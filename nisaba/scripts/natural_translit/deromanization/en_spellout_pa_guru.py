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

"""English letter spellout for Punjabi Gurmukhi."""
import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import en_spellout as en


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):
      exporter = exporter_map[token_type]
      exporter['SPELLOUT'] = en.speller(en.Language.PA, en.Script.GURU)


if __name__ == '__main__':
  multi_grm.run(generator_main)
