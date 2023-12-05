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

"""Typ tr to Brahmic dict for the subset of ISO Chars used by deromanizers."""

from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.utils import log_op as log

iso = iso_inventory.TRANSLIT_INVENTORY
ISO = 'iso'
DEVA = 'deva'
TAML = 'taml'

_FAIL = '!'
_DICT = {
    log.text_of(iso.VIR): {
        DEVA: '्', TAML: '்',
    },
    log.text_of(iso.A): {
        DEVA: '', TAML: '',
    },
    log.text_of(iso.A_I): {
        DEVA: 'अ', TAML: 'அ',
    },
    log.text_of(iso.AA): {
        DEVA: 'ा', TAML: 'ா',
    },
    log.text_of(iso.AA_I): {
        DEVA: 'आ', TAML: 'ஆ',
    },
    log.text_of(iso.E): {
        DEVA: 'ॆ', TAML: 'ெ',
    },
    log.text_of(iso.E_I): {
        DEVA: 'ऎ', TAML: 'எ',
    },
    log.text_of(iso.EE): {
        DEVA: 'े', TAML: 'ே',
    },
    log.text_of(iso.EE_I): {
        DEVA: 'ए', TAML: 'ஏ',
    },
    log.text_of(iso.I): {
        DEVA: 'ि', TAML: 'ி',
    },
    log.text_of(iso.I_I): {
        DEVA: 'इ', TAML: 'இ',
    },
    log.text_of(iso.II): {
        DEVA: 'ी', TAML: 'ீ',
    },
    log.text_of(iso.II_I): {
        DEVA: 'ई', TAML: 'ஈ',
    },
    log.text_of(iso.O): {
        DEVA: 'ॊ', TAML: 'ொ',
    },
    log.text_of(iso.O_I): {
        DEVA: 'ऒ', TAML: 'ஒ',
    },
    log.text_of(iso.OO): {
        DEVA: 'ो', TAML: 'ோ',
    },
    log.text_of(iso.OO_I): {
        DEVA: 'ओ', TAML: 'ஓ',
    },
    log.text_of(iso.U): {
        DEVA: 'ु', TAML: 'ு',
    },
    log.text_of(iso.U_I): {
        DEVA: 'उ', TAML: 'உ',
    },
    log.text_of(iso.UU): {
        DEVA: 'ू', TAML: 'ூ',
    },
    log.text_of(iso.UU_I): {
        DEVA: 'ऊ', TAML: 'ஊ',
    },
    log.text_of(iso.AI): {
        DEVA: 'ै', TAML: 'ை',
    },
    log.text_of(iso.AI_I): {
        DEVA: 'ऐ', TAML: 'ஐ',
    },
    log.text_of(iso.AU): {
        DEVA: 'ौ', TAML: 'ௌ',
    },
    log.text_of(iso.AU_I): {
        DEVA: 'औ', TAML: 'ஔ',
    },
    log.text_of(iso.B): {
        DEVA: 'ब',
    },
    log.text_of(iso.BH): {
        DEVA: 'भ',
    },
    log.text_of(iso.C): {
        DEVA: 'च', TAML: 'ச',
    },
    log.text_of(iso.CH): {
        DEVA: 'छ',
    },
    log.text_of(iso.D): {
        DEVA: 'द',
    },
    log.text_of(iso.DH): {
        DEVA: 'ध',
    },
    log.text_of(iso.G): {
        DEVA: 'ग',
    },
    log.text_of(iso.GH): {
        DEVA: 'घ',
    },
    log.text_of(iso.H): {
        DEVA: 'ह', TAML: 'ஹ',
    },
    log.text_of(iso.J): {
        DEVA: 'ज', TAML: 'ஜ',
    },
    log.text_of(iso.Z): {
        DEVA: 'ज़', TAML: 'ஃஜ'
    },
    log.text_of(iso.JH): {
        DEVA: 'झ',
    },
    log.text_of(iso.K): {
        DEVA: 'क', TAML: 'க',
    },
    log.text_of(iso.KH): {
        DEVA: 'ख',
    },
    log.text_of(iso.L): {
        DEVA: 'ल', TAML: 'ல',
    },
    log.text_of(iso.LR): {
        TAML: 'ழ',
    },
    log.text_of(iso.M): {
        DEVA: 'म', TAML: 'ம',
    },
    log.text_of(iso.N): {
        DEVA: 'न', TAML: 'ந',
    },
    log.text_of(iso.NA): {
        TAML: 'ன',
    },
    log.text_of(iso.P): {
        DEVA: 'प', TAML: 'ப',
    },
    log.text_of(iso.PH): {
        DEVA: 'फ',
    },
    log.text_of(iso.F): {
        DEVA: 'फ़', TAML: 'ஃப',
    },
    log.text_of(iso.R): {
        DEVA: 'र', TAML: 'ர',
    },
    log.text_of(iso.RR): {
        TAML: 'ற',
    },
    log.text_of(iso.S): {
        DEVA: 'स', TAML: 'ஸ',
    },
    log.text_of(iso.SH): {
        DEVA: 'श', TAML: 'ஶ',
    },
    log.text_of(iso.T): {
        DEVA: 'त', TAML: 'த',
    },
    log.text_of(iso.TH): {
        DEVA: 'थ',
    },
    log.text_of(iso.V): {
        DEVA: 'व', TAML: 'வ',
    },
    log.text_of(iso.Y): {
        DEVA: 'य', TAML: 'ய',
    },
    log.text_of(iso.ANS): {
        DEVA: 'ं', TAML: '',
    },
}


def _br_of_tr(tr: str, script: str) -> str:
  tr_str = log.text_of(tr)
  if not tr_str or tr_str == 'Fst_<no_text>': return ''
  if script == ISO: return tr_str[1:-1]
  br_dict = _DICT.get(tr_str, {})
  if not br_dict: log.dbg_return('', 'No dict entry for %s' % tr_str)
  br = br_dict.get(script, _FAIL)
  if br == _FAIL: log.dbg_return('', 'No %s entry for %s' % (script, tr_str))
  return br


def cross(script: str) -> list[list[str]]:
  return [[tr, _br_of_tr(tr, script)] for tr in _DICT]
