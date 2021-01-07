# Copyright 2021 Nisaba Authors.
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


"""Tests for FAR API."""

import pathlib

from absl.testing import absltest
from nisaba.brahmic import far


class FarTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    brahmic_dir = pathlib.Path('com_google_nisaba/nisaba/brahmic/')
    self._fst = far.Far(brahmic_dir / 'iso.far').Fst('FROM_BRAHMIC')

  def testApplyOnText(self):
    self.assertEqual('kˑlaba', self._fst.ApplyOnText('क़्लब'))


if __name__ == '__main__':
  absltest.main()
