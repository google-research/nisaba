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

"""English spellout deromanization."""

import itertools

import pynini as pyn
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import type_op as ty


# TODO(): Add Language to PhonologicalSymbol descriptive features and
# use it instead of this enum.
class Language(ty.TempStrEnum):
  """List of languages."""

  BN = 'bn'
  GU = 'gu'
  HI = 'hi'
  KN = 'kn'
  ML = 'ml'
  MR = 'mr'
  OR = 'or'
  PA = 'pa'
  SD = 'sd'
  SI = 'si'
  TA = 'ta'
  TE = 'te'
  UR = 'ur'


# TODO: Use Script from grapheme.py instead of this enum.
class Script(ty.TempStrEnum):
  """List of scripts."""

  BENG = 'beng'
  DEVA = 'deva'
  GUJR = 'gujr'
  GURU = 'guru'
  ORYA = 'orya'
  SINH = 'sinh'
  KNDA = 'knda'
  MLYM = 'mlym'
  TAML = 'taml'
  TELU = 'telu'
  ARAB = 'arab'


class _EnLetterSpellOut(i.Inventory):
  """English letter spellouts."""

  def __init__(
      self,
      letter: str,
      bn_beng: str,
      gu_gujr: str,
      hi_deva: str,
      kn_knda: str,
      ml_mlym: str,
      mr_deva: str,
      or_orya: str,
      pa_guru: str,
      sd_arab: str,
      si_sinh: str,
      ta_taml: str,
      te_telu: str,
      ur_arab: str,
  ):
    super().__init__(letter.lower())
    self.letter = self.alias
    self.bn_beng = bn_beng
    self.gu_gujr = gu_gujr
    self.hi_deva = hi_deva
    self.kn_knda = kn_knda
    self.ml_mlym = ml_mlym
    self.mr_deva = mr_deva
    self.or_orya = or_orya
    self.pa_guru = pa_guru
    self.sd_arab = sd_arab
    self.si_sinh = si_sinh
    self.ta_taml = ta_taml
    self.te_telu = te_telu
    self.ur_arab = ur_arab

  class Separator(ty.TempStrEnum):
    SPACE = ' '
    ZWNJ = '‌'  # U+200C


