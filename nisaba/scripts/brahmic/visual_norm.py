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

r"""Grammar for visual norm of major Brahmic script texts.

To try each rule:

```sh
bazel build -c opt @org_opengrm_thrax//:rewrite-tester \
                   nisaba/scripts/brahmic:visual_norm

bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/visual_norm.far \
  --rules=MLYM < /tmp/mlym_words.txt
```
"""

import os

import pynini
from pynini.export import multi_grm
from pynini.lib import pynutil
import nisaba.scripts.brahmic.char_util as cu
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.char as uc
import nisaba.scripts.utils.file as uf
import nisaba.scripts.utils.rewrite as ur
import nisaba.scripts.utils.rule as rule


def visual_norm(rewrite_file: os.PathLike, preserve_file: os.PathLike,
                consonant_file: os.PathLike, *,
                sigma: pynini.Fst) -> pynini.Fst:
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

  mark_preserve = ur.Rewrite(
      preserve, consonant, consonant, sigma=intermediate_sigma)
  clean_joiner = ur.Rewrite(
      pynutil.delete(pynini.union(uc.ZWNJ, uc.ZWJ, uc.ZWS)),
      sigma=intermediate_sigma)
  reinstate = ur.Rewrite(pynini.invert(preserve), sigma=intermediate_sigma)

  return pynini.optimize(
      rewrite_fst @ mark_preserve @ clean_joiner @ reinstate
      # We right-compose with sigma.star to ensure the generated_symbols don't
      # leak through into the visual_norm fst.
      @ sigma.star)


def open_nfc(script_code: str, *, token_type: str) -> pynini.Fst:
  return u.OpenFstFromBrahmicFar('nfc', script_code, token_type=token_type)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FSTs for visual normalization of Brahmic scripts."""
  for token_type in ('byte', 'utf8'):
    rewrite_map = {}
    with pynini.default_token_type(token_type):
      sigma_map = {}
      for script in u.SCRIPTS:
        sigma = u.OpenSigma(script, token_type=token_type)
        sigma_map[script] = sigma
        dedup = cu.dedup_marks_fst(script, sigma=sigma)
        nfc = open_nfc(script, token_type=token_type)
        rewrite_map[script] = (nfc @ dedup @ visual_norm(
            u.SCRIPT_DIR / script / 'visual_rewrite.tsv',
            u.SCRIPT_DIR / script / 'preserve.tsv',
            u.SCRIPT_DIR / script / 'consonant.tsv',
            sigma=sigma)).optimize()

      for script, langs in u.LANG_SCRIPT_MAP.items():
        for lang in langs:
          sigma = sigma_map[script]
          consonant_map = uf.StringFile(u.SCRIPT_DIR / script / 'consonant.tsv')
          consonant = pynini.project(consonant_map, 'input')

          before_cons = uf.StringFile(
              u.SCRIPT_DIR / script / lang / 'before_consonant.tsv')
          rewrite_before_cons = ur.Rewrite(before_cons, '', consonant,
                                           sigma=sigma)
          after_cons = uf.StringFile(
              u.SCRIPT_DIR / script / lang / 'after_consonant.tsv')
          rewrite_after_cons = ur.Rewrite(
              after_cons, '', consonant, sigma=sigma)
          rewrite_map[lang] = (rewrite_map[script] @
                               rewrite_before_cons @
                               rewrite_after_cons).optimize()

      exporter = exporter_map[token_type]
      for name, fst in rewrite_map.items():
        exporter[name.upper()] = fst

if __name__ == '__main__':
  multi_grm.run(generator_main)
