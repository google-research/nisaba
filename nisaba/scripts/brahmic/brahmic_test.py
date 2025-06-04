# Copyright 2025 Nisaba Authors.
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

"""Tests for the main brahmic package."""

import warnings

from absl.testing import absltest
from nisaba.scripts import brahmic


class BrahmicTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self._nfc = brahmic.Nfc()
    self._iso = brahmic.ToIso()
    self._iso_to_deva = brahmic.IsoTo('Deva')
    self._visual_norm_deva = brahmic.VisualNorm('Deva')
    self._wellformed_deva = brahmic.WellFormed('Deva')
    self._wellformed_mlym = brahmic.WellFormed('Mlym')
    self._norm_acceptor_deva = brahmic.NormalizingAcceptor('Deva')
    self._norm_acceptor_sinh = brahmic.NormalizingAcceptor('Sinh')

  def testApplyOnText(self):
    self.assertEqual('क़्लब', self._nfc.ApplyOnText('क़्लब'))
    self.assertEqual('kˑlaba', self._iso.ApplyOnText('क़्लब'))
    self.assertEqual('क़्लब', self._iso_to_deva.ApplyOnText('kˑlaba'))
    self.assertEqual('क़्लब', self._visual_norm_deva.ApplyOnText('क़्लब'))

  def testAcceptText(self):
    self.assertTrue(self._wellformed_deva.AcceptText('लब'))
    self.assertFalse(self._wellformed_deva.AcceptText('काु'))
    self.assertFalse(self._wellformed_mlym.AcceptText('്ന'))

  def testAcceptTextWarning(self):
    # Raises a warning about underlying FST.
    with warnings.catch_warnings(record=True) as warns:
      self.assertTrue(self._visual_norm_deva.AcceptText('क़्लब'))

      # TODO: restrict to len == 1 check once  is submitted.
      self.assertNotEmpty(warns)
      warn = warns[0]
      self.assertTrue(issubclass(warn.category, RuntimeWarning))
      self.assertIn('not an acceptor', str(warn.message))

  def testNormalizingAcceptor_ApplyOnWord(self):
    self.assertEqual('ශ්‍රී', self._norm_acceptor_sinh.ApplyOnWord('ශ්‍රී'))
    self.assertEqual('ऐरावत', self._norm_acceptor_deva.ApplyOnWord('एेरावत'))
    with self.assertRaises(brahmic.IllFormedError):
      self._norm_acceptor_deva.ApplyOnWord('काु')  # Two adjacent vowel signs
    with self.assertRaises(brahmic.IllFormedError):
      self._norm_acceptor_deva.ApplyOnWord('ऐरावत ऐरावत')  # Embedded space

  def testNormalizingAcceptor_ApplyOnText(self):
    self.assertEqual('ऐरावत ऐरावत\n',
                     self._norm_acceptor_deva.ApplyOnText('एेरावत एेरावत\n'))
    with self.assertRaises(brahmic.IllFormedError):
      # Two adjacent vowel signs
      self._norm_acceptor_deva.ApplyOnText('एेरावत, एेरावत:\n काु')
      # Unacceptable ascii punctuations
      self._norm_acceptor_deva.ApplyOnText('एेरावत, एेरावत:\n')

  def testNormalizingAcceptor_ScriptError(self):
    with self.assertRaises(brahmic.ScriptError):
      brahmic.NormalizingAcceptor('Xyzz')  # Invalid script tag.

if __name__ == '__main__':
  absltest.main()
