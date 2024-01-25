// Copyright 2024 Nisaba Authors.
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

// Miscellaneous UTF8 string delimiters for use with absl strings.
//
// A `Delimiter` is an object with a `Find()` function that knows how to find
// the first occurrence of itself in a given `absl::string_view`. See
//
//   https://github.com/abseil/abseil-cpp/blob/master/absl/strings/str_split.h
//
// for documentation.

#ifndef NISABA_PORT_UTF8_DELIMITERS_H_
#define NISABA_PORT_UTF8_DELIMITERS_H_

#include <cstdint>

#include "absl/container/flat_hash_set.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace utf8 {

// Characters matching a given set of UTF8 strings are considered delimiters.
class Utf8Delimiter {
 public:
  // Finds the first occurrence of itself in a given `text`.
  absl::string_view Find(absl::string_view text, size_t pos) const;

 protected:
  Utf8Delimiter(const absl::flat_hash_set<char32_t> &delimiters) :
      delimiters_(delimiters) {}

 private:
  const absl::flat_hash_set<char32_t> &delimiters_;
};

// Concrete delimiter type that provides splitting on Unicode whitespace.
class Utf8WhitespaceDelimiter : public Utf8Delimiter {
 public:
  Utf8WhitespaceDelimiter();
};

}  // namespace utf8
}  // namespace nisaba

#endif  // NISABA_PORT_UTF8_DELIMITERS_H_
