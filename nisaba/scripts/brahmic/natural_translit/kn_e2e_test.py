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

"""Tests for kn_e2e."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import kn_e2e
from nisaba.scripts.utils import test_util

_TEST_CASES = [
    (kn_e2e.iso_to_psaf, [
        ('hiṁdi', 'hindi'),
        ('iṁḍiyā', 'indiyaa'),
        ('keṁpu', 'kempu'),
        ('jñāna', 'gnyaana'),
    ]),
    (kn_e2e.iso_to_psac, [
        ('hiṁdi', 'hindi'),
        ('iṁḍiyā', 'indiya'),
        ('jñāna', 'gnyana'),
    ]),
    (kn_e2e.iso_to_ipa, [
        ('hiṁdi', 'hin̪d̪i'),
        ('iṁḍiyā', 'iɳɖijaː'),
        ('jñāna', 'ɡɲaːn̪a'),
        ('sīre', 'siːre')
    ]),
]


class KnE2ETest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
