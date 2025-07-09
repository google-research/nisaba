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

"""Calculates earth mover's distance from json line."""

import numpy as np
import pyemd

# Returns the edits, flow, and length from EMD.
def earth_movers_distance(jline):
  p1 = np.array(jline['p1'], dtype=np.float64)
  p2 = np.array(jline['p2'], dtype=np.float64)
  D = np.array(jline['D'], dtype=np.float64)
  L = np.array(jline['L'], dtype=np.float64)
  R = pyemd.emd_with_flow(p1, p2, D)
  return [R[0], R[1], L]

# Returns the edits and reference length from EMD.
def emd_error_and_length(jline):
  [Edits, Flows, Len] = earth_movers_distance(jline)
  RefLen = 0
  for flow in Flows:
    RefLen += np.dot(flow, Len)
  return [Edits, RefLen]
