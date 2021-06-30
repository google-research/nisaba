// Copyright 2021 Nisaba Authors.
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

#include "utf8/checked.h"

namespace nisaba {
namespace utf8 {
namespace {

const absl::flat_hash_set<char32_t> kUnicodeWhitespace = {
  U'\u0009',  // character tabulation
  U'\u000A',  // line feed
  U'\u000B',  // line tabulation
  U'\u000C',  // form feed
  U'\u000D',  // carriage return
  U'\u0020',  // space
  U'\u0085',  // next line
  U'\u00A0',  // no-break space
  U'\u1680',  // ogham space mark
  U'\u180E',  // mongolian vowel separator
  U'\u2000',  // en quad
  U'\u2001',  // em quad
  U'\u2002',  // en space
  U'\u2003',  // em space
  U'\u2004',  // three-per-em space
  U'\u2005',  // four-per-em space
  U'\u2006',  // six-per-em space
  U'\u2007',  // figure space
  U'\u2008',  // punctuation space
  U'\u2009',  // thin space
  U'\u200A',  // hair space
  U'\u200B',  // zero width space
  U'\u200C',  // zero width non-joiner
  U'\u200D',  // zero width joiner
  U'\u2028',  // line separator
  U'\u2029',  // paragraph separator
  U'\u202F',  // narrow no-break space
  U'\u205F',  // medium mathematical space
  U'\u2060',  // word joiner
  U'\u3000',  // ideographic space
};

}  // namespace

Utf8WhitespaceDelimiter::Utf8WhitespaceDelimiter() :
    Utf8Delimiter(kUnicodeWhitespace) {}

// TODO: We don't deal with malformed encodings yet.
absl::string_view Utf8Delimiter::Find(absl::string_view text,
                                      size_t pos) const {
  const absl::string_view tail = absl::ClippedSubstr(text, pos);
  absl::flat_hash_set<char32_t>::const_iterator del_iter;
  absl::string_view::const_iterator u8_pos = tail.begin();
  while (u8_pos != tail.end()) {
    const absl::string_view::const_iterator prev_u8_pos = u8_pos;
    const char32_t u32_c = ::utf8::next(u8_pos, tail.end());
    del_iter = delimiters_.find(u32_c);
    if (del_iter != delimiters_.end()) {
      const int u8_offset = prev_u8_pos - tail.begin();
      const int delim_length = u8_pos - prev_u8_pos;
      return absl::string_view(tail.data() + u8_offset, delim_length);
    }
  }
  return absl::string_view(tail.end(), 0);
}

}  // namespace utf8
}  // namespace nisaba