def _spellout_inventory() -> i.Inventory:
  """Returns an inventory of English letter spellings in various scripts."""
  spellouts = [
      (
          'a',
          'এ',  # bn_beng
          'એ',  # gu_gujr
          'ए',  # hi_deva
          'ಎ',  # kn_knda
          'എ',  # ml_mlym
          'ए',  # mr_deva
          'ଏ',  # or_orya
          'ਏ',  # pa_guru
          'اي',  # sd_arab
          'ඒ',  # si_sinh
          'ஏ',  # ta_taml
          'ఎ',  # te_telu
          'اے',  # ur_arab
      ),
      (
          'b',
          'বি',  # bn_beng
          'બી',  # gu_gujr
          'बी',  # hi_deva
          'ಬಿ',  # kn_knda
          'ബി',  # ml_mlym
          'बी',  # mr_deva
          'ବି',  # or_orya
          'ਬੀ',  # pa_guru
          'بي',  # sd_arab
          'බී',  # si_sinh
          'பி',  # ta_taml
          'బి',  # te_telu
          'بی',  # ur_arab
      ),
      (
          'c',
          'সি',  # bn_beng
          'સી',  # gu_gujr
          'सी',  # hi_deva
          'ಸಿ',  # kn_knda
          'സി',  # ml_mlym
          'सी',  # mr_deva
          'ସି',  # or_orya
          'ਸੀ',  # pa_guru
          'سي',  # sd_arab
          'සී',  # si_sinh
          'சி',  # ta_taml
          'సి',  # te_telu
          'سی',  # ur_arab
      ),
      (
          'd',
          'ডি',  # bn_beng
          'ડી',  # gu_gujr
          'डी',  # hi_deva
          'ಡಿ',  # kn_knda
          'ഡി',  # ml_mlym
          'डी',  # mr_deva
          'ଡି',  # or_orya
          'ਡੀ',  # pa_guru
          'ڊي',  # sd_arab
          'ඩී',  # si_sinh
          'டி',  # ta_taml
          'డి',  # te_telu
          'ڈی',  # ur_arab
      ),
      (
          'e',
          'ই',  # bn_beng
          'ઈ',  # gu_gujr
          'ई',  # hi_deva
          'ಇ',  # kn_knda
          'ഇ',  # ml_mlym
          'ई',  # mr_deva
          'ଇ',  # or_orya
          'ਈ',  # pa_guru
          'اي',  # sd_arab
          'ඊ',  # si_sinh
          'இ',  # ta_taml
          'ఇ',  # te_telu
          'ای',  # ur_arab
      ),
      (
          'f',
          'এফ',  # bn_beng
          'એફ',  # gu_gujr
          'एफ़',  # hi_deva
          'ಎಫ್‌',  # kn_knda
          'എഫ്‌',  # ml_mlym
          'एफ',  # mr_deva
          'ଏଫ',  # or_orya
          'ਐੱਫ਼',  # pa_guru
          'ايف',  # sd_arab
          'එෆ්',  # si_sinh
          'எஃப்',  # ta_taml
          'ఎఫ్‌',  # te_telu
          'ایف',  # ur_arab
      ),
      (
          'g',
          'জি',  # bn_beng
          'જી',  # gu_gujr
          'जी',  # hi_deva
          'ಜಿ',  # kn_knda
          'ജി',  # ml_mlym
          'जी',  # mr_deva
          'ଜି',  # or_orya
          'ਜੀ',  # pa_guru
          'جي',  # sd_arab
          'ජී',  # si_sinh
          'ஜி',  # ta_taml
          'జి',  # te_telu
          'جی',  # ur_arab
      ),
      (
          'h',
          'এইচ',  # bn_beng
          'એચ',  # gu_gujr
          'एच',  # hi_deva
          'ಎಚ್‌',  # kn_knda
          'എച്ച്‌',  # ml_mlym
          'एच',  # mr_deva
          'ଏଇଚ',  # or_orya
          'ਐੱਚ',  # pa_guru
          'ايڇ',  # sd_arab
          'එච්',  # si_sinh
          'ஹெச்',  # ta_taml
          'హెచ్‌',  # te_telu
          'ایچ',  # ur_arab
      ),
      (
          'i',
          'আই',  # bn_beng
          'આઇ',  # gu_gujr
          'आई',  # hi_deva
          'ಐ',  # kn_knda
          'ഐ',  # ml_mlym
          'आय',  # mr_deva
          'ଆଇ',  # or_orya
          'ਆਈ',  # pa_guru
          'آءِ',  # sd_arab
          'අයි',  # si_sinh
          'ஐ',  # ta_taml
          'ఐ',  # te_telu
          'آئی',  # ur_arab
      ),
      (
          'j',
          'জে',  # bn_beng
          'જે',  # gu_gujr
          'जे',  # hi_deva
          'ಜೆ',  # kn_knda
          'ജെ',  # ml_mlym
          'जे',  # mr_deva
          'ଜେ',  # or_orya
          'ਜੇ',  # pa_guru
          'جي',  # sd_arab
          'ජේ',  # si_sinh
          'ஜே',  # ta_taml
          'జె',  # te_telu
          'جے',  # ur_arab
      ),
      (
          'k',
          'কে',  # bn_beng
          'કે',  # gu_gujr
          'के',  # hi_deva
          'ಕೆ',  # kn_knda
          'കെ',  # ml_mlym
          'के',  # mr_deva
          'କେ',  # or_orya
          'ਕੇ',  # pa_guru
          'ڪي',  # sd_arab
          'කේ',  # si_sinh
          'கே',  # ta_taml
          'కె',  # te_telu
          'کے',  # ur_arab
      ),
      (
          'l',
          'এল',  # bn_beng
          'એલ',  # gu_gujr
          'एल',  # hi_deva
          'ಎಲ್‌',  # kn_knda
          'എൽ',  # ml_mlym
          'एल',  # mr_deva
          'ଏଲ',  # or_orya
          'ਐੱਲ',  # pa_guru
          'ايل',  # sd_arab
          'එල්',  # si_sinh
          'எல்',  # ta_taml
          'ఎల్‌',  # te_telu
          'ایل',  # ur_arab
      ),
      (
          'm',
          'এম',  # bn_beng
          'એમ',  # gu_gujr
          'एम',  # hi_deva
          'ಎಂ',  # kn_knda
          'എം',  # ml_mlym
          'एम',  # mr_deva
          'ଏମ',  # or_orya
          'ਐੱਮ',  # pa_guru
          'ايم',  # sd_arab
          'එම්',  # si_sinh
          'எம்',  # ta_taml
          'ఎం',  # te_telu
          'ایم',  # ur_arab
      ),
      (
          'n',
          'এন',  # bn_beng
          'એન',  # gu_gujr
          'एन',  # hi_deva
          'ಎನ್‌',  # kn_knda
          'എൻ',  # ml_mlym
          'एन',  # mr_deva
          'ଏନ',  # or_orya
          'ਐੱਨ',  # pa_guru
          'اين',  # sd_arab
          'එන්',  # si_sinh
          'என்',  # ta_taml
          'ఎన్‌',  # te_telu
          'این',  # ur_arab
      ),
      (
          'o',
          'ও',  # bn_beng
          'ઓ',  # gu_gujr
          'ओ',  # hi_deva
          'ಒ',  # kn_knda
          'ഒ',  # ml_mlym
          'ओ',  # mr_deva
          'ଓ',  # or_orya
          'ਓ',  # pa_guru
          'او',  # sd_arab
          'ඕ',  # si_sinh
          'ஓ',  # ta_taml
          'ఒ',  # te_telu
          'او',  # ur_arab
      ),
      (
          'p',
          'পি',  # bn_beng
          'પી',  # gu_gujr
          'पी',  # hi_deva
          'ಪಿ',  # kn_knda
          'പി',  # ml_mlym
          'पी',  # mr_deva
          'ପି',  # or_orya
          'ਪੀ',  # pa_guru
          'پي',  # sd_arab
          'පී',  # si_sinh
          'பி',  # ta_taml
          'పి',  # te_telu
          'پی',  # ur_arab
      ),
      (
          'q',
          'কিউ',  # bn_beng
          'ક્યુ',  # gu_gujr
          'क्यू',  # hi_deva
          'ಕ್ಯೂ',  # kn_knda
          'ക്യു',  # ml_mlym
          'क्यू',  # mr_deva
          'କିଉ',  # or_orya
          'ਕਿਊ',  # pa_guru
          'کيو',  # sd_arab
          'කියු',  # si_sinh
          'கியூ',  # ta_taml
          'క్యు',  # te_telu
          'کیو',  # ur_arab
      ),
      (
          'r',
          'আর',  # bn_beng
          'આર',  # gu_gujr
          'आर',  # hi_deva
          'ಆರ್‌',  # kn_knda
          'ആർ',  # ml_mlym
          'आर',  # mr_deva
          'ଆର',  # or_orya
          'ਆਰ',  # pa_guru
          'آر',  # sd_arab
          'ආර්',  # si_sinh
          'ஆர்',  # ta_taml
          'ఆర్‌',  # te_telu
          'آر',  # ur_arab
      ),
      (
          's',
          'এস',  # bn_beng
          'એસ',  # gu_gujr
          'एस',  # hi_deva
          'ಎಸ್‌',  # kn_knda
          'എസ്‌',  # ml_mlym
          'एस',  # mr_deva
          'ଏସ',  # or_orya
          'ਐੱਸ',  # pa_guru
          'ايس',  # sd_arab
          'එස්',  # si_sinh
          'எஸ்',  # ta_taml
          'ఎస్‌',  # te_telu
          'ایس',  # ur_arab
      ),
      (
          't',
          'টি',  # bn_beng
          'ટી',  # gu_gujr
          'टी',  # hi_deva
          'ಟಿ',  # kn_knda
          'ടി',  # ml_mlym
          'टी',  # mr_deva
          'ଟି',  # or_orya
          'ਟੀ',  # pa_guru
          'ٽي',  # sd_arab
          'ටී',  # si_sinh
          'டி',  # ta_taml
          'టి',  # te_telu
          'ٹی',  # ur_arab
      ),
      (
          'u',
          'ইউ',  # bn_beng
          'યુ',  # gu_gujr
          'यू',  # hi_deva
          'ಯು',  # kn_knda
          'യു',  # ml_mlym
          'यू',  # mr_deva
          'ଇଉ',  # or_orya
          'ਯੂ',  # pa_guru
          'يو',  # sd_arab
          'යූ',  # si_sinh
          'யூ',  # ta_taml
          'యు',  # te_telu
          'یو',  # ur_arab
      ),
      (
          'v',
          'ভি',  # bn_beng
          'વી',  # gu_gujr
          'वी',  # hi_deva
          'ವಿ',  # kn_knda
          'വി',  # ml_mlym
          'व्ही',  # mr_deva
          'ଭି',  # or_orya
          'ਵੀ',  # pa_guru
          'وي',  # sd_arab
          'වී',  # si_sinh
          'வி',  # ta_taml
          'వి',  # te_telu
          'وی',  # ur_arab
      ),
      (
          'w',
          'ডাবলিউ',  # bn_beng
          'ડબ્લ્યુ',  # gu_gujr
          'डब्ल्यू',  # hi_deva
          'ಡಬ್ಲೂ',  # kn_knda
          'ഡബ്ല്യു',  # ml_mlym
          'डब्ल्यू',  # mr_deva
          'ଡବ୍ଲୁ',  # or_orya
          'ਡੱਬਲਿਊ',  # pa_guru
          'ڊبليو',  # sd_arab
          'ඩබ්ලිව්',  # si_sinh
          'டபிள்யூ',  # ta_taml
          'డబ్ల్యు',  # te_telu
          'ڈبلیو',  # ur_arab
      ),
      (
          'x',
          'এক্স',  # bn_beng
          'એક્સ',  # gu_gujr
          'एक्स',  # hi_deva
          'ಎಕ್ಸ್‌',  # kn_knda
          'എക്സ്‌',  # ml_mlym
          'एक्स',  # mr_deva
          'ଏକ୍ସ',  # or_orya
          'ਐੱਕਸ',  # pa_guru
          'ايڪس',  # sd_arab
          'එක්ස්',  # si_sinh
          'எக்ஸ்',  # ta_taml
          'ఎక్స్‌',  # te_telu
          'ایکس',  # ur_arab
      ),
      (
          'y',
          'ওয়াই',  # bn_beng
          'વાય',  # gu_gujr
          'वाई',  # hi_deva
          'ವೈ',  # kn_knda
          'വൈ',  # ml_mlym
          'वाय',  # mr_deva
          'ୱାଇ',  # or_orya
          'ਵਾਈ',  # pa_guru
          'وائي',  # sd_arab
          'වයි',  # si_sinh
          'ஒய்',  # ta_taml
          'వై',  # te_telu
          'وائے',  # ur_arab
      ),
      (
          'z',
          'জেড',  # bn_beng
          'ઝેડ',  # gu_gujr
          'ज़ेड',  # hi_deva
          'ಝಡ್‌',  # kn_knda
          'ഇസെഡ്‌',  # ml_mlym
          'झेड',  # mr_deva
          'ଜେଡ',  # or_orya
          'ਜ਼ੈਡ',  # pa_guru
          'زيڊ',  # sd_arab
          'සඩ්',  # si_sinh
          'இஜட்',  # ta_taml
          'జడ్‌',  # te_telu
          'زیڈ',  # ur_arab
      ),
  ]
  return i.Inventory.from_list(
      [_EnLetterSpellOut(*spellout) for spellout in spellouts]
  )


