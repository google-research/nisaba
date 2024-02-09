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

f = feature.Feature


def _test_inventory() -> f.Inventory:
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

r = _test_inventory()


class FeatureTest(absltest.TestCase):

  def test_feature_text(self):
    self.assertEqual(r.warmth.vcold.text, 'very_cold')

  def test_aspect_of_feature(self):
    self.assertEqual(r.warmth.warm.aspect, r.warmth)

  def test_list_as_supp(self):
    self.assertIn('cls', r.door.supp_aliases)

  def test_set_empty(self):
    self.assertEmpty(f.Set())

  def test_set_reset(self):
    self.assertEmpty(f.Set(r.warmth.cold).reset())

  def test_set_all(self):
    self.assertIn(r.warmth.warm, r.warmth.all)

  def test_set_range(self):
    self.assertIn(r.warmth.tpd, r.warmth.moderate)

  def test_set_range_reverse(self):
    self.assertEqual(
        str(r.color.has_red), 'has_red: {orange, purple, red}'
    )

  def test_set_not(self):
    self.assertIn(r.warmth.warm, r.warmth.not_cold)

  def test_set_not_false(self):
    self.assertNotIn(r.warmth.cold, r.warmth.not_cold)

  def test_max_dist(self):
    self.assertEqual(r.warmth.max_dist, 3.00)

  def test_feature_dist_same_feature(self):
    self.assertEqual(r.warmth.warm.distance(r.warmth.warm), 0)

  def test_feature_dist_same_aspect(self):
    self.assertEqual(r.warmth.warm.distance(r.warmth.cold), 1.5)

  def test_feature_dist_different_aspect(self):
    self.assertEqual(r.warmth.warm.distance(r.color.red), f.ERROR_DISTANCE)

  def test_feature_dist_any(self):
    self.assertEqual(r.warmth.warm.distance(r.warmth.any), 0)

  def test_feature_dist_in_set(self):
    self.assertEqual(r.warmth.warm.distance(r.warmth.moderate), 0)

  def test_feature_dist_out_of_set(self):
    self.assertEqual(r.warmth.cold.distance(r.warmth.moderate), 0.5)

  def test_set_dist_in_set(self):
    self.assertEqual(r.warmth.moderate.distance(r.warmth.warm), 0)

  def test_set_dist_out_of_set(self):
    self.assertEqual(r.warmth.moderate.distance(r.warmth.vcold), 1)

  def test_set_to_set_overlap(self):
    self.assertEqual(r.warmth.moderate.distance(r.warmth.not_cold), 0)

  def test_set_to_set_no_overlap(self):
    self.assertEqual(r.warmth.hot_end.distance(r.warmth.cold_end), 2)

  def test_linear(self):
    self.assertEqual(
        str(r.warmth),
        'warmth (3.00):\n'
        '  vcold (very_cold) = {\n'
        '        cold (cold): 0.50\n'
        '        chl (chilly): 1.00\n'
        '        tpd (tepid): 1.50\n'
        '        warm (warm): 2.00\n'
        '        hot (hot): 2.50\n'
        '        vhot (very_hot): 3.00\n'
        '  }\n'
        '  cold (cold) = {\n'
        '        vcold (very_cold): 0.50\n'
        '        chl (chilly): 0.50\n'
        '        tpd (tepid): 1.00\n'
        '        warm (warm): 1.50\n'
        '        hot (hot): 2.00\n'
        '        vhot (very_hot): 2.50\n'
        '  }\n'
        '  chl (chilly) = {\n'
        '        vcold (very_cold): 1.00\n'
        '        cold (cold): 0.50\n'
        '        tpd (tepid): 0.50\n'
        '        warm (warm): 1.00\n'
        '        hot (hot): 1.50\n'
        '        vhot (very_hot): 2.00\n'
        '  }\n'
        '  tpd (tepid) = {\n'
        '        vcold (very_cold): 1.50\n'
        '        cold (cold): 1.00\n'
        '        chl (chilly): 0.50\n'
        '        warm (warm): 0.50\n'
        '        hot (hot): 1.00\n'
        '        vhot (very_hot): 1.50\n'
        '  }\n'
        '  warm (warm) = {\n'
        '        vcold (very_cold): 2.00\n'
        '        cold (cold): 1.50\n'
        '        chl (chilly): 1.00\n'
        '        tpd (tepid): 0.50\n'
        '        hot (hot): 0.50\n'
        '        vhot (very_hot): 1.00\n'
        '  }\n'
        '  hot (hot) = {\n'
        '        vcold (very_cold): 2.50\n'
        '        cold (cold): 2.00\n'
        '        chl (chilly): 1.50\n'
        '        tpd (tepid): 1.00\n'
        '        warm (warm): 0.50\n'
        '        vhot (very_hot): 0.50\n'
        '  }\n'
        '  vhot (very_hot) = {\n'
        '        vcold (very_cold): 3.00\n'
        '        cold (cold): 2.50\n'
        '        chl (chilly): 2.00\n'
        '        tpd (tepid): 1.50\n'
        '        warm (warm): 1.00\n'
        '        hot (hot): 0.50\n'
        '  }\n'
    )

  def test_equidistant_different(self):
    self.assertEqual(
        str(r.function),
        'function (1.00):\n'
        '  bedroom (bedroom) = {\n'
        '        living_room (living_room): 1.00\n'
        '        office (office): 1.00\n'
        '  }\n'
        '  living_room (living_room) = {\n'
        '        bedroom (bedroom): 1.00\n'
        '        office (office): 1.00\n'
        '  }\n'
        '  office (office) = {\n'
        '        bedroom (bedroom): 1.00\n'
        '        living_room (living_room): 1.00\n'
        '  }\n'
    )

  def test_cyclic(self):
    self.assertEqual(
        str(r.color),
        'color (1.50):\n'
        '  red (red) = {\n'
        '        org (orange): 0.50\n'
        '        ylw (yellow): 1.00\n'
        '        grn (green): 1.50\n'
        '        blue (blue): 1.00\n'
        '        prp (purple): 0.50\n'
        '  }\n'
        '  org (orange) = {\n'
        '        red (red): 0.50\n'
        '        ylw (yellow): 0.50\n'
        '        grn (green): 1.00\n'
        '        blue (blue): 1.50\n'
        '        prp (purple): 1.00\n'
        '  }\n'
        '  ylw (yellow) = {\n'
        '        red (red): 1.00\n'
        '        org (orange): 0.50\n'
        '        grn (green): 0.50\n'
        '        blue (blue): 1.00\n'
        '        prp (purple): 1.50\n'
        '  }\n'
        '  grn (green) = {\n'
        '        red (red): 1.50\n'
        '        org (orange): 1.00\n'
        '        ylw (yellow): 0.50\n'
        '        blue (blue): 0.50\n'
        '        prp (purple): 1.00\n'
        '  }\n'
        '  blue (blue) = {\n'
        '        red (red): 1.00\n'
        '        org (orange): 1.50\n'
        '        ylw (yellow): 1.00\n'
        '        grn (green): 0.50\n'
        '        prp (purple): 0.50\n'
        '  }\n'
        '  prp (purple) = {\n'
        '        red (red): 0.50\n'
        '        org (orange): 1.00\n'
        '        ylw (yellow): 1.50\n'
        '        grn (green): 1.00\n'
        '        blue (blue): 0.50\n'
        '  }\n'
    )

  def test_nested_linear_eq(self):
    self.assertEqual(
        str(r.door),
        'door (1.50):\n'
        '  open (open) = {\n'
        '        ajar (ajar): 0.50\n'
        '        closed (closed): 1.00\n'
        '        shut (shut): 1.00\n'
        '        locked (locked): 1.50\n'
        '  }\n'
        '  ajar (ajar) = {\n'
        '        open (open): 0.50\n'
        '        closed (closed): 0.50\n'
        '        shut (shut): 0.50\n'
        '        locked (locked): 1.00\n'
        '  }\n'
        '  closed (closed) = {\n'
        '        open (open): 1.00\n'
        '        ajar (ajar): 0.50\n'
        '        shut (shut): 0.00\n'
        '        locked (locked): 0.50\n'
        '  }\n'
        '  shut (shut) = {\n'
        '        open (open): 1.00\n'
        '        ajar (ajar): 0.50\n'
        '        closed (closed): 0.00\n'
        '        locked (locked): 0.50\n'
        '  }\n'
        '  locked (locked) = {\n'
        '        open (open): 1.50\n'
        '        ajar (ajar): 1.00\n'
        '        closed (closed): 0.50\n'
        '        shut (shut): 0.50\n'
        '  }\n'
    )

  def test_profile_room1(self):
    self.assertEqual(
        str(r.room1),
        'Profile: {\n'
        '    warmth: {cold}\n'
        '    lighting: {any}\n'
        '    function: {bedroom}\n'
        '    color: {red}\n'
        '    door: {closed}\n'
        '}\n'
    )

  def test_profile_room2(self):
    self.assertEqual(
        str(r.room2),
        'Profile: {\n'
        '    warmth: {chilly, hot, tepid, very_hot, warm}\n'
        '    lighting: {fluorescent}\n'
        '    function: {living_room}\n'
        '    color: {not_applicable}\n'
        '    door: {shut}\n'
        '}\n'
    )

  def test_profile_room3(self):
    self.assertEqual(
        str(r.room3),
        'Profile: {\n'
        '    warmth: {cold}\n'
        '    lighting: {fluorescent}\n'
        '    function: {living_room}\n'
        '    color: {not_applicable}\n'
        '    door: {shut}\n'
        '}\n'
    )

  def test_profile_compare_all(self):
    self.assertEqual(
        r.room1.comparison(r.room2),
        'room1 - room2 room_features comparison:\n'
        '    warmth: {cold} vs warmth: {chilly, hot, tepid, very_hot, warm} '
        '= 0.50\n'
        '    lighting: {any} vs lighting: {fluorescent} = 0.00\n'
        '    function: {bedroom} vs function: {living_room} = 1.00\n'
        '    color: {red} vs color: {not_applicable} = 1.50\n'
        '    door: {closed} vs door: {shut} = 0.00\n'
        '    Total distance = 3.00/8.00\n'
        '    Similarity = 0.625\n'
    )

  def test_profile_compare_aspect_list(self):
    self.assertEqual(
        r.room1.comparison(r.room2, [r.function, r.color]),
        'room1 - room2 room_features comparison:\n'
        '    function: {bedroom} vs function: {living_room} = 1.00\n'
        '    color: {red} vs color: {not_applicable} = 1.50\n'
        '    Total distance = 2.50/2.50\n'
        '    Similarity = 0.000\n'
    )

  def test_profile_compare_with_copy(self):
    self.assertEqual(
        r.room2.comparison(r.room3),
        'room2 - room3 room_features comparison:\n'
        '    warmth: {chilly, hot, tepid, very_hot, warm}'
        ' vs warmth: {cold} = 0.50\n'
        '    lighting: {fluorescent} vs lighting: {fluorescent} = 0.00\n'
        '    function: {living_room} vs function: {living_room} = 0.00\n'
        '    color: {not_applicable} vs color: {not_applicable} = 0.00\n'
        '    door: {shut} vs door: {shut} = 0.00\n'
        '    Total distance = 0.50/8.00\n'
        '    Similarity = 0.938\n'
    )

if __name__ == '__main__':
  absltest.main()
