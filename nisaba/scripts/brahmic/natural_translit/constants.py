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

# Lint as: python3
"""Constants that make up phonemes, graphemes, and markers."""

import pynini as p
from pynini.lib import byte

SIGMA_STAR = byte.BYTE.star
LETTERS = p.union('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                  'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                  's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_')
SEP = p.accep(',')  # Separates symbols in a sequence
L_BOUND = p.accep('(')  # Left boundary of an assignment
R_BOUND = p.accep(')')  # Right boundary of an assignment
ASSIGN = p.accep('=')  # Grapheme to phoneme or graphemee to translit assignment
SEQUENCE = p.union(LETTERS.star, SEP.star).star  # A sequence of symbols
L_SIDE = L_BOUND + SEQUENCE + ASSIGN  # Left side of an assigment
