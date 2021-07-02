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

#include "nisaba/port/file_util.h"

#include <errno.h>
#include <stdlib.h>

#include "absl/strings/str_cat.h"
#include "tools/cpp/runfiles/runfiles.h"

using ::bazel::tools::cpp::runfiles::Runfiles;

#if defined(WIN32)
#  define PATH_SEPARATOR "\\"
#else
#  define PATH_SEPARATOR "/"
#endif  // WIN32

namespace {

std::string GetProgramName() {
#ifdef __GLIBC__
  return program_invocation_name;
#else // *BSD and OS X.
  return ::getprogname();
#endif  // __GLIBC__
}

}  // namespace

namespace nisaba {
namespace file {

absl::StatusOr<std::string> GetRunfilesResourcePath(absl::string_view path) {
  std::string error;
  std::unique_ptr<Runfiles> runfiles(
      Runfiles::Create(::GetProgramName(), &error));
  if (!runfiles) {
    return absl::NotFoundError(error);
  }
  return runfiles->Rlocation(std::string(path));
}

std::string JoinPath(absl::string_view dirname, absl::string_view basename) {
  if ((!basename.empty() && basename[0] == PATH_SEPARATOR[0]) ||
      dirname.empty()) {
    return std::string(basename);
  } else if (dirname[dirname.size() - 1] == PATH_SEPARATOR[0]) {
    return absl::StrCat(dirname, basename);
  } else {
    return absl::StrCat(dirname, PATH_SEPARATOR, basename);
  }
}

}  // namespace file
}  // namespace nisaba
