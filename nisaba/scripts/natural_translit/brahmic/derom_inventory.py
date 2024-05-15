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

"""Latin Brahmic character mappings."""

from typing import Any, Callable, Iterable
import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import inventory as i
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = iso_inventory.TRANSLIT_INVENTORY

# TODO: Remove dicts and private functions when graphemes have these
# conversions as class methods.


def _get_from_dict(
    dictionary: dict[str, pyn.FstLike], key: pyn.FstLike
) -> ty.FstIterable:
  try:
    return log.dbg_return(log.text_of(dictionary[key]))
  except KeyError:
    return log.dbg_return(ty.MISSING, 'invalid key')


_BRH_MONO_DICT_ARGS = [
    [iso.A, iso.A_I, iso.AA, iso.AA_I],
    [iso.E, iso.E_I, iso.EE, iso.EE_I],
    [iso.I, iso.I_I, iso.II, iso.II_I],
    [iso.O, iso.O_I, iso.OO, iso.OO_I],
    [iso.U, iso.U_I, iso.UU, iso.UU_I],
]
_BRH_DIPH_DICT_ARGS = [
    [iso.AI, iso.AI_I],
    [iso.AU, iso.AU_I],
    [iso.EE, iso.EE_I],
    [iso.OO, iso.OO_I],
]


def _sign_independent_dict():
  sign_independent_dict = {
      log.text_of(arg[0]): arg[1]
      for arg in _BRH_MONO_DICT_ARGS + _BRH_DIPH_DICT_ARGS
  }
  sign_independent_dict.update(
      {log.text_of(arg[2]): arg[3] for arg in _BRH_MONO_DICT_ARGS}
  )
  return sign_independent_dict

_SIGN_INDEPENDENT_DICT = _sign_independent_dict()


def _independent_vowel(vowel_sign: pyn.FstLike) -> ty.FstIterable:
  return _get_from_dict(_SIGN_INDEPENDENT_DICT, log.text_of(vowel_sign))


def _short_long_dict():
  short_long_dict = {log.text_of(arg[0]): arg[2] for arg in _BRH_MONO_DICT_ARGS}
  short_long_dict.update(
      {log.text_of(arg[1]): arg[3] for arg in _BRH_MONO_DICT_ARGS}
  )
  return short_long_dict

_SHORT_LONG_DICT = _short_long_dict()


def _long_vowel(arg: pyn.FstLike) -> ty.FstIterable:
  return _get_from_dict(_SHORT_LONG_DICT, log.text_of(arg))

_BRH_ASP_DICT_ARGS = [
    [iso.B, iso.BH],
    [iso.C, iso.CH],
    [iso.D, iso.DH],
    [iso.G, iso.GH],
    [iso.J, iso.JH],
    [iso.K, iso.KH],
    [iso.P, iso.PH],
    [iso.T, iso.TH],
]
_UNASP_ASP_DICT = {log.text_of(arg[0]): arg[1] for arg in _BRH_ASP_DICT_ARGS}


def _aspirated_consonant(arg: pyn.FstLike) -> ty.FstIterable:
  return _get_from_dict(_UNASP_ASP_DICT, log.text_of(arg))


