# Copyright 2026 Nisaba Authors.
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
    rw.rewrite(ph.A, ph.EC) @  # pyrefly: ignore[missing-attribute]
    rw.rewrite(ph.EC + ph.DURH, ph.A + ph.DURH)  # pyrefly: ignore[missing-attribute]
)
A_AE = rw.reassign(gr.A_I, ph.A, ph.AE)  # pyrefly: ignore[missing-attribute]

# Ungliding: Diphthong to monophthong shift
AI_TO_EH_LONG = rw.rewrite(ph.A_I, ph.EH + ph.DURH)  # pyrefly: ignore[missing-attribute]
AU_TO_OH_LONG = rw.rewrite(ph.A_U, ph.OH + ph.DURH)  # pyrefly: ignore[missing-attribute]

# Vocalic liquids


def vocalic(vcl: pyn.FstLike, vcl_l: pyn.FstLike) -> pyn.Fst:
  """Pronunciation of the vowel part of the vocalic Rs and Ls."""
  return rw.rewrite(ph.SYL, vcl) @ rw.rewrite(ph.SYL + ph.DURH, vcl_l)  # pyrefly: ignore[missing-attribute]

VOCALIC_I = vocalic(ph.I, ph.I + ph.DURH)  # pyrefly: ignore[missing-attribute]
VOCALIC_U = vocalic(ph.U, ph.U + ph.DURH)  # pyrefly: ignore[missing-attribute]
VOCALIC_EC = vocalic(ph.EC, ph.EC + ph.DURH)  # pyrefly: ignore[missing-attribute]

# Schwa handling


def default_schwa(schwa: pyn.FstLike) -> pyn.Fst:
  """Pronounces unassigned schwas as the default phoneme for the language."""
  return rw.rewrite((ph.V_TNT | ph.V_PRN), schwa)  # pyrefly: ignore[missing-attribute]

SCHWA_A = default_schwa(ph.A)  # pyrefly: ignore[missing-attribute]
SCHWA_EC = default_schwa(ph.EC)  # pyrefly: ignore[missing-attribute]
SCHWA_OH = default_schwa(ph.OH)  # pyrefly: ignore[missing-attribute]


def vocal_schwa(
    preceding: pyn.FstLike = al.EPSILON,
    following: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Pronounces schwa depending on the context."""

  return rw.rewrite(
      ph.V_TNT,  # pyrefly: ignore[missing-attribute]
      ph.V_PRN,  # pyrefly: ignore[missing-attribute]
      preceding,
      following)


def silent_schwa(
    preceding: pyn.FstLike = al.EPSILON,
    following: pyn.FstLike = al.EPSILON) -> pyn.Fst:
  """Deletes schwa depending on the context."""

  return rw.rewrite(
      ph.V_TNT,  # pyrefly: ignore[missing-attribute]
      ph.SIL,  # pyrefly: ignore[missing-attribute]
      preceding,
      following)

# Schwa is pronounced before coda graphemes
_SCHWA_BEFORE_CODA = vocal_schwa(following=gr.CODA)  # pyrefly: ignore[missing-attribute]
_SCHWA_BEFORE_IND_VOWEL = vocal_schwa(following=gr.VOWEL_I)  # pyrefly: ignore[missing-attribute]
# Schwa is pronounced after {i}{y} and {i}{:h}{y}
_SCHWA_AFTER_IY = vocal_schwa(cc.concat_r((ph.I | (ph.I + ph.DURH)), ph.Y))  # pyrefly: ignore[missing-attribute]


def schwa_eow(coda_cl) -> pyn.Fst:
  """Deletes the word final schwa if it's preceded by a legal coda."""
  return silent_schwa(
      syl.legal_coda(ph.VOWEL, ph.CONSONANT, coda_cl),  # pyrefly: ignore[missing-attribute]
      al.EOS)


def schwa_between_syllables(onset_cl, coda_cl) -> pyn.Fst:
  """Deletes schwa between two well-formed syllables."""
  return silent_schwa(
      syl.legal_coda(ph.VOWEL, ph.CONSONANT, coda_cl),  # pyrefly: ignore[missing-attribute]
      syl.legal_onset(ph.VOWEL, ph.CONSONANT, onset_cl))  # pyrefly: ignore[missing-attribute]


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
      ph.NSL,  # pyrefly: ignore[missing-attribute]
      phoneme,
      following=place)

DEFAULT_ANUSVARA_LABIAL = assign_nasal(gr.ANS, ph.M)  # pyrefly: ignore[missing-attribute]
DEFAULT_ANUSVARA_DENTAL = assign_nasal(gr.ANS, ph.NI)  # pyrefly: ignore[missing-attribute]
DEFAULT_ANUSVARA_VELAR = assign_nasal(gr.ANS, ph.NG)  # pyrefly: ignore[missing-attribute]
FINAL_ANUSVARA_NASALIZATION = rw.reassign_word_final(gr.ANS, ph.NASAL, ph.NSL)  # pyrefly: ignore[missing-attribute]

# Composes anusvara assimilation for all places of articulation.
ANUSVARA_ASSIMILATION = (assign_nasal(gr.ANS, ph.M, ph.LABIAL) @  # pyrefly: ignore[missing-attribute]
                         assign_nasal(gr.ANS, ph.NI, ph.DENTAL) @  # pyrefly: ignore[missing-attribute]
                         assign_nasal(gr.ANS, ph.NY, ph.ALVEOLAR) @  # pyrefly: ignore[missing-attribute]
                         assign_nasal(gr.ANS, ph.NY, ph.PALATAL) @  # pyrefly: ignore[missing-attribute]
                         assign_nasal(gr.ANS, ph.NN, ph.RETROFLEX) @  # pyrefly: ignore[missing-attribute]
                         assign_nasal(gr.ANS, ph.NG, ph.VELAR)).optimize()  # pyrefly: ignore[missing-attribute]

