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

#include <filesystem>

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"

namespace nisaba {
namespace file {
namespace {

const char kFilename[] = "hello.txt";

TEST(File_UtilTest, CheckTempFilePath) {
  const std::string path = TempFilePath(kFilename);
  EXPECT_FALSE(path.empty());
}

TEST(File_UtilTest, CheckWriteTempTextFile) {
  const auto write_status = WriteTempTextFile(kFilename, "hello");
  EXPECT_OK(write_status.status());
  const std::string path = write_status.value();
  EXPECT_FALSE(path.empty());
  EXPECT_TRUE(std::filesystem::remove(path));
}

TEST(File_UtilTest, CheckReadBinaryFile) {
  const auto write_status = WriteTempTextFile(kFilename, "hello");
  EXPECT_OK(write_status.status());
  auto read_status = ReadBinaryFile(write_status.value());
  EXPECT_OK(read_status.status());
  const std::string contents = read_status.value();
  EXPECT_EQ("hello", contents);
  read_status = ReadBinaryFile("invalid file");
  EXPECT_FALSE(read_status.ok());
}

}  // namespace
}  // namespace file
}  // namespace nisaba
