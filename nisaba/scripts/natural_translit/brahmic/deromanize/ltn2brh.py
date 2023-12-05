# Copyright 2023 Nisaba Authors.
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

from typing import Any, Callable, Iterable, Union
import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import type_op as ty

_FstOrList = Union[pyn.FstLike, list[pyn.FstLike]]

ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = iso_inventory.TRANSLIT_INVENTORY


def _rep(fst: pyn.FstLike) -> pyn.FstLike:
  return fst + fst


class Ltn2Brh(ty.Thing):
  """Latin to Brahmic rewrite mapping."""

  _HAS_DYNAMIC_ATTRIBUTES = True

  def __init__(
      self,
      alias: str, lta: _FstOrList, isa: pyn.FstLike
  ) -> None:
    super().__init__()
    self.set_alias(alias)
    if isinstance(lta, list):
      self.grs = lta
      self.ltn = lta[0]
      for l in lta[1:]:
        self.ltn = self.ltn + l
    else:
      self.ltn = lta
      self.grs = [lta]
    self.iso = isa

  STAR = Union[ty.Nothing, 'Ltn2Brh', Iterable['Ltn2Brh']]

  @classmethod
  def as_list(cls, *args):
    ls = []
    for arg in args:
      if isinstance(arg, Ltn2Brh): ls.append(arg)
      if isinstance(arg, Iterable): ls.extend(cls.as_list(*arg))
    return ls

  @classmethod
  def monophthong(
      cls, alias: str, lta: _FstOrList, isa: pyn.FstLike,
      iso_i: pyn.FstLike, iso_l: pyn.FstLike, iso_l_i: pyn.FstLike
  ) -> 'Ltn2Brh':
    new = cls(alias, lta, isa)
    new.add_fields([
        ['ltn_l', _rep(new.ltn)],
        ['iso_i', iso_i], ['iso_l', iso_l], ['iso_l_i', iso_l_i],
    ])
    return new

  @classmethod
  def diphthong(
      cls, alias: str, lta: _FstOrList, isa: pyn.FstLike, iso_i: pyn.FstLike
  ) -> 'Ltn2Brh':
    new = cls(alias, lta, isa)
    new.add_field('iso_i', iso_i)
    return new

  @classmethod
  def consonant(
      cls, alias: str, lta: _FstOrList, isa: pyn.FstLike,
  ) -> 'Ltn2Brh':
    new = cls(alias, lta, isa)
    vir = new.iso + iso.VIR
    rep = _rep(new.ltn)
    if new.ltn != new.grs[0]: rep = pyn.union(rep, new.grs[0] + new.ltn)
    new.add_fields([
        ['vir', vir],
        ['ltn_l', rep],
        ['gem', vir + new.iso],
        ['gem_vir', vir + vir],
    ])
    return new

  @classmethod
  def aspirated(
      cls, alias: str, lta: _FstOrList, isa: pyn.FstLike, asp: pyn.FstLike,
  ) -> 'Ltn2Brh':
    new = cls.consonant(alias, lta, isa)
    ltn_h = new.ltn + ltn.H
    asp_vir = asp + iso.VIR
    new.add_fields([
        ['ltn_h', ltn_h],
        ['ltn_l_h', new.ltn_l + ltn.H],
        ['ltn_h_l', ltn_h + ltn_h],
        ['asp', asp],
        ['asp_vir', asp_vir],
        ['gem_asp', new.vir + asp],
        ['asp_gem', asp_vir + asp],
        ['asp_unasp', asp_vir + new.iso],
    ])
    return new

  @classmethod
  def foreign(
      cls, alias: str, lta: _FstOrList, isa: pyn.FstLike, nkt: pyn.FstLike,
  ) -> 'Ltn2Brh':
    new = cls.consonant(alias, lta, isa)
    nkt_vir = nkt + iso.VIR
    new.add_fields([
        ['nkt', nkt],
        ['nkt_vir', nkt_vir],
        ['nkt_gem', nkt_vir + nkt],
    ])
    return new

  # @classmethod
  # def substring(
  #     cls, alias: str, lta: _FstOrList, isa: pyn.FstLike,
  # ) -> 'Ltn2Brh':
  #   new = cls(alias, lta, isa)
  #   if new.trs[0] in ltn.VOWEL: add ind condition
  #   if new.trs[-1] not in ltn.VOWEL: add vir condition

  def add_field(self, field: str, value: pyn.FstLike = '') -> None:
    if not hasattr(self, field): self.__dict__[field] = value

  def add_fields(self, args_list: list[list[pyn.FstLike]]) -> None:
    for args in args_list:
      self.add_field(*args)

  def get(self, attr: str) -> pyn.FstLike:
    return getattr(self, attr)