TIPPI_ASSIMILATION = (assign_nasal(gr.TIP, ph.M, ph.LABIAL) @  # pyrefly: ignore[missing-attribute]
                      assign_nasal(gr.TIP, ph.NI, ph.DENTAL) @  # pyrefly: ignore[missing-attribute]
                      assign_nasal(gr.TIP, ph.NY, ph.ALVEOLAR) @  # pyrefly: ignore[missing-attribute]
                      assign_nasal(gr.TIP, ph.NY, ph.PALATAL) @  # pyrefly: ignore[missing-attribute]
                      assign_nasal(gr.TIP, ph.NN, ph.RETROFLEX) @  # pyrefly: ignore[missing-attribute]
                      assign_nasal(gr.TIP, ph.NG, ph.VELAR)).optimize()  # pyrefly: ignore[missing-attribute]


# JNY clusters


def rewrite_jny(
    j: pyn.FstLike,
    ny: pyn.FstLike) -> pyn.Fst:
  """Jny clusters are pronounced differently across languages."""
  return rw.reassign_adjacent_alignments(
      gr.J, ph.D_ZH, j,  # pyrefly: ignore[missing-attribute]
      gr.NY, ph.NY, ny)  # pyrefly: ignore[missing-attribute]

JNY_TO_GNY = rewrite_jny(ph.G, ph.NY)  # pyrefly: ignore[missing-attribute]
JNY_TO_GY = rewrite_jny(ph.G, ph.Y)  # pyrefly: ignore[missing-attribute]
JNY_TO_NY = rewrite_jny(ph.SIL, ph.NY)  # pyrefly: ignore[missing-attribute]
JNY_TO_DNY = rewrite_jny(ph.DI, ph.NY)  # pyrefly: ignore[missing-attribute]
JNY_TO_GG = rewrite_jny(ph.G, ph.G)  # pyrefly: ignore[missing-attribute]

YY_Y = rw.delete(ph.ASP, gr.YY)  # pyrefly: ignore[missing-attribute]
OOYY_V = (
    rw.merge(gr.OO_I, ph.O + ph.DURH, gr.YY, ph.Y, ph.VU)  # pyrefly: ignore[missing-attribute]
    @ rw.reassign(gr.A, ph.OH, ph.SIL, following=gr.OO_I + gr.YY)  # pyrefly: ignore[missing-attribute]
)

PH_F = rw.reassign(gr.PH, ph.P + ph.ASP, ph.F)  # pyrefly: ignore[missing-attribute]
BH_V = rw.reassign(gr.BH, ph.B + ph.ASP, ph.VU, ph.ALL)  # pyrefly: ignore[missing-attribute]
B_V = rw.reassign(gr.B, ph.B, ph.VU, ph.CONSONANT)  # pyrefly: ignore[missing-attribute]

# <ph><ph> pronounced {f}{f}. Should only occur in Perso-Arabic words.
# TODO: Move this when there is a Perso-Arabic module.
PHPH_TO_FF = rw.reassign_adjacent_alignments(
    gr.PH, ph.P + ph.ASP, ph.F,  # pyrefly: ignore[missing-attribute]
    gr.PH, ph.P + ph.ASP, ph.F,)  # pyrefly: ignore[missing-attribute]
REMOVE_ASP_FROM_GEMINATE = rw.delete(ph.ASP, following=(ph.ALL + ph.ASP))  # pyrefly: ignore[missing-attribute]

RT_TO_R = rw.rewrite(ph.RT, ph.R)  # pyrefly: ignore[missing-attribute]

RR_TT = rw.merge_repeated_alignment(gr.RR, ph.R, ph.T + ph.T)  # pyrefly: ignore[missing-attribute]
NR_NDR = rw.merge(gr.NA, ph.N, gr.RR, ph.R, ph.N + ph.D + ph.R)  # pyrefly: ignore[missing-attribute]
WF_VIRAMA_U = rw.rewrite_word_final(
    al.EPSILON, al.align(gr.U, ph.U), al.align(gr.SCH_CONS, ph.ALL.star))  # pyrefly: ignore[missing-attribute]

H_ASP = rw.reassign(
    gr.H, ph.H, ph.ASP, (ph.M | ph.NI | ph.VU | ph.L | ph.R)  # pyrefly: ignore[missing-attribute]
)

ADDAK = rw.rewrite_ls(
    [(char.ph, char.ph + char.ph) for char in iso.ONSET_CONSONANT], ph.SIL  # pyrefly: ignore[missing-attribute]
)

AUM_AON = rw.reassign(gr.U_I, ph.U, ph.O, following=(gr.ANS + al.SKIP + al.EOW))  # pyrefly: ignore[missing-attribute]
OAM_AON = rw.merge(
    gr.OO, ph.O + ph.DURH, gr.AA_I, ph.A + ph.DURH,  # pyrefly: ignore[missing-attribute]
    ph.EC + ph.O,  # pyrefly: ignore[missing-attribute]
    following=(gr.ANS + al.SKIP + al.EOW)  # pyrefly: ignore[missing-attribute]
)
ANSVA_AON = rw.merge(
    gr.ANS, ph.NSL, gr.V, ph.VU, ph.O + ph.NSL,  # pyrefly: ignore[missing-attribute]
    following=(gr.A + al.SKIP + al.EOW)  # pyrefly: ignore[missing-attribute]
)
