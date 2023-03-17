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

"""Simple placeholder for the phonological feature structure."""

import collections
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import list_op as ls

# cat: category, val: value
PhonFeature = collections.namedtuple(
    'PhonFeature', ['alias', 'cat'])


def ft_inventory(feature_list: [PhonFeature]) -> collections.namedtuple:
  return i.make_inventory(i.alias_list(feature_list), feature_list)

# TODO:Enum features by category
FEATURES = ls.apply_foreach(PhonFeature, [
    ['silent', 'pronunciation'],
    ['syllabic', 'syllabicity'],
    ['nonsyllabic', 'syllabicity'],
    ['pulmonic', 'airstream'],
    ['nonpulmonic', 'airstream'],
    ['oral_central', 'airflow'],
    ['oral_lateral', 'airflow'],
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
    ['long', 'duration'],
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
])
FEATURE_INVENTORY = ft_inventory(FEATURES)
