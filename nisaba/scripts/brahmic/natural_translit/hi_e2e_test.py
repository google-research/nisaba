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

"""Tests for hi_e2e."""

from absl.testing import absltest
from nisaba.scripts.brahmic.natural_translit import hi_e2e
from nisaba.scripts.utils import test_util


_TEST_CASES = [
    (hi_e2e.iso_to_psaf, [
        # ('hiṁdī', 'hindii'),
        ('hindī', 'hindii'),
        # ('iṁḍiyā', 'indiyaa'),
        # ('caṁbā', 'chambaa'),
        # ('haḍḍiyōṁ', 'haddiyoon'),
        # ('ajñāna', 'agyaana'),
        # ('jhāṁkī', 'jhaankii'),
    ]),
    (hi_e2e.iso_to_psac, [
        # ('hiṁdī', 'hindi'),
        ('hindī', 'hindi'),
        # ('iṁḍiyā', 'indiya'),
        # ('ajñāna', 'agyana'),
        # ('jhāṁkī', 'jhanki'),
    ]),
    (hi_e2e.iso_to_ipa, [
        ('hiṁdī', 'hin̪d̪iː'),
        # ('hindī', 'hin̪d̪iː'),
        # ('iṁḍiyā', 'iɳɖijaː'),
        # ('ajñāna', 'aɡjaːn̪0'),
        # ('jʰāṁkī', 'd͡ʒʰaːŋkiː'),
    ]),
]


class HiE2ETest(test_util.FstTestCase):

  def test_all(self):
    self.assertFstStrIoTestCases(_TEST_CASES)


if __name__ == '__main__':
  absltest.main()
