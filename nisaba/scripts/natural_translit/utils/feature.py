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

"""Feature class.

Features are defined in Inventories, which are organised by aspects.
For example, objects that have phonological features such as phonemes or
graphemes can be described in terms of syllabicity, voicing, place of
articulation, etc. Each of these would be defined as an aspect in a phonological
feature inventory.
An Aspect object contains all features that are used to describe an aspect, and
keeps track of the distance between all possible features within that aspect,
which can be used to derive weights when constructing fsts or to calculate
similarity scaores for evaluation.
For example,
```
ph_features = Feature.Inventory(
  'phonological_features',
  Feature.Aspect(f.equidistant(
      'syllabicity',
      Feature('syllabic'),
      Feature('nonsyllabic'),
  )),
  Feature.Aspect(Feature.linear(
      'psv_art',
      Feature('alv', 'alveolar'),
      Feature('plt', 'palatal'),
      Feature('vlr', 'velar'),
      step=0.5
  )),
  Feature.Aspect(Feature.linear(
      'act_art',
      Feature('lmn', 'laminal'),
      Feature('adrs', 'antero_dorsal'),
      Feature('pdrs', 'postero_dorsal'),
      step=0.5
  )),
  Feature.Aspect(Feature.linear(
      'stricture',
      Feature('slight'),  # approximant
      Feature('partial'),  # fricative
      Feature('full'),  # stop
  ))
)
```
provides features for describing a phonological object in terms of
syllabicity, passive articulator, active articulator,
and stricture (vocal tract closure).
The active articulator 'act_art' aspect consists of three features,
'laminal', 'antero_dorsal and 'postero_dorsal. It is quantizied linearly,
with a predetermined step of 0.5, meaning that the distance between 'laminal'
and 'antero_dorsal' is 0.5 and the distance between 'laminal' and
'postero_dorsal' is 0.1. Aspect objects keep a dictionary of these hard-coded
distances between all feature pairs in it.

A feature set is a container for features. Feature sets only contain Feature
objects and have a flat structure. The features in a set can be a subset
of possible values for an aspect,
```
dorsal = Feature.Set(ph_features.act_art.adrs, ph_features.act_art.pdrs)
```
or can contain features from different aspects.
```
stop = Feature.Set(
    ph_features.syllabicity.non_syllabic,
    ph_features.stricture.full,
)
velar_dorsal = Feature.Set(
    ph_features.psv_art.vlr,
    dorsal,
)
```

A feature profile defines an object in terms of all aspects in an inventory.
For example:
```
k.phonological_profile = Feature.Profile(
    inventory=ph_features,
    stop,
    velar_dorsal,
)
```
builds a profile for phoneme 'k' as follows:
- syllabicity: non_syllabic
- passive_articulator: velar
- active_articulator: antero_dorsal or postero_dorsal
- stricture: full
"""

from __future__ import annotations

import enum
from typing import Iterable, Union

import tabulate

from nisaba.scripts.natural_translit.utils import inventory
from nisaba.scripts.natural_translit.utils import type_op as ty


_L_BRACE = '{'
_R_BRACE = '}'


