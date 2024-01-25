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

#include "nisaba/port/file.h"

#include <sys/stat.h>
#include <sys/types.h>

#include <iostream>
#include <memory>

#include "absl/log/check.h"
#include "absl/log/log.h"
#include "nisaba/port/file_util.h"
#include "google/protobuf/text_format.h"

#if defined(_MSC_VER)
#include <io.h>
#define access _access
#define F_OK 0
#else
#include <unistd.h>
#endif

File::File(FILE* const f_des, const absl::string_view& name)
    : f_(f_des), name_(name) {}

bool File::Delete(const char* const name) { return remove(name) == 0; }

bool File::Exists(const char* const name) { return access(name, F_OK) == 0; }

size_t File::Size() {
  struct stat f_stat;
  stat(name_.data(), &f_stat);
  return f_stat.st_size;
}

bool File::Flush() { return fflush(f_) == 0; }

bool File::Close() {
  if (fclose(f_) == 0) {
    f_ = nullptr;
    return true;
  } else {
    return false;
  }
}

absl::Status File::Close(int flags) {
  if (flags != file::Defaults())
    return absl::Status(absl::StatusCode::kInvalidArgument, "Wrong flags");
  return Close()
             ? absl::OkStatus()
             : absl::Status(absl::StatusCode::kInvalidArgument,
                            absl::StrCat("Could not close file '", name_, "'"));
}

void File::ReadOrDie(void* const buf, size_t size) {
  CHECK_EQ(fread(buf, 1, size, f_), size);
}

size_t File::Read(void* const buf, size_t size) {
  return fread(buf, 1, size, f_);
}

void File::WriteOrDie(const void* const buf, size_t size) {
  CHECK_EQ(fwrite(buf, 1, size, f_), size);
}
size_t File::Write(const void* const buf, size_t size) {
  return fwrite(buf, 1, size, f_);
}

File* File::OpenOrDie(const char* const name, const char* const flag) {
  FILE* const f_des = fopen(name, flag);
  if (f_des == nullptr) {
    std::cerr << "Cannot open " << name;
    exit(1);
  }
  File* const f = new File(f_des, name);
  return f;
}

File* File::Open(const char* const name, const char* const flag) {
  FILE* const f_des = fopen(name, flag);
  if (f_des == nullptr) return nullptr;
  File* const f = new File(f_des, name);
  return f;
}

char* File::ReadLine(char* const output, uint64_t max_length) {
  return fgets(output, max_length, f_);
}

int64_t File::ReadToString(std::string* const output, uint64_t max_length) {
  CHECK(output != nullptr);
  output->clear();

  if (max_length == 0) return 0;

  int64_t needed = max_length;
  int bufsize = (needed < (2 << 20) ? needed : (2 << 20));

  std::unique_ptr<char[]> buf(new char[bufsize]);

  int64_t nread = 0;
  while (needed > 0) {
    nread = Read(buf.get(), (bufsize < needed ? bufsize : needed));
    if (nread > 0) {
      output->append(buf.get(), nread);
      needed -= nread;
    } else {
      break;
    }
  }
  return (nread >= 0 ? static_cast<int64_t>(output->size()) : -1);
}

size_t File::WriteString(const std::string& line) {
  return Write(line.c_str(), line.size());
}

bool File::WriteLine(const std::string& line) {
  if (Write(line.c_str(), line.size()) != line.size()) return false;
  return Write("\n", 1) == 1;
}

absl::string_view File::filename() const { return name_; }

bool File::Open() const { return f_ != nullptr; }

void File::Init() {}

namespace file {



File* OpenOrDie(const absl::string_view& filename,
                const absl::string_view& mode, int flags) {
  File* f;
  CHECK_EQ(flags, Defaults());
  f = File::Open(filename, mode.data());
  if (f == nullptr) {
    LOG(FATAL) << absl::StrCat("Could not open '", filename, "'");
  }
  return f;
}

absl::Status WriteString(File* file, const absl::string_view& contents,
                         int flags) {
  if (flags == Defaults() && file != nullptr &&
      file->Write(contents.data(), contents.size()) == contents.size()) {
    return absl::OkStatus();
  }
  return absl::Status(
      absl::StatusCode::kInvalidArgument,
      absl::StrCat("Could not write ", contents.size(), " bytes"));
}

bool ReadFileToProto(const absl::string_view& file_name,
                     google::protobuf::Message* proto) {
  const auto &str_or = ::nisaba::file::ReadTextFile(file_name);
  if (!str_or.ok()) {
    LOG(INFO) << "Could not read \"" << file_name << "\": " << str_or.status();
    return false;
  }
  std::string str = *str_or;
  // Attempt to decode ASCII before deciding binary. Do it in this order because
  // it is much harder for a binary encoding to happen to be a valid ASCII
  // encoding than the other way around. For instance "index: 1\n" is a valid
  // (but nonsensical) binary encoding. We want to avoid printing errors for
  // valid binary encodings if the ASCII parsing fails, and so specify a no-op
  // error collector.
  google::protobuf::TextFormat::Parser parser;
  if (parser.ParseFromString(str, proto)) {
    return true;
  }
  if (proto->ParseFromString(str)) {
    return true;
  }
  // Re-parse the ASCII, just to show the diagnostics (we could also get them
  // out of the ErrorCollector but this way is easier).
  google::protobuf::TextFormat::ParseFromString(str, proto);
  LOG(INFO) << "Could not parse contents of " << file_name;
  return false;
}

absl::Status GetTextProto(const absl::string_view& filename,
                          google::protobuf::Message* proto, int flags) {
  if (flags == Defaults()) {
    if (ReadFileToProto(filename, proto)) return absl::OkStatus();
  }
  return absl::Status(
      absl::StatusCode::kInvalidArgument,
      absl::StrCat("Could not read proto from '", filename, "'."));
}

}  // namespace file
