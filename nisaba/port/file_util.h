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

// Miscellaneous file I/O helper utilities.

#ifndef NISABA_PORT_FILE_UTIL_H_
#define NISABA_PORT_FILE_UTIL_H_

#include <string>
#include <vector>

#include "absl/status/statusor.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace file {

// Returns full path of the resource that resides under runfiles directory.
absl::StatusOr<std::string> GetRunfilesResourcePath(absl::string_view path);

// Portable path joiner.
std::string JoinPath(absl::string_view dirname, absl::string_view basename);

// Returns a path to a temporary file given its filename.
std::string TempFilePath(absl::string_view filename);

// Writes temporary text file given its filename and contents. Returns its
// full path or error.
absl::StatusOr<std::string> WriteTempTextFile(absl::string_view filename,
                                              absl::string_view contents);

// Writes text file given the contents.
absl::Status WriteTextFile(absl::string_view file_path,
                           absl::string_view contents);

// Reads binary file into a buffer or returns error.
absl::StatusOr<std::string> ReadBinaryFile(absl::string_view file_path);

// Reads text file into a buffer or returns error.
absl::StatusOr<std::string> ReadTextFile(absl::string_view file_path);

// Reads lines from a text file removing the trailing carriage return and line
// feed characters.
absl::StatusOr<std::vector<std::string>> ReadLines(
    absl::string_view input_file, int max_line_length = -1);

}  // namespace file
}  // namespace nisaba

#endif  // NISABA_PORT_FILE_UTIL_H_
