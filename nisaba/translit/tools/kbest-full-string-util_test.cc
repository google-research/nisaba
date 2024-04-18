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

#include "nisaba/translit/tools/kbest-full-string-util.h"

#include <cmath>
#include <filesystem>  // NOLINT
#include <fstream>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "gtest/gtest.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"

namespace nisaba {
namespace translit {
namespace tools {
namespace {

constexpr float kFloatDelta = 0.00001;  // Delta for float comparisons.

class KbestFullStringUtilTest : public ::testing::Test {
 protected:
  // Creates data for testing ensembling methods.
  void SetUpEnsemblingData() {
    // Example 1 ensembling: three input tokens w/diffs on middle token.
    ensemble_input_lengths_.push_back(3);
    std::vector<std::pair<std::string, double>> cands_example0;
    cands_example0.push_back(std::make_pair("ABC DEF XYZ", -log(0.7)));
    cands_example0.push_back(std::make_pair("ABC DEE XYZ", -log(0.3)));
    cands_example0.push_back(std::make_pair("ABC EEE XYZ", -log(0.6)));
    cands_example0.push_back(std::make_pair("ABC DEF XYZ", -log(0.4)));
    ensemble_cands_.push_back(cands_example0);
    // Example 1 ensembling: DEF occurs twice, so sum the probabilities. Total
    // probability mass is 2.0 (i.e., two systems), so divides probabilities by
    // 2 to normalize.
    std::vector<std::pair<std::string, double>> expected_outputs_example0;
    expected_outputs_example0.push_back(
        std::make_pair("ABC DEF XYZ", -log(0.55)));
    expected_outputs_example0.push_back(
        std::make_pair("ABC EEE XYZ", -log(0.3)));
    expected_outputs_example0.push_back(
        std::make_pair("ABC DEE XYZ", -log(0.15)));
    ensemble_expected_outputs_.push_back(expected_outputs_example0);

    // Example 2 ensembling: three input tokens, some mismatch on output length.
    ensemble_input_lengths_.push_back(3);
    std::vector<std::pair<std::string, double>> cands_example1;
    cands_example1.push_back(std::make_pair("ABC DEF XYZ", -log(0.6)));
    cands_example1.push_back(std::make_pair("ABC DEE XYZ", -log(0.4)));
    cands_example1.push_back(std::make_pair("ABC DEE XYZ", -log(0.6)));
    cands_example1.push_back(std::make_pair("ABC DE EE XYZ", -log(0.4)));
    ensemble_cands_.push_back(cands_example1);
    // Example 2 ensembling: DEE occurs twice, so sum the probabilities.
    // Candidate with 4 output tokens is discarded. Total probability mass
    // is 1.6 (i.e., two systems, but 0.4 from the second system not included),
    // so divides probabilities by 1.6 to normalize.
    std::vector<std::pair<std::string, double>> expected_outputs_example1;
    expected_outputs_example1.push_back(
        std::make_pair("ABC DEE XYZ", -log(0.625)));
    expected_outputs_example1.push_back(
        std::make_pair("ABC DEF XYZ", -log(0.375)));
    ensemble_expected_outputs_.push_back(expected_outputs_example1);
  }

