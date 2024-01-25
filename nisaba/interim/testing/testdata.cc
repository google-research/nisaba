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

// Library used for textproto-based grammar testdata.

#include "nisaba/interim/testing/testdata.h"

#include "nisaba/port/file.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/proto_file_stream.h"
#include "absl/log/log.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "google/protobuf/text_format.h"
#include "nisaba/port/status_macros.h"

namespace testing {

// Loads rewrites from textproto file or fails.
absl::StatusOr<Rewrites> GetRewritesTextProto(absl::string_view filename) {
  Rewrites rewrites;
  RETURN_IF_ERROR(
      ::file::GetTextProto(filename, &rewrites, ::file::Defaults()));
  return rewrites;
}

// Serializes rewrites from file to textproto or fails.
absl::Status SetRewritesTextProto(absl::string_view filename,
                                  const Rewrites &rewrites) {
  // Opens file and creates output stream.
  File *sink = ::file::OpenOrDie(filename, "w", ::file::Defaults());
  ::nisaba::proto::ProtoFileOutputStream ostream(sink);
  // Writes header.
  static const auto *const kOutputFileHeader = new absl::Cord(
      R"(# proto-file: third_party/nisaba/interim/testing/testdata.proto
# proto-message: Rewrites
)");
  if (!ostream.WriteCord(*kOutputFileHeader)) {
    ostream.Close();
    return absl::UnknownError("Header writing failed");
  }
  // Writes message.
  static const auto *const kPrinter = [] {
    auto printer = new google::protobuf::TextFormat::Printer();
    printer->SetUseUtf8StringEscaping(true);
    return printer;
  }();
  if (!kPrinter->Print(rewrites, &ostream)) {
    ostream.Close();
    return absl::UnknownError("Proto writing failed");
  }
  if (!ostream.Close()) return absl::UnknownError("File closing failed");
  return absl::OkStatus();
}

}  // namespace testing
