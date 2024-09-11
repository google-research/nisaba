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

#include "benchmark/benchmark.h"

#include <string>
#include <vector>

#include "nisaba/port/file_util.h"
#include "nisaba/port/file.h"
#include "nisaba/port/file_util.h"
#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/log/check.h"
#include "absl/log/log.h"
#include "absl/strings/ascii.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/testing/testdata.pb.h"
#include "nisaba/scripts/brahmic/grammar.h"

// clang-format off

namespace nisaba {
namespace {

constexpr char kDataPath[] =
    "com_google_nisaba/nisaba/scripts/brahmic/testdata";

// Number of test strings used per language.
constexpr int TEST_STR_COUNT = 25;

static std::vector<std::string> TestStringsForTag(const std::string &tag) {
  testing::Rewrites data_pb;
  auto words = std::vector<std::string>();
  const auto tag_uppercase = absl::AsciiStrToUpper(tag);

  const std::vector<std::string> grammars({
      "iso", "nfc", "reading_norm", "visual_norm", "wellformed"});
  for (const auto &file_base : grammars) {
    if (words.size() >= TEST_STR_COUNT) break;
    const auto &data_pb_file = file::JoinPath(::testing::SrcDir(), kDataPath,
                                              file_base + ".textproto");
    EXPECT_OK(file::GetTextProto(data_pb_file, &data_pb, file::Defaults()));

    for (const testing::Rewrite &rewrite : data_pb.rewrite()) {
      if (words.size() >= TEST_STR_COUNT) break;
      auto rule_name = rewrite.rule().at(0);
      if (rule_name == tag_uppercase || rule_name == "FROM_" + tag_uppercase) {
        words.push_back(rewrite.input());
      }
    }
  }
  CHECK_GE(words.size(), TEST_STR_COUNT)
      << "Not enough test strings for '" << tag << "'";
  return words;
}

static void RunVisualNorm(const std::string &script,
                          const nisaba::brahmic::Normalizer &normalizer,
                          const std::vector<std::string> &testcases) {
  std::string output_str;
  for (const std::string &testcase : testcases) {
    CHECK_OK(normalizer.NormalizeOnly(testcase, &output_str));
  }
}

static void BM_VisualNorm(benchmark::State &state, const std::string &script) {
  const auto testcases = TestStringsForTag(script);
  nisaba::brahmic::Normalizer normalizer(script);
  ASSERT_OK(normalizer.Load());
  int count = 0;
  for (auto _ : state) {
    RunVisualNorm(script, normalizer, testcases);
    count += testcases.size();
  }
  state.SetItemsProcessed(count);
}

#define BM_VISUAL_NORM(tag)                                  \
  static void BM_VisualNorm_##tag(benchmark::State &state) { \
    BM_VisualNorm(state, #tag);                              \
  }                                                          \
  BENCHMARK(BM_VisualNorm_##tag)

// Only scripts with a reasonable number of strings in textproto files are
// listed:
BM_VISUAL_NORM(Beng);
BM_VISUAL_NORM(Deva);
BM_VISUAL_NORM(Lepc);
BM_VISUAL_NORM(Limb);
BM_VISUAL_NORM(Mlym);
BM_VISUAL_NORM(Mtei);
BM_VISUAL_NORM(Sylo);
BM_VISUAL_NORM(Thaa);

// Not enough test strings for the following scripts:
// BM_VISUAL_NORM(Bugi);
// BM_VISUAL_NORM(Gujr);
// BM_VISUAL_NORM(Guru);
// BM_VISUAL_NORM(Knda);
// BM_VISUAL_NORM(Newa);
// BM_VISUAL_NORM(Orya);
// BM_VISUAL_NORM(Sinh);
// BM_VISUAL_NORM(Takr);
// BM_VISUAL_NORM(Taml);
// BM_VISUAL_NORM(Telu);
// BM_VISUAL_NORM(Tglg);
// BM_VISUAL_NORM(Tirh);

}  // namespace
}  // namespace nisaba

// Run the benchmark
BENCHMARK_MAIN();
