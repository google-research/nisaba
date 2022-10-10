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


def _anusvara_assimilation_labial() -> p.Fst:
  """Anusvara assimilates to {m} before labials."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.M,
      following=ph.LABIAL)

ANUSVARA_ASSIMILATION_LABIAL = _anusvara_assimilation_labial()


def _anusvara_assimilation_dental() -> p.Fst:
  """Anusvara assimilates to {ni} before dentals."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.NI,
      following=ph.DENTAL)

ANUSVARA_ASSIMILATION_DENTAL = _anusvara_assimilation_dental()


def _anusvara_assimilation_alveolar() -> p.Fst:
  """Anusvara assimilates to {n} before alveolars."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.N,
      following=ph.ALVEOLAR)

ANUSVARA_ASSIMILATION_ALVEOLAR = _anusvara_assimilation_alveolar()


def _anusvara_assimilation_palatal() -> p.Fst:
  """Anusvara assimilates to {ny} before palatals."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.NY,
      following=ph.PALATAL)

ANUSVARA_ASSIMILATION_PALATAL = _anusvara_assimilation_palatal()


def _anusvara_assimilation_retroflex() -> p.Fst:
  """Anusvara assimilates to {nn} before retroflexes."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.NN,
      following=ph.RETROFLEX)

ANUSVARA_ASSIMILATION_RETROFLEX = _anusvara_assimilation_retroflex()


def _anusvara_assimilation_velar() -> p.Fst:
  """Anusvara assimilates to {ng} before velars."""
  return rw.reassign_by_context(
      gr.ANS,
      ph.NSL,
      ph.NG,
      following=ph.VELAR)

ANUSVARA_ASSIMILATION_VELAR = _anusvara_assimilation_velar()


def _anusvara_assimilation() -> p.Fst:
  """Composes all anusvara place assimilations."""
  return (ANUSVARA_ASSIMILATION_LABIAL @
          ANUSVARA_ASSIMILATION_DENTAL @
          ANUSVARA_ASSIMILATION_ALVEOLAR @
          ANUSVARA_ASSIMILATION_PALATAL @
          ANUSVARA_ASSIMILATION_RETROFLEX @
          ANUSVARA_ASSIMILATION_VELAR).optimize()

ANUSVARA_ASSIMILATION = _anusvara_assimilation()


def _default_anusvara_dental() -> p.Fst:
  """Unassimilated anusvara defaults to n."""
  return rw.reassign(gr.ANS, ph.NSL, ph.NI)

DEFAULT_ANUSVARA_DENTAL = _default_anusvara_dental()


def _default_anusvara_labial() -> p.Fst:
  """Unassimilated anusvara defaults to m."""
  return rw.reassign(gr.ANS, ph.NSL, ph.M)

DEFAULT_ANUSVARA_LABIAL = _default_anusvara_labial()


def _final_anusvara_nasalization() -> p.Fst:
  """Word final anusvara nasalizes the preceding vowel."""
  return rw.reassign_word_final(gr.ANS, ph.NASAL, ph.NSL)

FINAL_ANUSVARA_NASALIZATION = _final_anusvara_nasalization()

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


def _jny_to_gny() -> p.Fst:
  """jny pronounced as gny."""
  return rw.rewrite(
      u.align(gr.J, ph.JH) + u.align(gr.NY, ph.NY),
      u.align(gr.J, ph.G) + u.align(gr.NY, ph.NY))

JNY_TO_GNY = _jny_to_gny()


def _jny_to_gy() -> p.Fst:
  """jny pronounced as gy."""
  return rw.rewrite(
      u.align(gr.J, ph.JH) + u.align(gr.NY, ph.NY),
      u.align(gr.J, ph.G) + u.align(gr.NY, ph.Y))

JNY_TO_GY = _jny_to_gy()


def _jny_to_ny() -> p.Fst:
  """jny pronounced as ny."""
  return rw.rewrite(
      u.align(gr.J, ph.JH) + u.align(gr.NY, ph.NY),
      u.align(gr.J, ph.SIL) + u.align(gr.NY, ph.NY))

JNY_TO_NY = _jny_to_ny()
