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

"""Feature, FeatureSet and FeatureInventory classes."""

from typing import Union
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


class Feature(ty.Thing):
  """Feature class."""

  def __init__(self, alias: str, category: str, group: str = ''):
    super().__init__()
    self.set_alias(alias)
    self.text = alias
    self.category = category
    self.group = group if group else ty.UNASSIGNED


class FeatureSet:
  """FeatureSet class."""

  UNION = Union[Feature, 'FeatureSet', ty.Nothing]

  def __init__(
      self,
      *items: UNION
  ):
    super().__init__()
    self._items = set()
    self.add(*items)

  def __iter__(self):
    return self._items.__iter__()

  def __len__(self):
    return len(self._items)

  def __str__(self):
    return self.str()

  def _set(self, arg: UNION) -> set[Feature]:
    if isinstance(arg, Feature): return {arg}
    if isinstance(arg, FeatureSet): return {f for f in arg}
    return set()

  def _flat_set(self, *args: UNION) -> set[Feature]:
    s = set()
    for arg in args:
      s.update(self._set(arg))
    return s

  def str(self):
    return '(%s)' % ', '.join(f.text for f in self._items)

  def add(self, *args: UNION) -> None:
    old = self.str()
    self._items.update(self._flat_set(*args))
    log.dbg_message('(%s) to %s: %s' % (
        ', '.join(log.class_and_text(arg) for arg in args),
        old, self.str()
    ))

  def remove(self, *args: UNION) -> None:
    old = self.str()
    for f in self._flat_set(*args):
      self._items.discard(f)
    log.dbg_message('(%s) to %s: %s' % (
        ', '.join(log.class_and_text(arg) for arg in args),
        old, self.str()
    ))


class FeatureInventory(inventory2.Inventory):
  """Feature inventory."""

  def __init__(self, category: str):
    super().__init__()
    self.category = category
    self.group_aliases = []

  def add_feature(self, alias: str) -> None:
    self.add_item(Feature(alias, self.category))

  def make_group(self, group: str, aliases: list[str]) -> None:
    features = []
    for alias in aliases:
      new = Feature(alias, self.category, group)
      if self.add_item(new): features.append(new)
    self.make_supp(group, features)
    self.group_aliases.append(group)

  def add_feature_set(
      self, set_alias: str, *features: FeatureSet.UNION
  ) -> None:
    self.make_supp(set_alias, FeatureSet(*features))
