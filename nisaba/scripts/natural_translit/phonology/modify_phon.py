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

"""Functions for deriving and composing Phons."""

import copy
import pynini as pyn
from nisaba.scripts.natural_translit.phonology import feature
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import type_op as ty

f = feature.FEATURE_INVENTORY


def modifier_phon(mod_alias: str, txn: str, ftr: list[str], ipa: str) -> p.Phon:
  return p.Phon.base(txn, ftr, ipa, alias=mod_alias)


def qualified_modifier(modifier: p.Phon, qualifier: p.Phon, ipa: str) -> p.Phon:
  """Derives a modifier feature with a qualifier."""
  return modifier_phon(
      modifier.alias + qualifier.txn.upper(),
      modifier.txn + qualifier.txn,
      modifier.ftr + qualifier.ftr,
      ipa
  )

COMBINER = [modifier_phon('CMB', '+', [f.composite], '͡')]

MODIFIER_FEATURE = [modifier_phon(*args) for args in [
    ['DVC', 'o', [f.devoiced], '̥'],  # devoiced
    ['NPL', 'e', [f.nonpulmonic], '`'],  # nonpulmonic
    ['DUR', ':', [f.duration], 'ː'],
    ['STR', '*', [f.stress], ''],
    ['TPT', '^', [f.pitch], ''],
    ['TCN', '&', [f.contour], ''],
    ['INT', '!', [f.intonation], ''],
]]
_M = p.phon_inventory(MODIFIER_FEATURE)

FEATURE_QUALIFIER = [modifier_phon(*args) for args in [
    ['TOP', 't', [f.top], ''],
    ['HGH', 'h', [f.high], ''],
    ['MDL', 'm', [f.middle], ''],
    ['LOW', 'w', [f.low], ''],
    ['BTM', 'b', [f.bottom], ''],
    ['RSN', 'r', [f.rising], ''],
    ['FLN', 'f', [f.falling], ''],
    ['TRP', 'k', [f.interrupt], ''],
]]
_F = p.phon_inventory(FEATURE_QUALIFIER)


def duration(value: p.Phon, ipa: str) -> p.Phon:
  return qualified_modifier(_M.DUR, value, ipa)

DURATION = [duration(*args) for args in [
    [_F.BTM, '̆'],
    [_F.MDL, 'ˑ'],
    [_F.HGH, 'ː'],
    [_F.TOP, 'ːː']
]]

MOD = p.phon_inventory(
    COMBINER + MODIFIER_FEATURE + FEATURE_QUALIFIER + DURATION
)

# Derivation functions


def derive_with_suffix(
    phon: p.Phon,
    modifier: p.Phon,
    new_tr: pyn.Fst = pyn.Fst()
) -> p.Phon:
  """Makes a new Phon from a phoneme Phon and a suffix Phon.

  TODO: Split phonemes, modifying features, and standalone features into
  distinct classes.

  Args:
    phon: A phoneme Phon to be modified.
    modifier: A suffix Phon.
    new_tr: The default translit for the new Phon. If None, the new entry will
    be a copy of the base entry of the phon arg.

  Returns:
    Phon

  Given:
  (alias='B', txn='b', ftr=[stop, vcd], ph={b}, ipa='b', {'base': tr.B})
  (alias='DVC', txn='o', ftr=[dvc], ph={o}, ipa='̥', {'base': tr.DEL})

  Following call:
  ```
  derive_with_suffix(ph.B, ph.DVC, tr.P)
  ```
  will return:
  ```
  Phon(
    alias='BO', txn='bo', ftr=[stop, dvc], ph={bo}, ipa='b̥',
    tr_dict={'base': tr.B 'dvc': tr.P}
  )
  ```
  """
  txn = phon.txn + modifier.txn
  return p.Phon(
      phon.alias + modifier.txn.upper(),
      txn,
      phon.ftr + modifier.ftr,
      al.enclose_phoneme(txn),
      phon.ipa + modifier.ipa,
      phon.tr_dict | p.new_tr(modifier.ftr[0], new_tr, phon.tr_dict['base'])
  )


def devoiced(phon: p.Phon) -> p.Phon:
  """Voiceless derivation for prototypically voiced Phons."""
  new_phon = copy.deepcopy(phon)
  new_phon.ftr.remove(f.voiced)
  return derive_with_suffix(new_phon, MOD.DVC)


def nonpulmonic(phon: p.Phon) -> p.Phon:
  """Ejective and implosive derivation."""
  return derive_with_suffix(phon, MOD.NPL)


def stress(value: p.Phon, ipa: str) -> p.Phon:
  return qualified_modifier(MOD.STR, value, ipa)


