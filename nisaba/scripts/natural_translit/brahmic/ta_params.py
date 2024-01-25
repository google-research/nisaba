# Copyright 2024 Nisaba Authors.
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

"""Grammar parameters for Ta."""

from nisaba.scripts.natural_translit.brahmic import derom_inventory as derom
from nisaba.scripts.natural_translit.brahmic import deromanizer

drm = derom.DEROMANIZATION_INVENTORY

deromanize = deromanizer.Deromanizer.params(
    script='taml',
    monophthong=(drm.a, drm.e, drm.i, drm.o, drm.u),
    diphthong=(drm.ai, drm.au, drm.ae_ee, drm.oa_oo),
    drops_aspirated=(
        drm.b_p, drm.ch, drm.d_t, drm.g_k, drm.j, drm.k, drm.p, drm.t
    ),
    no_aspirated=(
        drm.c, drm.h, drm.l, drm.m, drm.n, drm.q, drm.r, drm.s,
        drm.sh, drm.v, drm.w, drm.x, drm.y, drm.zh_lr
    ),
    only_geminated=(drm.tr_rr),
    foreign=(drm.f, drm.z),
)
