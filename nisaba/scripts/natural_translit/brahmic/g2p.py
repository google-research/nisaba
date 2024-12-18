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

"""Brahmic g2p rules."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import grapheme_inventory as iso
from nisaba.scripts.natural_translit.brahmic import phoneme_inventory as psa
from nisaba.scripts.natural_translit.phonology.operations import syllable as syl
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import concat as cc
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw


TYP_TO_TXN = fl.FstList.make(
    al.assign, *[(char.gr, char.ph) for char in iso.CHAR]
).union_star()


def iso_to_txn() -> pyn.Fst:
  """ISO graphemes to txn pronunciation."""
  return iso.iso_to_typ_rules().add(TYP_TO_TXN).compose()


gr = iso.GRAPHEME_INVENTORY
ph = psa.PHONEME_INVENTORY

# Vowels

# TODO: Convert this constant to a function where duration and diphthong
# context are passed as arguments, and remove the recovery rule.
# The current rule rewrites all /a/ to /ə/ including the diphthongs like /ai/,
# and recovers long a with /ə:/ -> /a:/ but not the diphthongs.
A_TO_EC = (
    rw.rewrite(ph.A, ph.EC) @
    rw.rewrite(ph.EC + ph.DURH, ph.A + ph.DURH)
)
A_AE = rw.reassign(gr.A_I, ph.A, ph.AE)

# Ungliding: Diphthong to monophthong shift
AI_TO_EH_LONG = rw.rewrite(ph.A_I, ph.EH + ph.DURH)
AU_TO_OH_LONG = rw.rewrite(ph.A_U, ph.OH + ph.DURH)

# Vocalic liquids


def vocalic(vcl: pyn.FstLike, vcl_l: pyn.FstLike) -> pyn.Fst:
  """Pronunciation of the vowel part of the vocalic Rs and Ls."""
  return rw.rewrite(ph.SYL, vcl) @ rw.rewrite(ph.SYL + ph.DURH, vcl_l)

VOCALIC_I = vocalic(ph.I, ph.I + ph.DURH)
VOCALIC_U = vocalic(ph.U, ph.U + ph.DURH)
VOCALIC_EC = vocalic(ph.EC, ph.EC + ph.DURH)

# Schwa handling


def default_schwa(schwa: pyn.FstLike) -> pyn.Fst:
  """Pronounces unassigned schwas as the default phoneme for the language."""
  return rw.rewrite((ph.V_TNT | ph.V_PRN), schwa)

SCHWA_A = default_schwa(ph.A)
SCHWA_EC = default_schwa(ph.EC)
SCHWA_OH = default_schwa(ph.OH)


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
# Schwa is pronounced after {i}{y} and {i}{:h}{y}
_SCHWA_AFTER_IY = vocal_schwa(cc.concat_r((ph.I | (ph.I + ph.DURH)), ph.Y))


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


def assign_nasal(
    nasal: pyn.FstLike,
    phoneme: pyn.FstLike,
    place: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Pronunciation of anusvara.

  Anusvara is mapped to nasalisation by default. The pronunciation of it
  can change across languages and it can be assimilated to the place of
  articulation of the following phoneme.

  Args:
    nasal: Nasal diacritic to be assigned.
    phoneme: Pronuncation of <ans>.
    place: Following phoneme.

  Returns:
    Rewrite fst.

  Following call:
  ```
  assign_nasal(ph.M, ph.LABIAL)
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
      nasal,
      ph.NSL,
      phoneme,
      following=place)

DEFAULT_ANUSVARA_LABIAL = assign_nasal(gr.ANS, ph.M)
DEFAULT_ANUSVARA_DENTAL = assign_nasal(gr.ANS, ph.NI)
DEFAULT_ANUSVARA_VELAR = assign_nasal(gr.ANS, ph.NG)
FINAL_ANUSVARA_NASALIZATION = rw.reassign_word_final(gr.ANS, ph.NASAL, ph.NSL)

# Composes anusvara assimilation for all places of articulation.
ANUSVARA_ASSIMILATION = (assign_nasal(gr.ANS, ph.M, ph.LABIAL) @
                         assign_nasal(gr.ANS, ph.NI, ph.DENTAL) @
                         assign_nasal(gr.ANS, ph.NY, ph.ALVEOLAR) @
                         assign_nasal(gr.ANS, ph.NY, ph.PALATAL) @
                         assign_nasal(gr.ANS, ph.NN, ph.RETROFLEX) @
                         assign_nasal(gr.ANS, ph.NG, ph.VELAR)).optimize()

TIPPI_ASSIMILATION = (assign_nasal(gr.TIP, ph.M, ph.LABIAL) @
                      assign_nasal(gr.TIP, ph.NI, ph.DENTAL) @
                      assign_nasal(gr.TIP, ph.NY, ph.ALVEOLAR) @
                      assign_nasal(gr.TIP, ph.NY, ph.PALATAL) @
                      assign_nasal(gr.TIP, ph.NN, ph.RETROFLEX) @
                      assign_nasal(gr.TIP, ph.NG, ph.VELAR)).optimize()


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
JNY_TO_DNY = rewrite_jny(ph.DI, ph.NY)
JNY_TO_GG = rewrite_jny(ph.G, ph.G)

YY_Y = rw.delete(ph.ASP, gr.YY)
OOYY_V = (
    rw.merge(gr.OO_I, ph.O + ph.DURH, gr.YY, ph.Y, ph.VU)
    @ rw.reassign(gr.A, ph.OH, ph.SIL, following=gr.OO_I + gr.YY)
)

PH_F = rw.reassign(gr.PH, ph.P + ph.ASP, ph.F)
BH_V = rw.reassign(gr.BH, ph.B + ph.ASP, ph.VU, ph.ALL)
B_V = rw.reassign(gr.B, ph.B, ph.VU, ph.CONSONANT)

# <ph><ph> pronounced {f}{f}. Should only occur in Perso-Arabic words.
# TODO: Move this when there is a Perso-Arabic module.
PHPH_TO_FF = rw.reassign_adjacent_alignments(
    gr.PH, ph.P + ph.ASP, ph.F,
    gr.PH, ph.P + ph.ASP, ph.F,)
REMOVE_ASP_FROM_GEMINATE = rw.delete(ph.ASP, following=(ph.ALL + ph.ASP))

RT_TO_R = rw.rewrite(ph.RT, ph.R)

RR_TT = rw.merge_repeated_alignment(gr.RR, ph.R, ph.T + ph.T)
NR_NDR = rw.merge(gr.NA, ph.N, gr.RR, ph.R, ph.N + ph.D + ph.R)
WF_VIRAMA_U = rw.rewrite_word_final(
    al.EPSILON, al.align(gr.U, ph.U), al.align(gr.SCH_CONS, ph.ALL.star))

H_ASP = rw.reassign(
    gr.H, ph.H, ph.ASP, (ph.M | ph.NI | ph.VU | ph.L | ph.R)
)

ADDAK = rw.rewrite_ls(
    [(char.ph, char.ph + char.ph) for char in iso.ONSET_CONSONANT], ph.SIL
)

AUM_AON = rw.reassign(gr.U_I, ph.U, ph.O, following=(gr.ANS + al.SKIP + al.EOW))
OAM_AON = rw.merge(
    gr.OO, ph.O + ph.DURH, gr.AA_I, ph.A + ph.DURH,
    ph.EC + ph.O,
    following=(gr.ANS + al.SKIP + al.EOW)
)
ANSVA_AON = rw.merge(
    gr.ANS, ph.NSL, gr.V, ph.VU, ph.O + ph.NSL,
    following=(gr.A + al.SKIP + al.EOW)
)
