// Copyright 2025 Nisaba Authors.
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

#include <iterator>

#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "utf8/checked.h"

namespace {
using utf8_iterator = ::utf8::iterator<absl::string_view::const_iterator>;
}  // namespace

namespace nisaba {
namespace utf8 {

std::vector<std::string> StrSplitByChar(absl::string_view input) {
     if (!::utf8::is_valid(input.begin(), input.end())) {
       return {};  // Refuse to split invalid UTF8 input.
     }
     const int num_codepoints = ::utf8::distance(input.begin(), input.end());
     std::vector<std::string> result;
     result.reserve(num_codepoints);

     utf8_iterator pos(input.begin(), input.begin(), input.end());
     const utf8_iterator pos_end(input.end(), input.begin(), input.end());
     while (pos != pos_end) {
       std::string codepoint;
       ::utf8::append(*pos, std::back_inserter(codepoint));
       result.push_back(codepoint);
       ++pos;
     }
     return result;
}

int DecodeUnicodeChar(absl::string_view input, char32 *first_char) {
     if (input.empty()) {  // Do nothing.
       *first_char = 0;
       return 1;
     }
     if (!::utf8::is_valid(input.begin(), input.end())) {  // Error.
       *first_char = kBadUTF8Char;
       return 1;
     }
     utf8_iterator pos(input.begin(), input.begin(), input.end());
     const utf8_iterator pos_end(input.end(), input.begin(), input.end());
     if (pos == pos_end) {  // This probably should not happen. Error.
       *first_char = kBadUTF8Char;
       return 1;
     }
     *first_char = *pos;
     ++pos;
     return pos.base() - input.begin();  // Number of bytes.
}

std::vector<int> StrSplitByCharToUnicode(absl::string_view input) {
  const std::vector<std::string> input_chars = StrSplitByChar(input);
  std::vector<int> input_codepoints(input_chars.size());
  for (int i = 0; i < input_chars.size(); ++i) {
    DecodeSingleUnicodeChar(input_chars[i], &(input_codepoints[i]));
  }
  return input_codepoints;
}

bool DecodeSingleUnicodeChar(absl::string_view input, char32 *utf8_value) {
  int num_bytes = DecodeUnicodeChar(input, utf8_value);
  if (num_bytes != input.length() && *utf8_value != kBadUTF8Char) {
    // Indicates decoding was successful but input has more than one character.
    *utf8_value = kBadUTF8Char;
  }
  // Returns false for input strings that do not consist of exactly one Unicode
  // character (num_bytes != input.length()) or if decoding failed (which
  // returns *utf8_value == kBadUTF8Char and num_bytes == 1); otherwise true.
  return num_bytes == input.length() &&
         (*utf8_value != kBadUTF8Char || num_bytes > 1);
}

std::string EncodeUnicodeChar(char32 input) {
     std::string result;
     ::utf8::append(input, std::back_inserter(result));
     return result;
}

}  // namespace utf8
}  // namespace nisaba