class DeromMapping(ty.Thing):
  """Latin to Brahmic character mapping."""

  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(
      self,
      alias: str,
      rom_list: ty.FstIterable,
      brh_list: ty.FstIterable,
      priority: int = 0,
  ) -> None:
    """Initializes common attributes of deromanization mappings.

    Args:
      alias: The string which will be used to refer to this mapping.
      rom_list: A string, an Fst, or an Iterable of Latin characters in
      romanization.
        Eg. '<i>' for 'i' and FstList('<p>', '<h>') for string 'ph'.
      brh_list: A string, an Fst, or an Iterable of corresponding Brahmic
        characters.
        Eg. '`i`' for ISO 'i' and deva 'ि' or
        FstList('`k`', '`vir`', '`s`', '`a`') for ISO 'ksa' and deva 'क्स'
      priority: By default, deromanizer.py applies the mapping rules in
        descending order of the number of Latin characters in rom_list. Setting
        the priority higher than 0 will move up the rules for this mapping in
        the final rule list.
        Eg. `DeromMapping('zh_lr', [ltn.Z, ltn.H], iso.LR, 1)`, increases the
        priority of zh_lr mapping from 2 to 3, placing it before other 2-letter
        rules.

    In order to restrict sigma to ASCII, and to distinguish between the input
    symbol and the output symbols, we use the [typ representation]
    (https://github.com/google-research/nisaba/blob/main/nisaba/scripts/natural_translit/README.md#typ-representation-and-script-inventories).

    Further common attributes:
      rom: The concatenated fst of the romanization for the base form, which is
        the short unaspirated schwa-bearing consonant ('<p>' for '`p`' 'प'),
        the short modal vowel sign ('<i>' for '`i`' 'ि'),
        a diacritic or a coda ('<n>' for anusvara '`ans`' 'ं').
      brh: The concatenated fst of the brahmic characters for the base form.

    Each class of characters have pre-concatenated fst fields for convinience.
    Common suffixes:
      _l: long form, can be used for both rom and brh fields.
      _h: Latin characters followed by Latin 'h'.
      _i: independent Brahmic vowel.
      _v: a schwa-bearing consonant letter followed by a virama.

    TODO: remove fields when graphemes have the corresponding methods.
    """

    super().__init__(alias)
    self.rom_list = fl.FstList(rom_list)
    self.rom = self.rom_list.concat()
    self.brh_list = fl.FstList(brh_list)
    self.brh = self.brh_list.concat()
    self.priority = len(self.rom_list)
    if ty.is_specified(priority): self.priority += priority

  @ classmethod
  def vowel(
      cls,
      alias: str,
      rom_list: ty.FstIterable,
      brh_list: ty.FstIterable,
      priority: int = 0,
  ) -> 'DeromMapping':
    new = cls(alias, rom_list, brh_list, priority)
    new.add_fst_fields([
        ['rom_l', new.rom + new.rom],  # eg. latin ii
        ['brh_i', _independent_vowel(new.brh)],  # eg. iso .i
        ['brh_l', _long_vowel(new.brh)],  # eg. iso ī
        ['brh_l_i', _independent_vowel(_long_vowel(new.brh))],  # eg. iso .ī
        ])
    return new

  @classmethod
  def consonant(
      cls,
      alias: str,
      rom_list: ty.FstIterable,
      brh_list: ty.FstIterable,
      priority: int = 0,
  ) -> 'DeromMapping':
    new = cls(alias, rom_list, brh_list, priority)
    brh_v = new.brh + iso.VIR
    rom_l = new.rom + new.rom  # eg. shsh
    if len(new.rom_list) > 1:
      rom_l = pyn.union(rom_l, new.rom_list.item(0) + new.rom)  # eg. ssh
    new.add_fst_fields([
        ['rom_h', new.rom + ltn.H],  # eg. latin ph
        ['rom_l', rom_l],  # eg. latin pp
        ['brh_v', brh_v],  # eg. iso p
        ['brh_l', brh_v + new.brh],  # eg. iso ppa
        ['brh_l_v', brh_v + brh_v],  # eg. iso pp
    ])
    asp = _aspirated_consonant(new.brh)
    if ty.is_found(asp):
      asp_v = asp + iso.VIR
      new.add_fst_fields([
          ['rom_l_h', new.rom_l + ltn.H],  # eg. latin pph
          ['rom_h_l', new.rom_h + new.rom_h],  # eg. phph
          ['brh_asp', asp],  # eg. iso pʰa
          ['brh_asp_v', asp_v],  # eg. iso pʰ
          ['brh_l_asp', brh_v + asp],  # eg. iso ppʰa
          ['brh_l_asp_v', brh_v + asp_v],  # eg. iso ppʰ
          ['brh_asp_l', asp_v + asp],  # eg. iso pʰpʰa
          ['brh_asp_l_v', asp_v + asp_v],  # eg. iso pʰpʰ
      ])
    return new

  @classmethod
  def foreign_consonant(
      cls,
      alias: str,
      rom_list: ty.FstIterable,
      brh_list: pyn.FstLike,
      frg: pyn.FstLike,
      priority: int = 0,
  ) -> 'DeromMapping':
    new = cls.consonant(alias, rom_list, brh_list, priority)
    frg_v = frg + iso.VIR
    new.add_fst_fields([
        ['frg', frg],  # eg. iso fa
        ['frg_v', frg_v],  # eg. iso f
        ['frg_l', frg_v + frg],  # eg. iso ffa
        ['frg_l_v', frg_v + frg_v],  # eg. iso ff
    ])
    return new

  @classmethod
  def as_list(cls, *args) -> list['DeromMapping']:
    """Returns a list of DeromMappings. Flattens tree structures in args."""
    ls = []
    for arg in args:
      if isinstance(arg, DeromMapping): ls.append(arg)
      if isinstance(arg, Iterable): ls.extend(cls.as_list(*arg))
    return ls

  def add_field(self, field: str, value: pyn.FstLike = '') -> None:
    if not hasattr(self, field): self.__dict__[field] = value

  def add_fst_field(self, field: str, *args) -> None:
    fst_list = fl.FstList(*args)
    if fst_list: self.add_field(field, fst_list.concat())

  def add_fst_fields(self, args_list: list[list[pyn.FstLike]]) -> None:
    for args in args_list:
      self.add_fst_field(*args)

  def get(self, attr: str) -> pyn.FstLike:
    return getattr(self, attr)

  def high_priority(self) -> bool:
    return self.priority > len(self.rom_list)


