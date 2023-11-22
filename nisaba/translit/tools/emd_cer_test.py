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

"""Tests for nisaba.translit.tools.emd_cer."""

from nisaba.translit.tools import emd_cer
from absl.testing import absltest
import json

# Precision tolerance for floating-point value tests.
ERROR_TOLERANCE = 1.0e-6

class EmdTest(absltest.TestCase):

  def assertNear(self, expected, value):
    assert abs(expected - value) <= ERROR_TOLERANCE, (
        '%s not in range [%s, %s]' %
        (value, expected - ERROR_TOLERANCE, expected + ERROR_TOLERANCE))

  # Given reference strings sieberling (p=0.7) and zeeberlin (p=0.3), and
  # system output (hypothesis) strings seeverling (p=0.6) and siefelin (p=0.4),
  # this should arrive at a flow that yields 2.7 edits and reference length 9.7.
  # This is based on the following Levenshtein distances:
  # D(seeverling, sieberling) = 2 (subst i/e and b/v).
  # D(siefelin, sieberling) = 3 (subst b/f, insert r, delete g).
  # D(seeverling, zeeberlin) = 3 (subst z/s and b/v, insert g).
  # D(siefelin, zeeberlin) = 4 (subst z/s, e/i, b/f, delete r).
  # As the lowest number of edits, the 0.6 prob of the 'seeverling' hyp should
  # flow to the 'sieberling' reference, leaving just 0.1 left of that reference
  # for the 'siefelin' hyp, with distance 3.  The remaining 0.3 of 'siefelin'
  # flows to the 'zeeberlin' reference.  This yields the following edits:
  # Edits = 0.6 * 2 + 0.1 * 3 + 0.3 * 4 = 2.7.  Since 'sieberling' is length 10
  # and 'zeeberlin' length 9, we get the following reference length:
  # RefLen = 0.7 * 10 + 0.3 * 9 = 9.7.
  def testCalcEditsRefLen1(self):
    hyp_str = "{\"hyp\": {\"seeverling\": 0.6, \"siefelin\": 0.4}, "
    ref_str = "\"ref\": {\"sieberling\": 0.7, \"zeeberlin\": 0.3}, "
    p1p2_str = "\"p1\": [0.6, 0.4, 0, 0],\"p2\": [0, 0, 0.7, 0.3], "
    d_str = "\"D\": [[0, 0, 2, 3], [0, 0, 3, 4], [2, 3, 0, 0], [3, 4, 0, 0]], "
    l_str = "\"L\": [0, 0, 10, 9]}"
    json_str = hyp_str + ref_str + p1p2_str + d_str + l_str
    [Edits, RefLen] = emd_cer.emd_error_and_length(json.loads(json_str))
    self.assertNear(Edits, 2.7)
    self.assertNear(RefLen, 9.7)

  # Given reference strings UFOshipt (p=0.6) and youeffOshp (p=0.3), and
  # system output (hypothesis) strings UFOship (p=0.4), youFOsheep (p=0.3),
  # UFOsheep (p=0.2) and youeffohship (p=0.1), this should arrive at a flow
  # that yields 2.8 edits and reference length 8.8, based on these distances:
  # D(UFOship, UFOshipt) = 1 (delete t)
  # D(youFOsheep, UFOshipt) = 6 (you/U and eep/ipt)
  # D(UFOsheep, UFOshipt) = 3 (eep/ipt)
  # D(youeffohship, UFOshipt) = 9 (everything but ship)
  # D(UFOship, youeffOshp) = 7 (UF/youeff and insert i)
  # D(youFOsheep, youeffOshp) = 5 (F/eff and insert ee)
  # D(UFOsheep, youeffOshp) = 8 (UF/youeff and insert ee)
  # D(youeffohship, youeffOshp) = 3 (oh/O and insert i)
  # The best solution is sending all 0.4 of the 'UFOship' hyp to the 'UFOshipt'
  # reference (distance 1), leaving 0.2 prob for that reference, just enough
  # for the 'UFOsheep' hyp (distance 3).  The other hypotheses must thus flow
  # entirely to the 'youeffOshp' reference (distances 5 and 3). This yields:
  # Edits = 0.4 * 1 + 0.2 * 3 + 0.3 * 5 + 0.1 * 3 = 2.8.
  # Since 'UFOshipt' is length 8 and 'youeffOshp' is length 10, we get:
  # RefLen = 0.6 * 8 + 0.4 * 10 = 8.8.
  def testCalcEditsRefLen1(self):
    hyp_str1 = "{\"hyp\": {\"UFOship\": 0.4, \"youFOsheep\": 0.3, "
    hyp_str2 = "\"UFOsheep\": 0.2, \"youeffohship\": 0.1}, "
    hyp_str = hyp_str1 + hyp_str2
    ref_str = "\"ref\": {\"UFOshipt\": 0.6, \"youeffOshp\": 0.4}, "
    p1_str = "\"p1\": [0.4, 0.3, 0.2, 0.1, 0, 0], "
    p2_str = "\"p2\": [0, 0, 0, 0, 0.6, 0.4], "
    p1p2_str = p1_str + p2_str
    d_str1 = "\"D\": [[0, 0, 0, 0, 1, 7], [0, 0, 0, 0, 6, 5], "
    d_str2 = "[0, 0, 0, 0, 3, 8], [0, 0, 0, 0, 9, 3], "
    d_str3 = "[1, 6, 3, 9, 0, 0], [7, 5, 8, 3, 0, 0]], "
    d_str = d_str1 + d_str2 + d_str3
    l_str = "\"L\": [0, 0, 0, 0, 8, 10]}"
    json_str = hyp_str + ref_str + p1p2_str + d_str + l_str
    [Edits, RefLen] = emd_cer.emd_error_and_length(json.loads(json_str))
    self.assertNear(Edits, 2.8)
    self.assertNear(RefLen, 8.8)


if __name__ == '__main__':
  absltest.main()
