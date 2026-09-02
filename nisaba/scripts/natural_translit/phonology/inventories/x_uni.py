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
          p(alias=alias, ipa=ipa, name=name, features=phf.vowel)  # pyrefly: ignore[missing-attribute]
          for ipa, alias, name in vowels
      ),
      list_alias='vowel',
  )

  # Default heights from IPA vowel chart.

  for open_vowel in [ph.a, ph.au, ph.aw, ph.ow, ph.oa]:  # pyrefly: ignore[missing-attribute]
    open_vowel.update_descriptives(phf.height.open)  # pyrefly: ignore[missing-attribute]
  for near_open_vowel in [ph.ae, ph.av]:  # pyrefly: ignore[missing-attribute]
    near_open_vowel.update_descriptives(phf.height.near_open)  # pyrefly: ignore[missing-attribute]
  for open_mid_vowel in [ph.eh, ph.ex, ph.ox, ph.oe, ph.oh, ph.ah]:  # pyrefly: ignore[missing-attribute]
    open_mid_vowel.update_descriptives(phf.height.open_mid)  # pyrefly: ignore[missing-attribute]
  for mid_vowel in [ph.ec]:  # pyrefly: ignore[missing-attribute]
    mid_vowel.update_descriptives(phf.height.mid)  # pyrefly: ignore[missing-attribute]
  for close_mid_vowel in [ph.e, ph.el, ph.eo, ph.o, ph.ol]:  # pyrefly: ignore[missing-attribute]
    close_mid_vowel.update_descriptives(phf.height.close_mid)  # pyrefly: ignore[missing-attribute]
  for near_close_vowel in [ph.iy, ph.uv, ph.uy]:  # pyrefly: ignore[missing-attribute]
    near_close_vowel.update_descriptives(phf.height.near_close)  # pyrefly: ignore[missing-attribute]
  for close_vowel in [ph.i, ph.ic, ph.u, ph.uc, ph.iu, ph.ui]:  # pyrefly: ignore[missing-attribute]
    close_vowel.update_descriptives(phf.height.close)  # pyrefly: ignore[missing-attribute]

  # Default backness from IPA vowel chart.

  for front_vowel in [
      ph.a,  # pyrefly: ignore[missing-attribute]
      ph.ae,  # pyrefly: ignore[missing-attribute]
      ph.e,  # pyrefly: ignore[missing-attribute]
      ph.eh,  # pyrefly: ignore[missing-attribute]
      ph.i,  # pyrefly: ignore[missing-attribute]
      ph.oi,  # pyrefly: ignore[missing-attribute]
      ph.oe,  # pyrefly: ignore[missing-attribute]
      ph.oa,  # pyrefly: ignore[missing-attribute]
      ph.ui,  # pyrefly: ignore[missing-attribute]
  ]:
    front_vowel.update_descriptives(phf.backness.front)  # pyrefly: ignore[missing-attribute]
  for near_front_vowel in [ph.iy, ph.av, ph.iy, ph.uy]:  # pyrefly: ignore[missing-attribute]
    near_front_vowel.update_descriptives(phf.backness.near_front)  # pyrefly: ignore[missing-attribute]
  for central_vowel in [
      ph.au,  # pyrefly: ignore[missing-attribute]
      ph.av,  # pyrefly: ignore[missing-attribute]
      ph.ec,  # pyrefly: ignore[missing-attribute]
      ph.el,  # pyrefly: ignore[missing-attribute]
      ph.ex,  # pyrefly: ignore[missing-attribute]
      ph.ox,  # pyrefly: ignore[missing-attribute]
      ph.ic,  # pyrefly: ignore[missing-attribute]
      ph.ol,  # pyrefly: ignore[missing-attribute]
      ph.uc,  # pyrefly: ignore[missing-attribute]
  ]:
    central_vowel.update_descriptives(phf.backness.central)  # pyrefly: ignore[missing-attribute]
  for near_back_vowel in [ph.uv]:  # pyrefly: ignore[missing-attribute]
    near_back_vowel.update_descriptives(phf.backness.near_back)  # pyrefly: ignore[missing-attribute]
  for back_vowel in [ph.aw, ph.ow, ph.eo, ph.o, ph.oh, ph.u, ph.iu, ph.ah]:  # pyrefly: ignore[missing-attribute]
    back_vowel.update_descriptives(phf.backness.back)  # pyrefly: ignore[missing-attribute]

  # Default roundness from IPA vowel chart.

  for rounded_vowel in [
      ph.ow,  # pyrefly: ignore[missing-attribute]
      ph.ox,  # pyrefly: ignore[missing-attribute]
      ph.o,  # pyrefly: ignore[missing-attribute]
      ph.oi,  # pyrefly: ignore[missing-attribute]
      ph.oe,  # pyrefly: ignore[missing-attribute]
      ph.oa,  # pyrefly: ignore[missing-attribute]
      ph.oh,  # pyrefly: ignore[missing-attribute]
      ph.ol,  # pyrefly: ignore[missing-attribute]
      ph.u,  # pyrefly: ignore[missing-attribute]
      ph.uc,  # pyrefly: ignore[missing-attribute]
      ph.uv,  # pyrefly: ignore[missing-attribute]
      ph.ui,  # pyrefly: ignore[missing-attribute]
      ph.uy,  # pyrefly: ignore[missing-attribute]
  ]:
    rounded_vowel.update_descriptives(phf.labialization.rounded)  # pyrefly: ignore[missing-attribute]

  for unrounded_vowel in [
      ph.a,  # pyrefly: ignore[missing-attribute]
      ph.au,  # pyrefly: ignore[missing-attribute]
      ph.ae,  # pyrefly: ignore[missing-attribute]
      ph.av,  # pyrefly: ignore[missing-attribute]
      ph.aw,  # pyrefly: ignore[missing-attribute]
      ph.e,  # pyrefly: ignore[missing-attribute]
      ph.ec,  # pyrefly: ignore[missing-attribute]
      ph.eh,  # pyrefly: ignore[missing-attribute]
      ph.el,  # pyrefly: ignore[missing-attribute]
      ph.ex,  # pyrefly: ignore[missing-attribute]
      ph.eo,  # pyrefly: ignore[missing-attribute]
      ph.i,  # pyrefly: ignore[missing-attribute]
      ph.iy,  # pyrefly: ignore[missing-attribute]
      ph.ic,  # pyrefly: ignore[missing-attribute]
      ph.iu,  # pyrefly: ignore[missing-attribute]
      ph.ah,  # pyrefly: ignore[missing-attribute]
  ]:
    unrounded_vowel.update_descriptives(phf.labialization.unrounded)  # pyrefly: ignore[missing-attribute]

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
          p(alias=alias, ipa=ipa, name=name, features=phf.consonant)  # pyrefly: ignore[missing-attribute]
          for ipa, alias, name in consonants
      ),
      list_alias='consonant',
  )

  # Default manner from IPA consonant table rows.

  for nasal_consonant in [ph.m, ph.mi, ph.n, ph.ng, ph.nj, ph.nn, ph.ny]:  # pyrefly: ignore[missing-attribute]
    nasal_consonant.update_descriptives(phf.nasal)  # pyrefly: ignore[missing-attribute]
  for stop_consonant in [
      ph.b,  # pyrefly: ignore[missing-attribute]
      ph.c,  # pyrefly: ignore[missing-attribute]
      ph.d,  # pyrefly: ignore[missing-attribute]
      ph.dd,  # pyrefly: ignore[missing-attribute]
      ph.g,  # pyrefly: ignore[missing-attribute]
      ph.gy,  # pyrefly: ignore[missing-attribute]
      ph.j,  # pyrefly: ignore[missing-attribute]
      ph.k,  # pyrefly: ignore[missing-attribute]
      ph.ky,  # pyrefly: ignore[missing-attribute]
      ph.p,  # pyrefly: ignore[missing-attribute]
      ph.q,  # pyrefly: ignore[missing-attribute]
      ph.t,  # pyrefly: ignore[missing-attribute]
      ph.tt,  # pyrefly: ignore[missing-attribute]
      ph.x,  # pyrefly: ignore[missing-attribute]
  ]:
    stop_consonant.update_descriptives(phf.manner.stop)  # pyrefly: ignore[missing-attribute]
  for sibilant_fricative in [
      ph.s,  # pyrefly: ignore[missing-attribute]
      ph.sh,  # pyrefly: ignore[missing-attribute]
      ph.ss,  # pyrefly: ignore[missing-attribute]
      ph.sy,  # pyrefly: ignore[missing-attribute]
      ph.z,  # pyrefly: ignore[missing-attribute]
      ph.zh,  # pyrefly: ignore[missing-attribute]
      ph.zy,  # pyrefly: ignore[missing-attribute]
      ph.zz,  # pyrefly: ignore[missing-attribute]
  ]:
    sibilant_fricative.update_descriptives(phf.manner.sibilant)  # pyrefly: ignore[missing-attribute]
  for nonsibilant_fricative in [
      ph.bh,  # pyrefly: ignore[missing-attribute]
      ph.ch,  # pyrefly: ignore[missing-attribute]
      ph.cha,  # pyrefly: ignore[missing-attribute]
      ph.dh,  # pyrefly: ignore[missing-attribute]
      ph.f,  # pyrefly: ignore[missing-attribute]
      ph.gh,  # pyrefly: ignore[missing-attribute]
      ph.h,  # pyrefly: ignore[missing-attribute]
      ph.ha,  # pyrefly: ignore[missing-attribute]
      ph.hw,  # pyrefly: ignore[missing-attribute]
      ph.hy,  # pyrefly: ignore[missing-attribute]
      ph.jh,  # pyrefly: ignore[missing-attribute]
      ph.kh,  # pyrefly: ignore[missing-attribute]
      ph.ph,  # pyrefly: ignore[missing-attribute]
      ph.qh,  # pyrefly: ignore[missing-attribute]
      ph.sj,  # pyrefly: ignore[missing-attribute]
      ph.th,  # pyrefly: ignore[missing-attribute]
      ph.v,  # pyrefly: ignore[missing-attribute]
      ph.yy,  # pyrefly: ignore[missing-attribute]
  ]:
    nonsibilant_fricative.update_descriptives(phf.manner.non_sibilant)  # pyrefly: ignore[missing-attribute]
  for approximant_consonant in [ph.gu, ph.rru, ph.ru, ph.vu, ph.w, ph.y, ph.yw]:  # pyrefly: ignore[missing-attribute]
    approximant_consonant.update_descriptives(phf.manner.approximant)  # pyrefly: ignore[missing-attribute]
  for tap_consonant in [ph.rd, ph.rt, ph.vt]:  # pyrefly: ignore[missing-attribute]
    tap_consonant.update_descriptives(phf.manner.tap)  # pyrefly: ignore[missing-attribute]
  for trill_consonant in [ph.bb, ph.hh, ph.hho, ph.r, ph.rj]:  # pyrefly: ignore[missing-attribute]
    trill_consonant.update_descriptives(phf.manner.trill)  # pyrefly: ignore[missing-attribute]
  for lateral_fricative in [ph.sl, ph.ssl, ph.zl]:  # pyrefly: ignore[missing-attribute]
    lateral_fricative.update_descriptives(phf.lateral_fricative)  # pyrefly: ignore[missing-attribute]
  for lateral_approximant in [ph.l, ph.lg, ph.ll, ph.lw, ph.ly]:  # pyrefly: ignore[missing-attribute]
    lateral_approximant.update_descriptives(phf.lateral_approximant)  # pyrefly: ignore[missing-attribute]
  for lateral_tap in [ph.rl]:  # pyrefly: ignore[missing-attribute]
    lateral_tap.update_descriptives(
        phf.lateral_approximant  # pyrefly: ignore[missing-attribute]
    ).update_descriptives(phf.manner.tap)  # pyrefly: ignore[missing-attribute]

  # Default place of articulation from IPA consonant table columns.

  for bilabial_consonant in [ph.b, ph.bb, ph.bh, ph.m, ph.p, ph.ph]:  # pyrefly: ignore[missing-attribute]
    bilabial_consonant.update_descriptives(phf.bilabial)  # pyrefly: ignore[missing-attribute]
  for labiodental_consonant in [ph.f, ph.mi, ph.v, ph.vt, ph.vu]:  # pyrefly: ignore[missing-attribute]
    labiodental_consonant.update_descriptives(phf.labiodental)  # pyrefly: ignore[missing-attribute]
  for dental_consonant in [
      ph.dh,  # pyrefly: ignore[missing-attribute]
      ph.th,  # pyrefly: ignore[missing-attribute]
  ]:
    dental_consonant.update_descriptives(phf.dental)  # pyrefly: ignore[missing-attribute]
  for dental_alveolar_consonant in [ph.s, ph.z]:  # pyrefly: ignore[missing-attribute]
    dental_alveolar_consonant.update_descriptives(phf.dental, phf.alveolar)  # pyrefly: ignore[missing-attribute]
  for para_alveolar_consonant in [
      ph.d,  # pyrefly: ignore[missing-attribute]
      ph.l,  # pyrefly: ignore[missing-attribute]
      ph.n,  # pyrefly: ignore[missing-attribute]
      ph.r,  # pyrefly: ignore[missing-attribute]
      ph.rl,  # pyrefly: ignore[missing-attribute]
      ph.rt,  # pyrefly: ignore[missing-attribute]
      ph.ru,  # pyrefly: ignore[missing-attribute]
      ph.sl,  # pyrefly: ignore[missing-attribute]
      ph.t,  # pyrefly: ignore[missing-attribute]
      ph.zl,  # pyrefly: ignore[missing-attribute]
  ]:
    para_alveolar_consonant.update_descriptives(phf.para_alveolar)  # pyrefly: ignore[missing-attribute]
  for postalveolar_consonant in [ph.sh, ph.zh]:  # pyrefly: ignore[missing-attribute]
    postalveolar_consonant.update_descriptives(phf.postalveolar)  # pyrefly: ignore[missing-attribute]
  for retroflex_consonant in [
      ph.dd,  # pyrefly: ignore[missing-attribute]
      ph.ll,  # pyrefly: ignore[missing-attribute]
      ph.nn,  # pyrefly: ignore[missing-attribute]
      ph.rd,  # pyrefly: ignore[missing-attribute]
      ph.rru,  # pyrefly: ignore[missing-attribute]
      ph.ss,  # pyrefly: ignore[missing-attribute]
      ph.ssl,  # pyrefly: ignore[missing-attribute]
      ph.tt,  # pyrefly: ignore[missing-attribute]
      ph.zz,  # pyrefly: ignore[missing-attribute]
  ]:
    retroflex_consonant.update_descriptives(phf.retroflex)  # pyrefly: ignore[missing-attribute]
  for palatal_consonant in [
      ph.gy,  # pyrefly: ignore[missing-attribute]
      ph.hy,  # pyrefly: ignore[missing-attribute]
      ph.ky,  # pyrefly: ignore[missing-attribute]
      ph.ly,  # pyrefly: ignore[missing-attribute]
      ph.ny,  # pyrefly: ignore[missing-attribute]
      ph.sy,  # pyrefly: ignore[missing-attribute]
      ph.y,  # pyrefly: ignore[missing-attribute]
      ph.yw,  # pyrefly: ignore[missing-attribute]
      ph.yy,  # pyrefly: ignore[missing-attribute]
      ph.zy,  # pyrefly: ignore[missing-attribute]
  ]:
    palatal_consonant.update_descriptives(phf.palatal)  # pyrefly: ignore[missing-attribute]
  for velar_consonant in [
      ph.g,  # pyrefly: ignore[missing-attribute]
      ph.gh,  # pyrefly: ignore[missing-attribute]
      ph.gu,  # pyrefly: ignore[missing-attribute]
      ph.hw,  # pyrefly: ignore[missing-attribute]
      ph.k,  # pyrefly: ignore[missing-attribute]
      ph.kh,  # pyrefly: ignore[missing-attribute]
      ph.lg,  # pyrefly: ignore[missing-attribute]
      ph.lw,  # pyrefly: ignore[missing-attribute]
      ph.ng,  # pyrefly: ignore[missing-attribute]
      ph.sj,  # pyrefly: ignore[missing-attribute]
      ph.w,  # pyrefly: ignore[missing-attribute]
  ]:
    velar_consonant.update_descriptives(phf.velar)  # pyrefly: ignore[missing-attribute]
  for uvular_consonant in [ph.j, ph.jh, ph.nj, ph.q, ph.qh, ph.rj]:  # pyrefly: ignore[missing-attribute]
    uvular_consonant.update_descriptives(phf.uvular)  # pyrefly: ignore[missing-attribute]
  for epiglottal_consonant in [ph.c, ph.ch, ph.cha, ph.hh, ph.hho]:  # pyrefly: ignore[missing-attribute]
    epiglottal_consonant.update_descriptives(phf.epiglottal)  # pyrefly: ignore[missing-attribute]
  for glottal_consonant in [ph.h, ph.ha, ph.x]:  # pyrefly: ignore[missing-attribute]
    glottal_consonant.update_descriptives(phf.glottal)  # pyrefly: ignore[missing-attribute]

  # Update voicing for stops and fricatives.

  for voiceless_consonant in [
      ph.c,  # pyrefly: ignore[missing-attribute]
      ph.ch,  # pyrefly: ignore[missing-attribute]
      ph.f,  # pyrefly: ignore[missing-attribute]
      ph.h,  # pyrefly: ignore[missing-attribute]
      ph.hho,  # pyrefly: ignore[missing-attribute]
      ph.hw,  # pyrefly: ignore[missing-attribute]
      ph.hy,  # pyrefly: ignore[missing-attribute]
      ph.k,  # pyrefly: ignore[missing-attribute]
      ph.kh,  # pyrefly: ignore[missing-attribute]
      ph.ky,  # pyrefly: ignore[missing-attribute]
      ph.p,  # pyrefly: ignore[missing-attribute]
      ph.ph,  # pyrefly: ignore[missing-attribute]
      ph.q,  # pyrefly: ignore[missing-attribute]
      ph.qh,  # pyrefly: ignore[missing-attribute]
      ph.s,  # pyrefly: ignore[missing-attribute]
      ph.sh,  # pyrefly: ignore[missing-attribute]
      ph.sj,  # pyrefly: ignore[missing-attribute]
      ph.sl,  # pyrefly: ignore[missing-attribute]
      ph.ss,  # pyrefly: ignore[missing-attribute]
      ph.ssl,  # pyrefly: ignore[missing-attribute]
      ph.sy,  # pyrefly: ignore[missing-attribute]
      ph.t,  # pyrefly: ignore[missing-attribute]
      ph.th,  # pyrefly: ignore[missing-attribute]
      ph.tt,  # pyrefly: ignore[missing-attribute]
      ph.x,  # pyrefly: ignore[missing-attribute]
  ]:
    voiceless_consonant.update_descriptives(phf.voicing.voiceless)  # pyrefly: ignore[missing-attribute]
  for voiced_consonant in [
      ph.b,  # pyrefly: ignore[missing-attribute]
      ph.bh,  # pyrefly: ignore[missing-attribute]
      ph.cha,  # pyrefly: ignore[missing-attribute]
      ph.d,  # pyrefly: ignore[missing-attribute]
      ph.dd,  # pyrefly: ignore[missing-attribute]
      ph.dh,  # pyrefly: ignore[missing-attribute]
      ph.g,  # pyrefly: ignore[missing-attribute]
      ph.gh,  # pyrefly: ignore[missing-attribute]
      ph.gy,  # pyrefly: ignore[missing-attribute]
      ph.ha,  # pyrefly: ignore[missing-attribute]
      ph.j,  # pyrefly: ignore[missing-attribute]
      ph.jh,  # pyrefly: ignore[missing-attribute]
      ph.v,  # pyrefly: ignore[missing-attribute]
      ph.yy,  # pyrefly: ignore[missing-attribute]
      ph.z,  # pyrefly: ignore[missing-attribute]
      ph.zh,  # pyrefly: ignore[missing-attribute]
      ph.zl,  # pyrefly: ignore[missing-attribute]
      ph.zy,  # pyrefly: ignore[missing-attribute]
      ph.zz,  # pyrefly: ignore[missing-attribute]
  ]:
    voiced_consonant.update_descriptives(phf.voicing.voiced)  # pyrefly: ignore[missing-attribute]

  # Add secondary articulations.

  for labialized_consonant in [ph.hw, ph.lw, ph.w, ph.yw]:  # pyrefly: ignore[missing-attribute]
    labialized_consonant.update_descriptives(phf.labialization.labialized)  # pyrefly: ignore[missing-attribute]
  for palatalized_consonant in [ph.sj]:  # pyrefly: ignore[missing-attribute]
    palatalized_consonant.update_descriptives(phf.palatalization.heavy)  # pyrefly: ignore[missing-attribute]
  return ph.sync_atomics()  # pyrefly: ignore[bad-return]


PHONEMES = _phoneme_inventory()
