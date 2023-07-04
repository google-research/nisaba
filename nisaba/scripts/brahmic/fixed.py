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

r"""FST to convert fixed rule Brahmic romanization to corresponding native text.

By fixed rule romanization, we refer to the set of deterministic rules used
to unambiguously represent Brahmic scripts using ASCII characters, for input
purposes. ITRANS for Devanagari and Mozhi for Malayalam are examples.

The rules defined in the script specific fixed.tsv convert the ASCII text to
ISO 15919 as per the above schemes. The grammar defined here converts that
ISO 15919 output to respective Brahmic text using ISO-to-native conversion
defined in iso.py and associated data files.

Please refer to: https://en.wikipedia.org/wiki/ISO_15919 for ISO.

To try:

```sh
bazel build -c opt nlp/grm/language:rewrite-tester \
  nisaba/scripts/brahmic:fixed

cat /tmp/ml-latn-text.txt |
bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/fixed.far \
  --rules=MLYM > /tmp/ml-text.txt
```
"""

import string

import pynini
from pynini.export import multi_grm
import nisaba.scripts.brahmic.util as u
from nisaba.scripts.utils import rule
import nisaba.scripts.utils.char as uc
import nisaba.scripts.utils.file as uf

# ASCII printable characters used for the input.
# Pynini's symbol generation characters ('[', ']') are avoided.
_ASCII_INPUT_CHARS = set(string.printable) - set('[]')


def _fixed_rule_fst(script: str) -> pynini.Fst:
  """Creates an FST that transduces fixed rule romanization to ISO 15919."""
  path = u.SCRIPT_DIR / script / 'fixed.tsv'
  chars = uc.derive_chars(both_sides=[path])
  sigma = uc.derive_sigma(chars | _ASCII_INPUT_CHARS)
  resource_file = uf.AsResourcePath(path)
  return rule.fst_from_cascading_rule_file(resource_file, sigma)


def _ascii_acceptor() -> pynini.Fst:
  """Acceptor for ASCII printable charactrers."""
  return pynini.union(*[pynini.accep(ch) for ch in _ASCII_INPUT_CHARS]).star


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for ISO conversion of fixed rule romanization of Brahmic."""
  for token_type in ('byte', 'utf8'):
    with pynini.default_token_type(token_type):
      exporter = exporter_map[token_type]
      for script in u.FIXED_RULE_SCRIPTS:
        iso_fst = u.OpenFstFromBrahmicFar('iso', f'to_{script}', token_type)
        exporter[f'{script.upper()}'] = (
            _ascii_acceptor() @ _fixed_rule_fst(script) @ iso_fst
        ).optimize()


if __name__ == '__main__':
  multi_grm.run(generator_main)