class _Ltn2BrhInventory(inventory2.Inventory):
  """Latin to Brahmic rewrite inventory."""

  def __init__(self) -> None:
    super().__init__()
    self.make_inventory()

  def make_maps(
      self,
      maker: Callable[..., Ltn2Brh],
      args_list: list[list[Any]]
  ) -> None:
    for args in args_list:
      mapping = maker(*args)
      if mapping.ltn: self.add_item(maker(*args))

  def make_inventory(self):
    self.make_maps(Ltn2Brh.monophthong, [
        ['a', ltn.A, iso.A, iso.A_I, iso.AA, iso.AA_I],
        ['e', ltn.E, iso.E, iso.E_I, iso.EE, iso.EE_I],
        ['i', ltn.I, iso.I, iso.I_I, iso.II, iso.II_I],
        ['o', ltn.O, iso.O, iso.O_I, iso.OO, iso.OO_I],
        ['u', ltn.U, iso.U, iso.U_I, iso.UU, iso.UU_I],
    ])
    self.make_maps(Ltn2Brh.diphthong, [
        ['ai', [ltn.A, ltn.I], iso.AI, iso.AI_I],
        ['au', [ltn.A, ltn.U], iso.AU, iso.AU_I],
        ['ae_ee', [ltn.A, ltn.E], iso.EE, iso.EE_I],
        ['oa_oo', [ltn.O, ltn.A], iso.OO, iso.OO_I],
    ])
    self.make_maps(Ltn2Brh.aspirated, [
        ['b', ltn.B, iso.B, iso.BH],
        ['b_p', ltn.B, iso.P, iso.PH],
        ['ch', [ltn.C, ltn.H], iso.C, iso.CH],
        ['d', ltn.D, iso.D, iso.DH],
        ['d_t', ltn.D, iso.T, iso.TH],
        ['g', ltn.G, iso.G, iso.GH],
        ['g_k', ltn.G, iso.K, iso.KH],
        ['j', ltn.J, iso.J, iso.JH],
        ['k', ltn.K, iso.K, iso.KH],
        ['p', ltn.P, iso.P, iso.PH],
        ['t', ltn.T, iso.T, iso.TH],
    ])
    self.make_maps(Ltn2Brh.consonant, [
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
        ['x', ltn.X, iso.K + iso.VIR + iso.S],
        ['y', ltn.Y, iso.Y],
        ['tr_rr', [ltn.T, ltn.R], iso.RR],
        ['zh_lr', [ltn.Z, ltn.H], iso.LR],
    ])
    self.make_maps(Ltn2Brh.foreign, [
        ['f', ltn.F, iso.PH, iso.F],
        ['z', ltn.Z, iso.J, iso.Z],
    ])
    self.make_maps(Ltn2Brh, [
        ['ndr_narr', [ltn.N, ltn.D, ltn.R], iso.NA + iso.RR],
    ])
    self.make_supp('vcd_vcl', {
        self.b: self.p, self.d: self.t, self.g: self.k
    })

MAPPING_INVENTORY = _Ltn2BrhInventory()

