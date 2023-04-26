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

// This file implements ZeroCopyOutputStream in terms of File class.

#ifndef NISABA_PORT_PROTO_FILE_STREAM_H_
#define NISABA_PORT_PROTO_FILE_STREAM_H_

#include "nisaba/port/file.h"
#include "google/protobuf/io/zero_copy_stream.h"
#include "google/protobuf/io/zero_copy_stream_impl.h"

namespace nisaba {
namespace proto {

// A ZeroCopyOutputStream that writes to a File.
class ProtoFileOutputStream : public google::protobuf::io::ZeroCopyOutputStream {
 public:
  // Creates a stream that writes to the provided File.
  explicit ProtoFileOutputStream(File* fp, int block_size = -1);
  ~ProtoFileOutputStream() override;

  void SetCloseOnDelete(bool value);
  bool Close();
  bool Flush();

  // implements ZeroCopyOutputStream ---------------------------------
  bool Next(void** data, int* size) override;
  void BackUp(int count) override;
  int64_t ByteCount() const override;

 private:
  class CopyingProtoFileOutputStream : public google::protobuf::io::CopyingOutputStream {
   public:
    explicit CopyingProtoFileOutputStream(File* fp);
    ~CopyingProtoFileOutputStream() override;

    void SetCloseOnDelete(bool value);
    bool Close();
    bool Write(const void* buffer, int size) override;

   private:
    File* fp_;
    bool close_file_on_delete_;

    CopyingProtoFileOutputStream() = delete;
    CopyingProtoFileOutputStream(const CopyingProtoFileOutputStream &) = delete;
  };

  CopyingProtoFileOutputStream copying_output_;
  google::protobuf::io::CopyingOutputStreamAdaptor impl_;

  ProtoFileOutputStream() = delete;
  ProtoFileOutputStream(const ProtoFileOutputStream &) = delete;
};

// ===================================================================

}  // namespace proto
}  // namespace nisaba

#endif  // NISABA_PORT_PROTO_FILE_STREAM_H_
