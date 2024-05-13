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

"""Phon building functions."""

import pynini as pyn
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.natural_translit.utils import type_op as ty


class Phon(ty.Thing):
  """See README for Phon attributes."""

  def __init__(
      self,
      alias: str,
      txn: str,
      ftr: list[str],
      ph: pyn.Fst,
      ipa: str,
      tr_dict: dict[str, str],
      cmp: list['Phon']
  ):
    super().__init__(alias, ipa)
    self.txn = txn
    self.ftr = ftr
    self.ph = ph
    self.ipa = ipa
    self.tr_dict = tr_dict
    self.cmp = cmp

  @classmethod
  def base(
      cls,
      txn: str,
      ftr: list[str],
      ipa: str,
      base_tr: pyn.FstLike = None,
      alias: str = None
  ) -> 'Phon':
    """Makes a base Phon.

    The default alias is txn in uppercase. The translit dictionary is set up
    with the key 'base'. The ph fst is the txn enclosed in { }. A base phone has
    no components.

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
    tr_dict = new_tr('base', base_tr, al.enclose_translit('DEL'))
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

# Shortcut functions for building Phon and ph inventories from Phon lists.

# In a phon_inventory, the item aliases refer to Phons, allowing access to
# all fields of the tuple. In a ph_inventory, item aliases refer to the
# fsts in the ph field.

# CAVEAT: There is no type restriction on Stores in inventories.
# If a Phon list or inventory is added as a Store to a ph_inventory, the Store
# content will still refer to Phons, not their ph fields.


def ph_list(phon_list: [Phon]) -> [pyn.Fst]:
  return [phon.ph for phon in phon_list]


def ph_union(phon_list: [Phon]) -> pyn.Fst:
  return fl.FstList(ph_list(phon_list)).union_opt()


def ph_star(phon_list: [Phon]) -> pyn.Fst:
  return fl.FstList(ph_list(phon_list)).union_star()


def thing_ph_list(alias: str, phon_list: [Phon]) ->ty.Thing:
  return ty.Thing(alias, value_from=ph_list(phon_list))


def thing_ph_union(alias: str, phon_list: [Phon]) -> ty.Thing:
  return ty.Thing(alias, value_from=ph_union(phon_list))


def thing_ph_star(alias: str, phon_list: [Phon]) -> ty.Thing:
  return ty.Thing(alias, value_from=ph_star(phon_list))


# Shortcut for phonemes with optional modifiers.
# eg. ph.VOWEL + ph.VOWEL_MOD.star
# TODO: Possibly update + to rw.concat_r
def thing_ph_modified(
    alias: str,
    phon_list: [Phon],
    mod_list: [Phon]) -> ty.Thing:
  return ty.Thing(alias, value_from=ph_union(phon_list) + ph_star(mod_list))


def phon_inventory(
    phon_list: [Phon],
    suppl_list: [ty.Thing] = None) -> i.Inventory:
  return i.Inventory.from_list(phon_list, suppl_list)


def ph_inventory(
    phon_list: [Phon],
    suppl_list: [ty.Thing] = None) -> i.Inventory:
  return i.Inventory.from_list(phon_list, attr='ph', suppls=suppl_list)


def import_phon(
    phon: Phon,
    add_ftr: [str] = None,
    alt_tr_dict: dict[str] = None
) -> pyn.Fst:
  """Copies a Phon, optionally add features and translits."""
  new_ftr = phon.ftr.copy()
  if add_ftr:
    new_ftr.extend(add_ftr)
  new_tr_dict = phon.tr_dict.copy()
  if alt_tr_dict:
    new_tr_dict.update(alt_tr_dict)
  return Phon(
      phon.alias, phon.txn, new_ftr, phon.ph, phon.ipa, new_tr_dict, phon.cmp
      )

# Translit functions


def check_key(key: str) -> str:
  """Failsafe for translit_by_key_functions."""
  if key:
    return key
  else:
    return 'base'


def translit_by_key(phon: Phon, key: str) -> pyn.Fst:
  return rw.rewrite(phon.ph, phon.tr_dict[check_key(key)])


def translit_base(phon: Phon) -> pyn.Fst:
  return translit_by_key(phon, 'base')


def translit_ipa(phon: Phon) -> pyn.Fst:
  return rw.rewrite(phon.ph, phon.ipa)


def ls_translit_by_key(phon_list: [Phon], key: str) -> pyn.Fst:
  return rw.rewrite_ls(
      (phon.ph, phon.tr_dict[check_key(key)]) for phon in phon_list
  )


def ls_translit_base(phon_list: [Phon]) -> pyn.Fst:
  return ls_translit_by_key(phon_list, 'base')


def ls_translit_ipa(phon_list: [Phon]) -> pyn.Fst:
  return fl.FstList.cross(
      *[(phon.ph, phon.ipa) for phon in phon_list]
  ).union_star()


def print_only_ipa(phon_list: [Phon]) -> pyn.Fst:
  return (rw.EXTRACT_RIGHT_SIDE @ ls_translit_ipa(phon_list)).optimize()
