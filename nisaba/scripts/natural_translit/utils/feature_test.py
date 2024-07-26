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

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import feature
from nisaba.scripts.natural_translit.utils import test_op

f = feature.Feature


def _room_features() -> f.Inventory:
  room_features = f.Inventory(
      'room_features',
      f.Aspect(f.linear(
          'warmth',
          f('vcold', 'very_cold'), f('cold'), f('chl', 'chilly'),
          f('tpd', 'tepid'),
          f('warm'), f('hot'), f('vhot', 'very_hot'),
          step=0.5,
      )),
      f.Aspect(f.equidistant(
          'lighting',
          f('flr', 'fluorescent'),
          f('inc', 'incandescent'),
          f('led'),
      )),
      f.Aspect(f.equidistant(
          'function',
          f('bedroom'), f('living_room'), f('office'),
      )),
      f.Aspect(f.cyclic(
          'color',
          f('red'), f('org', 'orange'), f('ylw', 'yellow'),
          f('grn', 'green'), f('blue'), f('prp', 'purple'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'door',
          f('open'),
          f('ajar'),
          f.equidistant(
              'cls',
              f('closed'), f('shut'), step=0
          ),
          f('locked'),
          step=0.5,
      )),
  )
  room_features.warmth.set(
      'cold_end', room_features.warmth.cold, room_features.warmth.vcold
  )
  room_features.warmth.set(
      'hot_end', room_features.warmth.hot, room_features.warmth.vhot
  )
  room_features.warmth.set_range(
      'moderate', room_features.warmth.chl, room_features.warmth.warm
  )
  room_features.warmth.set_not(
      'not_cold', room_features.warmth.cold_end
  )
  room_features.color.set_range(
      'has_red', room_features.color.prp, room_features.color.org
  )
  room_features.make_sets(
      ('calming',
       [
           room_features.warmth.moderate,
           room_features.color.grn,
           room_features.color.blue,
           room_features.lighting.inc,
       ]
      )
  )
  room_features.add_profile(
      'room1',
      room_features.function.bedroom,
      room_features.warmth.cold,
      room_features.color.red,
      room_features.door.closed,
  )
  room_features.add_profile(
      'room2',
      room_features.function.living_room,
      room_features.lighting.flr,
      room_features.warmth.not_cold,
      room_features.color.n_a,
      room_features.door.shut,
  )
  room_features.copy_and_update_profile(
      room_features.room2, 'room3',
      room_features.warmth.cold,
  )
  return room_features

_R = _room_features()


def _animal_features() -> f.Inventory:
  animal_features = f.Inventory(
      'animal_features',
      f.Aspect(f.linear(
          'size',
          f('tiny'), f('small'), f('medium'), f('large'), f('huge'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'weight',
          f('light'), f('medium'), f('heavy'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'speed',
          f('slow'), f('medium'), f('fast'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'life_span',
          f('short'), f('medium'), f('long'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'gestation',
          f('short'), f('medium'), f('long'),
          step=0.5,
      )),
      f.Aspect(f.linear(
          'litter_size',
          f('small'), f('medium'), f('large'),
          step=0.5,
      )),
  )
  animal_features.add_profile(
      'cat',
      animal_features.size.small,
      animal_features.weight.light,
      animal_features.speed.fast,
      animal_features.life_span.medium,
      animal_features.gestation.medium,
      animal_features.litter_size.medium,
  )
  return animal_features

_A = _animal_features()


class FeatureTest(test_op.TestCase):

  def test_feature_text(self):
    self.assertEqual(_R.warmth.vcold.text, 'very_cold')

  def test_aspect_of_feature(self):
    self.assertEqual(_R.warmth.warm.aspect, _R.warmth)

  def test_list_as_suppl(self):
    self.assertIn('cls', _R.door.suppl_aliases)

  def test_set_empty(self):
    self.assertEmpty(f.Set())

  def test_set_alias_text(self):
    self.assertEqual(_R.warmth.all.alias, 'all')
    self.assertEqual(_R.warmth.all.text, 'all')

  def test_set_reset(self):
    self.assertEmpty(f.Set(_R.warmth.cold).reset())

  def test_set_all(self):
    self.assertIn(_R.warmth.warm, _R.warmth.all)

  def test_set_range(self):
    self.assertIn(_R.warmth.tpd, _R.warmth.moderate)

  def test_set_range_reverse(self):
    self.AssertStrEqual(
        _R.color.has_red, 'has_red: {orange, purple, red}'
    )

  def test_set_not(self):
    self.assertIn(_R.warmth.warm, _R.warmth.not_cold)

  def test_set_not_false(self):
    self.assertNotIn(_R.warmth.cold, _R.warmth.not_cold)

  def test_feature_in(self):
    self.assertTrue(_R.door.shut.is_in([_R.warmth.warm, _R.door.cls]))
    self.assertFalse(_R.door.shut.is_in([_R.warmth.cold, _R.door.closed]))
    self.assertTrue(_R.door.cls.is_in(_R.room2.door))
    self.assertFalse(_R.door.open.is_in(_R.room2.door))
    self.AssertFeatureIn(_R.door.cls, _R.room2)
    self.AssertFeatureNotIn(_R.door.open, _R.room2)

  def test_has_feature(self):
    self.AssertHasFeature([_R.warmth.warm, _R.door.cls], _R.door.shut)
    self.AssertNotHasFeature([_R.warmth.cold, _R.door.closed], _R.door.shut)
    self.assertTrue(_R.room2.door.has_feature(_R.door.shut))
    self.assertTrue(_R.room2.door.has_feature(_R.door.cls))
    self.AssertNotHasFeature(_R.room2.door, _R.door.open)
    self.assertTrue(_R.room2.has_feature(_R.door.shut))
    self.assertTrue(_R.room2.has_feature(_R.door.cls))
    self.AssertNotHasFeature(_R.room2, _R.door.open)

  def test_set_non_generic(self):
    non_generic = f.Set(
        _R.warmth.cold, _R.lighting.n_a, _R.color.any, alias='set1'
    ).non_generic(alias='non_generic')
    self.AssertStrEqual(non_generic, 'non_generic: {cold}')

  def test_max_dist(self):
    self.assertEqual(_R.warmth.max_dist, 3.00)

  def test_feature_dist_same_feature(self):
    self.AssertFeatureDistance(_R.warmth.warm, _R.warmth.warm, 0)

  def test_feature_dist_same_aspect(self):
    self.AssertFeatureDistance(_R.warmth.warm, _R.warmth.cold, 1.5)

  def test_feature_dist_different_aspect(self):
    self.AssertFeatureDistance(_R.warmth.warm, _R.color.red, f.ERROR_DISTANCE)

  def test_feature_dist_any(self):
    self.AssertFeatureDistance(_R.warmth.warm, _R.warmth.any, 0)

  def test_feature_dist_in_set(self):
    self.AssertFeatureDistance(_R.warmth.warm, _R.warmth.moderate, 0)

  def test_feature_dist_out_of_set(self):
    self.AssertFeatureDistance(_R.warmth.cold, _R.warmth.moderate, 0.5)

  def test_set_dist_in_set(self):
    self.AssertFeatureDistance(_R.warmth.moderate, _R.warmth.warm, 0)

  def test_set_dist_out_of_set(self):
    self.AssertFeatureDistance(_R.warmth.moderate, _R.warmth.vcold, 1)

  def test_set_to_set_overlap(self):
    self.AssertFeatureDistance(_R.warmth.moderate, _R.warmth.not_cold, 0)

  def test_set_to_set_no_overlap(self):
    self.AssertFeatureDistance(_R.warmth.hot_end, _R.warmth.cold_end, 2)

  def test_linear(self):
    self.AssertStrEqual(
        _R.warmth,
        'aspect: warmth, max_dist: 3.00\n\n'
        '| distances   |   very_cold |   cold |   chilly |   tepid |   warm |'
        '   hot |   very_hot |\n'
        '|-------------|-------------|--------|----------|---------|--------|'
        '-------|------------|\n'
        '| very_cold   |         0   |    0.5 |      1   |     1.5 |    2   |'
        '   2.5 |        3   |\n'
        '| cold        |         0.5 |    0   |      0.5 |     1   |    1.5 |'
        '   2   |        2.5 |\n'
        '| chilly      |         1   |    0.5 |      0   |     0.5 |    1   |'
        '   1.5 |        2   |\n'
        '| tepid       |         1.5 |    1   |      0.5 |     0   |    0.5 |'
        '   1   |        1.5 |\n'
        '| warm        |         2   |    1.5 |      1   |     0.5 |    0   |'
        '   0.5 |        1   |\n'
        '| hot         |         2.5 |    2   |      1.5 |     1   |    0.5 |'
        '   0   |        0.5 |\n'
        '| very_hot    |         3   |    2.5 |      2   |     1.5 |    1   |'
        '   0.5 |        0   |\n',
    )

  def test_equidistant_different(self):
    self.AssertStrEqual(
        _R.function,
        'aspect: function, max_dist: 1.00\n\n'
        '| distances   |   bedroom |   living_room |   office |\n'
        '|-------------|-----------|---------------|----------|\n'
        '| bedroom     |         0 |             1 |        1 |\n'
        '| living_room |         1 |             0 |        1 |\n'
        '| office      |         1 |             1 |        0 |\n',
    )

  def test_cyclic(self):
    self.AssertStrEqual(
        _R.color,
        'aspect: color, max_dist: 1.50\n\n'
        '| distances   |   red |   orange |   yellow |   green |   blue |'
        '   purple |\n'
        '|-------------|-------|----------|----------|---------|--------|'
        '----------|\n'
        '| red         |   0   |      0.5 |      1   |     1.5 |    1   |'
        '      0.5 |\n'
        '| orange      |   0.5 |      0   |      0.5 |     1   |    1.5 |'
        '      1   |\n'
        '| yellow      |   1   |      0.5 |      0   |     0.5 |    1   |'
        '      1.5 |\n'
        '| green       |   1.5 |      1   |      0.5 |     0   |    0.5 |'
        '      1   |\n'
        '| blue        |   1   |      1.5 |      1   |     0.5 |    0   |'
        '      0.5 |\n'
        '| purple      |   0.5 |      1   |      1.5 |     1   |    0.5 |'
        '      0   |\n',
    )

  def test_nested_linear_eq(self):
    self.AssertStrEqual(
        _R.door,
        'aspect: door, max_dist: 1.50\n\n'
        '| distances   |   open |   ajar |   closed |   shut |   locked |\n'
        '|-------------|--------|--------|----------|--------|----------|\n'
        '| open        |    0   |    0.5 |      1   |    1   |      1.5 |\n'
        '| ajar        |    0.5 |    0   |      0.5 |    0.5 |      1   |\n'
        '| closed      |    1   |    0.5 |      0   |    0   |      0.5 |\n'
        '| shut        |    1   |    0.5 |      0   |    0   |      0.5 |\n'
        '| locked      |    1.5 |    1   |      0.5 |    0.5 |      0   |\n',
    )

  def test_inventory_set(self):
    self.AssertStrEqual(
        _R.calming, 'calming: {blue, chilly, green, incandescent, tepid, warm}'
    )

  def test_profile_room1(self):
    self.AssertStrEqual(
        _R.room1,
        'Profile: {\n'
        '    warmth: {cold}\n'
        '    lighting: {any}\n'
        '    function: {bedroom}\n'
        '    color: {red}\n'
        '    door: {closed}\n'
        '}\n'
    )

  def test_profile_room2(self):
    self.AssertStrEqual(
        _R.room2,
        'Profile: {\n'
        '    warmth: {chilly, hot, tepid, very_hot, warm}\n'
        '    lighting: {fluorescent}\n'
        '    function: {living_room}\n'
        '    color: {not_applicable}\n'
        '    door: {shut}\n'
        '}\n'
    )

  def test_profile_room3(self):
    self.AssertStrEqual(
        _R.room3,
        'Profile: {\n'
        '    warmth: {cold}\n'
        '    lighting: {fluorescent}\n'
        '    function: {living_room}\n'
        '    color: {not_applicable}\n'
        '    door: {shut}\n'
        '}\n'
    )

  def test_profile_default_value_n_a(self):
    self.AssertStrEqual(
        f.Profile(
            _A,
            'ornamental',
            _A.size.any,
            _A.weight.any,
            unspecified_aspect_n_a=True,
        ),
        'Profile: {\n'
        '    size: {any}\n'
        '    weight: {any}\n'
        '    speed: {not_applicable}\n'
        '    life_span: {not_applicable}\n'
        '    gestation: {not_applicable}\n'
        '    litter_size: {not_applicable}\n'
        '}\n',
    )

  def test_profile_aspect_applicable(self):
    self.assertTrue(_R.color.is_applicable(_R.room1))
    self.assertFalse(_R.color.is_applicable(_R.room2))
    self.assertFalse(_R.color.is_applicable(_A.cat))

  def test_profile_get(self):
    self.AssertStrEqual(_R.room1.get(_R.warmth), 'warmth: {cold}')
    self.AssertStrEqual(
        _R.room1.get(_A.size), 'animal_features_size: {not_applicable}'
    )

  def test_profile_compare_all(self):
    self.assertEqual(
        _R.room1.comparison_table(_R.room2),
        'room_features comparison (max distance = 8.00):\n\n'
        '| aspect         | room1   | room2                              |'
        '   distance |\n'
        '|----------------|---------|------------------------------------|'
        '------------|\n'
        '| warmth         | cold    | chilly, hot, tepid, very_hot, warm |'
        '      0.5   |\n'
        '| function       | bedroom | living_room                        |'
        '      1     |\n'
        '| color          | red     | not_applicable                     |'
        '      1.5   |\n'
        '| Total distance |         |                                    |'
        '      3     |\n'
        '| Similarity     |         |                                    |'
        '      0.625 |\n',
    )

  def test_profile_compare_verbose(self):
    self.assertEqual(
        _R.room1.comparison_table(_R.room2, verbose=True),
        'room_features comparison (max distance = 8.00):\n\n'
        '| aspect         | room1   | room2                              |'
        '   distance |\n'
        '|----------------|---------|------------------------------------|'
        '------------|\n'
        '| warmth         | cold    | chilly, hot, tepid, very_hot, warm |'
        '      0.5   |\n'
        '| lighting       | any     | fluorescent                        |'
        '      0     |\n'
        '| function       | bedroom | living_room                        |'
        '      1     |\n'
        '| color          | red     | not_applicable                     |'
        '      1.5   |\n'
        '| door           | closed  | shut                               |'
        '      0     |\n'
        '| Total distance |         |                                    |'
        '      3     |\n'
        '| Similarity     |         |                                    |'
        '      0.625 |\n',
    )

  def test_profile_compare_aspect_list(self):
    self.assertEqual(
        _R.room1.comparison_table(_R.room2, [_R.function, _R.color]),
        'room_features comparison (max distance = 2.50):\n\n'
        '| aspect         | room1   | room2          |   distance |\n'
        '|----------------|---------|----------------|------------|\n'
        '| function       | bedroom | living_room    |        1   |\n'
        '| color          | red     | not_applicable |        1.5 |\n'
        '| Total distance |         |                |        2.5 |\n'
        '| Similarity     |         |                |        0   |\n',
    )

  def test_profile_compare_with_copy(self):
    self.assertEqual(
        _R.room2.comparison_table(_R.room3),
        'room_features comparison (max distance = 8.00):\n\n'
        '| aspect         | room2                              | room3   |'
        '   distance |\n'
        '|----------------|------------------------------------|---------|'
        '------------|\n'
        '| warmth         | chilly, hot, tepid, very_hot, warm | cold    |'
        '      0.5   |\n'
        '| Total distance |                                    |         |'
        '      0.5   |\n'
        '| Similarity     |                                    |         |'
        '      0.938 |\n',
    )

  def test_profile_compare_inventory_mismatch(self):
    self.assertEqual(
        _R.room1.comparison_table(_A.cat),
        'room_features and animal_features profiles are not comparable\n'
        '    Similarity = 0\n',
    )

if __name__ == '__main__':
  absltest.main()
