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

r"""Grammar for visual norm of major Brahmic script texts.

To try each rule:

```sh
bazel build -c opt nlp/grm2/thrax:rewrite-tester \
                   nisaba/scripts/brahmic:visual_norm

bazel-bin/nisaba/interim/grm2/thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/visual_norm.far \
  --rules=MLYM < /tmp/mlym_words.txt
```
"""

import os
from typing import List

from absl import flags
import pynini
from pynini.export import grm
from pynini.lib import pynutil
import nisaba.scripts.brahmic.char_util as cu
import nisaba.scripts.brahmic.util as u
from nisaba.scripts.utils import rule
import nisaba.scripts.utils.char as uc
import nisaba.scripts.utils.file as uf
import nisaba.scripts.utils.rewrite as ur

_SCRIPT = flags.DEFINE_string('script', '', 'ISO 15924 script tag.')
_LANG = flags.DEFINE_string('lang', '', 'ISO 639-2/3 language tag.')
_TOKEN_TYPE = flags.DEFINE_enum('token_type', '', ['byte', 'utf8'],
                                'Token type: utf8 or byte')


def core_visual_norm_fsts(rewrite_file: os.PathLike[str],
                          preserve_file: os.PathLike[str],
                          consonant_file: os.PathLike[str],
                          sigma: pynini.Fst) -> List[pynini.Fst]:
  """Creates a visual normalization FST.

  Given a rewrite file, preserve file, and consonant file, returns an FST
  that will perform the rewrites described in the StringFile `rewrite_file`,
  additionally clearing out instances of ZWJ, ZWNJ, and ZWS except for those
  that match preserve_file when occurring between consonants (which are
  specified in the consonants file).

  Args:
    rewrite_file: Path relative to the runfiles directory of a StringFile of visual rewrites.
    preserve_file: Path relative to the runfiles directory of a StringFile of ZWJ sequences to
      preserve.
    consonant_file: Path relative to the runfiles directory of a StringFile containing a
      native--latin consonant mapping.
    sigma: An Fst with which to consider the complete alphabet for cdrewrites.
  Returns:
    Visual normalization FST.
  """
  rewrite_fst = rule.fst_from_rule_file(rewrite_file, sigma)
  preserve = uf.StringFile(preserve_file)
  consonant_map = uf.StringFile(consonant_file)
  consonant = pynini.project(consonant_map, 'input')

  # This makes sure that the generated symbols used as implementation
  # detail symbols for ZWJ preservation are considered as part of sigma.
  # Generated symbols are those delimited by square brackets, such as
  # `[ZWJ,VIRAMA]` for example.
  intermediate_sigma = u.BuildSigmaFstFromSymbolTable(
      pynini.generated_symbols()).union(sigma)

  mark_preserve = ur.Rewrite(preserve, intermediate_sigma, consonant, consonant)
  clean_joiner = ur.Rewrite(
      pynutil.delete(pynini.union(uc.ZWNJ, uc.ZWJ, uc.ZWS)), intermediate_sigma)
  reinstate = ur.Rewrite(pynini.invert(preserve), intermediate_sigma)

  return [rewrite_fst, mark_preserve, clean_joiner, reinstate,
          # We right-compose with sigma.star to ensure the generated_symbols
          # don't leak through into the visual_norm fst.
          sigma.star]


def open_nfc(script_code: str, token_type: str) -> pynini.Fst:
  return u.OpenFstFromBrahmicFar('nfc', script_code, token_type)


def generator_main(exporter: grm.Exporter):
  """Generates FSTs for visual normalization of Brahmic scripts."""
  script = _SCRIPT.value
  lang = _LANG.value
  token_type = _TOKEN_TYPE.value
  script_dir = u.SCRIPT_DIR / script

  with pynini.default_token_type(token_type):  # pytype: disable=wrong-arg-types
    sigma = u.OpenSigma(script, token_type)
    dedup = cu.dedup_marks_fst(script, sigma)
    nfc = open_nfc(script, token_type)
    script_fst = ur.ComposeFsts(
        [nfc, dedup] + core_visual_norm_fsts(
            script_dir / 'visual_rewrite.tsv',
            script_dir / 'preserve.tsv',
            script_dir / 'consonant.tsv',
            sigma))

    if not lang:
      exporter[script.upper()] = script_fst
    else:
      consonant_map = uf.StringFile(script_dir / 'consonant.tsv')
      consonant = pynini.project(consonant_map, 'input')

      lang_dir = script_dir / lang
      before_cons = uf.StringFile(lang_dir / 'before_consonant.tsv')
      rewrite_before_cons = ur.Rewrite(before_cons, sigma, right=consonant)
      after_cons = uf.StringFile(lang_dir / 'after_consonant.tsv')
      rewrite_after_cons = ur.Rewrite(after_cons, sigma, left=consonant)
      lang_fst = ur.ComposeFsts([
          script_fst, rewrite_before_cons, rewrite_after_cons])
      exporter[lang.upper()] = lang_fst


if __name__ == '__main__':
  grm.run(generator_main)
