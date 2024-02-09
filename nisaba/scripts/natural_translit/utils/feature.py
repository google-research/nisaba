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

import enum
from typing import Iterable, Union
from nisaba.scripts.natural_translit.utils import inventory2
from nisaba.scripts.natural_translit.utils import type_op as ty


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
    super().__init__()
    self.set_alias(alias)
    self.text = text if text else alias
    self.aspect = inventory2.Inventory.EMPTY
    self.inventory = inventory2.Inventory.EMPTY
    self.parent_list = []

  def __str__(self):
    text = '  %s (%s) = {\n' % (self.alias, self.text)
    for k, v in self.distance_dict().items():
      text += '        %s (%s): %.2f\n' % (k.alias, k.text, v)
    text += '  }\n'
    return text

  def add_distance(
      self, values: 'Feature.Aspect.VALUES', distance: float
  ) -> None:
    """Adds an entry to the distance dict for each feature in f."""
    if isinstance(values, Feature) and isinstance(self.aspect, Feature.Aspect):
      self.aspect.add_distance(self, values, distance)
    elif isinstance(values, Feature.ValueList):
      for value in values:
        self.add_distance(value, distance)

  def distance_dict(self) -> dict['Feature', float]:
    return self.aspect.distance_dict.get(self)

  def distance(self, features: 'Feature.ITERABLE') -> float:
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
      if features.aspect != self.aspect: return max_dist
      if (
          features == self
          or features == self.aspect.any
          or self == self.aspect.any
      ): return 0
      if features == self.aspect.n_a or self == self.aspect.n_a:
        return self.aspect.max_dist
      return self.distance_dict().get(features, self.aspect.max_dist)
    if isinstance(features, Feature.Set):
      if self in features: return 0
      return min(
          [max_dist] + [self.distance(feature) for feature in features]
      )
    return max_dist

  class Set(ty.Thing):
    """Feature set.

    A set can contain a subset of an aspect's features,
    not_cold = {
        warmth.chilly, warmth.tepid, warmth.warm, warmth.hot, warmth.very hot
    }
    or features from different aspects,
    blue_kitchen = {color.blue, function.kitchen}
    """

    def __init__(self, *features):
      super().__init__()
      self._items = set()
      self.add(*features)

    def __iter__(self):
      return self._items.__iter__()

    def __len__(self):
      return len(self._items)

    def __str__(self):
      items = [item.text for item in self._items]
      items.sort()
      return '%s: {%s}' % (
          self.alias, ', '.join(items)
      )

    @classmethod
    def with_alias(cls, alias: str, *features) -> 'Feature.Set':
      new = cls(*features)
      new.set_alias(alias)
      new.text = alias
      return new

    @classmethod
    def aspect_dict(
        cls, *features: 'Feature.ITERABLE'
    ) -> dict['Feature.Aspect', 'Feature.Set']:
      distances = {}
      for feature in Feature.Set(*features):
        value_set = distances.get(feature.aspect, Feature.Set())
        distances.update({feature.aspect: value_set.add(feature)})
      return distances

    # TODO: Decide what to do with any and n_a in add/remove/replace
    def add(self, *features) -> 'Feature.Set':
      """Adds features to the set, flattens tree structures in arguments."""
      for f in features:
        if isinstance(f, Feature):
          self._items.add(f)
        elif isinstance(f, Iterable):
          for item in f:
            self.add(item)
      return self

    def remove(self, *features) -> 'Feature.Set':
      for feature in Feature.Set(*features):
        self._items.discard(feature)
      return self

    def replace(
        self, old: tuple['Feature.ITERABLE', ...],
        new: tuple['Feature.ITERABLE', ...]
    ) -> 'Feature.Set':
      for feature in Feature.Set(old):
        self.remove(feature)
      for feature in Feature.Set(new):
        self.add(feature)
      return self

    def reset(self) -> 'Feature.Set':
      self._items = set()
      return self

    def update(self, *features) -> 'Feature.Set':
      return self.reset().add(*features)

    def copy(self) -> 'Feature.Set':
      return Feature.Set(self)

    def difference(self, *features) -> 'Feature.Set':
      return Feature.Set(*self._items.difference(Feature.Set(*features)))

    def union(self, *features) -> 'Feature.Set':
      return Feature.Set(*self._items.union(Feature.Set(*features)))

    def intersection(self, *features) -> 'Feature.Set':
      return Feature.Set(*self._items.intersection(Feature.Set(*features)))

    def distance(self, features: 'Feature.ITERABLE') -> float:
      """Returns the minimum distance between the items in this set and f."""
      min_dist = Feature.ERROR_DISTANCE
      for feature in Feature.Set(features):
        if feature in self: return 0
        dist = feature.distance(self)
        if dist == 0: return 0
        if dist < min_dist: min_dist = dist
      return min_dist

  class ValueListType(enum.Enum):
    EQUIDISTANT = 0
    LINEAR = 1
    CYCLIC = 2

  class ValueList(ty.Thing):
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
        self, alias: Union[str, tuple[str, str]],
        list_type: 'Feature.ValueListType',
        step: float, *features: 'Feature.Aspect.VALUES',
    ):
      super().__init__()
      alias, text = alias if isinstance(alias, tuple) else alias, alias
      self.set_alias(alias)
      self.text = text
      self._items = list(features)
      self.list_type = list_type
      self.step = step
      self.parent_list = self

    def __iter__(self):
      return self._items.__iter__()

    def __len__(self):
      return len(self._items)

    def distance(
        self, values1: 'Feature.Aspect.VALUES', values2: 'Feature.Aspect.VALUES'
    ) -> float:
      if values1 not in self or values2 not in self:
        return Feature.ERROR_DISTANCE
      delta = self._items.index(values2) - self._items.index(values1)
      match self.list_type:
        case Feature.ValueListType.EQUIDISTANT: return self.step
        case Feature.ValueListType.LINEAR: return delta * self.step
        case Feature.ValueListType.CYCLIC:
          return min(delta, len(self) - delta) * self.step
      return Feature.ERROR_DISTANCE

    def add_distance(
        self, values: 'Feature.Aspect.VALUES', distance: float
    ) -> None:
      for item in self._items:
        item.add_distance(values, distance)

    def populate(self, aspect: 'Feature.Aspect') -> None:
      """Populates the aspect from the features and lists in this list.

      Args:
        aspect: The aspect that will be populated by the features in this list.

      Adds features in this list as items to the aspects. Updates the distance
      dictionary. Adds self as supp to the aspect.

      """
      aspect.add_supp(self)
      for i, item in enumerate(self):
        item.parent_list = self
        if isinstance(item, Feature) and item not in aspect:
          aspect.add_feature(item)
        elif isinstance(item, Feature.ValueList):
          item.populate(aspect)
        for item2 in self._items[i+1:]:
          item.add_distance(item2, self.distance(item, item2))

    def set(self) -> 'Feature.Set':
      """Returns a set of features in this list."""
      return Feature.Set(self)

    def range(
        self, first: 'Feature.Aspect.VALUES', last: 'Feature.Aspect.VALUES'
    ) -> 'Feature.Set':
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
      if first.parent_list != self or last.parent_list != self:
        return Feature.Set()
      i1, i2 = self._items.index(first), self._items.index(last)
      start, stop = min(i1, i2), max(i1, i2)
      between = Feature.Set(self._items[start+1:stop])
      if i1 < i2: return between.union(first, last)
      return self.set().difference(between)

  class Aspect(inventory2.Inventory):
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

    def __init__(
        self,
        feature_list: 'Feature.ValueList'
    ):
      super().__init__()
      self.root_list = feature_list
      self.set_alias(feature_list.alias)
      self.text = feature_list.text
      self.inventory = ty.UNASSIGNED
      self.max_dist = 0
      self.distance_dict = {}

    def __str__(self):
      """String representation of distance dicts of features for this aspect."""
      text = '%s (%.2f):\n' % (self.text, self.max_dist)
      for feature in self:
        text += str(feature)
      return text

    def add_feature(self, feature: 'Feature') -> None:
      self.add_item(feature)
      feature.aspect = self
      feature.inventory = self.inventory
      self.distance_dict[feature] = {}

    def supp_feature(self, feature: 'Feature') -> None:
      self.add_supp(feature)
      feature.aspect = self
      feature.inventory = self.inventory

    def add_distance(
        self, feature1: 'Feature', feature2: 'Feature', distance: float
    ) -> None:
      if feature1 not in self: self.add_feature(feature1)
      if feature2 not in self: self.add_feature(feature2)
      self.distance_dict[feature1][feature2] = distance
      self.distance_dict[feature2][feature1] = distance
      if distance > self.max_dist: self.max_dist = distance

    def filter(self, *features) -> 'Feature.Set':
      return Feature.Set(*[
          feature for feature in Feature.Set(*features)
          if feature.aspect == self
      ])

    def _make_set(
        self, alias: str, *features, negation: bool = False
    ) -> 'Feature.Set':
      filtered = self.filter(*features)
      to_add = filtered if not negation else self.all.difference(filtered)
      return Feature.Set.with_alias(alias, to_add)

    def set(self, alias: str, *features) -> None:
      self.add_supp(self._make_set(alias, *features))

    def set_not(self, alias: str, *features) -> None:
      self.add_supp(self._make_set(alias, *features, negation=True))

    def set_range(
        self, alias: str,
        first: 'Feature.Aspect.VALUES', last: 'Feature.Aspect.VALUES'
    ) -> None:
      self.add_supp(
          self._make_set(alias, first.parent_list.range(first, last))
      )

    def populate(
        self,
        inventory: inventory2.Inventory
    ) -> None:
      """Populates the aspect from its root_list and adds it to inventory.

      Args:
        inventory: The Feature inventory this Aspect is defined in.

      The item values of the Aspect are the features in its root_list. Max_dist
      of an aspect is the max possible distance between two features of
      this aspect. Every aspect has two supp features: 'any' which returns 0
      distance to all features of this aspect, and n_a (not applicable),
      which returns max_dist to all features. The root_list and any value list
      within are added as supps to the aspect.

      """
      self.inventory = inventory
      self.inventory.add_item(self)
      self.root_list.populate(self)
      self.set('all', self)
      self.supp_feature(Feature('any'))
      self.supp_feature(Feature('n_a', 'not_applicable'))

  class Inventory(inventory2.Inventory):
    """An inventory of Aspects and their contrastive features.

    The structure of a feature inventory:

    Inventory:

    - Aspects: aspect.alias: aspect
        - Features: feature.alias: feature
        - ValueLists: list.alias: list
        - Sets: set.alias: set
    - Profiles: profile.alias: profile
        - Profile features: aspect.alias: set

    """

    def __init__(self, alias: str, *aspects: 'Feature.Aspect'):
      super().__init__(alias)
      for aspect in aspects:
        aspect.populate(self)

    def __str__(self):
      """String representation of all distance dicts in the inventory."""
      text = 'Inventory: %s\n' % self.text
      for a in self:
        text += str(a)
      return text

    def add_profile(
        self, alias: str,
        *params: 'Feature.ITERABLE',
    ) -> None:
      self.add_supp(Feature.Profile(self, alias, *params))

    def copy_and_update_profile(
        self, old: 'Feature.Profile', alias: str,
        *params: 'Feature.ITERABLE',
    ) -> None:
      self.add_supp(old.copy_and_update(alias, *params))

  class Profile(inventory2.Inventory):
    """"Feature profile for an object based on a feature inventory.

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
        self, feature_inventory: 'Feature.Inventory', alias: str,
        *params: 'Feature.ITERABLE'
    ):
      super().__init__(alias)
      self.inventory = feature_inventory
      self.max_dist = 0
      param_dict = Feature.Set.aspect_dict(*params)
      for aspect in self.inventory:
        value = param_dict.get(aspect, aspect.any)
        self.add_item(Feature.Set.with_alias(aspect.alias, value))
        self.max_dist += aspect.max_dist

    def __str__(self):
      text = 'Profile: {\n'
      for item in self:
        text += '    ' + str(item) + '\n'
      text += '}\n'
      return text

    def copy_and_update(
        self, alias: str,
        *updates: 'Feature.ITERABLE'
    ) -> 'Feature.Profile':
      """Copies the whole profile and applies the updates if provided..

      Args:
        alias: alias of the new profile.
        *updates: values to be replaced in the new profile.
      Returns:
        Profile.

      Example:
      room_features.add_profile(
          'white_office'
          room_features.function.office,
          room_features.color.white,
          room_features.ligthing.any,
          room_features.warmth.any,
          room_features.door.any,
      )

      white_office.copy_and_update(
          'wo_hot'
          room_features.warmth.hot
      )

      yields

      Profile(
          'wo_hot'
          room_features.function.office,
          room_features.color.white,
          room_features.ligthing.any,
          room_features.warmth.hot,
          room_features.door.any,
      )
      """
      new = Feature.Profile(self.inventory, alias, *self)
      update_dict = Feature.Set.aspect_dict(*updates)
      for aspect, value in update_dict.items():
        new.get(aspect.alias).update(value)
      return new

    def compare(
        self, p: 'Feature.Profile', aspects: 'Feature.ASPECTS' = ty.UNSPECIFIED,
    ) -> tuple[str, float]:
      """Compares this Profile to another Profile.

      Args:
        p: Profile to be compared.
        aspects: contrastive aspects to be included while calculating the
        distance and similarity.

      Returns:
        Similarity score

      """
      text = '%s - %s %s comparison:\n' % (
          self.alias, p.alias, self.inventory.alias
      )
      if p.inventory != self.inventory:
        return '    not comparable\n    Similarity = 0\n', 0
      if ty.is_nothing(aspects): aspects = self.inventory
      total_dist = 0
      max_dist = 0
      for aspect in aspects:
        item1 = self.get(aspect.alias)
        item2 = p.get(aspect.alias)
        dist = item1.distance(item2)
        total_dist += dist
        max_dist += aspect.max_dist
        text += '    %s vs %s = %.2f\n' % (
            str(item1), str(item2), dist
        )
      similarity = 1 - total_dist / max_dist
      text += '    Total distance = %.2f/%.2f\n' % (total_dist, max_dist)
      text += '    Similarity = %.3f\n' % similarity
      return text, similarity

    def comparison(
        self, p: 'Feature.Profile', aspects: 'Feature.ASPECTS' = ty.UNSPECIFIED,
    ) -> str:
      return self.compare(p, aspects)[0]

    def similarity(
        self, p: 'Feature.Profile', aspects: 'Feature.ASPECTS' = ty.UNSPECIFIED,
    ) -> float:
      return self.compare(p, aspects)[1]

  @classmethod
  def equidistant(
      cls, alias: Union[str, tuple[str, str]],
      *values: 'Feature.Aspect.VALUES', step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.EQUIDISTANT, step, *values)

  @classmethod
  def linear(
      cls, alias: Union[str, tuple[str, str]],
      *values: 'Feature.Aspect.VALUES', step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.LINEAR, step, *values)

  @classmethod
  def cyclic(
      cls, alias: Union[str, tuple[str, str]],
      *values: 'Feature.Aspect.VALUES', step: float = 1,
  ) -> ValueList:
    return cls.ValueList(alias, cls.ValueListType.CYCLIC, step, *values)

