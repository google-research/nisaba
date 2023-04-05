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


#include "nisaba/port/utf8_delimiters.h"

#include <string>

#include "gmock/gmock.h"
#include "gtest/gtest.h"

namespace nisaba {
namespace utf8 {
namespace {

TEST(Utf8DelimitersTest, WhitespaceBasicCheck) {
  Utf8WhitespaceDelimiter delim;
  // Check for basic byte-encodable whitespace.
  EXPECT_TRUE(delim.Find("abcdefg", 0).empty());
  std::string input_text = "\r\t ";
  EXPECT_EQ("\r", delim.Find(input_text, 0));
  EXPECT_EQ("\t", delim.Find(input_text, 1));
  EXPECT_EQ(" ", delim.Find(input_text, 2));

  input_text = "hello world ";
  EXPECT_EQ(" ", delim.Find(input_text, 0));
  EXPECT_EQ(" ", delim.Find(input_text, 6));
  EXPECT_EQ(" ", delim.Find("world ", 0));

  // Check Unicode whitespace:
  //   - [non-breaking] Mongolian vowel separator: U+180E => 0xE1 0xA0 0x8E.
  //   - [breaking] Ideographic space: U+3000 => 0xE3 0x80 0x80.
  input_text = "hello\xE1\xA0\x8Eworld\xE3\x80\x80";
  EXPECT_EQ("\xE3\x80\x80", delim.Find(input_text, 0));
  EXPECT_EQ("\xE3\x80\x80", delim.Find(input_text, 8));
}

}  // namespace
}  // namespace utf8
}  // namespace nisaba
