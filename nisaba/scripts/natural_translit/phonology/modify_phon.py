# Copyright 2022 Nisaba Authors.
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
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import feature
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls

f = feature.FEATURE_INVENTORY


def modifier_phon(
    mod_alias: str,
    txn: str,
    ftr: [str],
    ipa: str
) -> p.Phon:
  return p.base_phon(txn, ftr, ipa, alias=mod_alias)


def qualified_modifier(
    modifier: p.Phon,
    qualifier: p.Phon,
    ipa: str
) -> [p.Phon]:
  """Derives a modifier feature with a qualifier."""
  return modifier_phon(
      modifier.alias + qualifier.txn.upper(),
      modifier.txn + qualifier.txn,
      modifier.ftr + qualifier.ftr,
      ipa
  )

COMBINER = [modifier_phon('CMB', '+', [f.composite], '͡')]

MODIFIER_FEATURE = ls.apply_foreach(modifier_phon, [
    # TODO: move long to suprasegmental as a degree of duration.
    ['LONG', '_l', [f.long], 'ː'],
    ['DVC', 'o', [f.devoiced], '̥'],  # devoiced
    ['NPL', 'e', [f.nonpulmonic], '`'],  # nonpulmonic
    ['STR', '*', [f.stress], ''],
    ['TPT', '^', [f.pitch], ''],
    ['TCN', '&', [f.contour], ''],
    ['INT', '!', [f.intonation], ''],
])

FEATURE_QUALIFIER = ls.apply_foreach(modifier_phon, [
    ['TOP', 't', [f.top], ''],
    ['HGH', 'h', [f.high], ''],
    ['MDL', 'm', [f.middle], ''],
    ['LOW', 'w', [f.low], ''],
    ['BTM', 'b', [f.bottom], ''],
    ['RSN', 'r', [f.rising], ''],
    ['FLN', 'f', [f.falling], ''],
    ['TRP', 'k', [f.interrupt], ''],
])

MOD = p.phon_inventory(COMBINER + MODIFIER_FEATURE + FEATURE_QUALIFIER)

# Derivation functions


def derive_with_suffix(
    phon: p.Phon,
    modifier: p.Phon,
    new_tr: pyn.FstLike = None
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
  (alias='A', txn='a', ftr=['vowel'], ph={a}, ipa='a', {'base': tr.A})
  (alias='LONG', txn='_l', ftr=['long'], ph={_l}, ipa=':', {'base': tr.DEL})

  Following call:
  ```
  derive_with_suffix(ph.A, ph.LONG, tr.S_AA)
  ```
  will return:
  ```
  Phon(
    alias='A_L', txn='a_l', ftr=['vowel', 'long'], ph={a_l}, ipa='a:',
    tr_dict={'base': tr.A 'long': tr.S_AA}, cmp=[ph.A, ph.LONG]
  )
  ```
  """
  alias = phon.alias + modifier.txn.upper()
  txn = phon.txn + modifier.txn
  ftr = phon.ftr + modifier.ftr
  ph = al.enclose_phoneme(txn)
  ipa = phon.ipa + modifier.ipa
  tr_dict = phon.tr_dict.copy()
  tr_dict.update(p.new_tr(modifier.ftr[0], new_tr, phon.tr_dict['base']))
  return p.Phon(alias, txn, ftr, ph, ipa, tr_dict, cmp=None)


# TODO: Revisit default tr for substring bases.
def long(phon: p.Phon, long_tr: pyn.FstLike = None) -> p.Phon:
  """Derives a long Phon."""
  if not long_tr:
    long_tr = ltn.double_substring_tr(phon.tr_dict['base'])
  return derive_with_suffix(
      phon,
      MOD.LONG,
      long_tr)


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
    phons: [p.Phon],
    ftr: str,
    new_tr: str = None,
    alt_tr_dict: dict[str] = None,
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
    cmp_list.extend(p.get_cmp_list(phon))
  alias = cmp_list[0].alias
  new_txn = cmp_list[0].txn
  new_ftr = [ftr] + cmp_list[0].ftr
  new_ph = cmp_list[0].ph
  new_ipa = cmp_list[0].ipa
  new_base_tr = cmp_list[0].tr_dict['base'].copy()
  new_cmp = [cmp_list[0]]
  for cmp in cmp_list[1:]:
    alias += '_' + cmp.alias
    new_txn += MOD.CMB.txn + cmp.txn
    new_ftr.extend(cmp.ftr)
    new_ph = new_ph + MOD.CMB.ph + cmp.ph
    new_ipa += MOD.CMB.ipa + cmp.ipa
    new_base_tr += cmp.tr_dict['base']
    new_cmp.append(cmp)
  new_tr_dict = {'base': new_base_tr}
  new_tr_dict.update(p.new_tr(ftr, new_tr, new_base_tr))
  if alt_tr_dict:
    new_tr_dict.update(alt_tr_dict)
  return p.Phon(alias, new_txn, new_ftr, new_ph, new_ipa, new_tr_dict, new_cmp)


def diphthong(
    vowels: [p.Phon], diph: pyn.FstLike,
    semi: pyn.FstLike = None, mono: pyn.FstLike = None
) -> p.Phon:
  """Composes a diphthong."""
  tr_dict = {}
  if semi:
    tr_dict['semivowel'] = semi
  if mono:
    tr_dict['monophthong'] = mono
  return compose(vowels, f.diphthong, diph, tr_dict)


def affricate(
    cons: [p.Phon], affr: pyn.FstLike
) -> p.Phon:
  """Composes an affricate."""
  return compose(cons, f.affricate, affr)


def ls_affricate(
    stop: p.Phon, frics: [p.Phon], tr: pyn.FstLike
) -> [p.Phon]:
  """Composes list of affricates and their geminations."""
  affr = []
  gemm = long(stop)
  g_tr = ltn.double_substring_tr(tr)
  for fric in frics:
    affr += [affricate([stop, fric], tr), affricate([gemm, fric], g_tr)]
    if f.voiceless in fric.ftr:
      ejc = nonpulmonic(fric)
      affr += [affricate([stop, ejc], tr), affricate([gemm, ejc], g_tr)]
  return affr


def click(
    stop: p.Phon, release: p.Phon
) -> p.Phon:
  """Composes a click Phon from a stop and a click release."""
  return compose([stop, release], f.coarticulated)


def ls_click(stops: [p.Phon], releases: [p.Phon]) -> [p.Phon]:
  """Composes list of click co-articulations from stops and releases."""
  clicks = []
  for stop in stops:
    clicks += [click(stop, release) for release in releases]
  return clicks
