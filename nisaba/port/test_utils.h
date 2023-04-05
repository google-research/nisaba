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

// Collection of small utilities for use in tests.

#ifndef NISABA_PORT_TEST_UTILS_H_
#define NISABA_PORT_TEST_UTILS_H_

#include <string>

#include "absl/strings/string_view.h"

namespace nisaba {
namespace testing {

// Returns path to a file in a given directory under a test directory tree.
std::string TestFilePath(absl::string_view dir_name,
                         absl::string_view file_name);

}  // namespace testing
}  // namespace nisaba

#endif  // NISABA_PORT_TEST_UTILS_H_
