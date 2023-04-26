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


#ifndef NISABA_PORT_FILE_H_
#define NISABA_PORT_FILE_H_

#include "google/protobuf/message.h"
#include "absl/status/status.h"
#include "absl/strings/string_view.h"

class File {
 public:
  // Opens file "name" with flags specified by "flag".
  // Flags are defined by fopen(), that is "r", "r+", "w", "w+". "a", and "a+".
  static File* Open(const char* const name, const char* const flag);

#ifndef SWIG  // no overloading
  inline static File* Open(const absl::string_view& name,
                           const char* const mode) {
    return Open(name.data(), mode);
  }
#endif  // SWIG

  // Opens file "name" with flags specified by "flag".
  // If open failed, program will exit.
  static File* OpenOrDie(const char* const name, const char* const flag);

#ifndef SWIG  // no overloading
  inline static File* OpenOrDie(const absl::string_view& name,
                                const char* const flag) {
    return OpenOrDie(name.data(), flag);
  }
#endif  // SWIG

  // Reads "size" bytes to buff from file, buff should be pre-allocated.
  size_t Read(void* const buff, size_t size);

  // Reads "size" bytes to buff from file, buff should be pre-allocated.
  // If read failed, program will exit.
  void ReadOrDie(void* const buff, size_t size);

  // Reads a line from file to a string.
  // Each line must be no more than max_length bytes.
  char* ReadLine(char* const output, uint64_t max_length);

  // Reads the whole file to a string, with a maximum length of 'max_length'.
  // Returns the number of bytes read.
  int64_t ReadToString(std::string* const output, uint64_t max_length);

  // Writes "size" bytes of buff to file, buff should be pre-allocated.
  size_t Write(const void* const buff, size_t size);

  // Writes "size" bytes of buff to file, buff should be pre-allocated.
  // If write failed, program will exit.
  void WriteOrDie(const void* const buff, size_t size);

  // Writes a string to file.
  size_t WriteString(const std::string& line);

  // Writes a string to file and append a "\n".
  bool WriteLine(const std::string& line);

  // Closes the file.
  bool Close();
  absl::Status Close(int flags);

  // Flushes buffer.
  bool Flush();

  // Returns file size.
  size_t Size();

  // Inits internal data structures.
  static void Init();

  // Returns the file name.
  absl::string_view filename() const;

  // Deletes a file.
  static bool Delete(const char* const name);
  static bool Delete(const absl::string_view& name) {
    return Delete(name.data());
  }

  // Tests if a file exists.
  static bool Exists(const char* const name);

  bool Open() const;

 private:
  File(FILE* const f_des, const absl::string_view& name);

  FILE* f_;
  const absl::string_view name_;
};

namespace file {

using Options = int;

inline Options Defaults() { return 0xBABA; }

File* OpenOrDie(const absl::string_view& filename,
                const absl::string_view& mode, int flags);

absl::Status WriteString(File* file, const absl::string_view& contents,
                         int flags);

bool ReadFileToProto(const absl::string_view& file_name,
                     google::protobuf::Message* proto);

absl::Status GetTextProto(const absl::string_view& filename,
                          google::protobuf::Message* proto, int flags);

}  // namespace file

#endif  // NISABA_PORT_FILE_H_