def pitch(value: p.Phon, ipa: str) -> p.Phon:
  return qualified_modifier(MOD.TPT, value, ipa)


def contour(value: p.Phon, ipa: str) -> p.Phon:
  return qualified_modifier(MOD.TCN, value, ipa)


def intonation(value: p.Phon, ipa: str) -> p.Phon:
  return qualified_modifier(MOD.INT, value, ipa)


# Composition functions


def compose(
    phons: list[p.Phon],
    ftr: str,
    new_tr: ty.FstIterable = ty.UNSPECIFIED,
    alt_tr_dict: ty.DictOrNothing = ty.UNSPECIFIED,
) -> p.Phon:
  """Makes a composite Phon.

  Args:
    phons: The list of Phons to be composed.
    ftr: The class of the new Phon. Set as the first element of the new ftr.
    new_tr: The default translit of the composite Phon. If None, it will be the
      same as the new base tr, which is the concatenation of the base tr_dict of
      the component Phons.
    alt_tr_dict: A dictionary of alternative transliterations.

  Returns:
    Phon

  Given:
  (alias='A', txn='a', ftr=['vowel'], ph={a}, ipa='a', {'base': tr.A})
  (alias='U', txn='u', ftr=['vowel'], ph={u}, ipa='u', {'base': tr.U})
  (alias='CMB', txn='+', ftr=['composite'], ph={+}, ipa='͡', {'base': tr.DEL})

  Following call:
  ```
  compose(
      'A_U', [ph.A, ph.U], ph.CMB, 'diph', tr.S_AU,
      {'semi': tr.S_AW 'mono': tr.O}
  )
  ```
  will return:
  ```
  Phon(
    alias='A_U', txn='a+u', ftr=['diph', 'vowel', 'vowel'],
    ph={a}{+}{u}, ipa='a͡u',
    tr_dict={
        'base': tr.A + tr.U, 'diph': tr.S_AU, 'semi': tr.S_AW, 'mono': tr.O
    },
    cmp=[ph.A, ph.U]
  )
  ```
  """
  cmp_list = []
  for phon in phons:
    cmp_list += phon.cmp
  composed = p.Phon(
      cmp_list[0].alias,
      cmp_list[0].txn,
      [ftr] + cmp_list[0].ftr,
      cmp_list[0].ph,
      cmp_list[0].ipa,
      cmp=[cmp_list[0]],
  )
  base_tr = cmp_list[0].tr_dict['base'].copy()
  for cmp in cmp_list[1:]:
    composed.alias += '_' + cmp.alias
    composed.txn += MOD.CMB.txn + cmp.txn
    composed.ftr += cmp.ftr
    composed.ph = composed.ph + MOD.CMB.ph + cmp.ph
    composed.ipa += MOD.CMB.ipa + cmp.ipa
    composed.cmp.append(cmp)
    base_tr = base_tr + cmp.tr_dict['base']
  composed.tr_dict = {'base': base_tr} | p.new_tr(ftr, new_tr, base_tr)
  if isinstance(alt_tr_dict, dict):
    composed.tr_dict |= alt_tr_dict
  return composed


def diphthong(
    vowels: list[p.Phon],
    diph: pyn.FstLike,
    semi: ty.FstIterable = ty.UNSPECIFIED,
    mono: ty.FstIterable = ty.UNSPECIFIED,
) -> p.Phon:
  """Composes a diphthong."""
  tr_dict = {}
  if isinstance(semi, pyn.Fst):
    tr_dict['semivowel'] = semi
  if isinstance(mono, pyn.Fst):
    tr_dict['monophthong'] = mono
  return compose(vowels, f.diphthong, diph, tr_dict)


def affricate(cons: list[p.Phon], affr: pyn.FstLike) -> p.Phon:
  """Composes an affricate."""
  return compose(cons, f.affricate, affr)


def ls_affricate(
    stop: p.Phon, frics: list[p.Phon], tr: pyn.FstLike
) -> list[p.Phon]:
  """Composes list of affricates and their geminations."""
  affr = []
  for fric in frics:
    affr += [affricate([stop, fric], tr)]
    if f.voiceless in fric.ftr:
      ejc = nonpulmonic(fric)
      affr += [affricate([stop, ejc], tr)]
  return affr


def click(stop: p.Phon, release: p.Phon) -> p.Phon:
  """Composes a click Phon from a stop and a click release."""
  return compose([stop, release], f.coarticulated)


def ls_click(stops: list[p.Phon], releases: list[p.Phon]) -> list[p.Phon]:
  """Composes list of click co-articulations from stops and releases."""
  clicks = []
  for stop in stops:
    clicks += [click(stop, release) for release in releases]
  return clicks