class _DeromMappingInventory(i.Inventory):
  """Latin to Brahmic rewrite inventory."""

  def __init__(self) -> None:
    super().__init__()
    self.make_inventory()

  def make_maps(
      self, maker: Callable[..., DeromMapping], args_list: list[list[Any]]
  ) -> None:
    for args in args_list:
      self.add_item(maker(*args))

  def make_inventory(self):
    self.make_maps(DeromMapping.vowel, [
        ['a', ltn.A, iso.A],
        ['e', ltn.E, iso.E],
        ['i', ltn.I, iso.I],
        ['o', ltn.O, iso.O],
        ['u', ltn.U, iso.U],
        ['ai', [ltn.A, ltn.I], iso.AI],
        ['au', [ltn.A, ltn.U], iso.AU],
        ['ae_ee', [ltn.A, ltn.E], iso.EE],
        ['oa_oo', [ltn.O, ltn.A], iso.OO],
    ])
    self.make_maps(DeromMapping.consonant, [
        ['b', ltn.B, iso.B],
        ['b_p', ltn.B, iso.P],
        ['ch', [ltn.C, ltn.H], iso.C],
        ['d', ltn.D, iso.D],
        ['d_t', ltn.D, iso.T],
        ['g', ltn.G, iso.G],
        ['g_k', ltn.G, iso.K],
        ['j', ltn.J, iso.J],
        ['k', ltn.K, iso.K],
        ['p', ltn.P, iso.P],
        ['t', ltn.T, iso.T],
        ['c', ltn.C, iso.C],
        ['h', ltn.H, iso.H],
        ['l', ltn.L, iso.L],
        ['m', ltn.M, iso.M],
        ['n', ltn.N, iso.N],
        ['q', ltn.Q, iso.K],
        ['r', ltn.R, iso.R],
        ['s', ltn.S, iso.S],
        ['sh', [ltn.S, ltn.H], iso.SH],
        ['v', ltn.V, iso.V],
        ['w', ltn.W, iso.V],
        ['x', ltn.X, [iso.K, iso.VIR, iso.S]],
        ['y', ltn.Y, iso.Y],
        ['tr_rr', [ltn.T, ltn.R], iso.RR],
        ['zh_lr', [ltn.Z, ltn.H], iso.LR, 1],
    ])
    self.make_maps(DeromMapping.foreign_consonant, [
        ['f', ltn.F, iso.PH, iso.F],
        ['z', ltn.Z, iso.J, iso.Z],
    ])

DEROMANIZATION_INVENTORY = _DeromMappingInventory()
