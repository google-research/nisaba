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

"""Tests for abjad / alphabet package API."""

from absl.testing import absltest
import nisaba.scripts.abjad_alphabet as api


class ApiTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self._nfc = api.Nfc()
    self._to_roman = api.ToReversibleRoman()
    self._from_roman = api.FromReversibleRoman()
    self._visual_norm = api.VisualNorm()
    self._normalizer = api.Normalizer()

  def testApplyOnText(self):
    self.assertEqual('آپ', self._nfc.ApplyOnText('آپ'))
    self.assertEqual('ʼ͟āb', self._to_roman.ApplyOnText('آب'))
    self.assertEqual('آب', self._from_roman.ApplyOnText('ʼ͟āb'))
    self.assertEqual('آپ', self._visual_norm.ApplyOnText('آ​پ'))

  def testNormalizingAcceptor_ApplyOnWord(self):
    self.assertEqual('آپآپ', self._normalizer.ApplyOnWord('آ​پآپ'))

  def testNormalizingAcceptor_ApplyOnText(self):
    self.assertEqual('آپ آپ\n', self._normalizer.ApplyOnText('آ​پ آپ\n'))

  def testNormalizer_TagError(self):
    with self.assertRaises(api.TagError):
      api.Normalizer('zz')  # Invalid tag.

if __name__ == '__main__':
  absltest.main()
