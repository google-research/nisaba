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

"""Orthographic features."""

from nisaba.scripts.natural_translit.features import feature2
from nisaba.scripts.natural_translit.utils import list_op as ls


def _script() -> feature2.FeatureInventory:
  """Script inventory."""
  f = feature2.FeatureInventory('script')
  f.add_feature('test')
  ls.apply_foreach(f.make_group, [
      ['latin', ['basic']],
  ])
  return f

script = _script()


def _grapheme() -> feature2.FeatureInventory:
  """Grapheme feature inventory."""
  f = feature2.FeatureInventory('orthographic')
  ls.apply_foreach(f.make_group, [
      ['case', ['lower', 'upper']],
      ['texttype', ['raw', 'ctrl']],
      ['dependence', ['standalone', 'combining']],
  ])
  return f

grapheme = _grapheme()
