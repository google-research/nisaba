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

"""Language parameters for English."""

from nisaba.scripts.natural_translit.phonology.inventories import x_uni
from nisaba.scripts.natural_translit.script import grapheme as g
from nisaba.scripts.natural_translit.script.inventories import latn as l


LANGUAGE = g.Grapheme.LANGUAGE.en


def _latn_inventory() -> g.Grapheme.Inventory:
  """Builds a grapheme inventory for English."""
  latn = l.LATN
  ph = x_uni.PHONEMES
  gr = g.Grapheme.Inventory(g.Grapheme.GR_FEATURES.script.latn, LANGUAGE)
  lowercase = [
      latn.a,
      latn.b,
      latn.c,
      latn.d,
      latn.e,
      latn.f,
      latn.g,
      latn.h,
      latn.i,
      latn.j,
      latn.k,
      latn.l,
      latn.m,
      latn.n,
      latn.o,
      latn.p,
      latn.q,
      latn.r,
      latn.s,
      latn.t,
      latn.u,
      latn.v,
      latn.w,
      latn.x,
      latn.y,
      latn.z,
  ]
  gr.import_as_feature_pairs(
      g.Grapheme.GR_FEATURES.case.lower,
      g.Grapheme.GR_FEATURES.case.upper,
      *((lower, lower.upper) for lower in lowercase)
  )
  gr.make_iterable_suppl('letter', *gr.upper, *gr.lower)

  # Descriptive features from common one-to-one grapheme-phoneme mappings.
  # Many-to-many values for subbstrings, universal mappings such
  # as vowel reduction, and common phonological operations such as
  # palatalization will be matched through g2p/g2g alignables and/or built-in
  # phonological rules.

  # Initial values retrieved on 2025-01-24 from:
  # https://en.wikipedia.org/wiki/English_orthography#Spelling-to-sound_correspondences

  # Vowels.
  # Technically all durations are {short, long} through union of lax and tense/
  # heavy phonemes, but it's left as {any} for now.

  gr.a.update_descriptives_from_symbol(
      # lax: man, tense: mane, heavy: mar, heavy-r: mare
      ph.ae,  # lax nucleus
      ph.e,  # tense nucleus
      ph.iy,  # tense glide
      ph.aw,  # heavy nucleus
      ph.eh,  # heavy-r nucleus
      ph.ec,  # heavy-r glide
  )
  gr.e.update_descriptives_from_symbol(
      # lax: met, tense: meet, heavy: her, heavy-r: here
      ph.eh,  # lax nucleus
      ph.i,  # tense nucleus
      ph.ex,  # heavy nucleus
      ph.iy,  # heavy-r nucleus
      ph.ec,  # heavy-r glide
  )
  gr.i.update_descriptives_from_symbol(
      # lax: win, tense: wine, heavy: fir, heavy-r: fire
      ph.iy,  # lax nucleus; tense, heavy-r glide
      ph.a,  # tense, heavy-r nucleus
      ph.ex,  # heavy nucleus
      ph.ec,  # heavy-r second glide
  )
  gr.o.update_descriptives_from_symbol(
      # lax: mop, tense: mope, heavy: for, heavy-r: fore
      ph.ow,  # lax nucleus
      ph.o,  # tense nucleus
      ph.uv,  # tense glide
      ph.oh,  # heavy, heavy-r nucleus
  )
  gr.u.update_descriptives_from_symbol(
      # lax: hug, push, tense: huge, heavy: cur, heavy-r: cure
      ph.ah,  # lax nucleus
      ph.uv,  # lax, heavy-r nucleus
      ph.u,  # tense nucleus
      ph.ec,  # heavy-r glide
  )

  # Consonants.
  gr.b.update_descriptives_from_symbol(ph.b)
  gr.c.update_descriptives_from_symbol(
      ph.s,  # city
      ph.k,  # cat
  )
  gr.d.update_descriptives_from_symbol(
      ph.d,  # dog
  )
  gr.f.update_descriptives_from_symbol(
      ph.f,  # fine
  )
  gr.g.update_descriptives_from_symbol(
      ph.g,  # get
      ph.d,  # gin stop
      ph.zh,  # gin fricative
  )
  gr.h.update_descriptives_from_symbol(
      ph.h,  # honey
  )
  gr.j.update_descriptives_from_symbol(
      ph.d,  # jump stop
      ph.zh,  # jump fricative
      ph.y,  # hallelujah
      ph.h,  # jalapeno
  )
  gr.k.update_descriptives_from_symbol(
      ph.k,  # key
  )
  gr.l.update_descriptives_from_symbol(
      ph.l,  # line
  )
  gr.m.update_descriptives_from_symbol(
      ph.m,  # mine
  )
  gr.n.update_descriptives_from_symbol(
      ph.n,  # name
  )
  gr.p.update_descriptives_from_symbol(
      ph.p,  # pill
  )
  gr.q.update_descriptives_from_symbol(
      ph.k,  # quick
  )
  gr.r.update_descriptives_from_symbol(
      ph.r,  # red
  )
  gr.s.update_descriptives_from_symbol(
      ph.s,  # saw
      ph.z,  # prison
      ph.sh,  # sugar
      ph.zh,  # vision
  )
  gr.t.update_descriptives_from_symbol(
      ph.t,  # ten, righteous stop
      ph.sh,  # ration, righteous fricative
      ph.zh,  # equation
  )
  gr.v.update_descriptives_from_symbol(
      ph.v,  # vine
  )
  gr.w.update_descriptives_from_symbol(
      ph.w,  # water
  )
  gr.x.update_descriptives_from_symbol(
      ph.k,  # box, anxious, luxurious(gb) stop
      ph.s,  # box fricative
      ph.g,  # anxiety, luxurious(us) stop
      ph.z,  # anxiety fricative
      ph.zh,  # luxurious fricative
      ph.sh,  # anxious fricative
  )
  gr.y.update_descriptives_from_symbol(
      ph.y,  # yes
      gr.i,  # flynn, fry, fyrd, pyre
  )
  gr.z.update_descriptives_from_symbol(
      ph.z,  # zoo
      ph.zh,  # seizure
      ph.t,  # schizophrenia stop
      ph.s,  # schizophrenia fricative
  )
  for upper in gr.upper:
    upper.update_descriptives_from_symbol(upper.lower)
  vowels = [gr.a, gr.e, gr.i, gr.o, gr.u, gr.y]
  consonants = [
      gr.b,
      gr.c,
      gr.d,
      gr.f,
      gr.g,
      gr.h,
      gr.j,
      gr.k,
      gr.l,
      gr.m,
      gr.n,
      gr.p,
      gr.q,
      gr.r,
      gr.s,
      gr.t,
      gr.v,
      gr.w,
      gr.x,
      gr.y,
      gr.z,
  ]
  gr.make_iterable_suppl('vowel', *vowels, *(v.upper for v in vowels))
  gr.make_iterable_suppl(
      'consonant', *consonants, *(c.upper for c in consonants)
  )
  gr.import_graphemes(*latn.number, list_alias='number')
  return gr.sync_atomics(
      [gr.upper, gr.lower, gr.letter, gr.vowel, gr.consonant, gr.number]
  )


LATN = _latn_inventory()
