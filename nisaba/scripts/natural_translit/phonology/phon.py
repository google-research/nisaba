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

"""Phon building functions."""

import collections
import pynini as pyn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

# See README for Phon tuple details.
# TODO: add some structure to ftr and enumerate possible values.
Phon = collections.namedtuple(
    'Phon', ['alias', 'txn', 'ftr', 'ph', 'ipa', 'tr_dict', 'cmp'])


def base_phon(
    txn: str,
    ftr: [str],
    ipa: str,
    base_tr: pyn.FstLike,
    alias: str = None
) -> Phon:
  """Makes a base Phon.

  The default alias is txn in uppercase. The translit dictionary is set up with
  the key 'base'. The ph fst is the txn enclosed in { }. A base phone has no
  components.

  Args:
    txn: The txn of the Phon.
    ftr: The phonological features, currently as a list of str.
    ipa: The IPA representation of the Phon.
    base_tr: The default transliteration of the Phon.
    alias: The alias of the Phon that will be used in grammars.

  Returns:
    Phon

  Following call:
  ```
  base_phon('ec', ['vowel'], 'ə', tr.A)
  ```
  will return:
  ```
  Phon(alias='EC', txn='ec', ftr=['vowel'], ph={ec}, ipa='a', {'base': tr.A})
  ```
  """
  if alias:
    new_alias = alias
  else:
    new_alias = txn.upper()
  ph = al.enclose_phoneme(txn)
  tr_dict = {'base': base_tr}
  return Phon(new_alias, txn, ftr, ph, ipa, tr_dict, None)


def get_cmp_list(phon: Phon) -> [Phon]:
  if phon.cmp:
    return phon.cmp
  else:
    return [phon]


def new_tr(key: str, new: str, base: str) -> dict[str, str]:
  if new:
    return {key: new}
  else:
    return {key: base}


