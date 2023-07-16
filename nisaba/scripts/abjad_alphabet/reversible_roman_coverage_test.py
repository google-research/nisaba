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

"""Tests for letter_languages and reversible_roman compatiblity."""

import pynini
from absl.testing import absltest
import nisaba.scripts.abjad_alphabet.util as u
from nisaba.scripts.utils import letter_languages
from nisaba.scripts.utils import rewrite as rw
from nisaba.scripts.utils import test_util as ut
from nisaba.scripts.utils import unicode_strings_util
import nisaba.scripts.utils.file as uf

_TOKEN_TYPE = 'byte'


class LetterLanguagesRomanizationTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self._letters_proto = letter_languages.read_textproto(
        u.LANG_DIR / 'letter_languages.textproto')
    self._roman_proto = unicode_strings_util.read_textproto(
        u.LANG_DIR / 'reversible_roman.textproto')

    far = uf.OpenFar(u.FAR_DIR, 'reversible_roman', _TOKEN_TYPE)
    self._from_arab = far['FROM_ARAB']
    self._to_arab = far['TO_ARAB']

  def test_chars_have_romanization_and_language(self):
    """Check if characters have romanization and are used in a language."""

    romanizable_chars = set(item.raw for item in self._roman_proto.item)
    language_chars = set(item.letter.raw for item in self._letters_proto.item)

    romanizable_but_orphan_chars = romanizable_chars - language_chars
    unromanizable_char = language_chars - romanizable_chars

    self.assertEmpty(unromanizable_char, 'These characters miss romanization.')
    self.assertEmpty(romanizable_but_orphan_chars,
                     'These characters are not used for any language.')

  def test_language_chars_for_reversibile_romanization(self):
    """Make sure each letter_language character is romanizable reliably."""
    with pynini.default_token_type(_TOKEN_TYPE):
      for item in self._letters_proto.item:
        arab_char = pynini.accep(item.letter.raw)
        roundtrip = rw.ComposeFsts([arab_char, self._from_arab, self._to_arab])
        ut.AssertIdentity(arab_char, roundtrip)


if __name__ == '__main__':
  absltest.main()
