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

import pynini as pyn
from nisaba.scripts.natural_translit.latin import ltn_inventory as ltn
from nisaba.scripts.natural_translit.phonology import phon as p
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import list_op as ls


def modifier_phon(
    mod_alias: str,
    txn: str,
    ftr: [str],
    ipa: str
) -> p.Phon:
  return p.base_phon(txn, ftr, ipa, alias=mod_alias)

COMBINER = [modifier_phon('CMB', '+', ['composite'], '͡')]

MODIFIER_FEATURE = ls.apply_foreach(modifier_phon, [
    ['LONG', '_l', ['long'], 'ː'],
])

_MOD = p.phon_inventory(COMBINER + MODIFIER_FEATURE)

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
  cmp = p.get_cmp_list(phon) + p.get_cmp_list(modifier)
  return p.Phon(alias, txn, ftr, ph, ipa, tr_dict, cmp)


# TODO: Revisit default tr for substring bases.
def long(phon: p.Phon, long_tr: pyn.FstLike = None) -> p.Phon:
  """Derives a long Phon."""
  if not long_tr:
    long_tr = ltn.double_substring_tr(phon.tr_dict['base'])
  return derive_with_suffix(
      phon,
      _MOD.LONG,
      long_tr)


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
  new_base_tr = cmp_list[0].tr_dict['base']
  new_cmp = [cmp_list[0]]
  for cmp in cmp_list[1:]:
    alias += '_' + cmp.alias
    new_txn += _MOD.CMB.txn + cmp.txn
    new_ftr.extend(cmp.ftr)
    new_ph = new_ph + _MOD.CMB.ph + cmp.ph
    new_ipa += _MOD.CMB.ipa + cmp.ipa
    new_base_tr += cmp.tr_dict['base']
    new_cmp.append(cmp)
  new_tr_dict = {'base': new_base_tr}
  new_tr_dict.update(p.new_tr(ftr, new_tr, new_base_tr))
  if alt_tr_dict:
    new_tr_dict.update(alt_tr_dict)
  return p.Phon(alias, new_txn, new_ftr, new_ph, new_ipa, new_tr_dict, new_cmp)


def diphthong(
    vowels: [p.Phon], diph: pyn.FstLike,
    semi: pyn.FstLike = None, mono: pyn.FstLike = None) -> p.Phon:
  """Composes a diphthong."""
  tr_dict = {}
  if semi:
    tr_dict['semi'] = semi
  if mono:
    tr_dict['mono'] = mono
  return compose(vowels, 'diph', diph, tr_dict)


def affricate(
    cons: [p.Phon], affr: pyn.FstLike) -> p.Phon:
  """Composes an affricate."""
  return compose(cons, 'affr', affr)
