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

"""Grapheme inventory for basic Latin characters."""

from nisaba.scripts.natural_translit.script import grapheme


def _build_inventory() -> grapheme.Grapheme.Inventory:
  """Builds a grapheme inventory for basic Latin characters."""
  g = grapheme.Grapheme
  grf = g.GR_FEATURES
  phf = g.DESCRIPTIVE_FEATURES
  latn = g.Inventory(g.GR_FEATURES.script.latn)  # pyrefly: ignore[missing-attribute]
  lowercase_vowels = ['a', 'e', 'i', 'o', 'u']
  latn.add_graphemes(
      *(
          g.from_char(
              char, char, {grf.script.latn, grf.gr_class.letter, phf.vowel}  # pyrefly: ignore[missing-attribute]
          )
          for char in lowercase_vowels
      ),
      list_alias='vowel',
  )
  # Generic vowel features.
  latn.a.update_descriptives(  # pyrefly: ignore[missing-attribute]
      phf.height.open_like,  # pyrefly: ignore[missing-attribute]
      phf.backness.front_like,  # pyrefly: ignore[missing-attribute]
      phf.labialization.unrounded,  # pyrefly: ignore[missing-attribute]
  )
  latn.e.update_descriptives(  # pyrefly: ignore[missing-attribute]
      phf.height.mid_like,  # pyrefly: ignore[missing-attribute]
      phf.backness.front_like,  # pyrefly: ignore[missing-attribute]
      phf.labialization.unrounded,  # pyrefly: ignore[missing-attribute]
  )
  latn.i.update_descriptives(  # pyrefly: ignore[missing-attribute]
      phf.height.close_like,  # pyrefly: ignore[missing-attribute]
      phf.backness.front_like,  # pyrefly: ignore[missing-attribute]
      phf.labialization.unrounded,  # pyrefly: ignore[missing-attribute]
  )
  latn.o.update_descriptives(  # pyrefly: ignore[missing-attribute]
      phf.height.open_like,  # pyrefly: ignore[missing-attribute]
      phf.backness.back_like,  # pyrefly: ignore[missing-attribute]
      phf.labialization.rounded,  # pyrefly: ignore[missing-attribute]
  )
  latn.u.update_descriptives(  # pyrefly: ignore[missing-attribute]
      phf.height.close_like,  # pyrefly: ignore[missing-attribute]
      phf.backness.back_like,  # pyrefly: ignore[missing-attribute]
      phf.labialization.rounded,  # pyrefly: ignore[missing-attribute]
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
          g.from_char(
              char, char, {grf.script.latn, grf.gr_class.letter, phf.consonant}  # pyrefly: ignore[missing-attribute]
          )
          for char in lowercase_consonants
      ),
      list_alias='consonant',
  )
  # Generic consonant features.
  # Columns
  for bilabial in [latn.b, latn.m, latn.p]:  # pyrefly: ignore[missing-attribute]
    bilabial.update_descriptives(phf.bilabial)  # pyrefly: ignore[missing-attribute]
  for labiodental in [latn.f, latn.v]:  # pyrefly: ignore[missing-attribute]
    labiodental.update_descriptives(phf.labiodental)  # pyrefly: ignore[missing-attribute]
  for para_alveolar in [
      latn.c,  # pyrefly: ignore[missing-attribute]
      latn.d,  # pyrefly: ignore[missing-attribute]
      latn.j,  # pyrefly: ignore[missing-attribute]
      latn.l,  # pyrefly: ignore[missing-attribute]
      latn.n,  # pyrefly: ignore[missing-attribute]
      latn.r,  # pyrefly: ignore[missing-attribute]
      latn.s,  # pyrefly: ignore[missing-attribute]
      latn.t,  # pyrefly: ignore[missing-attribute]
      latn.z,  # pyrefly: ignore[missing-attribute]
  ]:
    para_alveolar.update_descriptives(phf.para_alveolar, phf.retroflex)  # pyrefly: ignore[missing-attribute]
  for palatal in [latn.y]:  # pyrefly: ignore[missing-attribute]
    palatal.update_descriptives(phf.palatal)  # pyrefly: ignore[missing-attribute]
  for velar in [latn.g, latn.k, latn.q]:  # pyrefly: ignore[missing-attribute]
    velar.update_descriptives(phf.velar)  # pyrefly: ignore[missing-attribute]
  for labial_velar in [latn.w]:  # pyrefly: ignore[missing-attribute]
    labial_velar.update_descriptives(phf.bilabial, phf.velar)  # pyrefly: ignore[missing-attribute]
  for alveolar_velar in [latn.x]:  # pyrefly: ignore[missing-attribute]
    alveolar_velar.update_descriptives(phf.alveolar, phf.velar)  # pyrefly: ignore[missing-attribute]
  for glottal in [latn.h]:  # pyrefly: ignore[missing-attribute]
    glottal.update_descriptives(phf.glottal)  # pyrefly: ignore[missing-attribute]
  # Rows
  for nasal in [latn.m, latn.n]:  # pyrefly: ignore[missing-attribute]
    nasal.update_descriptives(phf.nasal)  # pyrefly: ignore[missing-attribute]
  for stop in [latn.b, latn.d, latn.g, latn.k, latn.p, latn.t]:  # pyrefly: ignore[missing-attribute]
    stop.update_descriptives(phf.manner.stop)  # pyrefly: ignore[missing-attribute]
  for fricative in [latn.f, latn.h, latn.s, latn.v, latn.z]:  # pyrefly: ignore[missing-attribute]
    fricative.update_descriptives(phf.manner.fricative)  # pyrefly: ignore[missing-attribute]
  for affricate in [latn.c, latn.j, latn.x]:  # pyrefly: ignore[missing-attribute]
    affricate.update_descriptives(phf.manner.stop, phf.manner.fricative)  # pyrefly: ignore[missing-attribute]
  for approximant in [latn.w, latn.y]:  # pyrefly: ignore[missing-attribute]
    approximant.update_descriptives(phf.approximant)  # pyrefly: ignore[missing-attribute]
  for lateral_approximant in [latn.l]:  # pyrefly: ignore[missing-attribute]
    lateral_approximant.update_descriptives(phf.lateral_approximant)  # pyrefly: ignore[missing-attribute]
  for rhotic in [latn.r]:  # pyrefly: ignore[missing-attribute]
    rhotic.update_descriptives(phf.rhoticization.rhotic)  # pyrefly: ignore[missing-attribute]
  # Voicing for stops, fricatives, and affricates.
  for voiced in [latn.b, latn.d, latn.g, latn.j, latn.v, latn.z]:  # pyrefly: ignore[missing-attribute]
    voiced.update_descriptives(phf.voicing.voiced)  # pyrefly: ignore[missing-attribute]
  for voiceless in [
      latn.c,  # pyrefly: ignore[missing-attribute]
      latn.f,  # pyrefly: ignore[missing-attribute]
      latn.k,  # pyrefly: ignore[missing-attribute]
      latn.p,  # pyrefly: ignore[missing-attribute]
      latn.q,  # pyrefly: ignore[missing-attribute]
      latn.s,  # pyrefly: ignore[missing-attribute]
      latn.t,  # pyrefly: ignore[missing-attribute]
      latn.x,  # pyrefly: ignore[missing-attribute]
  ]:
    voiceless.update_descriptives(phf.voicing.voiceless)  # pyrefly: ignore[missing-attribute]
  latn.make_iterable_suppl('lower', *latn.vowel, *latn.consonant)  # pyrefly: ignore[missing-attribute]
  latn.make_iterable_suppl('upper')
  for char in latn.lower:  # pyrefly: ignore[missing-attribute]
    uppercase = g.from_char(
        char.text.upper(),
        char.alias + '_upper',
        {
            grf.script.latn,  # pyrefly: ignore[missing-attribute]
            grf.gr_class.letter,  # pyrefly: ignore[missing-attribute]
            grf.case.upper,  # pyrefly: ignore[missing-attribute]
            char.descriptives(),
        },
    )
    latn.add_graphemes(uppercase)
    latn.upper.add(uppercase)  # pyrefly: ignore[missing-attribute]
    char.feature_pair(uppercase, grf.case.lower, grf.case.upper)  # pyrefly: ignore[missing-attribute]
    if uppercase.has_feature(phf.ph_class.vowel):  # pyrefly: ignore[missing-attribute]
      latn.vowel.add(uppercase)  # pyrefly: ignore[missing-attribute]
    if uppercase.has_feature(phf.ph_class.consonant):  # pyrefly: ignore[missing-attribute]
      latn.consonant.add(uppercase)  # pyrefly: ignore[missing-attribute]
  latn.make_iterable_suppl('letter', *latn.lower, *latn.upper)  # pyrefly: ignore[missing-attribute]
  numbers = [
      (0, 'zero'),
      (1, 'one'),
      (2, 'two'),
      (3, 'three'),
      (4, 'four'),
      (5, 'five'),
      (6, 'six'),
      (7, 'seven'),
      (8, 'eight'),
      (9, 'nine'),
  ]
  latn.add_graphemes(
      *(
          g.from_char(
              str(number),
              alias,
              {grf.script.latn, grf.gr_class.number, phf.not_applicable},  # pyrefly: ignore[missing-attribute]
          )
          for number, alias in numbers
      ),
      list_alias='number',
  )
  return latn.sync_atomics([  # pyrefly: ignore[bad-return]
      latn.lower,  # pyrefly: ignore[missing-attribute]
      latn.upper,  # pyrefly: ignore[missing-attribute]
      latn.letter,  # pyrefly: ignore[missing-attribute]
      latn.vowel,  # pyrefly: ignore[missing-attribute]
      latn.consonant,  # pyrefly: ignore[missing-attribute]
      latn.number,  # pyrefly: ignore[missing-attribute]
  ])


LATN = _build_inventory()
