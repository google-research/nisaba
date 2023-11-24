# Copyright 2023 Nisaba Authors.
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

"""Phonological features."""

from nisaba.scripts.natural_translit.features import feature2
from nisaba.scripts.natural_translit.utils import list_op as ls


def _articulatory() -> feature2.FeatureInventory:
  """Articulatory features."""
  f = feature2.FeatureInventory('articulatory')
  ls.apply_foreach(f.make_group, [
      ['pronunciation', ['silent', 'vocal']],
      ['syllabicity', ['syllabic', 'nonsyllabic']],
      ['airstream', ['pulmonic', 'nonpulmonic']],
      ['airflow', ['central', 'lateral', 'nasal']],
      ['release', ['aspirated', 'unaspirated', 'click']],
      ['place', [
          'labial', 'nonlabial',
          'bilabial', 'labiodental', 'dental',
          'alveolar', 'postalveolar', 'palatal',
          'retroflex', 'velar', 'uvular',
          'pharyngeal', 'epiglottal', 'glottal',
      ]],
      ['rhoticity', ['rhotic', 'nonrhotic']],
      ['turbulence', ['none', 'sibilant', 'nonsibilant']],
      ['consonancy', ['vowel', 'consonant']],
      ['manner', ['stop', 'fricative', 'approximant', 'flap', 'trill']],
      ['voicing', ['voiceless', 'voiced', 'partially_voiced', 'devoiced']],
      ['composition', [
          'noncomposite', 'composite',
          'diphthong', 'affricate', 'coarticulated'
      ]],
      ['height', [
          'close', 'near_close',
          'close_mid', 'mid', 'open_mid',
          'near_open', 'open'
      ]],
      ['backness', ['front', 'near_front', 'center', 'near_back', 'back']]
  ])
  # Vowel rows
  ls.apply_foreach(f.add_feature_set, [
      ['close_vwl', f.vowel, f.close],
      ['n_close_vwl', f.vowel, f.near_close],
      ['c_mid_vwl', f.vowel, f.close_mid],
      ['mid_vwl', f.vowel, f.mid],
      ['o_mid_vwl', f.vowel, f.open_mid],
      ['n_open_vwl', f.vowel, f.near_open],
      ['open_vwl', f.vowel, f.open],
  ])
  # Vowel columns
  ls.apply_foreach(f.add_feature_set, [
      ['front_unr', f.front, f.nonlabial],
      ['front_rnd', f.front, f.labial],
      ['n_front_unr', f.near_front, f.nonlabial],
      ['n_front_rnd', f.near_front, f.labial],
      ['center_unr', f.center, f.nonlabial],
      ['center_rnd', f.center, f.labial],
      ['n_back_unr', f.near_back, f.nonlabial],
      ['n_back_rnd', f.near_back, f.labial],
      ['back_unr', f.back, f.nonlabial],
      ['back_rnd', f.back, f.labial],
  ])
  # Consonant rows - split by voicing
  ls.apply_foreach(f.add_feature_set, [
      ['vcd_nasal', f.nasal, f.stop, f.voiced],
      ['vcl_stop', f.stop, f.voiceless],
      ['vcd_stop', f.stop, f.voiced],
      ['vcl_nonsib_fricative', f.fricative, f.nonsibilant, f.voiceless],
      ['vcd_nonsib_fricative', f.fricative, f.nonsibilant, f.voiced],
      ['vcl_sib_fricative', f.fricative, f.sibilant, f.voiceless],
      ['vcd_sib_fricative', f.fricative, f.sibilant, f.voiced],
      ['vcl_lat_fricative', f.fricative, f.lateral, f.voiceless],
      ['vcd_lat_fricative', f.fricative, f.lateral, f.voiced],
      ['central_approximant', f.approximant, f.voiced],
      ['lateral_approximant', f.approximant, f.voiced, f.lateral],
      ['vlr_lbl', f.velar, f.labial],
      ['vcd_flap', f.flap, f.voiced],
      ['vcd_trill', f.trill, f.voiced],
  ])
  # Click features
  f.add_feature_set('click_release', f.click, f.nonpulmonic)
  return f

articulatory = _articulatory()


def _suprasegmental() -> feature2.FeatureInventory:
  """Suprasegmental features."""
  f = feature2.FeatureInventory('suprasegmental')
  # TODO: Convert suprasegmental features to groups of qualified features.
  # eg. f.make_group('duration', ['short', 'long'])
  f.make_group('suprasegmental', [
      'duration', 'stress', 'pitch', 'contour', 'intonation'
  ])
  return f

suprasegmental = _suprasegmental()
