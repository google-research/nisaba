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

"""Simple integrity test for the letter language registry."""

import contextlib
import logging
import os
import unicodedata

from absl import flags
import pycountry

from google.protobuf import text_format
from absl.testing import absltest
from nisaba.scripts.utils import letter_languages_pb2

flags.DEFINE_string(
    'input_text_proto', None,
    'Input text proto file in `nisaba.LetterLanguages` format.')

flags.mark_flag_as_required('input_text_proto')

FLAGS = flags.FLAGS


class LetterLanguagesIntegrityTest(absltest.TestCase):

  @contextlib.contextmanager
  def assertNotRaises(self, exc_type):
    try:
      yield None
    except exc_type:
      raise self.failureException('{} raised'.format(exc_type.__name__))

  def _lookup_char(self, uname_prefix, uname):
    prefix_and_name = uname_prefix + uname
    try:
      u_char = unicodedata.lookup(prefix_and_name)
    except KeyError:
      u_char = unicodedata.lookup(uname)
    return u_char

  def setUp(self):
    super().setUp()
    logging.info('Parsing %s ...', FLAGS.input_text_proto)
    self.assertTrue(os.path.exists(FLAGS.input_text_proto))
    letters_proto = letter_languages_pb2.LetterLanguages()
    with open(FLAGS.input_text_proto, encoding='utf8') as f:
      text_format.Parse(f.read(), letters_proto)
    num_letters = len(letters_proto.item)
    logging.info('Read %d letters.', num_letters)
    self.assertLess(0, num_letters)
    self._letters_proto = letters_proto

  def test_letters(self):
    """Make sure the unicode letter names map to raw characters correctly."""
    uname_prefix = self._letters_proto.uname_prefix
    if uname_prefix and not uname_prefix.endswith(' '):
      uname_prefix += ' '

    all_letters = set()
    for i, item in enumerate(self._letters_proto.item):
      # Letter message should not be empty.
      self.assertTrue(item.letter)
      self.assertTrue(item.letter.uname)
      self.assertLen(item.letter.uname, 1)
      self.assertTrue(item.letter.raw)

      # Check that unicode character name matches the raw character.
      uname = item.letter.uname[0]
      with self.assertNotRaises(KeyError):
        u_char = self._lookup_char(uname_prefix, uname)
      self.assertEqual(u_char, item.letter.raw)

      # Check that there are no duplicates and the letters are in the
      # Unicode codepoint order.
      self.assertNotIn(u_char, all_letters,
                       f'Letter {i}: Duplicate letter `{u_char}` found')
      all_letters.add(u_char)
      if i:
        this_codepoint = ord(u_char)
        prev_codepoint = ord(self._letters_proto.item[i - 1].letter.raw)
        self.assertLess(prev_codepoint, this_codepoint,
                        f'Letter {i}: Should be in Unicode codepoint order. '
                        f'This codepoint: {this_codepoint}, '
                        f'previous: {prev_codepoint}')

  def test_languages(self):
    """Sanity checks for language codes."""
    for i, item in enumerate(self._letters_proto.item):
      for code in item.language:
        # The language code should be in ISO 639 format and consists of
        # two letters for ISO 639-1 languages and three letters otherwise.
        self.assertLess(1, len(code))
        self.assertGreater(4, len(code))
        self.assertTrue(code.islower(), f'Line {i}: Language code should be '
                        'lower-case')
        if len(code) == 3:
          lang = pycountry.languages.get(alpha_3=code)
          self.assertTrue(lang, f'Failed to find language for code {code}')
          if hasattr(lang, 'alpha_2'):
            self.fail(f'Letter {i}: Please use two-letter code `{lang.alpha_2}`'
                      f' instead of `{lang.alpha_3}` for {lang.name}')
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
