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
      'descriptive',
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
      ('close_like', [features.height.close, features.height.near_close]),  # pyrefly: ignore[missing-attribute]
      (
          'mid_like',
          [
              features.height.close_mid,  # pyrefly: ignore[missing-attribute]
              features.height.mid,  # pyrefly: ignore[missing-attribute]
              features.height.open_mid,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      ('open_like', [features.height.near_open, features.height.open]),  # pyrefly: ignore[missing-attribute]
  ]:
    features.height.set(alias, feature_list)  # pyrefly: ignore[missing-attribute]
  for alias, feature_list in [
      ('front_like', [features.backness.front, features.backness.near_front]),  # pyrefly: ignore[missing-attribute]
      ('back_like', [features.backness.near_back, features.backness.back]),  # pyrefly: ignore[missing-attribute]
  ]:
    features.backness.set(alias, feature_list)  # pyrefly: ignore[missing-attribute]
  features.articulator.set(  # pyrefly: ignore[missing-attribute]
      'coronal',
      features.articulator.apical,  # pyrefly: ignore[missing-attribute]
      features.articulator.laminal,  # pyrefly: ignore[missing-attribute]
  )
  features.place.set(  # pyrefly: ignore[missing-attribute]
      'para_alveolar',
      features.place.dental,  # pyrefly: ignore[missing-attribute]
      features.place.alveolar,  # pyrefly: ignore[missing-attribute]
      features.place.postalveolar,  # pyrefly: ignore[missing-attribute]
  )
  # Place of articulation sets.
  features.make_sets(
      # Consonant rows that combine manner and secondary articulation.
      (
          'nasal',
          [
              features.manner.stop,  # pyrefly: ignore[missing-attribute]
              features.nasalization.nasalized,  # pyrefly: ignore[missing-attribute]
              features.voicing.voiced,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      ('approximant', [features.manner.approximant, features.voicing.voiced]),  # pyrefly: ignore[missing-attribute]
      (
          'lateral_fricative',
          [features.manner.non_sibilant, features.lateralization.lateral],  # pyrefly: ignore[missing-attribute]
      ),
      (
          'lateral_approximant',
          [
              features.manner.approximant,  # pyrefly: ignore[missing-attribute]
              features.voicing.voiced,  # pyrefly: ignore[missing-attribute]
              features.lateralization.lateral,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      # Consonant columns that combine active and passive articulators, as well
      # as voicing and secondary articulation where applicable.
      (
          'bilabial',
          [
              features.articulator.labial,  # pyrefly: ignore[missing-attribute]
              features.place.labial,  # pyrefly: ignore[missing-attribute]
              features.labialization.labialized,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      (
          'labiodental',
          [
              features.articulator.labial,  # pyrefly: ignore[missing-attribute]
              features.place.dental,  # pyrefly: ignore[missing-attribute]
              features.labialization.labialized,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      ('dental', [features.articulator.apical, features.place.dental]),  # pyrefly: ignore[missing-attribute]
      ('alveolar', [features.articulator.coronal, features.place.alveolar]),  # pyrefly: ignore[missing-attribute]
      (
          'para_alveolar',
          [features.articulator.coronal, features.place.para_alveolar],  # pyrefly: ignore[missing-attribute]
      ),
      (
          'postalveolar',
          [
              features.articulator.laminal,  # pyrefly: ignore[missing-attribute]
              features.place.postalveolar,  # pyrefly: ignore[missing-attribute]
              features.palatalization.light,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      (
          'retroflex',
          [
              features.articulator.apical,  # pyrefly: ignore[missing-attribute]
              features.place.postalveolar,  # pyrefly: ignore[missing-attribute]
              features.place.palatal,  # pyrefly: ignore[missing-attribute]
              features.palatalization.none,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      (
          'palatal',
          [
              features.articulator.coronal,  # pyrefly: ignore[missing-attribute]
              features.articulator.dorsal,  # pyrefly: ignore[missing-attribute]
              features.place.palatal,  # pyrefly: ignore[missing-attribute]
              features.palatalization.heavy,  # pyrefly: ignore[missing-attribute]
          ],
      ),
      ('velar', [features.articulator.dorsal, features.place.velar]),  # pyrefly: ignore[missing-attribute]
      ('uvular', [features.articulator.dorsal, features.place.uvular]),  # pyrefly: ignore[missing-attribute]
      (
          'epiglottal',
          [features.articulator.laryngeal, features.place.epiglottal],  # pyrefly: ignore[missing-attribute]
      ),
      ('glottal', [features.articulator.laryngeal, features.place.glottal]),  # pyrefly: ignore[missing-attribute]
  )
  # Default profiles.
  features.add_profile(
      'vowel',
      features.ph_class.vowel,  # pyrefly: ignore[missing-attribute]
      features.airstream.pulmonic,  # pyrefly: ignore[missing-attribute]
      features.manner.n_a,  # pyrefly: ignore[missing-attribute]
      features.place.n_a,  # pyrefly: ignore[missing-attribute]
      features.articulator.n_a,  # pyrefly: ignore[missing-attribute]
      features.breathiness.none,  # pyrefly: ignore[missing-attribute]
      features.voicing.voiced,  # pyrefly: ignore[missing-attribute]
      features.lateralization.n_a,  # pyrefly: ignore[missing-attribute]
      features.nasalization.none,  # pyrefly: ignore[missing-attribute]
      features.palatalization.none,  # pyrefly: ignore[missing-attribute]
      features.rhoticization.none,  # pyrefly: ignore[missing-attribute]
      features.syllabicity.syllabic,  # pyrefly: ignore[missing-attribute]
  )
  features.add_profile(
      'consonant',
      features.ph_class.consonant,  # pyrefly: ignore[missing-attribute]
      features.airstream.pulmonic,  # pyrefly: ignore[missing-attribute]
      features.height.n_a,  # pyrefly: ignore[missing-attribute]
      features.backness.n_a,  # pyrefly: ignore[missing-attribute]
      features.labialization.none,  # pyrefly: ignore[missing-attribute]
      features.lateralization.none,  # pyrefly: ignore[missing-attribute]
      features.nasalization.none,  # pyrefly: ignore[missing-attribute]
      features.palatalization.none,  # pyrefly: ignore[missing-attribute]
      features.rhoticization.none,  # pyrefly: ignore[missing-attribute]
      features.syllabicity.none,  # pyrefly: ignore[missing-attribute]
  )
  return features


FEATURES = _features()