class Feature(ty.Thing):
  """A Feature is a contrastive value for an Aspect of an object.

  For example, an object 'room' can have aspects and a list of possible features
  such as:
    - color: red, orange, yellow, green, blue, purple
    - warmth: very cold, cold, chilly, tepid, warm, hot, very hot
    - function: living room, bedroom, kitchen
  """

  ITERABLE = Union['Feature', Iterable, ty.Nothing]
  ASPECTS = Union['Feature.Aspect', Iterable['Feature.Aspect'], ty.Nothing]
  ERROR_DISTANCE = 1_000_000

  def __init__(self, alias: str, text: str = ''):
    super().__init__(alias)
    self.text = text if text else alias
    self.aspect = inventory.Inventory.EMPTY
    self.inventory = inventory.Inventory.EMPTY
    self.parent_list = []

  def __str__(self):
    text = f'  {self.alias} ({self.text}) = {_L_BRACE}\n'
    for k, v in self.distance_dict().items():
      text += f'        {k.alias} ({k.text}): {v:.2f}\n'
    text += f'  {_R_BRACE}\n'  # right curly bracket
    return text

  def add_distance(
      self, values: Feature.Aspect.VALUES, distance: float
  ) -> None:
    """Adds an entry to the distance dict for each feature in f."""
    if isinstance(values, Feature) and isinstance(self.aspect, Feature.Aspect):
      self.aspect.add_distance(self, values, distance)
    elif isinstance(values, Feature.ValueList):
      for value in values:
        self.add_distance(value, distance)

  def distance_dict(self) -> dict[Feature, float]:
    return self.aspect.distance_dict.get(self)

  def distance(self, features: Feature.ITERABLE) -> float:
    """The distance between this feature and the given feature or feature set.

    Args:
      features: Feature or Feature set to be compared.

    Returns:
    If the argument or an item in the argument is of the same aspect as this
    feature:
      If the argument is a feature, returns the distance between this feature
      and the argument.
      If the argument is a feature set, returns the minimum distance between
      this feature and the features in the argument.
    Else returns ERROR_DISTANCE.
    TODO: Reevaluate the distance for non-comparible features or sets.
    """
    max_dist = Feature.ERROR_DISTANCE
    if isinstance(features, Feature):
      if features.aspect != self.aspect:
        return max_dist
      if (
          features == self
          or features == self.aspect.any
          or self == self.aspect.any
      ):
        return 0
      if features == self.aspect.n_a or self == self.aspect.n_a:
        return self.aspect.max_dist
      return self.distance_dict().get(features, self.aspect.max_dist)
    if isinstance(features, Feature.Set):
      if self in features:
        return 0
      return min([max_dist] + [self.distance(feature) for feature in features])
    return max_dist

  def is_in(self, obj: ...) -> bool:
    """Checks if this feature is contained within the given object."""
    return value_in(self, obj)

  class Set(ty.IterableThing):
    """Feature set.

    A set can contain a subset of an aspect's features,
    not_cold = {
        warmth.chilly, warmth.tepid, warmth.warm, warmth.hot, warmth.very hot
    }
    or features from different aspects,
    blue_kitchen = {color.blue, function.kitchen}
    """

    def __init__(self, *features, alias: str = ''):
      super().__init__(alias=alias)
      if alias:
        self.text = alias
      self._items = set()
      self._item_type = Feature
      self.add(*features)

    def __str__(self):
      return (
          f'{self.alias}:'
          f' {_L_BRACE}{", ".join(self.sorted_item_texts())}{_R_BRACE}'
      )

    def sorted_item_texts(self) -> list[str]:
      return sorted(item.text for item in self._items)

    def _item_set(self) -> set[Feature]:
      return ty.type_check(self._items, set(self._items))

    def add(self, *features: Feature.ITERABLE) -> Feature.Set:
      for feature in features:
        if isinstance(feature, Feature):
          self._item_set().add(feature)
        elif isinstance(feature, Iterable):
          self.add(*feature)
      return self

    @classmethod
    def group_by_aspect(
        cls, *features: Feature.ITERABLE
    ) -> dict[Feature.Inventory, dict[Feature.Aspect, Feature.Set]]:
      dictionary = {}
      for feature in Feature.Set(*features):
        if feature.inventory not in dictionary:
          dictionary[feature.inventory] = {}
        value_set = dictionary[feature.inventory].get(
            feature.aspect, Feature.Set(alias=feature.aspect.alias)
        )
        dictionary[feature.inventory] |= {
            feature.aspect: value_set.add(feature)
        }
      return dictionary

    def remove(self, *features) -> Feature.Set:
      for feature in Feature.Set(*features):
        self._item_set().discard(feature)
      return self

    def replace(
        self,
        old: tuple[Feature.ITERABLE, ...],
        new: tuple[Feature.ITERABLE, ...],
    ) -> Feature.Set:
      self.remove(*Feature.Set(old))
      self.add(*Feature.Set(new))
      return self

    def reset(self) -> Feature.Set:
      self._items = set()
      return self

    def update(self, *features) -> Feature.Set:
      return self.reset().add(*features)

    def copy(self) -> Feature.Set:
      return Feature.Set(self)

    def difference(self, *features) -> Feature.Set:
      return Feature.Set(*self._item_set().difference(Feature.Set(*features)))

    def union(self, *features) -> Feature.Set:
      return Feature.Set(*self._item_set().union(Feature.Set(*features)))

    def intersection(self, *features) -> Feature.Set:
      return Feature.Set(*self._item_set().intersection(Feature.Set(*features)))

    def distance(self, features: Feature.ITERABLE) -> float:
      """Returns the minimum distance between the items in this set and f."""
      min_dist = Feature.ERROR_DISTANCE
      for feature in Feature.Set(features):
        if feature in self:
          return 0
        dist = feature.distance(self)
        if dist == 0:
          return 0
        if dist < min_dist:
          min_dist = dist
      return min_dist

    def has_feature(self, value: Feature.Aspect.VALUES):
      """Checks if the given value or one of its children is in this set."""
      if value in self:
        return True
      return any(value in feature.parent_list for feature in self)

    def non_generic(self, alias: str = '') -> Feature.Set:
      """Returns a copy of set without aspect.any and aspect.n_a features."""
      return Feature.Set(
          [
              feature
              for feature in self
              if feature != feature.aspect.any and feature != feature.aspect.n_a
          ],
          alias=(alias if alias else self.alias + '_non_generic'),
      )

    def is_equal(self, feature_set: Feature.Set) -> bool:
      return feature_set is self or set(self) == set(feature_set)

  class ValueListType(enum.Enum):
    EQUIDISTANT = 0
    LINEAR = 1
    CYCLIC = 2

  class ValueList(ty.IterableThing):
    """A list of contrastive features for an Aspect.

    The distance between the items of the list is calculated based on the list
    type and the step attribute.

    Equidistant: The distance between any two items is equal to step.
    Eg. function: 'bedroom, living_room, office', step = 1
      bedroom_features.distance_dict = {
          living_room: 1
          office: 1
      }

    Linear: The distance between two items increases by step in one direction.
    Eg. warmth: 'very_cold, cold, chilly, tepid, warm, hot, very_hot', step: 0.5
      very_cold.distance_dict = {
        cold: 0.50
        chilly: 1.00
        tepid: 1.50
        warm: 2.00
        hot: 2.50'
        very_hot: 3.00
      }

    Cyclic: The distance between two items increase in both directions until
      halfway, then starts decreasing by step so that the distance between the
      first and the last items in the list is equal to step.
    Eg. color: 'red, orange, yellow, green, blue, purple', step = 0.5
      red.distance_dict = {
        orange: 0.50
        yellow: 1.00
        green: 1.50
        blue: 1.00
        purple: 0.50
      }

    The step value can be 0, which means that there is no quantitative
    difference between the features, but there is a qualitative difference
    and distinct labels allow for more precise rules, eg.
    given
      shape: equidistant(
        square,
        triangle: equidistant(equilateral, isoceles, scalene, step=0)
        round
      )
    the distances for scalene would be:
      scalene.distance_dict = {
          square: 1.00
          equilaterl: 0.00
          isoceles: 0.00
          round: 1.00
      }
    resulting in all troangular rooms to match in terms of shape, but
    there can be different rules for the precise shapes eg.
    if room.has_feature(equilateral): do x
    """

    def __init__(
        self,
        alias: Union[str, tuple[str, str]],
        list_type: Feature.ValueListType,
        step: float,
        *features: Feature.Aspect.VALUES,
    ):
      alias, text = ty.type_check(alias, (alias, alias))
      super().__init__(alias=alias)
      self.text = text
      self._item_type = Union[Feature, Feature.ValueList]
      self.add(*features)
      self.list_type = list_type
      self.step = step
      self.parent_list = []

    def distance(
        self, values1: Feature.Aspect.VALUES, values2: Feature.Aspect.VALUES
    ) -> float:
      if values1 not in self or values2 not in self:
        return Feature.ERROR_DISTANCE
      delta = self._items.index(values2) - self._items.index(values1)
      match self.list_type:
        case Feature.ValueListType.EQUIDISTANT:
          return self.step
        case Feature.ValueListType.LINEAR:
          return delta * self.step
        case Feature.ValueListType.CYCLIC:
          return min(delta, len(self) - delta) * self.step
      return Feature.ERROR_DISTANCE

    def add_distance(
        self, values: Feature.Aspect.VALUES, distance: float
    ) -> None:
      for item in self._items:
        item.add_distance(values, distance)

    def populate(self, aspect: Feature.Aspect) -> None:
      """Populates the aspect from the features and lists in this list.

      Args:
        aspect: The aspect that will be populated by the features in this list.

      Adds features in this list as items to the aspects. Updates the distance
      dictionary. Adds self as supplement to the aspect.
      """
      aspect.add_suppl(self)
      for i, item in enumerate(self):
        item.parent_list = [self] + self.parent_list
        if isinstance(item, Feature) and item not in aspect:
          aspect.add_feature(item)
        elif isinstance(item, Feature.ValueList):
          item.populate(aspect)
        for item2 in self._items[i + 1 :]:
          item.add_distance(item2, self.distance(item, item2))

    def set(self) -> Feature.Set:
      """Returns a set of features in this list."""
      return Feature.Set(self)

    def range(
        self, first: Feature.Aspect.VALUES, last: Feature.Aspect.VALUES
    ) -> Feature.Set:
      """Returns a set of features in this list between and including the args.

      Args:
        first: The first feature or value list to be included in the range.
        last: The last feature or value list to be included in the range.

      Returns:
          Feature set.

      Range is defined cyclically regardless of the list type. For example:
      For list l with values [f1, f2, f3, f4, f5, f6], whether the list is
      equidistant, linear, or cyclical
      `l.range(f2, f5)` returns `Feature.Set(f2, f3, f4, f5)`
      `l.range(f5, f2)` returns `Feature.Set(f5, f6, f1, f2)`

      If first and last are not items of the same list, returns an empty
      feature set.

      TODO: Decide what to do if the arguments are in the same aspect
      but not in the same list. For example:
      ```
      a = Aspect(linear(
        'a',
        f1, equidistant('b', f2, f3), f4, f5, linear('c', f6, f7, f8, f9), f10,
        ))
      ```
      the options for call `a.range(f3, f8)` are:
      a. empty set (current behaviour): `Feature.Set()`
      b. include items based on the order of definition:
        `Feature.Set(f3, f4, f5, f6, f7, f8)`
      c. include all items in sublists, eqivalent to `a.range(b, c)`
        `Feature.Set(f2, f3, f4, f5, f6, f7, f8, f9)`
      d. include all items in equidistant sublists, but only the range from/to
        the specified argument in the linear or cyclical sublists,
        equivalent to a.range(b, f5).union(c.range(f6, f8)):
        `Feature.Set(f2, f3, f4, f5, f6, f7, f8)`
      Option a requires ranges that begin and/or end in sublists to be defined
      using multiple ranges and unions, but it's the most precise way to
      make sure all and only the intended items are included.
      Options b and d make the order of items in equidistant lists and the
      starting point of cyclical lists more significant, and ranges that don't
      adhere to the aspect definition order will still require complicated range
      definitions a la option a.
      Options c and d can get out of hand when dealing with multiple levels
      of nesting, especially with mixed list types.
      ```
      """
      if first.parent_list[0] != self or last.parent_list[0] != self:
        return Feature.Set()
      i1, i2 = self._items.index(first), self._items.index(last)
      start, stop = min(i1, i2), max(i1, i2)
      between = Feature.Set(self._items[start + 1 : stop])
      if i1 < i2:
        return between.union(first, last)
      return self.set().difference(between)

    def has_feature(self, value: Feature.Aspect.VALUES) -> bool:
      """Checks if the given value or one of its children is in this list."""
      return value.is_in(self)

    def is_in(self, obj: ...) -> bool:
      """Checks if this list is contained within the given object."""
      return value_in(self, obj)

    def visualize(self) -> str:
      """Returns graphviz subgraph for the ValueList."""
      graph = ''
      for item in self:
        graph += (
            f'{item.alias} [label="{item.text.title()}"]\n'
            f'{self.alias} -- {item.alias}\n'
        )
        if isinstance(item, Feature.ValueList):
          graph += (
              f'subgraph {_L_BRACE}\n'
              f'{item.visualize()}{_R_BRACE}\n'
          )
      return graph

  class Aspect(inventory.Inventory):
    """An aspect that can be defined by a list of contrastive values.

    Each aspect has a distance dictionary with pre-calculated distances to
    other features for the same aspect. For example, for Feature 'red' in
    Aspect 'color' a sample dictionary can look like:

    color.distance_dict[red] = {
        orange: 0.50
        yellow: 1.00
        green: 1.50
        blue: 1.00
        purple: 0.50
    }

    TODO: Add bidict method to Inventory and convert distance_dict
    to bidict.
    """

    VALUES = Union['Feature', 'Feature.ValueList']

    def __init__(self, feature_list: Feature.ValueList):
      super().__init__(feature_list.alias)
      self.root_list = feature_list
      self.text = feature_list.text
      self.inventory = ty.UNASSIGNED
      self.max_dist = 0
      self.distance_dict = {}

    def __str__(self):
      """Distance matrix of this aspect as table in github format."""
      headers = ['distances'] + [feature.text for feature in self]
      table = [
          [feature1.text] + [feature1.distance(feature2) for feature2 in self]
          for feature1 in self
      ]
      return (
          f'aspect: {self.text}\nmax_dist: {self.max_dist:.2f}\n\n'
          + tabulate.tabulate(table, headers, tablefmt='github')
          + '\n'
      )

    def add_feature(self, feature: Feature) -> None:
      self.add_item(feature)
      feature.aspect = self
      feature.inventory = self.inventory
      self.distance_dict[feature] = {}

    def suppl_feature(self, feature: Feature) -> None:
      self.add_suppl(feature)
      feature.aspect = self
      feature.inventory = self.inventory

    def add_distance(
        self, feature1: Feature, feature2: Feature, distance: float
    ) -> None:
      if feature1 not in self:
        self.add_feature(feature1)
      if feature2 not in self:
        self.add_feature(feature2)
      self.distance_dict[feature1][feature2] = distance
      self.distance_dict[feature2][feature1] = distance
      if distance > self.max_dist:
        self.max_dist = distance

    def filter(self, *features) -> Feature.Set:
      return Feature.Set(*[
          feature
          for feature in Feature.Set(*features)
          if feature.aspect == self
      ])

    def _make_set(
        self, alias: str, *features, negation: bool = False
    ) -> Feature.Set:
      filtered = self.filter(*features)
      to_add = filtered if not negation else self.all.difference(filtered)
      return Feature.Set(to_add, alias=alias)

    def set(self, alias: str, *features) -> None:
      self.add_suppl(self._make_set(alias, *features))

    def set_not(self, alias: str, *features) -> None:
      self.add_suppl(self._make_set(alias, *features, negation=True))

    def set_range(
        self,
        alias: str,
        first: Feature.Aspect.VALUES,
        last: Feature.Aspect.VALUES,
    ) -> None:
      self.add_suppl(
          self._make_set(alias, first.parent_list[0].range(first, last))
      )

    def populate(self, ft_inventory: inventory.Inventory) -> None:
      """Populates the aspect from its root_list and adds it to inventory.

      Args:
        ft_inventory: The Feature inventory this Aspect is defined in.

      The item values of the Aspect are the features in its root_list. Max_dist
      of an aspect is the max possible distance between two features of
      this aspect. Every aspect has two supplement features: 'any' which returns
      0 distance to all features of this aspect, and n_a (not applicable),
      which returns max_dist to all features. The root_list and any value list
      within are added as supplements to the aspect.
      """
      self.inventory = ft_inventory
      self.inventory.add_item(self)
      self.root_list.populate(self)
      self.set('all', self)
      self.suppl_feature(Feature('any'))
      self.suppl_feature(Feature('n_a', 'not_applicable'))

    def has_feature(self, value: VALUES) -> bool:
      """Checks if the given value or one of its children is in this aspect."""
      return value.is_in(self)

    def is_applicable(self, profile: Feature.Profile) -> bool:
      """Checks if this aspect is applicable to the given profile."""
      return (
          profile.inventory == self.inventory
          and self.n_a not in profile.get(self)
      )

    def visualize(self) -> str:
      """Returns markdown dot code block for the Aspect."""
      r = self.root_list
      return (
          f'```dot\ngraph {_L_BRACE}\n'
          'ordering="out"\nsize = 12\nrankdir="LR"\nranksep="1, equally"\n'
          'style="invis"\nnode [shape="plain"]\n'
          f'{r.alias} [label="{r.text.capitalize()}"]\n{r.visualize()}'
          f'{_R_BRACE}\n```'
      )

  class Inventory(inventory.Inventory):
    """An inventory of Aspects and their contrastive features.

    The structure of a feature inventory:

    Inventory:

    - Aspects: aspect.alias: aspect
        - Features: feature.alias: feature
        - ValueLists: list.alias: list
        - Sets: set.alias: set
    - Profiles: profile.alias: profile
        - Profile features: aspect.alias: set

    All inventories have a 'n_a' profile with all aspects set to 'not
    applicable'. This will be used for objects that don't have any features
    for this inventory. Eg. while comparing the phonological profiles of a
    letter such as 'a' and a non-phonological character such as a zero-width
    space or a non-joiner, as well as handling error conditions.
    """

    def __init__(self, alias: str, *aspects: Feature.Aspect, text: str = ''):
      super().__init__(alias)
      if text:
        self.text = text
      for aspect in aspects:
        aspect.populate(self)
      self.add_profile('not_applicable', unspecified_aspect_n_a=True)

    def __str__(self):
      """String representation of all aspects in the inventory."""
      # Do not remove the header line.
      return f'{self.header()}\n\n' + '\n'.join(f'### {a}' for a in self)

    def aspect_dict(
        self, *features: Feature.ITERABLE
    ) -> dict[Feature.Aspect, Feature.Set]:
      return Feature.Set.group_by_aspect(*features).get(self, {})

    def add_profile(
        self,
        alias: str,
        *features: Feature.ITERABLE,
        unspecified_aspect_n_a: bool = False,
    ) -> Feature.Profile:
      new = Feature.Profile(
          self, alias, *features, unspecified_aspect_n_a=unspecified_aspect_n_a
      )
      self.add_suppl(new)
      return new

    def copy_profile(self, old: Feature.Profile, alias: str) -> Feature.Profile:
      return self.add_profile(alias, *old)

    def make_sets(self, *alias_features: tuple[str, Feature.ITERABLE]) -> None:
      """Adds mixed-aspect feature sets to the inventory as supplements."""
      for alias, features in alias_features:
        self.add_suppl(Feature.Set(features, alias=alias))

  class Profile(inventory.Inventory):
    """Feature profile for an object based on a feature inventory.

    The item aliases of a profile are the aspect aliases in the feature
    inventory, and item values are the features that apply to the object.

    Example:
      room_features.add_profile(
          'blue_bedroom_unlocked'
          room_features.function.bedroom,
          room_features.color.blue,
          room_features.ligthing.any,
          room_features.warmth.any,
          room_features.door.set_not(room_features.door.locked),
      )

    Commonly used profiles can be stored in the inventory and used by
    multiple objects, as well as dynamically copied and updated for new objects.
    For example, given a Room object with a 'with_profile' method,
    a list of blue_bedroom_unlocked rooms with different lighting options
    can be derived as:
    blue_bedrooms = [
        Room.with_profile(
            room_features.blue_bedroom_unlocked.copy_and_update(light)
            )
        for light in room_features.lighting
    ]
    """

    def __init__(
        self,
        feature_inventory: Feature.Inventory,
        alias: str,
        *features: Feature.ITERABLE,
        unspecified_aspect_n_a: bool = False,
    ):
      """Creates a feature profile for a given inventory.

      Args:
        feature_inventory: The inventory of features to be used in this profile.
        alias: The alias of the feature profile.
        *features: Features to be added to the profile.
        unspecified_aspect_n_a: If true, the default value for an aspect is n_a
          (not_applicable) instead of any.
      """
      super().__init__(alias)
      self.inventory = feature_inventory
      self.max_dist = 0
      aspect_dict = self.inventory.aspect_dict(*features)
      for aspect in self.inventory:
        value = aspect_dict.get(
            aspect, aspect.n_a if unspecified_aspect_n_a else aspect.any
        )
        self.add_item(Feature.Set(value, alias=aspect.alias))
        self.max_dist += aspect.max_dist

    def __str__(self):
      return (
          self.alias
          + ' profile:\n\n'
          + tabulate.tabulate(
              self.table_contents(),
              headers=['aspects', 'values'],
              tablefmt='github',
          )
          + '\n'
      )

    def table_contents(self) -> list[list[str]]:
      """Returns the profile as github table contents table."""
      return [
          [aspect.alias] + [', '.join(aspect.sorted_item_texts())]
          for aspect in self
      ]

    def get(self, aspect: Feature.Aspect) -> Feature.Set:
      """Gets the value set for the given aspect."""
      if aspect.inventory == self.inventory:
        inventory_alias = 'missing'
      else:
        inventory_alias = aspect.inventory.alias
      return super().get(
          aspect.alias,
          Feature.Set(aspect.n_a, alias=f'{inventory_alias}_{aspect.alias}'),
      )

    def copy(self, alias: str) -> Feature.Profile:
      return Feature.Profile(self.inventory, alias, *self)

    def update(self, *features: Feature.ITERABLE) -> Feature.Profile:
      """Updates the profile with the given features.

      Args:
        *features: values to be replaced.

      Returns:
        Profile.

      Example:
      Feature.Profile(
          room_features,
          'white_office'
          room_features.function.office,
          room_features.color.white,
          room_features.ligthing.any,
          room_features.warmth.any,
          room_features.door.any,
      )
      white_office.update(room_features.warmth.hot)

      yields

      Feature.Profile(
          room_features,
          'white_office'
          room_features.function.office,
          room_features.color.white,
          room_features.ligthing.any,
          room_features.warmth.hot,
          room_features.door.any,
      )
      """
      for aspect, value in self.inventory.aspect_dict(*features).items():
        self.get(aspect).update(value)
      return self

    def compare(
        self,
        p: Feature.Profile,
        aspects: Feature.ASPECTS = ty.UNSPECIFIED,
        verbose: bool = False,
    ) -> dict[str, Union[str, float]]:
      """Compares this Profile to another Profile.

      Args:
        p: Profile to be compared.
        aspects: contrastive aspects to be included while calculating the
          distance and similarity.
        verbose: If false, aspects with zero distance are not included in the
          output table.

      Returns:
        Comparison table as string, similarity score as float
      """
      if p.inventory != self.inventory:
        return {
            'text': (
                f'{self.inventory.alias} and {p.inventory.alias} profiles are'
                ' not comparable\n    Similarity = 0\n'
            ),
            'similarity': 0,
        }
      if isinstance(aspects, ty.Nothing):
        aspects = self.inventory
      total_dist = 0
      max_dist = 0
      headers = ['aspect', self.text, p.text, 'distance']
      table = []
      for aspect in aspects:
        item1 = self.get(aspect)
        item2 = p.get(aspect)
        dist = item1.distance(item2)
        total_dist += dist
        max_dist += aspect.max_dist
        if verbose or dist:
          table.append([
              aspect.alias,
              ', '.join(item1.sorted_item_texts()),
              ', '.join(item2.sorted_item_texts()),
              f'{dist:.2f}',
          ])
      similarity = 1 - total_dist / max_dist
      table.extend([
          ['Total distance', '', '', f'{total_dist:.2f}'],
          ['Similarity', '', '', f'{similarity:.3f}'],
      ])
      text = (
          self.inventory.alias
          + f' comparison (max distance = {max_dist:.2f}):\n\n'
          + tabulate.tabulate(table, headers, tablefmt='github')
          + '\n'
      )
      return {'text': text, 'similarity': similarity}

    def comparison_table(
        self,
        p: Feature.Profile,
        aspects: Feature.ASPECTS = ty.UNSPECIFIED,
        verbose: bool = False,
    ) -> str:
      return self.compare(p, aspects, verbose)['text']

    def similarity(
        self, p: Feature.Profile, aspects: Feature.ASPECTS = ty.UNSPECIFIED
    ) -> float:
      return self.compare(p, aspects)['similarity']

    def has_feature(self, value: Feature.Aspect.VALUES) -> bool:
      """Checks if the given value or one of its children is in this profile."""
      return any(feature_set.has_feature(value) for feature_set in self)

  class MultiProfile(inventory.Inventory):
    """Class for storing profiles for multiple feature inventories."""

    def __init__(self, alias: str):
      super().__init__(alias, typed=Feature.Profile)

    def __str__(self):
      """String representation of all profiles in the multi-profile."""
      headers = ['aspects', 'values']
      table = []
      for profile in self:
        table += [['**' + profile.alias + '**', ' ']] + profile.table_contents()
      return (
          self.alias
          + ' features:\n\n'
          + tabulate.tabulate(table, headers, tablefmt='github')
          + '\n'
      )

    def has_profile(self, feature_inventory: Feature.Inventory) -> bool:
      """Checks if the multi-profile has a profile for the given inventory."""
      return any(profile.inventory == feature_inventory for profile in self)

    def new_profile(self, profile: Feature.Profile) -> Feature.Profile:
      """Adds a copy of the given profile to the multi-profile.

      Args:
        profile: The profile to be copied and added. If there is already a
          profile for the same inventory, all aspects of the old profile will be
          replaced with the new profile. The alias for the new profile will be
          changed so that the profile can be called by the inventory alias.

      Returns:
        The new profile.

      Example:

      Given a phoneme 'ph.s' with a MultiProfile feature attribute and a feature
      inventory 'phonological' with a predefined profile 'fricative' with 'any'
      place:
      ```
      ph.s.features.new_profile(phonological.fricative)
      ```
      will add a copy of the fricative profile to ph.s.features.
      ```
      ph.s.features.phonological.update(phonological.place.alveolar)
      ```
      will update the place aspect of the phonological profile in 'ph.s'
      features without changing the predefined profile in the inventory.
      """
      new = profile.copy(profile.inventory.alias)
      if self.has_profile(profile.inventory):
        self.get(profile.inventory).update(new)
      else:
        self.add_item(new)
      return new

    def get(
        self,
        feature_inventory: Feature.Inventory,
        default: Union[Feature.Profile, ty.Nothing] = ty.UNSPECIFIED,
    ) -> Feature.Profile:
      """Gets the feature profile for the given inventory.

      Args:
        feature_inventory: The inventory requested for the profile.
        default: The default profile to be returned if there is no profile for
          the given inventory.

      Returns:
        The profile for the given inventory, or the default profile if there is
        no profile for the given inventory. If the default is not specified,
        the not_applicable profile for the given inventory is returned.
      """
      if self.has_profile(feature_inventory):
        return super().get(feature_inventory.alias)
      return ty.type_check(default, feature_inventory.not_applicable)

    def copy(self, alias: str = '') -> Feature.MultiProfile:
      new = Feature.MultiProfile(alias if alias else self.alias)
      for profile in self:
        new.new_profile(profile.copy(profile.alias))
      return new

  @classmethod
  def equidistant(
      cls,
      alias: Union[str, tuple[str, str]],
      *values: Feature.Aspect.VALUES,
      step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.EQUIDISTANT, step, *values)

  @classmethod
  def linear(
      cls,
      alias: Union[str, tuple[str, str]],
      *values: Feature.Aspect.VALUES,
      step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.LINEAR, step, *values)

  @classmethod
  def cyclic(
      cls,
      alias: Union[str, tuple[str, str]],
      *values: Feature.Aspect.VALUES,
      step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.CYCLIC, step, *values)


