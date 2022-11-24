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

"""Phonological operations that depend on iso graphemes."""

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso_inventory as gr
from nisaba.scripts.natural_translit.common import rewrite_functions as rw
from nisaba.scripts.natural_translit.common import util as u
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.phonology.operations import syllable as syl

# Vocalic liquids


def _vocalic(vcl: p.FstLike) -> p.Fst:
  """Pronunciation of the vowel part of the vocalic Rs and Ls."""
  return rw.rewrite(ph.VCL, vcl)

VOCALIC_I = _vocalic(ph.I)

VOCALIC_U = _vocalic(ph.U)

VOCALIC_EC = _vocalic(ph.EC)

# Schwa handling


def _default_schwa(schwa: p.FstLike) -> p.Fst:
  """Pronounces unassigned schwas as the default phoneme for the langauge."""
  return rw.rewrite(p.union(ph.SCHWA, ph.VCL_SCHWA), schwa)

SCHWA_A = _default_schwa(ph.A)

SCHWA_EC = _default_schwa(ph.EC)


def _vocal_schwa(
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Pronounces schwa depending on the context."""

  return rw.rewrite_by_context(
      ph.SCHWA,
      ph.VCL_SCHWA,
      preceding,
      following)


def _silent_schwa(
    preceding: p.FstLike = u.EPSILON,
    following: p.FstLike = u.EPSILON) -> p.Fst:
  """Deletes schwa depending on the context."""

  return rw.rewrite_by_context(
      ph.SCHWA,
      ph.SIL,
      preceding,
      following)

# Schwa is pronounced before coda graphemes
_SCHWA_BEFORE_CODA = _vocal_schwa(following=gr.CODA)

_SCHWA_BEFORE_IND_VOWEL = _vocal_schwa(following=gr.VOWEL_I)

# Schwa is pronounced after {i}{y} and {i_l}{y}
_SCHWA_AFTER_IY = _vocal_schwa(rw.concat_r(p.union(ph.I, ph.I_L), ph.Y))


def _schwa_eow(coda_cl) -> p.Fst:
  """Deletes the word final schwa if it's preceded by a legal coda."""
  return _silent_schwa(
      syl.legal_coda(coda_cl),
      u.EOS)


def _schwa_between_syllables(onset_cl, coda_cl) -> p.Fst:
  """Deletes schwa between two well-formed syllables."""
  return _silent_schwa(
      syl.legal_coda(coda_cl),
      syl.legal_onset(onset_cl))


def process_schwa(
    onset_cl: p.FstLike = u.EPSILON,
    coda_cl: p.FstLike = u.EPSILON
    ) -> p.Fst:
  """Compose fsts for schwa handling."""
  return (
      _SCHWA_BEFORE_CODA @
      _SCHWA_BEFORE_IND_VOWEL @
      _SCHWA_AFTER_IY @
      _schwa_eow(coda_cl) @
      _schwa_between_syllables(onset_cl, coda_cl)).optimize()

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

# JNY clusters


def _rewrite_jny(
    j: p.FstLike,
    ny: p.FstLike) -> p.Fst:
  """Jny clusters are pronounced differently across languages."""
  return rw.reassign_adjacent_alignments(
      gr.J, ph.JH, j,
      gr.NY, ph.NY, ny)

JNY_TO_GNY = _rewrite_jny(ph.G, ph.NY)

JNY_TO_GY = _rewrite_jny(ph.G, ph.Y)

JNY_TO_NY = _rewrite_jny(ph.SIL, ph.NY)

# <ph><ph> pronounced {f}{f}. Should only occur in Perso-Arabic words.
# TODO: Move this when there is a Perso-Arabic module.
PHPH_TO_FF = rw.reassign_adjacent_alignments(
    gr.PH, ph.P + ph.ASP, ph.F,
    gr.PH, ph.P + ph.ASP, ph.F,)

RT_TO_R = rw.rewrite(ph.RT, ph.R)

A_TO_EC = rw.rewrite(ph.A, ph.EC)