  // Creates data for testing k-best extraction methods.
  void SetUpExtractionData() {
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 0, "abc", "ABC", -log(0.7)), "\t"));
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 0, "abc", "ABK", -log(0.3)), "\t"));
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 1, "def", "DEF", -log(0.6)), "\t"));
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 1, "def", "DEE", -log(0.4)), "\t"));
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 2, "xyz", "XYZ", -log(0.8)), "\t"));
    extractor_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, 2, "xyz", "ZYX", -log(0.2)), "\t"));
    // The three best candidates include the one with the highest probability in
    // each position, and with the two highest probability second place items at
    // different positions (second and first). The sum of these candidates is
    // 0.704, which is used to normalize.
    std::vector<std::pair<std::string, double>> expected_kbests;
    expected_kbests.push_back(
        std::make_pair("ABC DEF XYZ", -log(0.336 / 0.704)));
    expected_kbests.push_back(
        std::make_pair("ABC DEE XYZ", -log(0.224 / 0.704)));
    expected_kbests.push_back(
        std::make_pair("ABK DEF XYZ", -log(0.144 / 0.704)));
    expected_kbests_.push_back(expected_kbests);
  }

  // Creates data for testing k-best rejoiner methods.
  void SetUpRejoinerData() {
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, "MY LEFT FOOT", -log(0.7)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(0, "MY LEFT FOOD", -log(0.3)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(1, "ABC DEF", -log(0.42)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(1, "ABC DEE", -log(0.28)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(1, "ABK DEF", -log(0.18)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(1, "ABK DEE", -log(0.12)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(2, "XYZ", -log(0.8)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(2, "ZYX", -log(0.2)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(3, "LAST ONE", -log(0.6)), "\t"));
    rejoiner_input_lines_.push_back(
        absl::StrJoin(std::make_tuple(3, "LAST WON", -log(0.4)), "\t"));
    // Write these input lines to file to test file-based initialization.
    const std::filesystem::path tmp_dir =
        std::filesystem::temp_directory_path();
    std::filesystem::path file_path = tmp_dir / "rejoiner_input.txt";
    rejoiner_input_file_ = file_path.string();
    std::ofstream input_lines_file(rejoiner_input_file_);
    EXPECT_TRUE(input_lines_file.good())
        << "Failed to open: " << rejoiner_input_file_;
    for (int i = 0; i < rejoiner_input_lines_.size(); ++i) {
      input_lines_file << absl::StrCat(rejoiner_input_lines_[i], "\n");
    }
    EXPECT_TRUE(input_lines_file.good())
        << "Failed to write to: " << rejoiner_input_file_;
    output_indices_.push_back(0);
    output_indices_.push_back(1);
    output_indices_.push_back(1);
    output_indices_.push_back(2);
    // Write these output indices to file to test file-based initialization.
    file_path = tmp_dir / "rejoiner_indices.txt";
    rejoiner_indices_file_ = file_path.string();
    std::ofstream indices_lines_file(rejoiner_indices_file_);
    EXPECT_TRUE(indices_lines_file.good())
        << "Failed to open: " << rejoiner_indices_file_;
    for (int i = 0; i < output_indices_.size(); ++i) {
      indices_lines_file << absl::StrCat(output_indices_[i], "\n");
    }
    EXPECT_TRUE(indices_lines_file.good())
        << "Failed to write to: " << rejoiner_indices_file_;
    std::vector<std::pair<std::string, double>> expected_output0;
    expected_output0.push_back(std::make_pair("MY LEFT FOOT", -log(0.7)));
    expected_output0.push_back(std::make_pair("MY LEFT FOOD", -log(0.3)));
    expected_rejoined_lists_.push_back(expected_output0);
    // Where rejoining happens, probabilities are multiplied, no softmax
    // normalization over the list is applied.
    std::vector<std::pair<std::string, double>> expected_output1;
    expected_output1.push_back(std::make_pair("ABC DEF XYZ", -log(0.42 * 0.8)));
    expected_output1.push_back(std::make_pair("ABC DEE XYZ", -log(0.28 * 0.8)));
    expected_rejoined_lists_.push_back(expected_output1);
    std::vector<std::pair<std::string, double>> expected_output2;
    expected_output2.push_back(std::make_pair("LAST ONE", -log(0.6)));
    expected_output2.push_back(std::make_pair("LAST WON", -log(0.4)));
    expected_rejoined_lists_.push_back(expected_output2);
  }

  void SetUp() override {
    SetUpEnsemblingData();
    SetUpExtractionData();
    SetUpRejoinerData();
  }

  // Kbest rejoiner file names.
  std::string rejoiner_input_file_;
  std::string rejoiner_indices_file_;

  // Kbest rejoiner data.
  std::vector<std::string> rejoiner_input_lines_;
  std::vector<int> output_indices_;
  std::vector<std::vector<std::pair<std::string, double>>>
      expected_rejoined_lists_;

  // Kbest extraction data.
  std::vector<std::string> extractor_input_lines_;
  std::vector<std::vector<std::pair<std::string, double>>> expected_kbests_;

  // Ensembling data.
  std::vector<std::vector<std::pair<std::string, double>>> ensemble_cands_;
  std::vector<std::vector<std::pair<std::string, double>>>
      ensemble_expected_outputs_;
  std::vector<int> ensemble_input_lengths_;
};

TEST_F(KbestFullStringUtilTest, InitEnsembleTest) {
  std::vector<std::pair<std::string, double>> empty_cands;
  EnsembleFullString input_ensemble(empty_cands);
  EXPECT_TRUE(input_ensemble.GetOutputs(/*kbest=*/10).empty());
}

TEST_F(KbestFullStringUtilTest, EnsembleTest) {
  for (int i = 0; i < ensemble_cands_.size(); ++i) {
    EnsembleFullString input_ensemble(ensemble_cands_[i]);
    input_ensemble.RunEnsemble(ensemble_input_lengths_[i]);
    const auto kbest_outputs = input_ensemble.GetOutputs(
        /*kbest=*/ensemble_expected_outputs_[i].size());
    EXPECT_EQ(kbest_outputs.size(), ensemble_expected_outputs_[i].size());
    for (int j = 0; j < ensemble_expected_outputs_[i].size(); ++j) {
      EXPECT_EQ(kbest_outputs[j].first, ensemble_expected_outputs_[i][j].first);
      EXPECT_NEAR(kbest_outputs[j].second,
                  ensemble_expected_outputs_[i][j].second, kFloatDelta);
    }
  }
}

TEST_F(KbestFullStringUtilTest, InitExtractionTest) {
  std::vector<std::string> empty_lines;
  KbestExtractor kbest_extractor(empty_lines);
  EXPECT_TRUE(kbest_extractor.GetBests(/*kbest=*/10).empty());
}

TEST_F(KbestFullStringUtilTest, ExtractionTest) {
  KbestExtractor kbest_extractor(extractor_input_lines_);
  const auto kbest_outputs = kbest_extractor.GetBests(/*kbest=*/3);
  EXPECT_EQ(kbest_outputs.size(), expected_kbests_.size());
  for (int i = 0; i < expected_kbests_.size(); ++i) {
    EXPECT_EQ(kbest_outputs[i].size(), expected_kbests_[i].size());
    for (int j = 0; j < expected_kbests_[i].size(); ++j) {
      EXPECT_EQ(kbest_outputs[i][j].first, expected_kbests_[i][j].first);
      EXPECT_NEAR(kbest_outputs[i][j].second,
                  expected_kbests_[i][j].second, kFloatDelta);
    }
  }
}

TEST_F(KbestFullStringUtilTest, InitRejoinerTest) {
  std::vector<std::string> empty_lines;
  std::vector<int> empty_indices;
  KbestRejoiner kbest_rejoiner(empty_lines, empty_indices, /*kbest=*/10);
  EXPECT_EQ(kbest_rejoiner.NumKbestLists(), 0);
}

TEST_F(KbestFullStringUtilTest, RejoinerTest) {
  KbestRejoiner kbest_rejoiner(rejoiner_input_lines_, output_indices_,
                               /*kbest=*/2);
  EXPECT_EQ(kbest_rejoiner.NumKbestLists(), expected_rejoined_lists_.size());
  for (int i = 0; i < expected_rejoined_lists_.size(); ++i) {
    const auto kbest_list = kbest_rejoiner.GetRejoinedList(i);
    for (int j = 0; j < expected_rejoined_lists_[i].size(); ++j) {
      EXPECT_EQ(kbest_list[j].first, expected_rejoined_lists_[i][j].first);
      EXPECT_NEAR(kbest_list[j].second, expected_rejoined_lists_[i][j].second,
                  kFloatDelta);
    }
  }
}

TEST_F(KbestFullStringUtilTest, RejoinerFileTest) {
  KbestRejoiner kbest_rejoiner(rejoiner_input_file_, rejoiner_indices_file_,
                               /*kbest=*/2);
  EXPECT_EQ(kbest_rejoiner.NumKbestLists(), expected_rejoined_lists_.size());
  for (int i = 0; i < expected_rejoined_lists_.size(); ++i) {
    const auto kbest_list = kbest_rejoiner.GetRejoinedList(i);
    for (int j = 0; j < expected_rejoined_lists_[i].size(); ++j) {
      EXPECT_EQ(kbest_list[j].first, expected_rejoined_lists_[i][j].first);
      EXPECT_NEAR(kbest_list[j].second, expected_rejoined_lists_[i][j].second,
                  kFloatDelta);
    }
  }
}

}  // namespace
}  // namespace tools
}  // namespace translit
}  // namespace nisaba
