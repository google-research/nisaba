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

"""Latin to ISO fallback grammar."""

import pynini as pyn
from nisaba.scripts.natural_translit.brahmic import iso_inventory
from nisaba.scripts.natural_translit.latin import ltn_inventory
from nisaba.scripts.natural_translit.script import char as c
from nisaba.scripts.natural_translit.utils import rewrite_functions as rw

ltn = ltn_inventory.GRAPHEME_INVENTORY
iso = iso_inventory.TRANSLIT_INVENTORY

LTN_GR = c.read_glyph(ltn_inventory.ASCII_LC)
ISO_TR = c.print_glyph(iso_inventory.CHAR)

LONG_VOWEL = rw.rewrite_ls([
    [ltn.A + ltn.A, iso.AA],
    [ltn.E + ltn.E, iso.EE],
    [ltn.I + ltn.I, iso.II],
    [ltn.O + ltn.O, iso.OO],
    [ltn.U + ltn.U, iso.UU],
    [ltn.A + ltn.I, iso.AI],
    [ltn.A + ltn.U, iso.AU],
])

HI_VOWEL = rw.rewrite_ls([
    [ltn.E, iso.EE],
    [ltn.O, iso.OO],
])

SHORT_VOWEL = rw.rewrite_ls([
    [ltn.A, iso.A],
    [ltn.E, iso.E],
    [ltn.I, iso.I],
    [ltn.O, iso.O],
    [ltn.U, iso.U],
])


BASE_TWO = rw.rewrite_ls([
    [ltn.C + ltn.H, iso.C],
    [ltn.S + ltn.H, iso.SH],
])

BASE_ONE = rw.rewrite_ls([
    [ltn.B, iso.B],
    [ltn.C, iso.K],
    [ltn.D, iso.D],
    [ltn.F, iso.P + iso.H],
    [ltn.G, iso.G],
    [ltn.H, iso.H],
    [ltn.J, iso.J],
    [ltn.K, iso.K],
    [ltn.L, iso.L],
    [ltn.M, iso.M],
    [ltn.N, iso.N],
    [ltn.Q, iso.K],
    [ltn.P, iso.P],
    [ltn.R, iso.R],
    [ltn.S, iso.S],
    [ltn.T, iso.T],
    [ltn.V, iso.V],
    [ltn.W, iso.V],
    [ltn.X, iso.K + iso.S],
    [ltn.Y, iso.Y],
    [ltn.Z, iso.J],
])

ASPIRATION = rw.rewrite_ls([
    [ltn.B + ltn.H, iso.BH],
    [ltn.C + ltn.H + ltn.H, iso.CH],
    [ltn.D + ltn.H, iso.DH],
    [ltn.G + ltn.H, iso.GH],
    [ltn.J + ltn.H, iso.JH],
    [ltn.K + ltn.H, iso.KH],
    [ltn.P + ltn.H, iso.PH],
    [ltn.T + ltn.H, iso.TH],
])

NUKTA = rw.rewrite_ls([
    [ltn.F, iso.F],
    [ltn.Z, iso.Z],
])

VIS = rw.rewrite_ls([
    [ltn.F, iso.VIS + iso.P],
])

SCHWA_INSERTION = rw.insert(
    iso.A, iso.SCH_CONS, pyn.union(iso.SCH_CONS, rw.al.EOW)
)
