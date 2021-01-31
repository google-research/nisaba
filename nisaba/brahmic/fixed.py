# Copyright 2021 Nisaba Authors.
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


r"""Grammar to convert Brahmic fixed rule romanization to ISO 15919.

By fixed rule romanization, we refer to the set of deterministic rules used
to unambiguously represent Brahmic scripts using ASCII characters, for input
purposes. ITRANS for Devanagari and Mozhi for Malayalam are examples.

The grammar defined here converts the ASCII text to ISO 15919 as per the rules
of these schemes, coded in script specific fixed.tsv. The conversion
from ISO 15919 to respective Brahmic text is available through the grammar
defined in iso.py of this library. This would complete the conversion to Brahmic
from ASCII as per the respective fixed rule specification.

Please refer to: https://en.wikipedia.org/wiki/ISO_15919 for ISO.

To try:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
  nisaba/brahmic:fixed

cat /tmp/ml-latn-text.txt |
bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/brahmic/fixed.far \
  --rules=MLYM > /tmp/ml-latn-iso-text.txt
```
"""


import string

import pynini
from pynini.export import multi_grm
from nisaba.brahmic import rule
import nisaba.brahmic.char_util as cu
import nisaba.brahmic.util as u
import nisaba.utils.file as uf


def _fixed_rule_fst(script: str) -> pynini.Fst:
  """Creates an FST that transduces fixed rule romanization to ISO 15919."""
  path = u.SCRIPT_DIR / script / 'fixed.tsv'
  resource_file = uf.AsResourcePath(path)
  chars = cu.derive_chars(both_sides=[path], input_side=[])
  # ASCII printable characters are pass through.
  # Pynini's symbol generation characters ('[', ']') are avoided.
  sigma = cu.derive_sigma(chars | set(string.printable) - set('[]'))
  return rule.fst_from_cascading_rule_file(resource_file, sigma)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """FSTs for ISO conversion of fixed rule romanization of Brahmic."""
  for token_type in ('byte', 'utf8'):
    # TODO(): Once typing.Literal support is able to tell
    # that our token_type variable will only be "byte" or "utf8", drop
    # the pytype disable comment.
    with pynini.default_token_type(token_type):  # pytype: disable=wrong-arg-types
      exporter = exporter_map[token_type]
      for script in u.FIXED_RULE_SCRIPTS:
        exporter[f'{script.upper()}'] = _fixed_rule_fst(script)


if __name__ == '__main__':
  multi_grm.run(generator_main)
