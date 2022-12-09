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

"""Romanization rules that depend on iso graphemes."""

import pynini as p
from nisaba.scripts.natural_translit.brahmic import iso_inventory as gr
from nisaba.scripts.natural_translit.common import rewrite_functions as rw
from nisaba.scripts.natural_translit.latin import ltn_inventory as tr
from nisaba.scripts.natural_translit.phonology import phoneme_inventory as ph
from nisaba.scripts.natural_translit.phonology import txn2ltn

## Rules to apply before txn to ltn mappings

# <v> is "w" after {s}, {ss}, and {sh}.
SIBV_TO_SIBW = rw.reassign_by_context(
    gr.V,
    ph.VU,
    tr.W,
    ph.SIBILANT)


# Palatal and velar assimilated anusvara is transliterated as "n".
_NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,
    p.union(ph.NG, ph.NY),
    tr.N)


def _transliterate_vocalic(vcl_tr: p.FstLike) -> p.Fst:
  """Transliterates all vowels in vocalics as vcl_tr."""
  return rw.rewrite_by_context(
      p.union(ph.VOWEL, ph.SYL),
      vcl_tr,
      gr.VOCALICS)

VOCALIC_TR_I = _transliterate_vocalic(tr.I)

# Word initial <aa> is "aa".
AA_WI = rw.reassign_word_initial(
    gr.AA_I,
    ph.A_L,
    tr.AA)

# Rules for two-letter geminates.
# PSAC uses the most reduced form in every contexts.
# NAT depends on language and context.
# TODO: Generalise and compress this rule set.

# <c><c> is "ch"
CC_TO_CH = rw.reduce_repetition(gr.C, tr.CH)

# <c><c> is "cch"
CC_TO_CCH = rw.reduce_repetition(gr.C, tr.CH, tr.C + tr.CH)

# <c><ch> is "ch"
CCH_TO_CH = rw.merge(
    gr.C, tr.CH,
    gr.CH, tr.CH + tr.H,
    tr.CH)

# <c><ch> is "chh"
CCH_TO_CHH = rw.merge(
    gr.C, tr.CH,
    gr.CH, tr.CH + tr.H,
    tr.CH + tr.H)

# <ss><ss> is "sh"
SSSS_TO_SH = rw.reduce_repetition(gr.SS, tr.SH)

# <ss><ss> is "ssh"
SSSS_TO_SSH = rw.reduce_repetition(gr.SS, tr.SH, tr.S + tr.SH)

# <ss><ss> is "sh"
SHSH_TO_SH = rw.reduce_repetition(gr.SH, tr.SH)

# <ss><ss> is "ssh"
SHSH_TO_SSH = rw.reduce_repetition(gr.SH, tr.SH, tr.S + tr.SH)

# Converts txn to PSAF and outputs only translit strings.

# Compose common rules for romanization
TXN_TO_PSA_COMMON = (
    _NON_LABIAL_ANUSVARA @
    txn2ltn.MAP_VOWEL_SHORT @
    txn2ltn.MAP_CONSONANT @
    txn2ltn.MAP_FEATURE
    ).optimize()


TXN_TO_PSAF = (
    TXN_TO_PSA_COMMON @
    txn2ltn.MAP_VOWEL_LONG @
    txn2ltn.STRIP
    ).optimize()

# Converts txn to PSAC and outputs only translit strings.
TXN_TO_PSAC = (TXN_TO_PSA_COMMON @
               txn2ltn.MAP_VOWEL_IGNORE_LENGTH @
               CC_TO_CH @
               CCH_TO_CH @
               SSSS_TO_SH @
               SHSH_TO_SH @
               txn2ltn.STRIP).optimize()
