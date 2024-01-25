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

r"""Reading normalization grammar for abjad / alphabet script languages.

To try for Urdu:

```sh
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
  nisaba/scripts/abjad_alphabet:reading_norm

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
  --far \
    bazel-bin/nisaba/scripts/abjad_alphabet/reading_norm.far \
  --rules=UR \
  < /tmp/urdu_word_list.txt
```
"""

from pynini.export import grm
from nisaba.scripts.abjad_alphabet import reading_norm


if __name__ == '__main__':
  grm.run(lambda e: reading_norm.generator_main(e, 'utf8'))
