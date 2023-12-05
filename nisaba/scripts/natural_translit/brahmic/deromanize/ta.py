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

# Lint as: python3
"""Rule based deromanizer for ta_taml."""

import pynini as pyn
from pynini.export import multi_grm
from nisaba.scripts.natural_translit.brahmic.deromanize import fst_builder
from nisaba.scripts.natural_translit.brahmic.deromanize import ltn2brh

pan = ltn2brh.MAPPING_INVENTORY

ta = fst_builder.Deromanizer.params(
    script='taml',
    monophthong=(pan.a, pan.e, pan.i, pan.o, pan.u),
    diphthong=(pan.ai, pan.au, pan.ae_ee, pan.oa_oo),
    drop_aspirated=(
        pan.b_p, pan.ch, pan.d_t, pan.g_k, pan.j, pan.k, pan.p, pan.t
    ),
    no_aspirated=(
        pan.c, pan.h, pan.l, pan.m, pan.n, pan.q, pan.r, pan.s,
        pan.sh, pan.v, pan.w, pan.x, pan.y, pan.zh_lr
    ),
    gem_only=(pan.tr_rr),
    nukta=(pan.f, pan.z),
)


def generator_main(exporter_map: multi_grm.ExporterMapping):
  """Generates FAR for natural transliteration."""
  for token_type in ('byte', 'utf8'):
    with pyn.default_token_type(token_type):
      exporter = exporter_map[token_type]
      exporter['ISO'] = ta.ltn2iso
      exporter['TAML'] = ta.ltn2brh


if __name__ == '__main__':
  multi_grm.run(generator_main)
