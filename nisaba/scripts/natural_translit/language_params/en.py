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

"""Language parameters for English."""

from nisaba.scripts.natural_translit.phonology.inventories import x_uni
from nisaba.scripts.natural_translit.script import grapheme as g
from nisaba.scripts.natural_translit.script.inventories import latn as l


LANGUAGE = g.Grapheme.LANGUAGE.en


def _latn_inventory() -> g.Grapheme.Inventory:
  """Builds a grapheme inventory for English."""
  latn = l.LATN
  ph = x_uni.PHONEMES
  gr = g.Grapheme.Inventory(g.Grapheme.GR_FEATURES.script.latn, LANGUAGE)  # pyrefly: ignore[missing-attribute]
  lowercase = [
      latn.a,  # pyrefly: ignore[missing-attribute]
      latn.b,  # pyrefly: ignore[missing-attribute]
      latn.c,  # pyrefly: ignore[missing-attribute]
      latn.d,  # pyrefly: ignore[missing-attribute]
      latn.e,  # pyrefly: ignore[missing-attribute]
      latn.f,  # pyrefly: ignore[missing-attribute]
      latn.g,  # pyrefly: ignore[missing-attribute]
      latn.h,  # pyrefly: ignore[missing-attribute]
      latn.i,  # pyrefly: ignore[missing-attribute]
      latn.j,  # pyrefly: ignore[missing-attribute]
      latn.k,  # pyrefly: ignore[missing-attribute]
      latn.l,  # pyrefly: ignore[missing-attribute]
      latn.m,  # pyrefly: ignore[missing-attribute]
      latn.n,  # pyrefly: ignore[missing-attribute]
      latn.o,  # pyrefly: ignore[missing-attribute]
      latn.p,  # pyrefly: ignore[missing-attribute]
      latn.q,  # pyrefly: ignore[missing-attribute]
      latn.r,  # pyrefly: ignore[missing-attribute]
      latn.s,  # pyrefly: ignore[missing-attribute]
      latn.t,  # pyrefly: ignore[missing-attribute]
      latn.u,  # pyrefly: ignore[missing-attribute]
      latn.v,  # pyrefly: ignore[missing-attribute]
      latn.w,  # pyrefly: ignore[missing-attribute]
      latn.x,  # pyrefly: ignore[missing-attribute]
      latn.y,  # pyrefly: ignore[missing-attribute]
      latn.z,  # pyrefly: ignore[missing-attribute]
  ]
  gr.import_as_feature_pairs(
      g.Grapheme.GR_FEATURES.case.lower,  # pyrefly: ignore[missing-attribute]
      g.Grapheme.GR_FEATURES.case.upper,  # pyrefly: ignore[missing-attribute]
      *((lower, lower.upper) for lower in lowercase)
  )
  gr.make_iterable_suppl('letter', *gr.upper, *gr.lower)  # pyrefly: ignore[missing-attribute]

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

  gr.a.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      # lax: man, tense: mane, heavy: mar, heavy-r: mare
      ph.ae,  # lax nucleus  # pyrefly: ignore[missing-attribute]
      ph.e,  # tense nucleus  # pyrefly: ignore[missing-attribute]
      ph.iy,  # tense glide  # pyrefly: ignore[missing-attribute]
      ph.aw,  # heavy nucleus  # pyrefly: ignore[missing-attribute]
      ph.eh,  # heavy-r nucleus  # pyrefly: ignore[missing-attribute]
      ph.ec,  # heavy-r glide  # pyrefly: ignore[missing-attribute]
  )
  gr.e.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      # lax: met, tense: meet, heavy: her, heavy-r: here
      ph.eh,  # lax nucleus  # pyrefly: ignore[missing-attribute]
      ph.i,  # tense nucleus  # pyrefly: ignore[missing-attribute]
      ph.ex,  # heavy nucleus  # pyrefly: ignore[missing-attribute]
      ph.iy,  # heavy-r nucleus  # pyrefly: ignore[missing-attribute]
      ph.ec,  # heavy-r glide  # pyrefly: ignore[missing-attribute]
  )
  gr.i.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      # lax: win, tense: wine, heavy: fir, heavy-r: fire
      ph.iy,  # lax nucleus; tense, heavy-r glide  # pyrefly: ignore[missing-attribute]
      ph.a,  # tense, heavy-r nucleus  # pyrefly: ignore[missing-attribute]
      ph.ex,  # heavy nucleus  # pyrefly: ignore[missing-attribute]
      ph.ec,  # heavy-r second glide  # pyrefly: ignore[missing-attribute]
  )
  gr.o.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      # lax: mop, tense: mope, heavy: for, heavy-r: fore
      ph.ow,  # lax nucleus  # pyrefly: ignore[missing-attribute]
      ph.o,  # tense nucleus  # pyrefly: ignore[missing-attribute]
      ph.uv,  # tense glide  # pyrefly: ignore[missing-attribute]
      ph.oh,  # heavy, heavy-r nucleus  # pyrefly: ignore[missing-attribute]
  )
  gr.u.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      # lax: hug, push, tense: huge, heavy: cur, heavy-r: cure
      ph.ah,  # lax nucleus  # pyrefly: ignore[missing-attribute]
      ph.uv,  # lax, heavy-r nucleus  # pyrefly: ignore[missing-attribute]
      ph.u,  # tense nucleus  # pyrefly: ignore[missing-attribute]
      ph.ec,  # heavy-r glide  # pyrefly: ignore[missing-attribute]
  )

  # Consonants.
  gr.b.update_descriptives_from_symbol(ph.b)  # pyrefly: ignore[missing-attribute]
  gr.c.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.s,  # city  # pyrefly: ignore[missing-attribute]
      ph.k,  # cat  # pyrefly: ignore[missing-attribute]
  )
  gr.d.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.d,  # dog  # pyrefly: ignore[missing-attribute]
  )
  gr.f.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.f,  # fine  # pyrefly: ignore[missing-attribute]
  )
  gr.g.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.g,  # get  # pyrefly: ignore[missing-attribute]
      ph.d,  # gin stop  # pyrefly: ignore[missing-attribute]
      ph.zh,  # gin fricative  # pyrefly: ignore[missing-attribute]
  )
  gr.h.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.h,  # honey  # pyrefly: ignore[missing-attribute]
  )
  gr.j.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.d,  # jump stop  # pyrefly: ignore[missing-attribute]
      ph.zh,  # jump fricative  # pyrefly: ignore[missing-attribute]
      ph.y,  # hallelujah  # pyrefly: ignore[missing-attribute]
      ph.h,  # jalapeno  # pyrefly: ignore[missing-attribute]
  )
  gr.k.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.k,  # key  # pyrefly: ignore[missing-attribute]
  )
  gr.l.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.l,  # line  # pyrefly: ignore[missing-attribute]
  )
  gr.m.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.m,  # mine  # pyrefly: ignore[missing-attribute]
  )
  gr.n.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.n,  # name  # pyrefly: ignore[missing-attribute]
  )
  gr.p.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.p,  # pill  # pyrefly: ignore[missing-attribute]
  )
  gr.q.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.k,  # quick  # pyrefly: ignore[missing-attribute]
  )
  gr.r.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.r,  # red  # pyrefly: ignore[missing-attribute]
  )
  gr.s.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.s,  # saw  # pyrefly: ignore[missing-attribute]
      ph.z,  # prison  # pyrefly: ignore[missing-attribute]
      ph.sh,  # sugar  # pyrefly: ignore[missing-attribute]
      ph.zh,  # vision  # pyrefly: ignore[missing-attribute]
  )
  gr.t.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.t,  # ten, righteous stop  # pyrefly: ignore[missing-attribute]
      ph.sh,  # ration, righteous fricative  # pyrefly: ignore[missing-attribute]
      ph.zh,  # equation  # pyrefly: ignore[missing-attribute]
  )
  gr.v.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.v,  # vine  # pyrefly: ignore[missing-attribute]
  )
  gr.w.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.w,  # water  # pyrefly: ignore[missing-attribute]
  )
  gr.x.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.k,  # box, anxious, luxurious(gb) stop  # pyrefly: ignore[missing-attribute]
      ph.s,  # box fricative  # pyrefly: ignore[missing-attribute]
      ph.g,  # anxiety, luxurious(us) stop  # pyrefly: ignore[missing-attribute]
      ph.z,  # anxiety fricative  # pyrefly: ignore[missing-attribute]
      ph.zh,  # luxurious fricative  # pyrefly: ignore[missing-attribute]
      ph.sh,  # anxious fricative  # pyrefly: ignore[missing-attribute]
  )
  gr.y.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.y,  # yes  # pyrefly: ignore[missing-attribute]
      gr.i,  # flynn, fry, fyrd, pyre  # pyrefly: ignore[missing-attribute]
  )
  gr.z.update_descriptives_from_symbol(  # pyrefly: ignore[missing-attribute]
      ph.z,  # zoo  # pyrefly: ignore[missing-attribute]
      ph.zh,  # seizure  # pyrefly: ignore[missing-attribute]
      ph.t,  # schizophrenia stop  # pyrefly: ignore[missing-attribute]
      ph.s,  # schizophrenia fricative  # pyrefly: ignore[missing-attribute]
  )
  for upper in gr.upper:  # pyrefly: ignore[missing-attribute]
    upper.update_descriptives_from_symbol(upper.lower)
  vowels = [gr.a, gr.e, gr.i, gr.o, gr.u, gr.y]  # pyrefly: ignore[missing-attribute]
  consonants = [
      gr.b,  # pyrefly: ignore[missing-attribute]
      gr.c,  # pyrefly: ignore[missing-attribute]
      gr.d,  # pyrefly: ignore[missing-attribute]
      gr.f,  # pyrefly: ignore[missing-attribute]
      gr.g,  # pyrefly: ignore[missing-attribute]
      gr.h,  # pyrefly: ignore[missing-attribute]
      gr.j,  # pyrefly: ignore[missing-attribute]
      gr.k,  # pyrefly: ignore[missing-attribute]
      gr.l,  # pyrefly: ignore[missing-attribute]
      gr.m,  # pyrefly: ignore[missing-attribute]
      gr.n,  # pyrefly: ignore[missing-attribute]
      gr.p,  # pyrefly: ignore[missing-attribute]
      gr.q,  # pyrefly: ignore[missing-attribute]
      gr.r,  # pyrefly: ignore[missing-attribute]
      gr.s,  # pyrefly: ignore[missing-attribute]
      gr.t,  # pyrefly: ignore[missing-attribute]
      gr.v,  # pyrefly: ignore[missing-attribute]
      gr.w,  # pyrefly: ignore[missing-attribute]
      gr.x,  # pyrefly: ignore[missing-attribute]
      gr.y,  # pyrefly: ignore[missing-attribute]
      gr.z,  # pyrefly: ignore[missing-attribute]
  ]
  gr.make_iterable_suppl('vowel', *vowels, *(v.upper for v in vowels))
  gr.make_iterable_suppl(
      'consonant', *consonants, *(c.upper for c in consonants)
  )
  gr.import_graphemes(*latn.number, list_alias='number')  # pyrefly: ignore[missing-attribute]
  return gr.sync_atomics(  # pyrefly: ignore[bad-return]
      [gr.upper, gr.lower, gr.letter, gr.vowel, gr.consonant, gr.number]  # pyrefly: ignore[missing-attribute]
  )


LATN = _latn_inventory()
