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

"""Pan South Asian phoneme inventory."""

import pynini as pyn
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import feature
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.phonology import phoneme_inventory
from nisaba.scripts.natural_translit.utils import type_op as ty

f = feature.FEATURE_INVENTORY
ph = phoneme_inventory.PHON_INVENTORY
mod = phoneme_inventory.MOD_INVENTORY
tr = ltn.TRANSLIT_INVENTORY


def _import_to_psa(
    phon: p.Phon,
    psa: ty.FstIterable = ty.UNSPECIFIED,
) -> p.Phon:
  """Import Phons and add Pan South Asian translits."""
  # Check phon class to set the default translit.
  if isinstance(psa, pyn.Fst):
    psa_tr = psa
  elif f.affricate in phon.ftr:  # pyrefly: ignore[missing-attribute]
    psa_tr = phon.tr_dict[f.affricate]
  elif f.diphthong in phon.ftr:  # pyrefly: ignore[missing-attribute]
    psa_tr = phon.tr_dict[f.diphthong]
  else:
    psa_tr = phon.tr_dict['base']
  return p.import_phon(phon, alt_tr_dict={'psa': psa_tr})

SILENCE = [_import_to_psa(ph.SIL)]  # pyrefly: ignore[missing-attribute]

VOWEL_MOD = [
    _import_to_psa(phon) for phon in [ph.NSY, ph.NSL, mod.DURH]  # pyrefly: ignore[missing-attribute]
]

CONS_MOD = [_import_to_psa(ph.ASP)]  # pyrefly: ignore[missing-attribute]

VOWEL = [_import_to_psa(*args) for args in [
    [ph.V_TNT], [ph.V_PRN], [ph.SYL, tr.I],  # pyrefly: ignore[missing-attribute]
    [ph.A], [ph.AE, tr.S_AE],  # pyrefly: ignore[missing-attribute]
    [ph.E], [ph.EC, tr.A], [ph.EH],  # pyrefly: ignore[missing-attribute]
    [ph.I], [ph.O], [ph.OH], [ph.U],  # pyrefly: ignore[missing-attribute]
    [ph.A_I], [ph.A_U],  # pyrefly: ignore[missing-attribute]
]]

NASAL = [
    _import_to_psa(phon) for phon in [ph.M, ph.NI, ph.N, ph.NN, ph.NY, ph.NG]  # pyrefly: ignore[missing-attribute]
]

VOICELESS_STOP = [
    _import_to_psa(phon) for phon in [ph.P, ph.TI, ph.T, ph.TT, ph.K, ph.Q]  # pyrefly: ignore[missing-attribute]
]

VOICED_STOP = [
    _import_to_psa(phon) for phon in [ph.B, ph.DI, ph.D, ph.DD, ph.G]  # pyrefly: ignore[missing-attribute]
]

VOICELESS_FRICATIVE = [_import_to_psa(*args) for args in [
    [ph.F], [ph.S], [ph.SH], [ph.SS], [ph.KH, tr.S_KH], [ph.H],  # pyrefly: ignore[missing-attribute]
]]

VOICED_FRICATIVE = [_import_to_psa(*args) for args in [
    [ph.Z], [ph.ZH], [ph.GH, tr.G],  # pyrefly: ignore[missing-attribute]
]]

VOICELESS_AFFRICATE = [_import_to_psa(ph.T_SH)]  # pyrefly: ignore[missing-attribute]

VOICED_AFFRICATE = [_import_to_psa(ph.D_ZH)]  # pyrefly: ignore[missing-attribute]

APPROXIMANT = [_import_to_psa(*args) for args in [
    [ph.VU], [ph.RRU, tr.S_ZH], [ph.Y], [ph.L], [ph.LL],  # pyrefly: ignore[missing-attribute]
]]

TAP_TRILL = [_import_to_psa(phon) for phon in [ph.R, ph.RT, ph.RD]]  # pyrefly: ignore[missing-attribute]

CONSONANT = (
    NASAL + VOICELESS_STOP + VOICED_STOP +
    VOICELESS_FRICATIVE + VOICED_FRICATIVE +
    VOICELESS_AFFRICATE + VOICED_AFFRICATE +
    APPROXIMANT + TAP_TRILL
)

PHONEMES = SILENCE + VOWEL_MOD + CONS_MOD + VOWEL + CONSONANT
PH = p.phon_inventory(PHONEMES)

PH_STORE = [p.thing_ph_union(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['NASAL', NASAL],
    ['FRICATIVE', VOICELESS_FRICATIVE + VOICED_FRICATIVE],
    ['VOICED', VOICED_STOP + VOICED_FRICATIVE + VOICED_AFFRICATE],
    ['APPROXIMANT', APPROXIMANT],
    ['RHOTIC', TAP_TRILL + [PH.RRU]],  # pyrefly: ignore[missing-attribute]
    ['LIQUID', TAP_TRILL + [PH.RRU, PH.L, PH.LL]],  # pyrefly: ignore[missing-attribute]
    ['SIBILANT', [PH.S, PH.Z, PH.SH, PH.ZH, PH.SS]],  # pyrefly: ignore[missing-attribute]
    ['LABIAL', [PH.M, PH.B, PH.P]],  # pyrefly: ignore[missing-attribute]
    ['DENTAL', [PH.NI, PH.DI, PH.TI]],  # pyrefly: ignore[missing-attribute]
    ['ALVEOLAR', [PH.N, PH.D, PH.T]],  # pyrefly: ignore[missing-attribute]
    ['PALATAL', [PH.NY, PH.Y]],  # pyrefly: ignore[missing-attribute]
    ['RETROFLEX', [PH.NN, PH.DD, PH.TT]],  # pyrefly: ignore[missing-attribute]
    ['VELAR', [PH.NG, PH.G, PH.K]],  # pyrefly: ignore[missing-attribute]
]]

PH_MOD_STORE = [p.thing_ph_modified(*args) for args in [  # pyrefly: ignore[bad-argument-type]
    ['VOWEL', VOWEL, VOWEL_MOD],
    ['STOP', VOICELESS_STOP + VOICED_STOP, CONS_MOD],
    ['AFFRICATE', VOICELESS_AFFRICATE + VOICED_AFFRICATE, CONS_MOD],
    ['CONSONANT', CONSONANT, CONS_MOD],
]]

PH_ALL_STORE = p.thing_ph_union('ALL', PHONEMES)

PHONEME_INVENTORY = p.ph_inventory(
    PHONEMES,
    PH_STORE + PH_MOD_STORE + [PH_ALL_STORE],
)
