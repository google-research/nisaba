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

"""Starlark constants for Brahmic targets."""

# Script and language codes are used as per IANA registry:
# https://www.iana.org/assignments/language-subtag-registry
SCRIPTS = [
    "Beng",
    "Bugi",
    "Deva",
    "Gujr",
    "Guru",
    "Knda",
    "Lepc",
    "Limb",
    "Mlym",
    "Mtei",
    "Newa",
    "Orya",
    "Sinh",
    "Sylo",
    "Takr",
    "Taml",
    "Telu",
    "Tglg",
    "Thaa",
    "Tirh",
]

VISUAL_NORM_LANGS = [
    ("Beng", "as"),
    ("Beng", "bn"),
]

READING_NORM_LANGS = [
    ("Deva", "hi"),
    # Following entries are not language-specific
    ("Beng", ""),
    ("Lepc", ""),
    ("Mlym", ""),
]

FIXED_RULE_SCRIPTS = ["Mlym"]

NATURAL_TRANSLIT_LANGS = [
    "hi",
    "kn",
    "ml",
    "te",
]
