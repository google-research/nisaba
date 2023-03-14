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

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory as iso
from nisaba.scripts.natural_translit.brahmic import psa_phoneme_inventory as psa
from nisaba.scripts.natural_translit.phonology.operations import syllable as syl
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

gr = iso.GRAPHEME_INVENTORY
ph = psa.PHONEME_INVENTORY

# Vowels

A_TO_EC = rw.rewrite(ph.A, ph.EC)

# Ungliding: Diphthong to monophthong shift
AI_TO_EH_L = rw.rewrite(ph.A_I, ph.EH_L)
AU_TO_OH_L = rw.rewrite(ph.A_U, ph.OH_L)

# Vocalic liquids


def vocalic(vcl: pyn.FstLike, vcl_l: pyn.FstLike) -> pyn.Fst:
  """Pronunciation of the vowel part of the vocalic Rs and Ls."""
  return rw.rewrite(ph.SYL, vcl) @ rw.rewrite(ph.SYL_L, vcl_l)

VOCALIC_I = vocalic(ph.I, ph.I_L)
VOCALIC_U = vocalic(ph.U, ph.U_L)
VOCALIC_EC = vocalic(ph.EC, ph.EC_L)

# Schwa handling


def default_schwa(schwa: pyn.FstLike) -> pyn.Fst:
  """Pronounces unassigned schwas as the default phoneme for the language."""
  return rw.rewrite(ls.union_opt(ph.V_TNT, ph.V_PRN), schwa)

SCHWA_A = default_schwa(ph.A)
SCHWA_EC = default_schwa(ph.EC)


def vocal_schwa(
    preceding: pyn.FstLike = al.EPSILON,
    following: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Pronounces schwa depending on the context."""

  return rw.rewrite(
      ph.V_TNT,
      ph.V_PRN,
      preceding,
      following)


def silent_schwa(
    preceding: pyn.FstLike = al.EPSILON,
    following: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Deletes schwa depending on the context."""

  return rw.rewrite(
      ph.V_TNT,
      ph.SIL,
      preceding,
      following)

# Schwa is pronounced before coda graphemes
_SCHWA_BEFORE_CODA = vocal_schwa(following=gr.CODA)
_SCHWA_BEFORE_IND_VOWEL = vocal_schwa(following=gr.VOWEL_I)
# Schwa is pronounced after {i}{y} and {i_l}{y}
_SCHWA_AFTER_IY = vocal_schwa(cc.concat_r(ls.union_opt(ph.I, ph.I_L), ph.Y))


def schwa_eow(coda_cl) -> pyn.Fst:
  """Deletes the word final schwa if it's preceded by a legal coda."""
  return silent_schwa(
      syl.legal_coda(ph.VOWEL, ph.CONSONANT, coda_cl),
      al.EOS)


def schwa_between_syllables(onset_cl, coda_cl) -> pyn.Fst:
  """Deletes schwa between two well-formed syllables."""
  return silent_schwa(
      syl.legal_coda(ph.VOWEL, ph.CONSONANT, coda_cl),
      syl.legal_onset(ph.VOWEL, ph.CONSONANT, onset_cl))


def process_schwa(
    onset_cl: pyn.FstLike = al.EPSILON,
    coda_cl: pyn.FstLike = al.EPSILON
    ) -> pyn.Fst:
  """Compose fsts for schwa handling."""
  return (
      _SCHWA_BEFORE_CODA @
      _SCHWA_BEFORE_IND_VOWEL @
      _SCHWA_AFTER_IY @
      schwa_eow(coda_cl) @
      schwa_between_syllables(onset_cl, coda_cl)).optimize()

# Anusvara place of articulation assimilation functions


def assign_anusvara(
    phoneme: pyn.FstLike,
    place: pyn.FstLike = al.EPSILON) -> pyn.Fst:
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
  assign_anusvara(ph.M, ph.LABIAL)
  ```
  will return:
  ```
  pyn.cdrewrite(
      pyn.cross('<ans>{N}', '<ans>{m}')
      '',
      pyn.union(ph.M, ph.P, ph.B),
      al.BYTE_STAR)
  ```
  """
  return rw.reassign(
      gr.ANS,
      ph.NSL,
      phoneme,
      following=place)

DEFAULT_ANUSVARA_LABIAL = assign_anusvara(ph.M)
DEFAULT_ANUSVARA_DENTAL = assign_anusvara(ph.NI)
ANUSVARA_ASSIMILATION_LABIAL = assign_anusvara(ph.M, ph.LABIAL)
ANUSVARA_ASSIMILATION_DENTAL = assign_anusvara(ph.NI, ph.DENTAL)
ANUSVARA_ASSIMILATION_ALVEOLAR = assign_anusvara(ph.N, ph.ALVEOLAR)
ANUSVARA_ASSIMILATION_PALATAL = assign_anusvara(ph.NY, ph.PALATAL)
ANUSVARA_ASSIMILATION_RETROFLEX = assign_anusvara(ph.NN, ph.RETROFLEX)
ANUSVARA_ASSIMILATION_VELAR = assign_anusvara(ph.NG, ph.VELAR)
FINAL_ANUSVARA_NASALIZATION = rw.reassign_word_final(gr.ANS, ph.NASAL, ph.NSL)

# Composes anusvara assimilation for all places of articulation.
ANUSVARA_ASSIMILATION = (ANUSVARA_ASSIMILATION_LABIAL @
                         ANUSVARA_ASSIMILATION_DENTAL @
                         ANUSVARA_ASSIMILATION_ALVEOLAR @
                         ANUSVARA_ASSIMILATION_PALATAL @
                         ANUSVARA_ASSIMILATION_RETROFLEX @
                         ANUSVARA_ASSIMILATION_VELAR).optimize()

# JNY clusters


def rewrite_jny(
    j: pyn.FstLike,
    ny: pyn.FstLike) -> pyn.Fst:
  """Jny clusters are pronounced differently across languages."""
  return rw.reassign_adjacent_alignments(
      gr.J, ph.D_ZH, j,
      gr.NY, ph.NY, ny)

JNY_TO_GNY = rewrite_jny(ph.G, ph.NY)
JNY_TO_GY = rewrite_jny(ph.G, ph.Y)
JNY_TO_NY = rewrite_jny(ph.SIL, ph.NY)

# <ph><ph> pronounced {f}{f}. Should only occur in Perso-Arabic words.
# TODO: Move this when there is a Perso-Arabic module.
PHPH_TO_FF = rw.reassign_adjacent_alignments(
    gr.PH, ph.P + ph.ASP, ph.F,
    gr.PH, ph.P + ph.ASP, ph.F,)

RT_TO_R = rw.rewrite(ph.RT, ph.R)
