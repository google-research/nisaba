# Copyright 2022 Nisaba Authors.
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

"""Rudimentary unit tests for the utility library."""

from absl.testing import absltest
from nisaba.scripts.brahmic import util as u
import nisaba.scripts.utils.file as uf


class UtilTest(absltest.TestCase):

  def testFileExistence(self):
    filename = 'dead_consonant.tsv'
    self.assertTrue(uf.IsFileExist(u.SCRIPT_DIR / 'Beng' / filename))
    self.assertFalse(uf.IsFileExist(u.SCRIPT_DIR / 'Taml' / filename))


if __name__ == '__main__':
  absltest.main()
