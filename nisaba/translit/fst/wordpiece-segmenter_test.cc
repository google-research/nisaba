// Copyright 2025 Nisaba Authors.
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

#include "nisaba/translit/fst/wordpiece-segmenter.h"

#include <memory>
#include <string>
#include <vector>

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "nisaba/port/test_utils.h"

namespace nisaba {
namespace translit {
namespace fst {
namespace {

constexpr char kTestDataDir[] =
    "com_google_nisaba/nisaba/translit/fst/testdata";
constexpr char kEarnestModelTextFile[] = "wp_earnest.50.model.txt";

class WordpieceSegmenterTest : public ::testing::Test {
 protected:
  void SetUp() override {
    wordpiece_model_file_ =
        testing::TestFilePath(kTestDataDir, kEarnestModelTextFile);
    word_initial_prefix_ = "";  // Empty string prompts default at initializer.
  }

  std::string wordpiece_model_file_;
  std::string word_initial_prefix_;
};

TEST_F(WordpieceSegmenterTest, InitModelTest) {
  std::unique_ptr<WordpieceSegmenter> wpm;
  wpm = std::make_unique<WordpieceSegmenter>(word_initial_prefix_);
  ASSERT_OK(wpm->InitWordpieces(wordpiece_model_file_));
}

TEST_F(WordpieceSegmenterTest, SingleWordInVocabTest) {
  std::unique_ptr<WordpieceSegmenter> wpm;
  wpm = std::make_unique<WordpieceSegmenter>(word_initial_prefix_);
  ASSERT_OK(wpm->InitWordpieces(wordpiece_model_file_));
  const std::string input_string = "HELLO";
  const std::vector<std::string> expected_output{"▁", "HE", "LL", "O"};
  const auto wp_status = wpm->GetWordpieces(input_string);
  ASSERT_OK(wp_status);
  const auto &actual_output = wp_status.value();
  ASSERT_EQ(expected_output.size(), actual_output.size());
  for (int i = 0; i < actual_output.size(); ++i) {
    ASSERT_EQ(expected_output[i], actual_output[i]);
  }
}

TEST_F(WordpieceSegmenterTest, MultiWordInVocabTest) {
  std::unique_ptr<WordpieceSegmenter> wpm;
  wpm = std::make_unique<WordpieceSegmenter>(word_initial_prefix_);
  ASSERT_OK(wpm->InitWordpieces(wordpiece_model_file_));
  const std::string input_string = "HELLO WORLD";
  const std::vector<std::string> expected_output{"▁", "HE", "LL", "O", "▁W",
                                                 "O", "R",  "L",  "D"};
  const auto wp_status = wpm->GetWordpieces(input_string);
  ASSERT_OK(wp_status);
  const auto &actual_output = wp_status.value();
  ASSERT_EQ(expected_output.size(), actual_output.size());
  for (int i = 0; i < actual_output.size(); ++i) {
    ASSERT_EQ(expected_output[i], actual_output[i]);
  }
}

TEST_F(WordpieceSegmenterTest, MultiWordOutOfVocabTest) {
  std::unique_ptr<WordpieceSegmenter> wpm;
  wpm = std::make_unique<WordpieceSegmenter>(word_initial_prefix_);
  ASSERT_OK(wpm->InitWordpieces(wordpiece_model_file_));
  const std::string input_string = "HeLLO WORLD";
  const std::vector<std::string> expected_output{"▁",  "H", "e", "LL", "O",
                                                 "▁W", "O", "R", "L",  "D"};
  const auto wp_status = wpm->GetWordpieces(input_string);
  ASSERT_OK(wp_status);
  const auto &actual_output = wp_status.value();
  ASSERT_EQ(expected_output.size(), actual_output.size());
  for (int i = 0; i < actual_output.size(); ++i) {
    ASSERT_EQ(expected_output[i], actual_output[i]);
  }
}

}  // namespace
}  // namespace fst
}  // namespace translit
}  // namespace nisaba
