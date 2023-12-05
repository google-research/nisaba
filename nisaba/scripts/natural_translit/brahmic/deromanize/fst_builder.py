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

"""Brahmic deromanizer."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.brahmic.deromanize import ltn2brh as l2b
from nisaba.scripts.natural_translit.brahmic.deromanize import typ2brh as t2b
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.natural_translit.utils import type_op as ty
from nisaba.scripts.utils import rewrite

ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = iso_inventory.TRANSLIT_INVENTORY
pan = l2b.MAPPING_INVENTORY
_FST0 = pyn.intersect(pyn.accep('a'), pyn.accep('b'))


class RuleList(ty.Thing):
  """A thing whose value is a list of fsts."""

  def __init__(self, alias: str, *fsts):
    super().__init__()
    self.set_alias(alias)
    self.value = []
    self.add(*fsts)

  def add(self, *fsts):
    fst_list = []
    for fst in fsts:
      if ty.is_instance(fst, pyn.Fst): fst_list.append(fst)
      if ty.is_instance(fst, list): fst_list.extend(fst)
      if ty.is_instance(fst, RuleList): fst_list.extend(fst.value)
    self.value.extend([f for f in fst_list if ty.is_instance(f, pyn.Fst)])


class Deromanizer(inventory2.Inventory):
  """Fst inventory for Brahmic deromanization."""

  def __init__(self):
    super().__init__()
    self.script = ty.UNASSIGNED
    self.schwa_deletion = False
    self.init_items()
    self.init_supps()

  def make_rule(self, alias: str, *fsts) -> pyn.Fst:
    self.add_item(RuleList(alias, *fsts))

  def init_items(self) -> None:
    ls.apply_foreach(self.make_rule, [
        ['ltn2typ', self.rw_ltn2typ()],
        ['typ_ops'],
        ['anusvara'],
        ['cons_first'],
        ['cons_nukta'],
        ['cons_asp'],
        ['cons_drop_asp'],
        ['cons_drop_gem'],
        ['cons_gem_only'],
        ['cons_base'],
        ['mono_long'],
        ['diph_base'],
        ['mono_base_as_long'],
        ['mono_base'],
        ['schwa_as_long_wf'],
        ['cluster_wi'],
        ['cluster_wf'],
        ['typ2brh'],
        ['typ2iso', self.rw_typ2iso()],
    ])

  def init_supps(self) -> None:
    ls.apply_foreach(self.make_supp, [
        ['group_vowel', {}],
        ['group_mono', {}],
        ['group_base_as_long', {}],
        ['group_diph', {}],
        ['group_consonant', {}],
        ['group_has_aspirated', {}],
        ['group_no_aspirated', {}],
        ['group_drop_aspirated', {}],
        ['group_drop_gem', {}],
        ['group_gem_only', {}],
        ['group_nukta', {}],
        ['group_substring', {}],
        ['ltn2brh', _FST0],
        ['ltn2iso', _FST0],
    ])

  @classmethod
  def params(
      cls,
      script: str = '',
      schwa_deletion: bool = False,
      schwa_deletion_wf: bool = False,
      monophthong: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      base_as_long: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      diphthong: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      has_aspirated: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      drop_aspirated: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      no_aspirated: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      drop_gem: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      gem_only: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      nukta: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
      anusvara_labial: bool = False,
      anusvara_n: bool = False,
      substring: l2b.Ltn2Brh.STAR = ty.UNSPECIFIED,
    ) -> 'Deromanizer':
    new = cls()
    new.set_script(script)
    new.set_schwa_deletion(schwa_deletion, schwa_deletion_wf)
    new.set_anusvara(anusvara_labial, anusvara_n)
    if ty.is_specified(monophthong): new.add_monophthong(monophthong)
    if ty.is_specified(base_as_long): new.add_base_as_long(base_as_long)
    if ty.is_specified(diphthong): new.add_diphthong(diphthong)
    if ty.is_specified(has_aspirated): new.add_has_aspirated(has_aspirated)
    if ty.is_specified(drop_aspirated): new.add_drop_aspirated(drop_aspirated)
    if ty.is_specified(no_aspirated): new.add_no_aspirated(no_aspirated)
    if ty.is_specified(drop_gem): new.add_drop_gem(drop_gem)
    if ty.is_specified(gem_only): new.add_gem_only(gem_only)
    if ty.is_specified(nukta): new.add_nukta(nukta)
    if ty.is_specified(substring): new.add_substring(substring)
    new.set_group_rules()
    new.set_typ_ops()
    new.set_e2e()
    return new

  def set_script(self, script: str) -> None:
    if script:
      self.script = script
      self.typ2brh.add(self.rw_typ2brh())
    else:
      self.typ2brh = self.typ2iso

  def set_schwa_deletion(
      self,
      schwa_deletion: bool,
      schwa_deletion_wf: bool,
  ) -> None:
    self.schwa_deletion = schwa_deletion
    if not schwa_deletion: return
    self.cluster_wi.add(self.rw_cluster_wi())
    if schwa_deletion_wf:
      self.schwa_as_long_wf.add(self.rw_schwa_as_long_wf())
      self.cluster_wf.add(self.rw_cluster_wf())

  def set_anusvara(self, anusvara_labial: bool, anusvara_n: bool) -> None:
    if anusvara_n:
      if anusvara_labial:
        self.anusvara.add(self.rw_ans_labial())
      self.anusvara.add(self.rw_ans_n())

  def set_group_rules(self) -> None:
    for gl in self.group_lists(self.group_mono):
      self.mono_base.add(self.rw_vowel(gl))
      self.mono_long.add(self.rw_vowel(gl, 'long', 'long'))
    for gl in self.group_lists(self.group_base_as_long):
      self.mono_base_as_long.add(self.rw_vowel(gl, 'short', 'long'))
    for gl in self.group_lists(self.group_diph):
      self.diph_base.add(self.rw_vowel(gl))
    for gl in self.group_lists(self.group_nukta):
      self.cons_nukta.add(self.rw_cons(gl, new='nkt'))
    for gl in self.group_lists(self.group_drop_aspirated):
      self.cons_drop_asp.add(self.rw_drop_aspirated(gl))
    for gl in self.group_lists(self.group_has_aspirated):
      self.cons_asp.add(self.rw_aspirated(gl))
    for gl in self.group_lists(self.group_drop_gem):
      self.cons_drop_gem.add(self.rw_cons(gl))
    for gl in self.group_lists(self.group_gem_only):
      self.cons_gem_only.add(self.rw_cons(gl, rw_one=False))
    for gl in self.group_lists(self.group_consonant):
      self.cons_base.add(self.rw_cons(gl))
      if pan.zh_lr in gl:
        self.cons_first.add(self.rw_cons([pan.zh_lr]))

  def set_typ_ops(self) -> None:
    rules = (
        self.anusvara,
        self.cons_first,
        self.cons_nukta,
        self.cons_drop_asp,
        self.cons_drop_gem,
        self.cons_asp,
        self.cons_gem_only,
        self.cons_base,
        self.mono_long,
        self.diph_base,
        self.mono_base_as_long,
        self.mono_base,
        self.schwa_as_long_wf,
        self.cluster_wi,
        self.cluster_wf
    )
    self.typ_ops.add(*[rule.value for rule in rules])

  def set_e2e(self) -> None:
    self.ltn2brh = rewrite.ComposeFsts(
        self.ltn2typ.value + self.typ_ops.value + self.typ2brh.value
    )
    self.ltn2iso = rewrite.ComposeFsts(
        self.ltn2typ.value + self.typ_ops.value + self.typ2iso.value
    )

  def add_to_group(
      self,
      group: str,
      member: l2b.Ltn2Brh,
      priority: ty.IntOrNothing = ty.UNSPECIFIED
  ) -> None:
    if group not in self.supp_aliases: self.make_supp(group, {})
    supp = ty.enforce_dict(self.get(group))
    k = priority if isinstance(priority, int) else len(member.grs)
    m_list = supp.get(k, [])
    if member not in m_list: m_list.append(member)
    supp[k] = m_list

  def add_to_groups(self, member, *groups) -> None:
    for group in groups:
      self.add_to_group(group, member)

  def group_lists(
      self, group: dict[int, list[l2b.Ltn2Brh]]
  ) -> list[list[l2b.Ltn2Brh]]:
    return [group[k] for k in sorted(group.keys(), reverse=True)]

  def add_monophthong(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_vowel', 'group_mono')

  def add_base_as_long(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(
          m, 'group_vowel', 'group_mono', 'group_base_as_long'
      )

  def add_diphthong(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_vowel', 'group_diph')

  def add_has_aspirated(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_consonant', 'group_has_aspirated')

  def add_no_aspirated(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_consonant', 'group_no_aspirated')

  def add_drop_aspirated(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_consonant', 'group_drop_aspirated')

  def add_drop_gem(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_consonant', 'group_drop_gem')

  def add_gem_only(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_gem_only')

  def add_nukta(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_consonant', 'group_nukta')

  def add_substring(self, *args) -> None:
    for m in l2b.Ltn2Brh.as_list(*args):
      self.add_to_groups(m, 'group_substring')

  def rw_ltn2typ(self) -> pyn.Fst:
    return c.read_glyph(ltn_inventory.ASCII_LC)

  def rw_typ2iso(self) -> pyn.Fst:
    return [
        rw.insert(iso.A, iso.SCH_CONS),
        rw.delete(iso.A, following=pyn.union(iso.VWL_S, iso.VIR)),
        c.print_glyph(iso_inventory.CHAR + iso_inventory.VIRAMA),
        rw.delete('.', rw.al.BOW)
    ]

  def rw_typ2brh(self) -> pyn.Fst:
    return rw.rewrite_ls(t2b.cross(self.script))

  def rw_vowel(
      self, args: list[l2b.Ltn2Brh], old: str = 'short', new: str = 'short'
  ) -> pyn.Fst:
    rom = 'ltn_l' if old == 'long' else 'ltn'
    sgn = 'iso_l' if new == 'long' else 'iso'
    ind = 'iso_l_i' if new == 'long' else 'iso_i'
    return [
        rw.rewrite_ls(
            [(arg.get(rom), arg.get(sgn)) for arg in args],
            iso.SCH_CONS
        ),
        rw.rewrite_ls(
            [(arg.get(rom), arg.get(ind)) for arg in args],
        )
    ]

  def rw_schwa_as_long_wf(self) -> pyn.Fst:
    return rw.rewrite_word_final(iso.A, iso.AA)

  def rw_cluster_wi(self) -> pyn.Fst:
    return rw.insert(iso.VIR, rw.al.BOW + iso.SCH_CONS, iso.ONSET_CONS)

  def rw_cluster_wf(self) -> pyn.Fst:
    return rw.insert(iso.VIR, iso.SCH_CONS, iso.ONSET_CONS + rw.al.EOW)

  def rw_drop_aspirated(self, args: list[l2b.Ltn2Brh]) -> pyn.Fst:
    if self.schwa_deletion:
      return [
          rw.rewrite_ls((
              (arg.ltn_l_h | arg.ltn_h_l | arg.ltn_h + arg.ltn),
              arg.gem
          ) for arg in args),
          rw.rewrite_ls((arg.ltn_h, arg.iso) for arg in args),
      ]
    return [
        rw.rewrite_ls(
            [(arg.ltn_h, arg.iso) for arg in args], following=ltn.VOWEL
        ),
        rw.rewrite_ls([(arg.ltn_h, arg.vir) for arg in args]),
    ]

  def rw_aspirated(self, args: list[l2b.Ltn2Brh]) -> pyn.Fst:
    if self.schwa_deletion:
      return [
          rw.rewrite_ls((arg.ltn_l_h, arg.gem_asp) for arg in args),
          rw.rewrite_ls((arg.ltn_h_l, arg.asp_gem) for arg in args),
          rw.rewrite_ls((arg.ltn_h, arg.asp) for arg in args),
      ]
    return [
        rw.rewrite_ls(
            [(arg.ltn_h, arg.asp) for arg in args], following=ltn.VOWEL
        ),
        rw.rewrite_ls([(arg.ltn_h, arg.asp_vir) for arg in args]),
    ]

  def rw_drop_gem(
      self, args: list[l2b.Ltn2Brh], new: str = 'iso',
  ) -> list[pyn.Fst]:
    gem_cross = [(arg.ltn_l, arg.get(new)) for arg in args]
    if self.schwa_deletion:
      gem_rw = [rw.rewrite_ls(gem_cross)]
    else:
      vir = 'vir' if new == 'iso' else new + '_vir'
      gem_rw = [
          rw.rewrite_ls(gem_cross, following=ltn.VOWEL),
          rw.rewrite_ls((arg.ltn_l, arg.get(vir)) for arg in args)
          ]
    return gem_rw

  def rw_cons(
      self, args: list[l2b.Ltn2Brh], old: str = 'ltn', new: str = 'iso',
      rw_one: bool = True, rw_gem: bool = True
  ) -> list[pyn.Fst]:
    gem = 'gem' if new == 'iso' else new + '_gem'
    gem_cross = [(arg.ltn_l, arg.get(gem)) for arg in args]
    one_cross = [(arg.get(old), arg.get(new)) for arg in args]
    if self.schwa_deletion:
      gem_rw = [rw.rewrite_ls(gem_cross)]
      one_rw = [rw.rewrite_ls(one_cross)]
    else:
      vir = 'vir' if new == 'iso' else new + '_vir'
      gem_rw = [
          rw.rewrite_ls(gem_cross, following=ltn.VOWEL),
          rw.rewrite_ls((arg.ltn_l, arg.get(gem) + iso.VIR) for arg in args)
          ]
      one_rw = [
          rw.rewrite_ls(one_cross, following=ltn.VOWEL),
          rw.rewrite_ls((arg.get(old), arg.get(vir)) for arg in args)
      ]
    rws = []
    if rw_gem: rws.extend(gem_rw)
    if rw_one: rws.extend(one_rw)
    return rws

  def rw_ans_labial(self) -> pyn.Fst:
    return rw.rewrite(ltn.M, iso.ANS, ltn.VOWEL, pyn.union(ltn.B, ltn.P))

  def rw_ans_n(self) -> pyn.Fst:
    return rw.rewrite(
        ltn.N, iso.ANS,
        ltn.VOWEL, pyn.union((ltn.CONS - (ltn.N | ltn.M)), rw.al.EOW)
    )
