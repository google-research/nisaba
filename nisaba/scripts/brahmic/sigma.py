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


r"""Acyclic acceptor accepting characters from Brahmic scripts."""

import pynini
from pynini.export import grm
import nisaba.scripts.brahmic.char_util as cu
import nisaba.scripts.brahmic.util as u
import nisaba.scripts.utils.char as uc


def generator_main(exporter: grm.Exporter):
  """Generate FSAs accepting the alphabet of each Brahmic script."""

  # NOTE: It isn't useful for us to create a byte-mode sigma, so only export
  # utf8-mode sigma.
  with pynini.default_token_type('utf8'):
    for script in u.SCRIPTS:
      chars = cu.script_chars(script)
      exporter[script.upper()] = uc.derive_sigma(chars)


if __name__ == '__main__':
  grm.run(generator_main)
