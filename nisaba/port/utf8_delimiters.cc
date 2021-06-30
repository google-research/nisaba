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

#include "nisaba/port/unicode_properties.h"
#include "utf8/checked.h"

namespace nisaba {
namespace utf8 {
namespace {

const absl::flat_hash_set<char32_t> kBreakingWhitespace =
    GetBreakingWhitespaceChars();

}  // namespace

Utf8WhitespaceDelimiter::Utf8WhitespaceDelimiter() :
    Utf8Delimiter(kBreakingWhitespace) {}

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
