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

#include "nisaba/port/proto_file_stream.h"

#include "nisaba/port/file.h"
#include "nisaba/port/file_util.h"
#include "fst/log.h"
#include "fst/log.h"
#include "nisaba/port/status_macros.h"

namespace nisaba {
namespace proto {

ProtoFileOutputStream::ProtoFileOutputStream(File* fp, int block_size)
    : copying_output_(fp), impl_(&copying_output_, block_size) {}

ProtoFileOutputStream::~ProtoFileOutputStream() { impl_.Flush(); }

bool ProtoFileOutputStream::Close() {
  bool flush_succeeded = impl_.Flush();
  return copying_output_.Close() && flush_succeeded;
}

void ProtoFileOutputStream::SetCloseOnDelete(bool value) {
  copying_output_.SetCloseOnDelete(value);
}

bool ProtoFileOutputStream::Flush() { return impl_.Flush(); }

bool ProtoFileOutputStream::Next(void** data, int* size) {
  return impl_.Next(data, size);
}

void ProtoFileOutputStream::BackUp(int count) { impl_.BackUp(count); }

int64_t ProtoFileOutputStream::ByteCount() const { return impl_.ByteCount(); }

ProtoFileOutputStream::CopyingProtoFileOutputStream::
    CopyingProtoFileOutputStream(File* fp)
    : fp_(fp), close_file_on_delete_(false) {}

ProtoFileOutputStream::CopyingProtoFileOutputStream::
    ~CopyingProtoFileOutputStream() {
  if (close_file_on_delete_ && fp_ != nullptr) Close();
}

bool ProtoFileOutputStream::CopyingProtoFileOutputStream::Close() {
  if (fp_ == nullptr) {
    LOG(FATAL) << "File has already been closed!";
  }
  bool retval = fp_->Close(::file::Defaults()).ok();
  fp_ = nullptr;
  return retval;
}

void ProtoFileOutputStream::CopyingProtoFileOutputStream::SetCloseOnDelete(
    bool value) {
  close_file_on_delete_ = value;
}

bool ProtoFileOutputStream::CopyingProtoFileOutputStream::Write(
    const void* buffer, int size) {
  CHECK(fp_ != nullptr);
  return ::file::WriteString(
             fp_,
             absl::string_view(reinterpret_cast<const char*>(buffer), size),
             ::file::Defaults())
      .ok();
}

}  // namespace proto
}  // namespace nisaba
