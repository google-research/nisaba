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

"""Utility functions and definitions used in this package."""

import itertools as it
import pathlib

import pynini
import nisaba.scripts.utils.char as uc
import nisaba.scripts.utils.file as uf

FAR_DIR = pathlib.Path('com_google_nisaba/nisaba/scripts/abjad_alphabet')
SCRIPT_DIR = FAR_DIR / 'data'
SCRIPT_NAME = 'Arab'

LANG_DIR = SCRIPT_DIR / SCRIPT_NAME
LANGS = ('ar', 'azb', 'bal', 'ckb', 'fa', 'ks', 'ms', 'pa', 'prs', 'ps', 'sd',
         'ug', 'ur', 'uz')


def sigma_from_common_data_files() -> pynini.Fst:
  """Computes sigma from any abjad / alphabet romanizer.

  Returns:
    pynini.Fst: An unweighted FSA that accepts this finite sigma language.
  """
  common_files = ['nfc', 'presentation_forms', 'reversible_roman']
  lang_files = ['reading_norm',
                'visual_norm',
                'visual_norm_final_isolated',
                'visual_norm_isolated',
                'visual_norm_nonfinal']
  files = [f'{lang}/{file}' for lang, file in it.product(LANGS, lang_files)]
  paths = [LANG_DIR / f'{file}.tsv' for file in files + common_files]
  chars = uc.derive_chars(input_side=paths)
  return uc.derive_sigma(chars)


def open_fst_from_far(far_name: str, fst_name: str,
                      token_type: str) -> pynini.Fst:
  """Loads FST given by `fst_name` from FAR specified by `far_name`."""
  return uf.OpenFstFromFar(FAR_DIR, far_name, token_type, fst_name)
