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

"""Grapheme inventory for basic Latin characters."""

from nisaba.scripts.natural_translit.script import grapheme


def _build_inventory() -> grapheme.Grapheme.Inventory:
  """Builds a grapheme inventory for basic Latin characters."""
  g = grapheme.Grapheme
  grf = g.GR_FEATURES
  phf = g.PH_DESCRIPTIVE_FEATURES
  latn = g.Inventory(g.GR_FEATURES.script.latn)
  lowercase_vowels = ['a', 'e', 'i', 'o', 'u']
  latn.add_graphemes(
      *(
          g.from_char(char, char, {grf.script.latn, phf.vowel})
          for char in lowercase_vowels
      ),
      list_alias='vowel',
  )
  # Generic vowel features.
  latn.a.update_descriptives(
      phf.height.open_like,
      phf.backness.front_like,
      phf.labialization.unrounded,
  )
  latn.e.update_descriptives(
      phf.height.mid_like,
      phf.backness.front_like,
      phf.labialization.unrounded,
  )
  latn.i.update_descriptives(
      phf.height.close_like,
      phf.backness.front_like,
      phf.labialization.unrounded,
  )
  latn.o.update_descriptives(
      phf.height.open_like,
      phf.backness.back_like,
      phf.labialization.rounded,
  )
  latn.u.update_descriptives(
      phf.height.close_like,
      phf.backness.back_like,
      phf.labialization.rounded,
  )
  lowercase_consonants = [
      'b',
      'c',
      'd',
      'f',
      'g',
      'h',
      'j',
      'k',
      'l',
      'm',
      'n',
      'p',
      'q',
      'r',
      's',
      't',
      'v',
      'w',
      'x',
      'y',
      'z',
  ]
  latn.add_graphemes(
      *(
          g.from_char(char, char, {grf.script.latn, phf.consonant})
          for char in lowercase_consonants
      ),
      list_alias='consonant',
  )
  # Generic consonant features.
  # Columns
  for bilabial in [latn.b, latn.m, latn.p]:
    bilabial.update_descriptives(phf.bilabial)
  for labiodental in [latn.f, latn.v]:
    labiodental.update_descriptives(phf.labiodental)
  for para_alveolar in [
      latn.c,
      latn.d,
      latn.j,
      latn.l,
      latn.n,
      latn.r,
      latn.s,
      latn.t,
      latn.z,
  ]:
    para_alveolar.update_descriptives(phf.para_alveolar, phf.retroflex)
  for palatal in [latn.y]:
    palatal.update_descriptives(phf.palatal)
  for velar in [latn.g, latn.k, latn.q]:
    velar.update_descriptives(phf.velar)
  for labial_velar in [latn.w]:
    labial_velar.update_descriptives(phf.bilabial, phf.velar)
  for alveolar_velar in [latn.x]:
    alveolar_velar.update_descriptives(phf.alveolar, phf.velar)
  for glottal in [latn.h]:
    glottal.update_descriptives(phf.glottal)
  # Rows
  for nasal in [latn.m, latn.n]:
    nasal.update_descriptives(phf.nasal)
  for stop in [latn.b, latn.d, latn.g, latn.k, latn.p, latn.t]:
    stop.update_descriptives(phf.manner.stop)
  for fricative in [latn.f, latn.h, latn.s, latn.v, latn.z]:
    fricative.update_descriptives(phf.manner.fricative)
  for affricate in [latn.c, latn.j, latn.x]:
    affricate.update_descriptives(phf.manner.stop, phf.manner.fricative)
  for approximant in [latn.w, latn.y]:
    approximant.update_descriptives(phf.approximant)
  for lateral_approximant in [latn.l]:
    lateral_approximant.update_descriptives(phf.lateral_approximant)
  for rhotic in [latn.r]:
    rhotic.update_descriptives(phf.rhoticization.rhotic)
  # Voicing for stops, fricatives, and affricates.
  for voiced in [latn.b, latn.d, latn.g, latn.j, latn.v, latn.z]:
    voiced.update_descriptives(phf.voicing.voiced)
  for voiceless in [
      latn.c,
      latn.f,
      latn.k,
      latn.p,
      latn.q,
      latn.s,
      latn.t,
      latn.x,
  ]:
    voiceless.update_descriptives(phf.voicing.voiceless)
  latn.make_iterable_suppl('lower', *latn.vowel, *latn.consonant)
  latn.make_iterable_suppl('upper')
  for char in latn.lower:
    uppercase = g.from_char(
        char.text.upper(),
        char.alias + '_upper',
        {grf.script.latn, grf.case.upper, char.descriptives()},
    )
    latn.add_graphemes(uppercase)
    latn.upper.add(uppercase)
    char.feature_pair(uppercase, grf.case.lower, grf.case.upper)
    if uppercase.has_feature(phf.ph_class.vowel):
      latn.vowel.add(uppercase)
    if uppercase.has_feature(phf.ph_class.consonant):
      latn.consonant.add(uppercase)
  latn.make_iterable_suppl('letter', *latn.lower, *latn.upper)
  return latn.sync_atomics(
      [latn.lower, latn.upper, latn.letter, latn.vowel, latn.consonant]
  )


GRAPHEMES = _build_inventory()
