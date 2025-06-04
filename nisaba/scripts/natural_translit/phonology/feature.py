# Copyright 2025 Nisaba Authors.
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

"""Simple placeholder for the phonological feature structure."""

from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import type_op as ty


class PhonFeature(ty.Thing):
  """Phonological feature."""

  def __init__(self, alias: str, category: str):
    super().__init__(alias, alias)
    self.category = category


def ft_inventory(
    feature_list: list[PhonFeature],
    suppl_list: ty.ListOrNothing = ty.UNSPECIFIED,
) -> i.Inventory:
  return i.Inventory.from_list(feature_list, attr='alias', suppls=suppl_list)

# TODO:Enum features by category
ARTICULATION_FEATURE = [PhonFeature(alias, cat) for alias, cat in [
    ['silent', 'pronunciation'],
    ['syllabic', 'syllabicity'],
    ['nonsyllabic', 'syllabicity'],
    ['pulmonic', 'airstream'],
    ['nonpulmonic', 'airstream'],
    ['central', 'airflow'],
    ['lateral', 'airflow'],
    ['nasal', 'airflow'],
    ['aspirated', 'release'],
    ['click', 'release'],
    ['labial', 'place'],
    ['nonlabial', 'place'],
    ['bilabial', 'place'],
    ['labiodental', 'place'],
    ['dental', 'place'],
    ['alveolar', 'place'],
    ['postalveolar', 'place'],
    ['palatal', 'place'],
    ['retroflex', 'place'],
    ['velar', 'place'],
    ['uvular', 'place'],
    ['pharyngeal', 'place'],
    ['epiglottal', 'place'],
    ['glottal', 'place'],
    ['rhotic', 'rhoticity'],
    ['sibilant', 'amplitude'],
    ['nonsibilant', 'amplitude'],
    ['vowel', 'class'],
    ['stop', 'manner'],
    ['fricative', 'manner'],
    ['approximant', 'manner'],
    ['flap', 'manner'],
    ['trill', 'manner'],
    ['voiceless', 'voicing'],
    ['voiced', 'voicing'],
    ['partially_voiced', 'voicing'],
    ['devoiced', 'voicing'],
    ['composite', 'composite'],
    ['diphthong', 'composite'],
    ['affricate', 'composite'],
    ['coarticulated', 'composite'],
    ['close', 'height'],
    ['near_close', 'height'],
    ['close_mid', 'height'],
    ['mid', 'height'],
    ['open_mid', 'height'],
    ['near_open', 'height'],
    ['open', 'height'],
    ['front', 'backness'],
    ['near_front', 'backness'],
    ['center', 'backness'],
    ['near_back', 'backness'],
    ['back', 'backness'],
    ['duration', 'suprasegmental'],
    ['stress', 'suprasegmental'],
    ['pitch', 'suprasegmental'],
    ['contour', 'suprasegmental'],
    ['intonation', 'suprasegmental'],
]]

FEATURE_QUALIFIER = [PhonFeature(alias, cat) for alias, cat in [
    ['top', 'degree'],
    ['high', 'degree'],
    ['middle', 'degree'],
    ['low', 'degree'],
    ['bottom', 'degree'],
    ['rising', 'change'],
    ['falling', 'change'],
    ['interrupt', 'change'],
]]

FEATURES = ARTICULATION_FEATURE + FEATURE_QUALIFIER
_F = ft_inventory(FEATURES)

ROWS = [ty.Thing(alias, value_from=features) for alias, features in [
    ['close_vwl', [_F.vowel, _F.close]],
    ['n_close_vwl', [_F.vowel, _F.near_close]],
    ['c_mid_vwl', [_F.vowel, _F.close_mid]],
    ['mid_vwl', [_F.vowel, _F.mid]],
    ['o_mid_vwl', [_F.vowel, _F.open_mid]],
    ['n_open_vwl', [_F.vowel, _F.near_open]],
    ['open_vwl', [_F.vowel, _F.open]],
    ['front_unr', [_F.front, _F.nonlabial]],
    ['front_rnd', [_F.front, _F.labial]],
    ['n_front_unr', [_F.near_front, _F.nonlabial]],
    ['n_front_rnd', [_F.near_front, _F.labial]],
    ['center_unr', [_F.center, _F.nonlabial]],
    ['center_rnd', [_F.center, _F.labial]],
    ['n_back_unr', [_F.near_back, _F.nonlabial]],
    ['n_back_rnd', [_F.near_back, _F.labial]],
    ['back_unr', [_F.back, _F.nonlabial]],
    ['back_rnd', [_F.back, _F.labial]],
    ['vcd_nasal', [_F.nasal, _F.stop, _F.voiced]],
    ['vcl_stop', [_F.stop, _F.voiceless]],
    ['vcd_stop', [_F.stop, _F.voiced]],
    ['vcl_nonsib_fricative', [_F.fricative, _F.nonsibilant, _F.voiceless]],
    ['vcd_nonsib_fricative', [_F.fricative, _F.nonsibilant, _F.voiced]],
    ['vcl_sib_fricative', [_F.fricative, _F.sibilant, _F.voiceless]],
    ['vcd_sib_fricative', [_F.fricative, _F.sibilant, _F.voiced]],
    ['vcl_lat_fricative', [_F.fricative, _F.lateral, _F.voiceless]],
    ['vcd_lat_fricative', [_F.fricative, _F.lateral, _F.voiced]],
    ['central_approximant', [_F.approximant, _F.voiced]],
    ['lateral_approximant', [_F.approximant, _F.voiced, _F.lateral]],
    ['vlr_lbl', [_F.velar, _F.labial]],
    ['vcd_flap', [_F.flap, _F.voiced]],
    ['vcd_trill', [_F.trill, _F.voiced]],
    ['click_release', [_F.click, _F.nonpulmonic]],
]]

FEATURE_INVENTORY = ft_inventory(FEATURES, ROWS)
