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

#include "nisaba/port/unicode_properties.h"

#include <algorithm>
#include <iterator>

namespace nisaba {
namespace utf8 {
namespace {

const absl::flat_hash_set<char32_t> kBreakingWhitespace = {
  U'\u0009',  // character tabulation
  U'\u000A',  // line feed
  U'\u000B',  // line tabulation
  U'\u000C',  // form feed
  U'\u000D',  // carriage return
  U'\u0020',  // space
  U'\u0085',  // next line
  U'\u00A0',  // no-break space
  U'\u1680',  // ogham space mark
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
  U'\u2028',  // line separator
  U'\u2029',  // paragraph separator
  U'\u202F',  // narrow no-break space
  U'\u205F',  // medium mathematical space
  U'\u3000',  // ideographic space
};

const absl::flat_hash_set<char32_t> kNonBreakingWhitespace = {
  U'\u180E',  // mongolian vowel separator
  U'\u200B',  // zero width space
  U'\u200C',  // zero width non-joiner
  U'\u200D',  // zero width joiner
  U'\u2060',  // word joiner
  U'\uFEFF',  // zero width non-breaking space
};

}  // namespace

absl::flat_hash_set<char32_t> GetBreakingWhitespaceChars() {
  return kBreakingWhitespace;
}

absl::flat_hash_set<char32_t> GetNonBreakingWhitespaceChars() {
  return kNonBreakingWhitespace;
}

absl::flat_hash_set<char32_t> GetAllWhitespaceChars() {
  absl::flat_hash_set<char32_t> all_chars;
  std::set_union(kBreakingWhitespace.begin(), kBreakingWhitespace.end(),
                 kNonBreakingWhitespace.begin(), kNonBreakingWhitespace.end(),
                 std::inserter(all_chars, all_chars.begin()));
  return all_chars;
}

}  // namespace utf8
}  // namespace nisaba
