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

"""Brahmic deromanizer."""

from typing import Any, Callable, Iterable, Union
import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import derom_inventory as derom
from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import alignment as al
from nisaba.scripts.natural_translit.utils import fst_list as fl
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import list_op as ls
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw
from nisaba.scripts.natural_translit.utils import type_op as ty

ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = iso_inventory.TRANSLIT_INVENTORY
drm = derom.DEROMANIZATION_INVENTORY

FstListArg = Union[ty.Nothing, pyn.FstLike, Iterable]
ParamArg = Union[ty.Nothing, derom.DeromMapping, Iterable]


class Deromanizer(inventory2.Inventory):
  """Rule inventory for Brahmic deromanization."""

  def __init__(self):
    super().__init__()
    self.script = ''
    self.schwa_deletion = False
    self._init_items()
    self._init_supls()

  def _add_fst_list(self, alias: str, *fsts) -> None:
    self.add_item(fl.FstList(*fsts, alias=alias))

  def _make_mapping_group(
      self, alias: str, value: ... = ty.UNSPECIFIED
  ) -> None:
    self.make_supl(alias, value if ty.is_specified(value) else {})

  def _init_items(self) -> None:
    ls.apply_foreach(self._add_fst_list, [
        ['ltn2typ', self._rw_ltn2typ()],
        ['typ_ops'], ['anusvara'], ['cons_foreign'],
        ['cons_drop_asp'], ['cons_asp'], ['cons_gem_only'], ['cons_base'],
        ['mono_long'], ['mono_base_long'], ['mono_base'], ['diph_base'],
        ['cluster_vir'], ['high_priority'], ['ind_to_sign']
    ])

  def _init_supls(self) -> None:
    ls.apply_foreach(self._make_mapping_group, [
        ['vowel'], ['monophthong'], ['always_long_vowel'], ['diphthong'],
        ['consonant'], ['has_aspirated'], ['no_aspirated'], ['drops_aspirated'],
        ['only_geminated'], ['foreign'],
    ])

  @classmethod
  def params(
      cls,
      script: str = '',
      schwa_deletion: bool = False,
      schwa_deletion_wf: bool = False,
      monophthong: ParamArg = ty.UNSPECIFIED,
      always_long_vowel: ParamArg = ty.UNSPECIFIED,
      diphthong: ParamArg = ty.UNSPECIFIED,
      has_aspirated: ParamArg = ty.UNSPECIFIED,
      drops_aspirated: ParamArg = ty.UNSPECIFIED,
      no_aspirated: ParamArg = ty.UNSPECIFIED,
      only_geminated: ParamArg = ty.UNSPECIFIED,
      foreign: ParamArg = ty.UNSPECIFIED,
      anusvara_n: bool = False,
      nasal_assimilation: bool = True,
    ) -> 'Deromanizer':
    """Deromanizer for Brahmic scripts.

    Args:
      script: Target script for deromanization.
      schwa_deletion: True if the language/script has schwa deletion.
      schwa_deletion_wf: True if the word-final schwa is deleted by default.
      monophthong: Monophthong vowel mappings with long and short forms.
      always_long_vowel: Vowels for which the short romanization will be
        deromanized as the long Brahmic vowel by default Eg. 'e' -> 'ē'.
      diphthong: Dipthongs, also includes vowels whose romanization is two
        different latin characters eg. 'ae' -> 'ē'.
      has_aspirated: Consonant + 'h' is aspirated, eg. 'ph' -> 'pʰ'
      drops_aspirated: Consonant + 'h' is unaspirated. eg. 'ph' -> 'p'
      no_aspirated: Consonant has no aspirated form. Consonant + 'h' is
        unaspirated followed by Brahmic 'h', eg. 'ph' -> 'ph'
      only_geminated: Only geminated form will be used for the rewrite,
        eg. Tamil 'tr' -> 'tr', 'trtr' -> 'ṟṟ'
      foreign: A specific deromanization for a foreign character.
        eg, 'f' -> 'f', which corresponds to 'फ़' in Deva and 'ஃப' in Taml.
      anusvara_n: Default anusvara is 'n'.
      nasal_assimilation: When true, if the default nasal is 'n', it is 'm'
        before labials 'b' and 'p'. If the default nasal is 'm', it is 'n'
        before dentals and velars 'd', 't', 'k', 'g'.

    Returns:
      An inventory with FstList items, mapping group supplements, and methods
      for composing end-to-end deromanization grammars.
    """
    new = cls()
    new.script = script
    new._set_schwa_deletion(schwa_deletion, schwa_deletion_wf)
    new._set_anusvara(anusvara_n, nasal_assimilation)
    new._set_vowel_rules(
        monophthong, always_long_vowel, diphthong
    )
    new._set_consonant_rules(
        has_aspirated, drops_aspirated, no_aspirated, only_geminated, foreign
    )
    new.rules()
    return new

  def _set_schwa_deletion(
      self,
      schwa_deletion: bool,
      schwa_deletion_wf: bool,
  ) -> None:
    self.schwa_deletion = schwa_deletion
    if not schwa_deletion: return
    # Consonant clusters
    # If romanization starts or ends with a consonant cluster, insert virama
    # between them to remove silent schwa.
    self.cluster_vir.add(self._rw_cluster_wi())
    if schwa_deletion_wf:
      self.cluster_vir.add(self._rw_cluster_wf())

  def _set_anusvara(self, anusvara_n: bool, nasal_assimilation: bool) -> None:
    if anusvara_n:
      if nasal_assimilation: self.anusvara.add(self._rw_nasal_labial())
      self.anusvara.add(self._rw_ans_n())

  def _add_to_groups(self, member_list: ParamArg, *groups) -> None:
    """Populates group dicts.

    Args:
      member_list: A mapping or list of mappings.
      *groups: Groups to which new members will be added.

    Each group is a dictionary where the keys are the priorities and the values
    are lists of mappings with that priority.

    Eg. Tamil consonant group:
    ta.consonant {
        3: [zh_lr]
        2: [ch, tr_rr, ...]
        1: [b_p, d_t, ...]
    }
    """
    members = derom.DeromMapping.as_list(member_list)
    for member in members:
      for group in groups:
        p_list = ty.dict_get(group, member.priority, [])
        if member not in p_list: p_list.append(member)
        group[member.priority] = p_list

  def _apply_by_priority(
      self,
      group: dict[int, list[derom.DeromMapping]],
      rule: fl.FstList,
      rewriter: Callable[..., Any],
      *args
  ) -> None:
    """Fills in a rewrite template with members of a group.

    Currently priority is enforced by rule order.
    TODO: Consider using weight instead of rule order.

    Args:
      group: Dict labeled by priority.
      rule: The FstList containing rewrites, eg. cons_aspirated rule contains
        rewrites consructed with _rw_aspiration.
      rewriter: The rewrite template that will applied to the mappings in
        the group.
        Eg. the _rw_aspiration: rewrite(mapping.rom_h, mapping.brh_asp)
        means that if the base romanization of the consonant is followed by 'h',
        it will be deromanized as the aspirated form of the consonant.
      *args: Additional arguments for the rewrite template, eg. for adding
        preceding/following context or specifying mapping fields.

    First groups are sorted by priority, then the rewrite rule is applied to
    each mapping list from highest priority to lowest. The default priority is
    the length of the romanization, forcing longer strings to be deromanized
    first. If the mapping has higher priority than its length, the rewrite rule
    will be added to the high_priority list, which will be applied before any
    other rule.
    """
    ps_list = [group[p] for p in sorted(group.keys(), reverse=True)]
    for ps in ps_list:
      high = [p for p in ps if p.high_priority()]
      normal = [p for p in ps if not p.high_priority()]
      self.high_priority.add(rewriter(high, *args))
      rule.add(rewriter(normal, *args))

  def _set_vowel_rules(
      self,
      monophthong: ParamArg,
      always_long_vowel: ParamArg,
      diphthong: ParamArg
  ) -> None:
    self._add_to_groups(monophthong, self.vowel, self.monophthong)
    self._add_to_groups(always_long_vowel, self.vowel, self.always_long_vowel)
    self._add_to_groups(diphthong, self.vowel, self.diphthong)
    self._apply_by_priority(
        self.monophthong, self.mono_long, self._rw_vowel, True, True
    )
    self._apply_by_priority(
        self.always_long_vowel, self.mono_base, self._rw_vowel, False, True
    )
    self._apply_by_priority(self.monophthong, self.mono_base, self._rw_vowel)
    self._apply_by_priority(self.diphthong, self.diph_base, self._rw_vowel)
    self._apply_by_priority(
        self.monophthong, self.ind_to_sign, self._rw_ind_to_sign, True
    )
    self._apply_by_priority(self.vowel, self.ind_to_sign, self._rw_ind_to_sign)

  def _set_consonant_rules(
      self,
      has_aspirated: ParamArg,
      drops_aspirated: ParamArg,
      no_aspirated: ParamArg,
      only_geminated: ParamArg,
      foreign: ParamArg,
  ) -> None:
    self._add_to_groups(has_aspirated, self.consonant, self.has_aspirated)
    self._add_to_groups(drops_aspirated, self.consonant, self.drops_aspirated)
    self._add_to_groups(no_aspirated, self.consonant, self.no_aspirated)
    self._add_to_groups(only_geminated, self.consonant, self.only_geminated)
    self._add_to_groups(foreign, self.consonant, self.foreign)
    self._apply_by_priority(
        self.foreign, self.cons_foreign, self._rw_foreign)
    self._apply_by_priority(
        self.drops_aspirated, self.cons_drop_asp, self._rw_drop_aspiration
    )
    self._apply_by_priority(
        self.has_aspirated, self.cons_asp, self._rw_aspiration
    )
    self._apply_by_priority(
        self.only_geminated, self.cons_gem_only, self._rw_gem_only
    )
    self._apply_by_priority(
        self.consonant, self.cons_base, self._rw_cons
    )

  def rules(self, *rules) -> None:
    """Adds rules to the typ_ops rule list.

    Args:
      *rules: Rules for converting from Latin typ to Brahmic typ.

    """
    default_rules = (
        self.high_priority,
        self.anusvara,
        self.cons_foreign,
        self.cons_drop_asp,
        self.cons_asp,
        self.cons_gem_only,
        self.cons_base,
        self.mono_long,
        self.diph_base,
        self.mono_base_long,
        self.mono_base,
        self.cluster_vir
    )
    self.typ_ops.add(rules if rules else default_rules)

  def to_iso(self) -> pyn.Fst:
    """Composes end-to-end fst for latin to ISO deromanization."""
    return fl.FstList(
        self.ltn2typ,
        self.typ_ops,
        self._rw_typ2iso()
    ).compose()

  def to_brahmic(self) -> pyn.Fst:
    """Composes end-to-end fst for latin to Brahmic deromanization."""
    if self.script in iso_inventory.DEROM_SCRIPTS:
      return fl.FstList(
          self.ltn2typ,
          self.typ_ops,
          self._rw_typ2brh()
      ).compose()
    return self.to_iso()

  # Rewrite templates

  def _rw_ltn2typ(self) -> pyn.Fst:
    """Latin string to Latin typ."""
    return c.read_glyph(ltn_inventory.ASCII_LC)

  def _rw_typ2brh(self) -> pyn.Fst:
    """Brahmic typ to Brahmic script."""
    return ls.cross_union_star(iso_inventory.ls_tr2brh(self.script))

  def _rw_typ2iso(self) -> pyn.Fst:
    """Brahmic typ to ISO."""
    return fl.FstList(
        rw.insert(iso.A, iso.SCH_CONS),
        rw.delete(iso.A, following=pyn.union(iso.VOWEL_S, iso.VIR)),
        self.ind_to_sign,
        c.print_glyph(iso_inventory.CHAR)
    ).compose()

  def _rw_fields(
      self, mapping_list: list[derom.DeromMapping],
      old_field: str, new_field: str,
      preceding: pyn.FstLike = '', following: pyn.FstLike = ''
  ) -> fl.FstList:
    """Template for rewriting mapping fields."""
    if not mapping_list: return fl.FstList()
    return fl.FstList(rw.rewrite_ls(
        [[m.get(old_field), m.get(new_field)] for m in mapping_list],
        preceding, following
    ))

  def _rw_vowel(
      self, mapping_list: list[derom.DeromMapping],
      rom_l: bool = False, brh_l: bool = False
  ) -> fl.FstList:
    """Template for rewriting vowel signs and independent letters."""
    old = 'rom_l' if rom_l else 'rom'
    new = 'brh_l' if brh_l else 'brh'
    ind = new + '_i'
    return fl.FstList(
        self._rw_fields(mapping_list, old, new, iso.SCH_CONS),
        self._rw_fields(mapping_list, old, ind),
    )

  def _rw_ind_to_sign(
      self, mapping_list: list[derom.DeromMapping], brh_l: bool = False
  ) -> fl.FstList:
    """Rewrites word initial vowels to remove superfluous dots in ISO."""
    new = 'brh_l' if brh_l else 'brh'
    old = new + '_i'
    return self._rw_fields(mapping_list, old, new, al.BOW)

  def _rw_cons_vir(
      self, mapping_list: list[derom.DeromMapping], old: str, new: str
  ) -> fl.FstList:
    """Adds virama to consonants not followed by a vowel sign."""
    new_v = new + '_v'
    return fl.FstList(
        self._rw_fields(mapping_list, old, new, following=ltn.VOWEL),
        self._rw_fields(mapping_list, old, new_v),
    )

  def _rw_cons(
      self, mapping_list: list[derom.DeromMapping],
      old: str = 'rom', new: str = 'brh',
      single: bool = True, geminated: bool = True
  ) -> fl.FstList:
    """Template for rewriting consonants.

    Args:
      mapping_list: Deromanization mappings.
      old: Field for input.
      new: Field for output.
      single: When true, non-geminated consonants will be rewritten.
      geminated: When true, geminated consonants will be rewritten.

    Returns:
      FstList

    """
    old_l = old + '_l'
    new_l = new + '_l'
    rewriter = self._rw_fields if self.schwa_deletion else self._rw_cons_vir
    rw_list = fl.FstList()
    if geminated: rw_list.add(rewriter(mapping_list, old_l, new_l))
    if single: rw_list.add(rewriter(mapping_list, old, new))
    return rw_list

  # Shortcuts for specific cases of consonant rewrites.

  def _rw_gem_only(self, mapping_list: list[derom.DeromMapping]) -> fl.FstList:
    return self._rw_cons(mapping_list, single=False)

  def _rw_aspiration(
      self, mapping_list: list[derom.DeromMapping],
      single: bool = True, geminated: bool = True
  ) -> fl.FstList:
    rw_list = fl.FstList()
    if self.schwa_deletion and geminated:
      rw_list.add(self._rw_fields(mapping_list, 'rom_l_h', 'brh_l_asp'))
    return rw_list.add(self._rw_cons(
        mapping_list, 'rom_h', 'brh_asp', single, geminated
    ))

  def _rw_drop_aspiration(
      self, mapping_list: list[derom.DeromMapping]
  ) -> fl.FstList:
    return self._rw_cons(mapping_list, 'rom_h')

  def _rw_foreign(
      self, mapping_list: list[derom.DeromMapping],
  ) -> fl.FstList:
    return self._rw_cons(mapping_list, new='frg')

  # Consonant cluster rewrites for language/scripts with schwa deletion.

  def _rw_cluster_wi(self) -> pyn.Fst:
    return rw.insert(iso.VIR, al.BOW + iso.SCH_CONS, iso.ONSET_CONS)

  def _rw_cluster_wf(self) -> fl.FstList:
    return fl.FstList(
        rw.rewrite_word_final(iso.A, iso.AA),
        rw.insert(iso.VIR, iso.SCH_CONS, iso.ONSET_CONS + al.EOW)
    )

  # Nasal assimilation rewrites.

  def _rw_nasal_labial(self) -> pyn.Fst:
    return rw.rewrite(ltn.M, iso.ANS, ltn.VOWEL, pyn.union(ltn.B, ltn.P))

  def _rw_ans_n(self) -> pyn.Fst:
    return rw.rewrite(
        ltn.N, iso.ANS,
        ltn.VOWEL, pyn.union((ltn.CONS - (ltn.N | ltn.M)), al.EOW)
    )
