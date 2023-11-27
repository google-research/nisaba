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

"""Simple placeholder for the phonological feature structure."""

from nisaba.scripts.natural_translit.features import feature2
from nisaba.scripts.natural_translit.utils import list_op as ls


def _qualifier() -> feature2.FeatureInventory:
  """Qualifiers."""
  f = feature2.FeatureInventory('qualifier')
  ls.apply_foreach(f.make_group, [
      ['degree', ['top', 'high', 'middle', 'low', 'bottom']],
      ['change', ['rising', 'falling', 'interrupt']],
  ])
  return f

qualifier = _qualifier()
