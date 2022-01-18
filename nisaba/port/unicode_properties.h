// Copyright 2022 Nisaba Authors.
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

// Various Unicode properties returned as sets of Unicode characters.
//
// This is an extremely simplified implementation that provides the sets of
// characters that we presently need.

#ifndef NISABA_PORT_UNICODE_PROPERTIES_H_
#define NISABA_PORT_UNICODE_PROPERTIES_H_

#include <cstdint>

#include "absl/container/flat_hash_set.h"

namespace nisaba {
namespace utf8 {

// Returns a set of breaking whitespace characters.
absl::flat_hash_set<char32_t> GetBreakingWhitespaceChars();

// Returns a set of non-breaking whitespace characters.
absl::flat_hash_set<char32_t> GetNonBreakingWhitespaceChars();

// Returns a set of all whitespace characters.
absl::flat_hash_set<char32_t> GetAllWhitespaceChars();

}  // namespace utf8
}  // namespace nisaba

#endif  // NISABA_PORT_UNICODE_PROPERTIES_H_
