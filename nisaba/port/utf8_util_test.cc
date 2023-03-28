// Copyright 2023 Nisaba Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "nisaba/port/utf8_util.h"

#include <string>
#include <vector>

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "nisaba/port/unicode_properties.h"

using ::testing::ElementsAre;

namespace nisaba {
namespace utf8 {
namespace {

TEST(Utf8UtilTest, CheckStrSplitByChar) {
  EXPECT_THAT(StrSplitByChar("abcdefg"), ElementsAre(
      "a", "b", "c", "d", "e", "f", "g"));
  EXPECT_THAT(StrSplitByChar("Բարեւ"), ElementsAre(
      "Բ", "ա", "ր", "ե", "ւ"));
  EXPECT_THAT(StrSplitByChar("ባህሪ"), ElementsAre(
      "ባ", "ህ", "ሪ"));
  EXPECT_THAT(StrSplitByChar("ස්වභාවය"), ElementsAre(
      "ස", "්", "ව", "භ", "ා", "ව", "ය"));
  EXPECT_THAT(StrSplitByChar("მოგესალმებით"), ElementsAre(
      "მ", "ო", "გ", "ე", "ს", "ა", "ლ", "მ", "ე", "ბ", "ი", "თ"));
  EXPECT_THAT(StrSplitByChar("ຍິນດີຕ້ອນຮັບ"), ElementsAre(
      "ຍ", "ິ", "ນ", "ດ", "ີ", "ຕ", "້", "ອ", "ນ", "ຮ", "ັ", "ບ"));
}

TEST(Utf8UtilTest, CheckStrSplitByCharToUnicode) {
  EXPECT_THAT(StrSplitByCharToUnicode("abcdefg"),
              ElementsAre(97, 98, 99, 100, 101, 102, 103));
  EXPECT_THAT(StrSplitByCharToUnicode("Բարեւ"),
              ElementsAre(1330, 1377, 1408, 1381, 1410));
  EXPECT_THAT(StrSplitByCharToUnicode("ባህሪ"), ElementsAre(4707, 4613, 4650));
  EXPECT_THAT(StrSplitByCharToUnicode("ස්වභාවය"),
              ElementsAre(3523, 3530, 3520, 3511, 3535, 3520, 3514));
  EXPECT_THAT(StrSplitByCharToUnicode("მოგესალმებით"),
              ElementsAre(4315, 4317, 4306, 4308, 4321, 4304, 4314, 4315, 4308,
                          4305, 4312, 4311));
  EXPECT_THAT(StrSplitByCharToUnicode("ຍິນດີຕ້ອນຮັບ"),
              ElementsAre(3725, 3764, 3737, 3732, 3765, 3733, 3785, 3757, 3737,
                          3758, 3761, 3738));
}

TEST(Utf8UtilTest, CheckDecodeUnicodeChar) {
  char32 code;
  EXPECT_EQ(1, DecodeUnicodeChar("z", &code));
  EXPECT_EQ(122, code);
  EXPECT_EQ(3, DecodeUnicodeChar("ස්", &code));
  EXPECT_EQ(3523, code);  // The first letter: Sinhala Letter Dantaja Sayanna.
  EXPECT_EQ(2, DecodeUnicodeChar("ܨ", &code));
  EXPECT_EQ(1832, code);  // Syriac Letter Sadhe.
  EXPECT_EQ(3, DecodeUnicodeChar("༄", &code));
  EXPECT_EQ(3844, code);  // TIBETAN MARK INITIAL YIG MGO MDUN MA

  // Invalid UTF8. For examples, see:
  //   https://www.cl.cam.ac.uk/~mgk25/ucs/examples/UTF-8-test.txt
  EXPECT_EQ(1, DecodeUnicodeChar("\xfe\xfe\xff\xff", &code));
  EXPECT_EQ(kBadUTF8Char, code);
}

TEST(Utf8UtilTest, CheckEncodeUnicodeChar) {
  EXPECT_EQ("z", EncodeUnicodeChar(122));
  EXPECT_EQ("ܨ", EncodeUnicodeChar(1832));
  EXPECT_EQ("༄", EncodeUnicodeChar(3844));
  // Cuneiform sign dag kisim5 times tak4 (U+1206B).
  EXPECT_EQ("𒁫", EncodeUnicodeChar(73835));
}

TEST(Utf8UtilTest, CheckPortableUtf8WhitespaceDelimiter) {
  // Basic ASCII whitespace.
  std::string input_text = " hello world again ";
  std::vector<absl::string_view> toks = absl::StrSplit(
      input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  ASSERT_EQ(3, toks.size());
  EXPECT_EQ("hello", toks[0]);
  EXPECT_EQ("world", toks[1]);
  EXPECT_EQ("again", toks[2]);

  // Mongolian script.
  input_text = "ᠲ᠋ᠤᠷᠬᠥᠬᠡᠬᠣᠲᠠ";
  toks = absl::StrSplit(
      input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  ASSERT_EQ(1, toks.size());
  EXPECT_EQ(input_text, toks[0]);
  const std::string punctuation_space = " \xE2\x80\x88 ";
  const std::string original_text = input_text;
  input_text += punctuation_space + "ᢆ";
  toks = absl::StrSplit(
      input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  ASSERT_EQ(2, toks.size());
  EXPECT_EQ(original_text, toks[0]);
  EXPECT_EQ("ᢆ", toks[1]);

  // Check that we don't break on non-breaking space.
  const std::string zero_width_non_breaking_space = "\xEF\xBB\xBF";
  const std::string final_part = zero_width_non_breaking_space + "ᠻᠦ᠋";
  input_text += final_part;
  toks = absl::StrSplit(
      input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  ASSERT_EQ(2, toks.size());
  EXPECT_EQ(original_text, toks[0]);
  EXPECT_EQ("ᢆ" + final_part, toks[1]);
}

TEST(Utf8UtilTest, BreakingVsNonBreakingWhitespaceSplit) {
  // Check that we don't break on non-breaking whitespace characters.
  const auto &non_break_chars = GetNonBreakingWhitespaceChars();
  for (auto u32_char : non_break_chars) {
    const std::string &no_delim = EncodeUnicodeChar(u32_char);
    const std::string input_text = "a" + no_delim + "b";
    const std::vector<absl::string_view> toks = absl::StrSplit(
        input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
    ASSERT_EQ(1, toks.size()) << "Expected non-breaking char: " << std::hex
                              << static_cast<uint32_t>(u32_char);
    EXPECT_EQ(toks[0], input_text);
  }

  // Check that the splitter works on breaking whitespace.
  const auto &breaking_chars = GetBreakingWhitespaceChars();
  for (auto u32_char : breaking_chars) {
    const std::string &delim = EncodeUnicodeChar(u32_char);
    const std::string input_text = "a" + delim + "b";
    const std::vector<absl::string_view> toks = absl::StrSplit(
        input_text, Utf8WhitespaceDelimiter(), absl::SkipEmpty());
    ASSERT_EQ(2, toks.size()) << "Expected breaking char: " << std::hex
                              << static_cast<uint32_t>(u32_char);
    EXPECT_EQ(toks[0], "a");
    EXPECT_EQ(toks[1], "b");
  }
}

}  // namespace
}  // namespace utf8
}  // namespace nisaba
