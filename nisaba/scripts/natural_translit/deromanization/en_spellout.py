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

"""English letter spellout for various South Asian languages."""
import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic import en_spellout

_LANG_SCRIPTS = (
    'bn_beng',
    'gu_gujr',
    'hi_deva',
    'kn_knda',
    'ml_mlym',
    'mr_deva',
    'or_orya',
    'pa_guru',
    'sd_arab',
    'si_sinh',
    'ta_taml',
    'te_telu',
    'ur_arab',
)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for spellout grammars for all supported language scripts."""
  for lang_script in _LANG_SCRIPTS:
    for token_type in ('byte', 'utf8'):
      with pyn.default_token_type(token_type):
        language_tag, script_tag = lang_script.split('_')
        language = en_spellout.Language(language_tag)
        script = en_spellout.Script(script_tag)
        exporter = exporter_map[token_type]
        exporter[lang_script.upper()] = en_spellout.speller(language, script)


if __name__ == '__main__':
  multi_grm.run(generator_main)
