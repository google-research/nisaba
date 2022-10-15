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

"""Multilingual phonological operations."""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.grapheme_inventory as gr
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.util as u


# Anusvara place of articulation assimilation functions


def _assign_anusvara(
    phoneme: p.FstLike,
    place: p.FstLike = u.EPSILON) -> p.Fst:
  """Pronunciation of anusvara.

  Anusvara is mapped to nasalisation by default. The pronunciation of it
  can change across languages and it can be assimilated to the place of
  articulation of the following phoneme.

  Args:
    phoneme: Pronuncation of <ans>.
    place: Following phoneme.

  Returns:
    Rewrite fst.

  Following call:
  ```
  _assign_anusvara(ph.M, ph.LABIAL)

  ```
  would return:
  ```
  p.cdrewrite(
      p.cross('<ans>{nsl}', '<ans>{m}')
      '',
      p.union(ph.M, ph.P, ph.B),
      u.BYTE_STAR)

  """
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      phoneme,
      following=place)

DEFAULT_ANUSVARA_LABIAL = _assign_anusvara(ph.M)

DEFAULT_ANUSVARA_DENTAL = _assign_anusvara(ph.NI)

ANUSVARA_ASSIMILATION_LABIAL = _assign_anusvara(ph.M, ph.LABIAL)

ANUSVARA_ASSIMILATION_DENTAL = _assign_anusvara(ph.NI, ph.DENTAL)

ANUSVARA_ASSIMILATION_ALVEOLAR = _assign_anusvara(ph.N, ph.ALVEOLAR)

ANUSVARA_ASSIMILATION_PALATAL = _assign_anusvara(ph.NY, ph.PALATAL)

ANUSVARA_ASSIMILATION_RETROFLEX = _assign_anusvara(ph.NN, ph.RETROFLEX)

ANUSVARA_ASSIMILATION_VELAR = _assign_anusvara(ph.NG, ph.VELAR)

FINAL_ANUSVARA_NASALIZATION = rw.reassign_word_final(gr.ANS, ph.NASAL, ph.NSL)

# Composes anusvara assimilation for all places of articulation.
ANUSVARA_ASSIMILATION = (ANUSVARA_ASSIMILATION_LABIAL @
                         ANUSVARA_ASSIMILATION_DENTAL @
                         ANUSVARA_ASSIMILATION_ALVEOLAR @
                         ANUSVARA_ASSIMILATION_PALATAL @
                         ANUSVARA_ASSIMILATION_RETROFLEX @
                         ANUSVARA_ASSIMILATION_VELAR).optimize()

# Voicing

VOICING_OP = p.union(
    p.cross(ph.CH, ph.JH),
    p.cross(ph.K, ph.G),
    p.cross(ph.P, ph.B),
    p.cross(ph.T, ph.D),
    p.cross(ph.TI, ph.DI),
    p.cross(ph.TT, ph.DD)).optimize()


def voicing(
    preceding: p.FstLike,
    following: p.FstLike) -> p.Fst:
  """Voicing. See rewrite_by_operation for argument details."""
  return rw.rewrite_operation_by_context(
      VOICING_OP,
      preceding,
      following)

# JNY clusters


def _rewrite_jny(
    j: p.FstLike,
    ny: p.FstLike) -> p.Fst:
  """Jny cluster rewrites.

  Jny clusters are pronounced and transliterated differently across languages.

  Args:
    j: Pronuncation of grapheme <j>.
    ny: Pronuncation of grapheme <ny>

  Returns:
    Rewrite fst.

  Following call:
  ```
  _rewrite_jny(ph.G, ph.Y)

  ```
  would return:
  ```
  p.cdrewrite(
      p.cross('<j>{jh}<ny>{ny}', '<j>{g}<ny>{y}')
      '',
      '',
      u.BYTE_STAR)

  """
  return rw.rewrite(
      u.align(gr.J, ph.JH) + u.align(gr.NY, ph.NY),
      u.align(gr.J, j) + u.align(gr.NY, ny))

JNY_TO_GNY = _rewrite_jny(ph.G, ph.NY)

JNY_TO_GY = _rewrite_jny(ph.G, ph.Y)

JNY_TO_NY = _rewrite_jny(ph.SIL, ph.NY)