def derive_with_suffix(
    phon: Phon,
    modifier: Phon,
    tr: pyn.FstLike = None
) -> Phon:
  """Makes a new Phon from a phoneme Phon and a suffix Phon.

  TODO: Split phonemes, modifying features, and standalone features into
  distinct classes.

  Args:
    phon: A phoneme Phon to be modified.
    modifier: A suffix Phon.
    tr: The default translit for the new Phon. If None, the new entry will be
    a copy of the base entry of the phon arg.

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
  tr_dict.update(new_tr(modifier.ftr[0], tr, phon.tr_dict['base']))
  cmp = get_cmp_list(phon) + get_cmp_list(modifier)
  return Phon(alias, txn, ftr, ph, ipa, tr_dict, cmp)


def compose(
    alias: str,
    phons: [Phon],
    combiner: Phon,
    ftr: str,
    tr: str = None,
    alt_tr_dict: dict[str] = None,
) -> Phon:
  """Make a composite Phon.

  Args:
    alias: The alias of the Phon that will be used in grammars.
    phons: The list of Phons to be composed.
    combiner: The combiner phoneme. Passed as arg to avoid cyclic dep.
      TODO remove combiner arg when the function is factored out.
    ftr: The class of the new Phon. Set as the first element of the new ftr.
    tr: The default translit of the composite Phon. If None, it will be the same
      as the new base tr, which is the concatenation of the base tr_dict of the
      component Phons.
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
      'AU', [ph.A, ph.U], ph.CMB, 'diph', tr.S_AU,
      {'semi': tr.S_AW 'mono': tr.O}
  )
  ```
  will return:
  ```
  Phon(
    alias='AU', txn='a+u', ftr=['diph', 'vowel', 'vowel'],
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
    cmp_list.extend(get_cmp_list(phon))
  new_txn = cmp_list[0].txn
  new_ftr = [ftr] + cmp_list[0].ftr
  new_ph = cmp_list[0].ph
  new_ipa = cmp_list[0].ipa
  new_base_tr = cmp_list[0].tr_dict['base']
  new_cmp = [cmp_list[0]]
  for cmp in cmp_list[1:]:
    new_txn += combiner.txn + cmp.txn
    new_ftr.extend(cmp.ftr)
    new_ph = new_ph + combiner.ph + cmp.ph
    new_ipa += combiner.ipa + cmp.ipa
    new_base_tr += cmp.tr_dict['base']
    new_cmp.append(cmp)
  new_tr_dict = {'base': new_base_tr}
  new_tr_dict.update(new_tr(ftr, tr, new_base_tr))
  if alt_tr_dict:
    new_tr_dict.update(alt_tr_dict)
  return Phon(alias, new_txn, new_ftr, new_ph, new_ipa, new_tr_dict, new_cmp)

# Shortcut functions for building Phon and ph inventories from Phon lists.

# In a phon_inventory, the non-store aliases refer to Phons, allowing access to
# all fields of the tuple. In a ph_inventory, non-store aliases refer to the
# fsts in the ph field.

# CAVEAT: There is no type restriction on Stores in inventories.
# If a Phon list or inventory is added as a Store to a ph_inventory, the Store
# content will still refer to Phons, not their ph fields.


def ph_list(phon_list: [Phon]) -> [pyn.Fst]:
  return [phon.ph for phon in phon_list]


def ph_union(phon_list: [Phon]) -> [pyn.Fst]:
  return ls.union_opt(*ph_list(phon_list))


def ph_star(phon_list: [Phon]) -> [pyn.Fst]:
  return ls.union_star(*ph_list(phon_list))


def store_ph_list(alias: str, phon_list: [Phon]) ->i.Store:
  return i.store_as(alias, ph_list(phon_list))


def store_ph_union(alias: str, phon_list: [Phon]) -> i.Store:
  return i.store_as(alias, ph_union(phon_list))


def store_ph_star(alias: str, phon_list: [Phon]) -> i.Store:
  return i.store_as(alias, ph_star(phon_list))


# Shortcut for phonemes with optional modifiers.
# eg. ph.VOWEL + ph.VOWEL_MOD.star
# TODO: Possibly update + to rw.concat_r
def store_ph_modified(
    alias: str,
    phon_list: [Phon],
    mod_list: [Phon]) -> i.Store:
  return i.store_as(alias, ph_union(phon_list) + ph_star(mod_list))


def phon_inventory(
    phon_list: [Phon],
    store_list: [i.Store] = None) -> collections.namedtuple:
  return i.make_inventory(phon_list, phon_list, store_list)


def ph_inventory(
    phon_list: [Phon],
    store_list: [i.Store] = None) -> collections.namedtuple:
  fst_list = ph_list(phon_list)
  return i.make_inventory(fst_list, phon_list, store_list)

# Translit functions


def translit_by_key(phon: Phon, key: str) -> pyn.Fst:
  return rw.rewrite(phon.ph, phon.tr_dict[key])


def translit_base(phon: Phon) -> pyn.Fst:
  return translit_by_key(phon, 'base')


def translit_ipa(phon: Phon) -> pyn.Fst:
  return rw.rewrite(phon.ph, phon.ipa)


def ls_translit_by_key(phon_list: [Phon], key: str) -> pyn.Fst:
  ph_to_tr = [pyn.cross(phon.ph, phon.tr_dict[key]) for phon in phon_list]
  return rw.rewrite_op(ls.union_opt(*ph_to_tr))


def ls_translit_base(phon_list: [Phon]) -> pyn.Fst:
  return ls_translit_by_key(phon_list, 'base')


def ls_translit_ipa(phon_list: [Phon]) -> pyn.Fst:
  ph_to_ipa = [pyn.cross(phon.ph, phon.ipa) for phon in phon_list]
  return ls.union_star(*ph_to_ipa)


def print_only_ipa(phon_list: [Phon]) -> pyn.Fst:
  return (rw.EXTRACT_RIGHT_SIDE @ ls_translit_ipa(phon_list)).optimize()