_SPELLOUTS = _spellout_inventory()


def _get_spellout(
    letter: _EnLetterSpellOut, language: Language, script: Script
) -> str:
  spellout = getattr(letter, language.value + '_' + script.value, letter.letter)
  if script == Script.ARAB:
    spellout += _EnLetterSpellOut.Separator.SPACE.value
  return spellout


def _separated(
    fst: pyn.Fst, spellouts: i.Inventory, seperator: _EnLetterSpellOut.Separator
) -> pyn.Fst:
  """Composes the FST with word-final separator deletion."""
  sigma = set(
      itertools.chain.from_iterable(spellout.value for spellout in spellouts)
  )
  delete = pyn.cdrewrite(
      pyn.cross(seperator.value, ''),
      '',
      '[EOS]',
      fl.FstList.accep(*sigma).union_star(),
  ).optimize()
  return (fst @ delete).optimize()


def speller(language: Language, script: Script) -> pyn.Fst:
  """Builds a speller FST for the given language and script."""
  has_zwnj = [Script.KNDA, Script.MLYM, Script.TELU]
  spellouts = i.Inventory.from_list([
      ty.Thing(
          letter.letter, value_from=_get_spellout(letter, language, script)
      )
      for letter in _SPELLOUTS
  ])
  fst = fl.FstList.cross(*[
      (pyn.union(letter.alias, letter.alias.upper()), letter.value)
      for letter in spellouts
  ]).union_star()
  if script == Script.ARAB:
    return _separated(fst, spellouts, _EnLetterSpellOut.Separator.SPACE)
  if script in has_zwnj:
    return _separated(fst, spellouts, _EnLetterSpellOut.Separator.ZWNJ)
  return fst
