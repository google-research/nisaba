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

#include "nisaba/port/file_util.h"

#include <errno.h>
#include <stdlib.h>

#include <filesystem>
#include <fstream>

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
#if !defined(WIN32) && !defined(_MSC_VER)
// UNIX platforms.
#ifdef __GLIBC__
  return program_invocation_name;
#else // *BSD and OS X.
  return ::getprogname();
#endif  // __GLIBC__
#else
  // TODO: Provide portable implementation for Windows platforms.
  return "";
#endif  // WIN32
}

}  // namespace

namespace nisaba {
namespace file {
namespace {

// For reading lines with file::ReadLines().
constexpr int kDefaultMaxLineLength = 32768;

}  // namespace

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

std::string TempFilePath(std::string_view filename) {
  const std::filesystem::path tmp_dir = std::filesystem::temp_directory_path();
  std::filesystem::path file_path = tmp_dir / filename;
  return file_path.string();
}

absl::StatusOr<std::string> WriteTempTextFile(std::string_view filename,
                                              std::string_view contents) {
  const std::string &path = TempFilePath(filename);
  std::ofstream out(path);
  if (!out) {
    return absl::PermissionDeniedError(
        absl::StrCat("Failed to open: ", std::string(path)));
  }
  out << contents;
  if (!out.good()) {
    return absl::InternalError(
        absl::StrCat("Failed to write to", std::string(path)));
  }
  return path;
}

absl::Status WriteTextFile(std::string_view file_path,
                           std::string_view contents) {
  std::ofstream output;
  output.open(std::string(file_path));
  if (!output) {
    return absl::PermissionDeniedError(
        absl::StrCat("Failed to open: ", std::string(file_path)));
  }
  output << contents;
  if (!output) {
    return absl::PermissionDeniedError(
        absl::StrCat("Failed to write: ", contents.size(), " bytes to ",
                     std::string(file_path)));
  }
  return absl::OkStatus();
}

namespace {

absl::StatusOr<std::string> ReadFile(std::string_view file_path,
                                     std::ios_base::openmode mode) {
  std::ifstream input;
  // Need to construct std::string explictly below. See:
  //   https://cplusplus.github.io/LWG/issue3430
  input.open(std::string(file_path), mode);
  if (!input) {
    return absl::NotFoundError(
        absl::StrCat("Failed to open: ", std::string(file_path)));
  }
  std::string contents;
  input.seekg(0, std::ios::end);
  const std::streampos file_size = input.tellg();
  if (file_size <= 0) {
    return absl::InternalError("File empty or invalid");
  }
  contents.reserve(file_size);
  input.seekg(0, std::ios::beg);
  contents.assign(std::istreambuf_iterator<char>(input),
                  std::istreambuf_iterator<char>());
  return contents;
}

}  // namespace

absl::StatusOr<std::string> ReadBinaryFile(std::string_view file_path) {
  return ReadFile(file_path, std::ifstream::in | std::ifstream::binary);
}

absl::StatusOr<std::string> ReadTextFile(std::string_view file_path) {
  return ReadFile(file_path, std::ifstream::in);
}

absl::StatusOr<std::vector<std::string>> ReadLines(absl::string_view input_file,
                                                   int max_line_length) {
  std::string::size_type max_length = max_line_length;
  if (max_line_length < 0) max_length = kDefaultMaxLineLength;
  std::vector<std::string> input_lines;
  std::ifstream ifs;
  ifs.open(std::string(input_file));
  if (!ifs) {
    return absl::PermissionDeniedError(absl::StrCat("Failed to open: ",
      input_file));
  }
  std::string line;
  while (std::getline(ifs, line)) {
    if (line.empty()) continue;
    if (line.size() >= max_length) line[max_length - 1] = '\0';
    input_lines.emplace_back(line);
  }
  return input_lines;
}

}  // namespace file
}  // namespace nisaba
