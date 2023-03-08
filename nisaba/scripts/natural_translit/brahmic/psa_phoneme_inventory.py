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

"""Pan South Asian phoneme inventory."""

from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.phonology import phoneme_inventory
from nisaba.scripts.natural_translit.utils import list_op as ls

ph = phoneme_inventory.PHON_INVENTORY
tr = ltn.TRANSLIT_INVENTORY


def _import_to_psa(
    phon: p.Phon,
    psaf: str = None,
    psac: str = None
) -> p.Phon:
  """Import Phons and add Pan South Asian translits."""
  # Check phon class to set the default translit.
  if 'affr' in phon.ftr:
    psa = phon.tr_dict['affr']
  elif 'diph' in phon.ftr:
    psa = phon.tr_dict['diph']
  else:
    psa = phon.tr_dict['base']
  psa_dict = {}
  # If psaf is set, psac defaults to psaf
  if psaf:
    psa_dict.update({'psaf': psaf})
    psa = psaf
  else:
    if 'vowel' in phon.ftr and 'long' in phon.ftr:
      psa_dict.update({'psaf': phon.tr_dict['long']})
    else:
      psa_dict.update({'psaf': psa})
  psa_dict.update(p.new_tr('psac', psac, psa))
  return p.import_phon(phon, alt_tr_dict=psa_dict)

SILENCE = [_import_to_psa(ph.SIL)]

VOWEL_MOD = ls.apply_foreach(_import_to_psa, (
    [ph.GLD], [ph.NSL]
))

CONS_MOD = [_import_to_psa(ph.ASP)]

VOWEL = ls.apply_foreach(_import_to_psa, [
    [ph.V_TNT], [ph.V_PRN],
    [ph.SYL, tr.I], [ph.SYL_L, tr.I],
    [ph.A], [ph.A_L],
    [ph.AE, tr.S_AE],
    [ph.E], [ph.E_L],
    [ph.EC, tr.A], [ph.EC_L, tr.S_AA, tr.A],
    [ph.EH], [ph.EH_L],
    [ph.I], [ph.I_L],
    [ph.O], [ph.O_L],
    [ph.OH], [ph.OH_L],
    [ph.U], [ph.U_L],
    [ph.A_I], [ph.A_U],
])

NASAL = ls.apply_foreach(_import_to_psa, [
    [ph.M], [ph.NI], [ph.N], [ph.NN], [ph.NY], [ph.NG],
])

VOICELESS_STOP = ls.apply_foreach(_import_to_psa, [
    [ph.P], [ph.TI], [ph.T], [ph.TT], [ph.K], [ph.Q],
])

VOICED_STOP = ls.apply_foreach(_import_to_psa, [
    [ph.B], [ph.DI], [ph.D], [ph.DD], [ph.G],
])

VOICELESS_FRICATIVE = ls.apply_foreach(_import_to_psa, [
    [ph.F], [ph.S], [ph.SH], [ph.SS], [ph.KH, tr.S_KH], [ph.H],
])

VOICED_FRICATIVE = ls.apply_foreach(_import_to_psa, [
    [ph.Z], [ph.ZH], [ph.GH, tr.G],
])

VOICELESS_AFFRICATE = [_import_to_psa(ph.T_SH)]

VOICED_AFFRICATE = [_import_to_psa(ph.D_ZH)]

APPROXIMANT = ls.apply_foreach(_import_to_psa, [
    [ph.VU], [ph.RRU, tr.S_ZH], [ph.Y], [ph.L], [ph.LL],
])

TAP_TRILL = ls.apply_foreach(_import_to_psa, [
    [ph.R], [ph.RT], [ph.RD],
])

CONSONANT = (
    NASAL + VOICELESS_STOP + VOICED_STOP +
    VOICELESS_FRICATIVE + VOICED_FRICATIVE +
    VOICELESS_AFFRICATE + VOICED_AFFRICATE +
    APPROXIMANT + TAP_TRILL
)

PHONEMES = SILENCE + VOWEL_MOD + CONS_MOD + VOWEL + CONSONANT
_ph = p.phon_inventory(PHONEMES)

PH_STORE = ls.apply_foreach(p.store_ph_union, [
    ['NASAL', NASAL],
    ['FRICATIVE', VOICELESS_FRICATIVE + VOICED_FRICATIVE],
    ['VOICED', VOICED_STOP + VOICED_FRICATIVE + VOICED_AFFRICATE],
    ['APPROXIMANT', APPROXIMANT],
    ['RHOTIC', TAP_TRILL + [_ph.RRU]],
    ['LIQUID', TAP_TRILL + [_ph.RRU, _ph.L, _ph.LL]],
    ['SIBILANT', [_ph.S, _ph.Z, _ph.SH, _ph.ZH, _ph.SS]],
    ['LABIAL', [_ph.M, _ph.B, _ph.P]],
    ['DENTAL', [_ph.NI, _ph.DI, _ph.TI]],
    ['ALVEOLAR', [_ph.N, _ph.D, _ph.T]],
    ['PALATAL', [_ph.NY, _ph.Y]],
    ['RETROFLEX', [_ph.NN, _ph.DD, _ph.TT]],
    ['VELAR', [_ph.NG, _ph.G, _ph.K]],
])

PH_MOD_STORE = ls.apply_foreach(p.store_ph_modified, [
    ['VOWEL', VOWEL, VOWEL_MOD],
    ['STOP', VOICELESS_STOP + VOICED_STOP, CONS_MOD],
    ['AFFRICATE', VOICELESS_AFFRICATE + VOICED_AFFRICATE, CONS_MOD],
    ['CONSONANT', CONSONANT, CONS_MOD],
])

PHONEME_INVENTORY = p.ph_inventory(
    PHONEMES,
    PH_STORE + PH_MOD_STORE
)