def value_in(value: Feature.Aspect.VALUES, obj: ...) -> bool:
  """Checks if a feature value is contained within an object.

  Args:
    value: The value to be checked.
    obj: The object to be checked.

  Returns:
    If the object is the same as the value or the object is an iterable and
      the value is in the iterable, returns True.
    If the object, for example a symbol, has a has_feature method, returns the
      result of has_feature.
    If the value is a ValueList, recursively checks all values contained within
      the list and returns true if a match is found.
    Example:
      ```
      f.Aspect(
          f.equidistant('gr_class',
              f.equidistant('boundary',
                  f.equidistant('punct',
                      f('end'), f('left'), f('right'), f('split'),
                      step=0.25,
                  ),
                  f('space'),
                  step=0.25,
          ),
      hyphen = Symbol(features={left, right, split})
      ```
      `value_in(gr_class.split, hyphen.features)`: `True`
      `value_in(gr_class.left, hyphen.features)`: `True`
      `value_in(gr_class.punct, hyphen.features)`: `True`
      `value_in(gr_class.boundary, hyphen.features)`: `True`
      `value_in(gr_class.space, hyphen.features)`: `False`
  """
  return (
      (hasattr(obj, 'has_feature') and obj.has_feature(value))
      or obj == value
      or obj in value.parent_list
      or (isinstance(obj, Iterable) and value in Feature.Set(obj))
  )
