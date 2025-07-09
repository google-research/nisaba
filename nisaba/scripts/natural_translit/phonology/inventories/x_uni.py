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

"""Multilingual Phon inventory."""

from nisaba.scripts.natural_translit.phonology import phonological_symbol as po


def _phoneme_inventory() -> po.Phon.Inventory:
  """Multilingual Phon inventory."""
  p = po.Phon
  phf = p.DESCRIPTIVE_FEATURES
  ph = po.Phon.Inventory()

  # Vowels.

  vowels = [
      ('a', 'a', 'open front unrounded vowel'),
      ('ä', 'au', 'open center unrounded vowel'),
      ('æ', 'ae', 'near_open front unrounded vowel'),
      ('ɐ', 'av', 'near_open center unrounded vowel'),
      ('ɑ', 'aw', 'open back unrounded vowel'),
      ('ɒ', 'ow', 'open back rounded vowel'),
      ('e', 'e', 'close_mid front unrounded vowel'),
      ('ə', 'ec', 'mid center unrounded vowel'),
      ('ɛ', 'eh', 'open_mid front unrounded vowel'),
      ('ɘ', 'el', 'close_mid center unrounded vowel'),
      ('ɜ', 'ex', 'open_mid center unrounded vowel'),
      ('ɞ', 'ox', 'open_mid center rounded vowel'),
      ('ɤ', 'eo', 'close_mid back unrounded vowel'),
      ('i', 'i', 'close front unrounded vowel'),
      ('ɪ', 'iy', 'near_close near_front unrounded vowel'),
      ('ɨ', 'ic', 'close center unrounded vowel'),
      ('o', 'o', 'close_mid back rounded vowel'),
      ('ø', 'oi', 'close_mid front rounded vowel'),
      ('œ', 'oe', 'open_mid front rounded vowel'),
      ('ɶ', 'oa', 'open front rounded vowel'),
      ('ɔ', 'oh', 'open_mid back rounded vowel'),
      ('ɵ', 'ol', 'close_mid center rounded vowel'),
      ('u', 'u', 'close back rounded vowel'),
      ('ʉ', 'uc', 'close center rounded vowel'),
      ('ɯ', 'iu', 'close back unrounded vowel'),
      ('ʊ', 'uv', 'near_close near_back rounded vowel'),
      ('ʌ', 'ah', 'open_mid back unrounded vowel'),
      ('y', 'ui', 'close front rounded vowel'),
      ('ʏ', 'uy', 'near_close near_front rounded vowel'),
  ]
  ph.add_phonemes(
      *(
          p(alias=alias, ipa=ipa, name=name, features=phf.vowel)
          for ipa, alias, name in vowels
      ),
      list_alias='vowel',
  )

  # Default heights from IPA vowel chart.

  for open_vowel in [ph.a, ph.au, ph.aw, ph.ow, ph.oa]:
    open_vowel.update_descriptives(phf.height.open)
  for near_open_vowel in [ph.ae, ph.av]:
    near_open_vowel.update_descriptives(phf.height.near_open)
  for open_mid_vowel in [ph.eh, ph.ex, ph.ox, ph.oe, ph.oh, ph.ah]:
    open_mid_vowel.update_descriptives(phf.height.open_mid)
  for mid_vowel in [ph.ec]:
    mid_vowel.update_descriptives(phf.height.mid)
  for close_mid_vowel in [ph.e, ph.el, ph.eo, ph.o, ph.ol]:
    close_mid_vowel.update_descriptives(phf.height.close_mid)
  for near_close_vowel in [ph.iy, ph.uv, ph.uy]:
    near_close_vowel.update_descriptives(phf.height.near_close)
  for close_vowel in [ph.i, ph.ic, ph.u, ph.uc, ph.iu, ph.ui]:
    close_vowel.update_descriptives(phf.height.close)

  # Default backness from IPA vowel chart.

  for front_vowel in [
      ph.a,
      ph.ae,
      ph.e,
      ph.eh,
      ph.i,
      ph.oi,
      ph.oe,
      ph.oa,
      ph.ui,
  ]:
    front_vowel.update_descriptives(phf.backness.front)
  for near_front_vowel in [ph.iy, ph.av, ph.iy, ph.uy]:
    near_front_vowel.update_descriptives(phf.backness.near_front)
  for central_vowel in [
      ph.au,
      ph.av,
      ph.ec,
      ph.el,
      ph.ex,
      ph.ox,
      ph.ic,
      ph.ol,
      ph.uc,
  ]:
    central_vowel.update_descriptives(phf.backness.central)
  for near_back_vowel in [ph.uv]:
    near_back_vowel.update_descriptives(phf.backness.near_back)
  for back_vowel in [ph.aw, ph.ow, ph.eo, ph.o, ph.oh, ph.u, ph.iu, ph.ah]:
    back_vowel.update_descriptives(phf.backness.back)

  # Default roundness from IPA vowel chart.

  for rounded_vowel in [
      ph.ow,
      ph.ox,
      ph.o,
      ph.oi,
      ph.oe,
      ph.oa,
      ph.oh,
      ph.ol,
      ph.u,
      ph.uc,
      ph.uv,
      ph.ui,
      ph.uy,
  ]:
    rounded_vowel.update_descriptives(phf.labialization.rounded)

  for unrounded_vowel in [
      ph.a,
      ph.au,
      ph.ae,
      ph.av,
      ph.aw,
      ph.e,
      ph.ec,
      ph.eh,
      ph.el,
      ph.ex,
      ph.eo,
      ph.i,
      ph.iy,
      ph.ic,
      ph.iu,
      ph.ah,
  ]:
    unrounded_vowel.update_descriptives(phf.labialization.unrounded)

  # Consonants.

  consonants = [
      ('b', 'b', 'voiced bilabial stop'),
      ('ʙ', 'bb', 'bilabial trill'),
      ('c', 'ky', 'voiceless palatal stop'),
      ('ç', 'hy', 'voiceless palatal non-sibilant fricative'),
      ('ɕ', 'sy', 'voiceless palatal sibilant fricative'),
      ('d', 'd', 'voiced alveolar stop'),
      ('ð', 'dh', 'voiced dental non-sibilant fricative'),
      ('ɖ', 'dd', 'voiced retro­flex stop'),
      ('f', 'f', 'voiceless labio­dental non-sibilant fricative'),
      ('ɡ', 'g', 'voiced velar stop'),
      ('ɢ', 'j', 'voiced uvular stop'),
      ('ɣ', 'gh', 'voiced velar non-sibilant fricative'),
      ('h', 'h', 'voiceless glottal non-sibilant fricative'),
      ('ħ', 'ch', 'voiceless pharyngeal non-sibilant fricative'),
      ('ʜ', 'hho', 'voiceless epiglottal trill'),
      ('ɦ', 'ha', 'voiced glottal non-sibilant fricative'),
      ('j', 'y', 'palatal approximant'),
      ('ʝ', 'yy', 'voiced palatal non-sibilant fricative'),
      ('ɟ', 'gy', 'voiced palatal stop'),
      ('k', 'k', 'voiceless velar stop'),
      ('l', 'l', 'alveolar lateral approximant'),
      ('ʟ', 'lg', 'velar lateral approximant'),
      ('ɬ', 'sl', 'voiceless alveolar lateral fricative'),
      ('ɭ', 'll', 'retro­flex lateral approximant'),
      ('ꞎ', 'ssl', 'voiceless retro­flex lateral fricative'),
      ('ɮ', 'zl', 'voiced alveolar lateral fricative'),
      ('ʎ', 'ly', 'palatal lateral approximant'),
      ('m', 'm', 'voiced bilabial nasal'),
      ('ɱ', 'mi', 'voiced labio­dental nasal'),
      ('n', 'n', 'voiced alveolar nasal'),
      ('ɴ', 'nj', 'voiced uvular nasal'),
      ('ɲ', 'ny', 'voiced palatal nasal'),
      ('ɳ', 'nn', 'voiced retro­flex nasal'),
      ('ŋ', 'ng', 'voiced velar nasal'),
      ('p', 'p', 'voiceless bilabial stop'),
      ('ɸ', 'ph', 'voiceless bilabial non-sibilant fricative'),
      ('q', 'q', 'voiceless uvular stop'),
      ('r', 'r', 'alveolar trill'),
      ('ʀ', 'rj', 'uvular trill'),
      ('ɹ', 'ru', 'alveolar approximant'),
      ('ɺ', 'rl', 'alveolar lateral flap'),
      ('ɻ', 'rru', 'retro­flex approximant'),
      ('ɽ', 'rd', 'retro­flex flap'),
      ('ɾ', 'rt', 'alveolar flap'),
      ('ʁ', 'jh', 'voiced uvular non-sibilant fricative'),
      ('s', 's', 'voiceless alveolar sibilant fricative'),
      ('ʂ', 'ss', 'voiceless retro­flex sibilant fricative'),
      ('ʃ', 'sh', 'voiceless post­alveolar sibilant fricative'),
      ('t', 't', 'voiceless alveolar stop'),
      ('ʈ', 'tt', 'voiceless retro­flex stop'),
      ('ɰ', 'gu', 'velar approximant'),
      ('v', 'v', 'voiced labio­dental non-sibilant fricative'),
      ('ʋ', 'vu', 'labio­dental approximant'),
      ('ⱱ', 'vt', 'labio­dental flap'),
      ('x', 'kh', 'voiceless velar non-sibilant fricative'),
      ('z', 'z', 'voiced alveolar sibilant fricative'),
      ('ʐ', 'zz', 'voiced retro­flex sibilant fricative'),
      ('ʑ', 'zy', 'voiced palatal sibilant fricative'),
      ('ʒ', 'zh', 'voiced post­alveolar sibilant fricative'),
      ('ʔ', 'x', 'glottal stop'),
      ('ʕ', 'cha', 'voiced pharyngeal non-sibilant fricative'),
      ('ʡ', 'c', 'epiglottal stop'),
      ('ʢ', 'hh', 'epiglottal trill'),
      ('β', 'bh', 'voiced bilabial non-sibilant fricative'),
      ('θ', 'th', 'voiceless dental non-sibilant fricative'),
      ('χ', 'qh', 'voiceless uvular non-sibilant fricative'),
      ('ɥ', 'yw', 'labial-palatal approximant'),
      ('ʍ', 'hw', 'voiceless labial-velar fricative'),
      ('w', 'w', 'labial-velar approximant'),
      ('ɧ', 'sj', 'voiceless palatal-velar fricative'),
      ('ɫ', 'lw', 'labial-velar lateral approximant'),
  ]
  ph.add_phonemes(
      *(
          p(alias=alias, ipa=ipa, name=name, features=phf.consonant)
          for ipa, alias, name in consonants
      ),
      list_alias='consonant',
  )

  # Default manner from IPA consonant table rows.

  for nasal_consonant in [ph.m, ph.mi, ph.n, ph.ng, ph.nj, ph.nn, ph.ny]:
    nasal_consonant.update_descriptives(phf.nasal)
  for stop_consonant in [
      ph.b,
      ph.c,
      ph.d,
      ph.dd,
      ph.g,
      ph.gy,
      ph.j,
      ph.k,
      ph.ky,
      ph.p,
      ph.q,
      ph.t,
      ph.tt,
      ph.x,
  ]:
    stop_consonant.update_descriptives(phf.manner.stop)
  for sibilant_fricative in [
      ph.s,
      ph.sh,
      ph.ss,
      ph.sy,
      ph.z,
      ph.zh,
      ph.zy,
      ph.zz,
  ]:
    sibilant_fricative.update_descriptives(phf.manner.sibilant)
  for nonsibilant_fricative in [
      ph.bh,
      ph.ch,
      ph.cha,
      ph.dh,
      ph.f,
      ph.gh,
      ph.h,
      ph.ha,
      ph.hw,
      ph.hy,
      ph.jh,
      ph.kh,
      ph.ph,
      ph.qh,
      ph.sj,
      ph.th,
      ph.v,
      ph.yy,
  ]:
    nonsibilant_fricative.update_descriptives(phf.manner.non_sibilant)
  for approximant_consonant in [ph.gu, ph.rru, ph.ru, ph.vu, ph.w, ph.y, ph.yw]:
    approximant_consonant.update_descriptives(phf.manner.approximant)
  for tap_consonant in [ph.rd, ph.rt, ph.vt]:
    tap_consonant.update_descriptives(phf.manner.tap)
  for trill_consonant in [ph.bb, ph.hh, ph.hho, ph.r, ph.rj]:
    trill_consonant.update_descriptives(phf.manner.trill)
  for lateral_fricative in [ph.sl, ph.ssl, ph.zl]:
    lateral_fricative.update_descriptives(phf.lateral_fricative)
  for lateral_approximant in [ph.l, ph.lg, ph.ll, ph.lw, ph.ly]:
    lateral_approximant.update_descriptives(phf.lateral_approximant)
  for lateral_tap in [ph.rl]:
    lateral_tap.update_descriptives(
        phf.lateral_approximant
    ).update_descriptives(phf.manner.tap)

  # Default place of articulation from IPA consonant table columns.

  for bilabial_consonant in [ph.b, ph.bb, ph.bh, ph.m, ph.p, ph.ph]:
    bilabial_consonant.update_descriptives(phf.bilabial)
  for labiodental_consonant in [ph.f, ph.mi, ph.v, ph.vt, ph.vu]:
    labiodental_consonant.update_descriptives(phf.labiodental)
  for dental_consonant in [
      ph.dh,
      ph.th,
  ]:
    dental_consonant.update_descriptives(phf.dental)
  for dental_alveolar_consonant in [ph.s, ph.z]:
    dental_alveolar_consonant.update_descriptives(phf.dental, phf.alveolar)
  for para_alveolar_consonant in [
      ph.d,
      ph.l,
      ph.n,
      ph.r,
      ph.rl,
      ph.rt,
      ph.ru,
      ph.sl,
      ph.t,
      ph.zl,
  ]:
    para_alveolar_consonant.update_descriptives(phf.para_alveolar)
  for postalveolar_consonant in [ph.sh, ph.zh]:
    postalveolar_consonant.update_descriptives(phf.postalveolar)
  for retroflex_consonant in [
      ph.dd,
      ph.ll,
      ph.nn,
      ph.rd,
      ph.rru,
      ph.ss,
      ph.ssl,
      ph.tt,
      ph.zz,
  ]:
    retroflex_consonant.update_descriptives(phf.retroflex)
  for palatal_consonant in [
      ph.gy,
      ph.hy,
      ph.ky,
      ph.ly,
      ph.ny,
      ph.sy,
      ph.y,
      ph.yw,
      ph.yy,
      ph.zy,
  ]:
    palatal_consonant.update_descriptives(phf.palatal)
  for velar_consonant in [
      ph.g,
      ph.gh,
      ph.gu,
      ph.hw,
      ph.k,
      ph.kh,
      ph.lg,
      ph.lw,
      ph.ng,
      ph.sj,
      ph.w,
  ]:
    velar_consonant.update_descriptives(phf.velar)
  for uvular_consonant in [ph.j, ph.jh, ph.nj, ph.q, ph.qh, ph.rj]:
    uvular_consonant.update_descriptives(phf.uvular)
  for epiglottal_consonant in [ph.c, ph.ch, ph.cha, ph.hh, ph.hho]:
    epiglottal_consonant.update_descriptives(phf.epiglottal)
  for glottal_consonant in [ph.h, ph.ha, ph.x]:
    glottal_consonant.update_descriptives(phf.glottal)

  # Update voicing for stops and fricatives.

  for voiceless_consonant in [
      ph.c,
      ph.ch,
      ph.f,
      ph.h,
      ph.hho,
      ph.hw,
      ph.hy,
      ph.k,
      ph.kh,
      ph.ky,
      ph.p,
      ph.ph,
      ph.q,
      ph.qh,
      ph.s,
      ph.sh,
      ph.sj,
      ph.sl,
      ph.ss,
      ph.ssl,
      ph.sy,
      ph.t,
      ph.th,
      ph.tt,
      ph.x,
  ]:
    voiceless_consonant.update_descriptives(phf.voicing.voiceless)
  for voiced_consonant in [
      ph.b,
      ph.bh,
      ph.cha,
      ph.d,
      ph.dd,
      ph.dh,
      ph.g,
      ph.gh,
      ph.gy,
      ph.ha,
      ph.j,
      ph.jh,
      ph.v,
      ph.yy,
      ph.z,
      ph.zh,
      ph.zl,
      ph.zy,
      ph.zz,
  ]:
    voiced_consonant.update_descriptives(phf.voicing.voiced)

  # Add secondary articulations.

  for labialized_consonant in [ph.hw, ph.lw, ph.w, ph.yw]:
    labialized_consonant.update_descriptives(phf.labialization.labialized)
  for palatalized_consonant in [ph.sj]:
    palatalized_consonant.update_descriptives(phf.palatalization.heavy)
  return ph.sync_atomics()


PHONEMES = _phoneme_inventory()
