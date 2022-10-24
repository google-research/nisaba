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

"""Pan-South Asian natural romanization."""

import pynini as p
import nisaba.scripts.brahmic.natural_translit.grapheme_inventory as gr
import nisaba.scripts.brahmic.natural_translit.phoneme_inventory as ph
import nisaba.scripts.brahmic.natural_translit.rewrite_functions as rw
import nisaba.scripts.brahmic.natural_translit.transliteration_inventory as tr
import nisaba.scripts.brahmic.natural_translit.util as u

STRIP = rw.strip_right_side(u.TR_BOUND)

## Natural translit rules that take phonemes as arguments

# <v> is "w" after {s}, {ss}, and {sh}.
SIBV_TO_SIBW = rw.reassign_by_context(
    gr.V,
    ph.VU,
    tr.W,
    ph.SIBILANT)


## Pan South Asian Rules

# Palatal and velar assimilated anusvara is transliterated as "n".
_NON_LABIAL_ANUSVARA = rw.reassign(
    gr.ANS,
    p.union(ph.NG, ph.NY),
    tr.N)


def _transliterate_vocalic(vcl_tr: p.FstLike) -> p.Fst:
  """Transliterates all vowels in vocalics as vcl_tr."""
  return rw.rewrite_by_context(
      p.union(ph.VOWEL, ph.VCL),
      vcl_tr,
      gr.VOCALICS)

VOCALIC_TR_I = _transliterate_vocalic(tr.I)

# txn to Pan South Asian translit mapping.
_TXN_TO_PSA = p.union(
    p.cross(ph.A, tr.A),
    p.cross(ph.A_L, tr.AA),
    p.cross(ph.AE, tr.AE),
    p.cross(ph.B, tr.B),
    p.cross(ph.CH, tr.CH),
    p.cross(ph.DD, tr.D),
    p.cross(ph.DI, tr.D),
    p.cross(ph.E, tr.E),
    p.cross(ph.E_L, tr.EE),
    p.cross(ph.EC, tr.A),
    p.cross(ph.F, tr.F),
    p.cross(ph.G, tr.G),
    p.cross(ph.H, tr.H),
    p.cross(ph.I, tr.I),
    p.cross(ph.I_L, tr.II),
    p.cross(ph.JH, tr.J),
    p.cross(ph.K, tr.K),
    p.cross(ph.L, tr.L),
    p.cross(ph.LL, tr.L),
    p.cross(ph.M, tr.M),
    p.cross(ph.N, tr.N),
    p.cross(ph.NG, tr.NG),
    p.cross(ph.NI, tr.N),
    p.cross(ph.NN, tr.N),
    p.cross(ph.NY, tr.NY),
    p.cross(ph.O, tr.O),
    p.cross(ph.O_L, tr.OO),
    p.cross(ph.P, tr.P),
    p.cross(ph.Q, tr.K),
    p.cross(ph.R, tr.R),
    p.cross(ph.RRT, tr.RD),
    p.cross(ph.RRU, tr.ZH),
    p.cross(ph.RT, tr.R),
    p.cross(ph.S, tr.S),
    p.cross(ph.SH, tr.SH),
    p.cross(ph.SS, tr.SH),
    p.cross(ph.T, tr.T),
    p.cross(ph.TI, tr.T),
    p.cross(ph.TT, tr.T),
    p.cross(ph.U, tr.U),
    p.cross(ph.U_L, tr.UU),
    p.cross(ph.VU, tr.V),
    p.cross(ph.X, tr.KH),
    p.cross(ph.XA, tr.G),
    p.cross(ph.Y, tr.Y),
    p.cross(ph.Z, tr.Z),
    p.cross(ph.ASP, tr.H),
    p.cross(ph.NSL, tr.N),
    p.cross(ph.SIL, tr.DEL),
    p.cross(ph.SCHWA, tr.DEL),
    p.cross(ph.VCL, tr.I)
    ).optimize()

MAP_TO_PSA = (_NON_LABIAL_ANUSVARA @
              rw.rewrite_operation(_TXN_TO_PSA)
              ).optimize()

# Converts txn to PSAF and outputs only translit strings.
TXN_TO_PSAF = (MAP_TO_PSA @ STRIP).optimize()

## Post PSA-mapping rules for PSAC and natural translit.

# Long vowels are transliterated as their short counterparts.
CONFLATE_LONG_VOWEL_OP = p.union(
    p.cross(tr.AA, tr.A),
    p.cross(tr.EE, tr.E),
    p.cross(tr.II, tr.I),
    p.cross(tr.OO, tr.O),
    p.cross(tr.UU, tr.U)
    ).optimize()

CONFLATE_LONG_VOWEL = rw.rewrite_operation(CONFLATE_LONG_VOWEL_OP)

# Word initial <aa> is "aa".
# Apply after long vowel conflation to prevent overwriting.
AA_WI = rw.reassign_word_initial(
    gr.AA,
    tr.A,
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


# Converts txn to PSAC and outputs only translit strings.
TXN_TO_PSAC = (MAP_TO_PSA @
               CONFLATE_LONG_VOWEL @
               CC_TO_CH @
               CCH_TO_CH @
               SSSS_TO_SH @
               SHSH_TO_SH @
               STRIP).optimize()
