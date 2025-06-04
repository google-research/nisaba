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

"""Simple integrity test for the letter language registry."""

import contextlib

from absl import flags
import pycountry

from absl.testing import absltest
from nisaba.scripts.utils import letter_languages

_INPUT = flags.DEFINE_string(
    'input_text_proto',
    None,
    'Input text proto file in `nisaba.LetterLanguages` format.',
    required=True,
)


class LetterLanguagesIntegrityTest(absltest.TestCase):

  @contextlib.contextmanager
  def assertNotRaises(self, ex):
    try:
      yield None
    except ex:
      raise self.failureException('{} raised'.format(ex.__name__)) from ex

  def setUp(self):
    super().setUp()
    self._letters_proto = letter_languages.read_textproto(_INPUT.value)

  def test_letters(self):
    """Make sure the unicode letter names map to raw characters correctly."""
    all_letters = set()
    self.assertTrue(self._letters_proto.item)
    for i, item in enumerate(self._letters_proto.item):
      # Letter message should not be empty.
      self.assertTrue(item.letter)
      self.assertTrue(item.letter.uname)
      self.assertLen(item.letter.uname, 1)
      self.assertTrue(item.letter.raw)

      # Check that there are no duplicates and the letters are in the
      # Unicode codepoint order.
      u_char = item.letter.raw
      self.assertNotIn(item.letter.raw, all_letters,
                       f'Letter {i}: Duplicate letter `{u_char}` found')
      all_letters.add(u_char)
      if i:
        this_codepoint = ord(u_char)
        prev_codepoint = ord(self._letters_proto.item[i - 1].letter.raw)
        self.assertLess(prev_codepoint, this_codepoint,
                        f'Letter {i}: Should be in Unicode codepoint order. '
                        f'This codepoint: {this_codepoint}, '
                        f'previous: {prev_codepoint}')
    self.assertEqual(len(self._letters_proto.item), len(all_letters))

  def test_languages(self):
    """Sanity checks for language codes."""
    for i, item in enumerate(self._letters_proto.item):
      for code in item.language:
        # The language code should be in ISO 639 format and consists of
        # two letters for ISO 639-1 languages and three letters otherwise.
        self.assertTrue(code, f'Empty language code in item {item}.')
        self.assertGreater(4, len(code),
                           f'`{code}` is too long a language code.')
        self.assertTrue(code.islower(), f'Language code `{code}` should be '
                        'lower-case.')
        if len(code) == 3:
          lang = pycountry.languages.get(alpha_3=code)
          self.assertTrue(lang, f'Failed to find language for code {code}')
          if hasattr(lang, 'alpha_2'):
            self.fail(f'Letter {i}: Please use two-letter code `{lang.alpha_2}`'
                      f' instead of `{lang.alpha_3}` for {lang.name} ({code})')
        else:
          lang = pycountry.languages.get(alpha_2=code)
          self.assertTrue(lang, f'Failed to find language for code {code}')

  def test_regions(self):
    """Sanity checks for region codes."""
    for i, item in enumerate(self._letters_proto.item):
      for code in item.region:
        # Region codes should be alpha-2 (where possible) or alpha-3 codes as
        # defined by ISO 3166 standard.
        self.assertLess(1, len(code))
        self.assertGreater(4, len(code))
        self.assertTrue(code.isupper(), f'Letter {i}: Region code `{code}` '
                        'should be upper-case')
        if len(code) == 3:
          country = pycountry.countries.get(alpha_3=code)
          self.assertTrue(country, f'Failed to find country for code `{code}`')
          if hasattr(country, 'alpha_2'):
            self.fail(f'Letter {i}: Please use two-letter code '
                      f'`{country.alpha_2}` instead of `{country.alpha_3}` '
                      f'for {country.name}')
        else:
          country = pycountry.countries.get(alpha_2=code)
          self.assertTrue(country, f'Failed to find country for code {code}')


if __name__ == '__main__':
  absltest.main()
