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

"""Descriptive phonological features based on IPA charts.

See
https://github.com/google-research/nisaba/blob/main/nisaba/scripts/natural_translit/phonology/doc/descriptive_features.md
for building profiles and interpreting feature distances.
"""

from nisaba.scripts.natural_translit.utils import feature


def _features() -> feature.Feature.Inventory:
  """Creates an inventory of descriptive phonological features."""
  f = feature.Feature
  features = f.Inventory(
      'phonology_descriptive',
      f.Aspect(
          f.equidistant(
              'ph_class',
              f('vowel'),
              f('consonant'),
          )
      ),
      # Articulation
      f.Aspect(
          f.equidistant(
              'airstream',
              f('pulmonic'),
              f.equidistant('glottalic', f('ejective'), f('implosive'), step=0),
              f('click'),
          )
      ),
      ## Consonant articulation
      f.Aspect(
          f.linear(
              'manner',
              f('stop'),
              f.equidistant(
                  'fricatives',
                  f('fricative'),
                  f.linear(
                      'amplitude',
                      f('sibilant'),
                      f('strident'),
                      f('non_sibilant'),
                      step=0.25,
                  ),
                  step=0,
              ),
              f.equidistant(
                  'approximant_like',
                  f('approximant'),
                  f.equidistant(
                      'tap_flap_trill',
                      f.equidistant('non_trill', f('tap'), f('flap'), step=0),
                      f('trill'),
                      step=0.5,
                  ),
              ),
          )
      ),
      f.Aspect(
          f.linear(
              'place',
              f('labial'),
              f('dental'),
              f('alveolar'),
              f('postalveolar'),
              f('palatal'),
              f('velar'),
              f('uvular'),
              f('epiglottal'),
              f('glottal'),
              step=0.5,
          )
      ),
      f.Aspect(
          f.equidistant(
              'articulator',
              f('labial'),
              f('apical'),
              f('laminal'),
              f('dorsal'),
              f('laryngeal'),
              step=0.5,
          )
      ),
      ## Vowel articulation
      f.Aspect(
          f.linear(
              'height',
              f('close'),
              f('near_close'),
              f('close_mid'),
              f('mid'),
              f('open_mid'),
              f('near_open'),
              f('open'),
              step=0.5,
          )
      ),
      f.Aspect(
          f.linear(
              'backness',
              f('front'),
              f('near_front'),
              f('central'),
              f('near_back'),
              f('back'),
              step=0.5,
          )
      ),
      # Phonation
      f.Aspect(
          f.equidistant(
              'breathiness',
              f.equidistant(
                  'is_breathy',
                  f('aspirated'),
                  f('breathy'),
                  f('murmured'),
                  step=0,
              ),
              f.equidistant('not_breathy', f('unaspirated'), f('none'), step=0),
          ),
      ),
      f.Aspect(f.equidistant('voicing', f('voiced'), f('voiceless'))),
      ## Secondary articulation.
      f.Aspect(
          f.equidistant(
              'labialization',
              f.equidistant(
                  'is_labialized', f('labialized'), f('rounded'), step=0
              ),
              f.equidistant(
                  'not_labialized', f('none'), f('unrounded'), step=0
              ),
          )
      ),
      f.Aspect(f.equidistant('lateralization', f('lateral'), f('none'))),
      f.Aspect(f.equidistant('nasalization', f('nasalized'), f('none'))),
      f.Aspect(
          f.linear(
              'palatalization', f('light'), f('heavy'), f('none'), step=0.5
          )
      ),
      f.Aspect(f.equidistant('rhoticization', f('rhotic'), f('none'))),
      # Suprasegmental
      f.Aspect(
          f.linear(
              'duration',
              f('extra_short'),
              f('short'),
              f('half_long'),
              f('long'),
              f('extra_long'),
              step=0.5,
          )
      ),
      f.Aspect(f.equidistant('syllabicity', f('syllabic'), f('none'))),
  )
  for alias, feature_list in [
      ('close_like', [features.height.close, features.height.near_close]),
      (
          'mid_like',
          [
              features.height.close_mid,
              features.height.mid,
              features.height.open_mid,
          ],
      ),
      ('open_like', [features.height.near_open, features.height.open]),
  ]:
    features.height.set(alias, feature_list)
  for alias, feature_list in [
      ('front_like', [features.backness.front, features.backness.near_front]),
      ('back_like', [features.backness.near_back, features.backness.back]),
  ]:
    features.backness.set(alias, feature_list)
  features.articulator.set(
      'coronal',
      features.articulator.apical,
      features.articulator.laminal,
  )
  features.place.set(
      'para_alveolar',
      features.place.dental,
      features.place.alveolar,
      features.place.postalveolar,
  )
  # Place of articulation sets.
  features.make_sets(
      # Consonant rows that combine manner and secondary articulation.
      (
          'nasal',
          [
              features.manner.stop,
              features.nasalization.nasalized,
              features.voicing.voiced,
          ],
      ),
      ('approximant', [features.manner.approximant, features.voicing.voiced]),
      (
          'lateral_fricative',
          [features.manner.non_sibilant, features.lateralization.lateral],
      ),
      (
          'lateral_approximant',
          [
              features.manner.non_sibilant,
              features.voicing.voiced,
              features.lateralization.lateral,
          ],
      ),
      # Consonant columns that combine active and passive articulators, as well
      # as voicing and secondary articulation where applicable.
      (
          'bilabial',
          [
              features.articulator.labial,
              features.place.labial,
              features.labialization.labialized,
          ],
      ),
      (
          'labiodental',
          [
              features.articulator.labial,
              features.place.dental,
              features.labialization.labialized,
          ],
      ),
      ('dental', [features.articulator.apical, features.place.dental]),
      ('alveolar', [features.articulator.coronal, features.place.alveolar]),
      (
          'para_alveolar',
          [features.articulator.coronal, features.place.para_alveolar],
      ),
      (
          'postalveolar',
          [
              features.articulator.laminal,
              features.place.postalveolar,
              features.palatalization.light,
          ],
      ),
      (
          'retroflex',
          [
              features.articulator.apical,
              features.place.postalveolar,
              features.place.palatal,
              features.palatalization.none,
          ],
      ),
      (
          'palatal',
          [
              features.articulator.coronal,
              features.articulator.dorsal,
              features.place.palatal,
              features.palatalization.heavy,
          ],
      ),
      ('velar', [features.articulator.dorsal, features.place.velar]),
      ('uvular', [features.articulator.dorsal, features.place.uvular]),
      (
          'epiglottal',
          [features.articulator.laryngeal, features.place.epiglottal],
      ),
      ('glottal', [features.articulator.laryngeal, features.place.glottal]),
  )
  # Default profiles.
  features.add_profile(
      'vowel',
      features.ph_class.vowel,
      features.airstream.pulmonic,
      features.manner.n_a,
      features.place.n_a,
      features.articulator.n_a,
      features.breathiness.none,
      features.voicing.voiced,
      features.lateralization.n_a,
      features.nasalization.none,
      features.palatalization.none,
      features.rhoticization.none,
      features.syllabicity.syllabic,
  )
  features.add_profile(
      'consonant',
      features.ph_class.consonant,
      features.airstream.pulmonic,
      features.height.n_a,
      features.backness.n_a,
      features.labialization.none,
      features.lateralization.none,
      features.nasalization.none,
      features.palatalization.none,
      features.rhoticization.none,
      features.syllabicity.none,
  )
  return features


FEATURES = _features()
