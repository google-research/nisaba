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

// Simple unit test for the decoder runner.

// Please note, this test does not verify the correctness of transliterations,
// it just checks that the overall API behaves and is sane.

#include "nisaba/translit/fst/pairlm_decoder_runner.h"

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/strings/string_view.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/test_utils.h"
#include "nisaba/translit/fst/pairlm_decoder_options.pb.h"

namespace nisaba {
namespace translit {
namespace fst {
namespace {

constexpr char kTestDataDir[] =
    "com_google_nisaba/nisaba/translit/fst/testdata";
constexpr char kHindiModelFileFsa[] =
    "hi.translit.sampled.train.visnorm.align1.WB15.mod.fst";
constexpr char kHindiModelFileFst[] =
    "hi.translit.sampled.train.visnorm.align1.WB15.mod.trans.fst";
constexpr char kHindiTestFile[] = "udhr_hi.txt";
constexpr char kLatinOutputFile[] = "latin.txt";

// Number of parallel workers for reading the input lines.
constexpr int kNumParallelWorkers = 2;

// Returns full file path under the test data.
std::string FullFilePath(absl::string_view file_name) {
  return testing::TestFilePath(kTestDataDir, file_name);
}

// Sets up the configuration.
PairLMDecoderOptions MakeOptions(absl::string_view model_file_name,
                                 bool is_transducer) {
  PairLMDecoderOptions options;
  options.set_pairlm_file(FullFilePath(model_file_name));
  options.set_pairlm_is_transducer(is_transducer);
  return options;
}

// Runs the decoder single-threaded. Please note, internally, the decoder may
// perform its own internal parallelizations on the token level.
void RunSequentialDecoding(const PairLMDecoderOptions &options,
                           absl::string_view test_file_name,
                           int num_workers = 1) {
  const std::string &input_file = FullFilePath(test_file_name);
  const std::string &output_file = file::TempFilePath(kLatinOutputFile);
  EXPECT_OK(RunPairLMDecoder(options,
                             /* k_best= */1, num_workers,
                             input_file, output_file))
      << "Failed to process " << input_file;
}

TEST(PairLMDecoderRunnerTest, CheckHindiAutomatonSequential) {
  PairLMDecoderOptions options = MakeOptions(kHindiModelFileFsa, false);
  options.set_max_parallel_tokens(1);
  RunSequentialDecoding(options, kHindiTestFile);
}

TEST(PairLMDecoderRunnerTest, CheckHindiTransducerSequential) {
  PairLMDecoderOptions options = MakeOptions(kHindiModelFileFst, true);
  options.set_max_parallel_tokens(1);
  RunSequentialDecoding(options, kHindiTestFile);
}

TEST(PairLMDecoderRunnerTest, CheckHindiAutomatonParallel) {
  const PairLMDecoderOptions options = MakeOptions(kHindiModelFileFsa, false);
  RunSequentialDecoding(options, kHindiTestFile, kNumParallelWorkers);
}

TEST(PairLMDecoderRunnerTest, CheckHindiTransducerParallel) {
  const PairLMDecoderOptions options = MakeOptions(kHindiModelFileFst, true);
  RunSequentialDecoding(options, kHindiTestFile, kNumParallelWorkers);
}

}  // namespace
}  // namespace fst
}  // namespace translit
}  // namespace nisaba
