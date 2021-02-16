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

"""Tests for Unicode strings proto parser."""

from nisaba.utils import unicode_strings_pb2
from nisaba.utils import unicode_strings_util as lib
from absl.testing import absltest


class UnicodeStringsUtilTest(absltest.TestCase):

  def _proto_entries_to_string(self, uname_prefix=None, uname=None, raw=None):
    return lib.proto_entries_to_string(uname_prefix, 0, uname, raw)

  def _convert_item(self, uname_prefix=None, uname=None, raw="",
                    to_uname=None, to_raw=""):
    item = unicode_strings_pb2.UnicodeStrings.Item()
    item.uname.extend(uname)
    item.raw = raw
    item.to_uname.extend(to_uname)
    item.to_raw = to_raw
    return lib.convert_item(uname_prefix, 0, item)

  def testProtoEntriesToString(self):
    """Tests the internal API for parsing `uname` and `raw` fields."""
    # The Unicode names or raw Unicode codepoint sequence specification is set.
    self.assertEqual("abc", self._proto_entries_to_string(raw="abc"))
    self.assertEqual("abc", self._proto_entries_to_string(
        uname_prefix="Latin Small Letter", uname=["A", "B", "C"]))
    with self.assertRaisesRegex(ValueError, r"Lookup failed"):
      # Invalid Unicode character name should fail.
      self._proto_entries_to_string(uname=["AZTEC LETTER Ы"])

    # Both the unicode names or raw Unicode codepoint sequence specification is
    # set. In this case, both need to be equivalent.
    brahmi_string = "𑀅𑀞𑀪𑀸𑀕𑀺𑀬𑁂𑀘"
    brahmi_unames = ["LETTER A", "LETTER TTHA", "LETTER BHA", "VOWEL SIGN AA",
                     "LETTER GA", "VOWEL SIGN I", "LETTER YA", "VOWEL SIGN E",
                     "LETTER CA"]
    self.assertEqual(brahmi_string, self._proto_entries_to_string(
        uname_prefix="BRAHMI", uname=brahmi_unames, raw=brahmi_string))

    # The Unicode name sequence mismatches the reference raw string.
    with self.assertRaisesRegex(ValueError, r"mismatch the contents"):
      self._proto_entries_to_string(
          uname_prefix="BRAHMI", uname=brahmi_unames + ["LETTER A"],
          raw=brahmi_string)
    with self.assertRaisesRegex(ValueError, r"mismatch the contents"):
      self._proto_entries_to_string(
          uname_prefix="BRAHMI", uname=brahmi_unames,
          raw=brahmi_string + "𑀞")

  def testConvertItem(self):
    """Tests the internal API for parsing UnicodeStrings.Item field."""
    # Only list items are set.
    source, dest = self._convert_item(raw="abc")
    self.assertEqual("abc", source)
    self.assertFalse(dest)
    latin_prefix = "Latin Small Letter"
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      uname=["A", "B", "C"])
    self.assertEqual("abc", source)
    self.assertFalse(dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      raw="abc", uname=["A", "B", "C"])
    self.assertEqual("abc", source)
    self.assertFalse(dest)

    # Either `uname` or `raw` or both have to be set.
    with self.assertRaisesRegex(ValueError, r"have to be defined"):
      self._convert_item(to_raw="abc")
    with self.assertRaisesRegex(ValueError, r"have to be defined"):
      self._convert_item(to_uname=["A", "B", "C"])

    # Mapping items are set.
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      raw="abc", to_uname=["D", "E", "F"])
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      raw="abc", uname=["A", "B", "C"],
                                      to_uname=["D", "E", "F"])
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      uname=["A", "B", "C"],
                                      to_uname=["D", "E", "F"])
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      uname=["A", "B", "C"],
                                      to_raw="def", to_uname=["D", "E", "F"])
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      raw="abc", to_raw="def")
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)
    source, dest = self._convert_item(uname_prefix=latin_prefix,
                                      raw="abc", uname=["A", "B", "C"],
                                      to_raw="def", to_uname=["D", "E", "F"])
    self.assertEqual("abc", source)
    self.assertEqual("def", dest)

    # Check equivalence of raw and uname fields on either side.
    with self.assertRaisesRegex(ValueError, r"mismatch the contents"):
      self._convert_item(uname_prefix=latin_prefix, raw="abc", uname=["X"])
    with self.assertRaisesRegex(ValueError, r"mismatch the contents"):
      self._convert_item(uname_prefix=latin_prefix,
                         raw="___", to_raw="abc", to_uname=["X"])


if __name__ == "__main__":
  absltest.main()
