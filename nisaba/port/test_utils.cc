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

#include "nisaba/port/test_utils.h"

#include <filesystem>

#include "google/protobuf/stubs/logging.h"
#include "gtest/gtest.h"
#include "absl/flags/flag.h"
#include "absl/strings/string_view.h"
#include "nisaba/port/file_util.h"

using nisaba::file::GetRunfilesResourcePath;
using nisaba::file::JoinPath;

namespace nisaba {
namespace testing {

std::string TestFilePath(absl::string_view dir_name,
                         absl::string_view file_name) {
  const auto status = GetRunfilesResourcePath(JoinPath(dir_name, file_name));
  std::filesystem::path model_path;
  if (status.ok()) {
    model_path = std::move(status.value());
  } else {
    GOOGLE_LOG(WARNING) << "Can't deduce runfiles path";
  }
  return model_path.make_preferred().string();
}

}  // namespace testing
}  // namespace nisaba
