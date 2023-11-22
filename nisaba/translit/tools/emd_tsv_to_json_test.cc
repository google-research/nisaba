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

#include <cmath>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

#include "gtest/gtest.h"
#include "absl/log/check.h"
#include "absl/strings/str_cat.h"
#include "include//nlohmann/json.hpp"
#include "nisaba/port/file_util.h"
#include "nisaba/port/utf8_util.h"
#include "nisaba/translit/tools/calculate_error_rate.h"

namespace nisaba {
namespace translit {
namespace tools {
namespace {

constexpr float kFloatDelta = 0.00001;  // Delta for float comparisons.

class EmdTsvToJsonTest : public ::testing::Test {
 protected:
  // Returns number of unicode codepoints.
  int string_length(const std::string &str) {
    const std::vector<std::string> tokenized_string = utf8::StrSplitByChar(str);
    return tokenized_string.size();
  }

  // Creates first file for testing tsv2json functionality (reference).
  // Also adds reference string lengths and probabilities for later testing.
  void CreateFileOne() {
    std::ofstream output_file(reference_);
    ASSERT_TRUE(output_file.good()) << "Failed to open: " << reference_;
    // References for first example.
    const std::string ref_00 = "sieberling";
    int count_00 = 7;
    const std::string ref_01 = "zeeberlin";
    int count_01 = 3;
    output_file << absl::StrCat(0, "\t", ref_00, "\t", count_00, "\n");
    output_file << absl::StrCat(0, "\t", ref_01, "\t", count_01, "\n");
    // Add reference lengths for first example, padded by sys output zeros.
    lengths_.push_back({0, 0, string_length(ref_00), string_length(ref_01)});
    // Add reference probabilities for 1st example, padded by sys output zeros.
    double denom = static_cast<double>(count_00 + count_01);
    double prob_00 = static_cast<double>(count_00) / denom;
    double prob_01 = static_cast<double>(count_01) / denom;
    probs2_.push_back({0, 0, prob_00, prob_01});
    // References for second example.
    const std::string ref_10 = "UFOshipt";
    int count_10 = 6;
    const std::string ref_11 = "youeffOshp";
    int count_11 = 4;
    output_file << absl::StrCat(1, "\t", ref_10, "\t", count_10, "\n");
    output_file << absl::StrCat(1, "\t", ref_11, "\t", count_11, "\n");
    ASSERT_TRUE(output_file.good()) << "Failed to write to " << reference_;
    // Add reference lengths for first example, padded by sys output zeros.
    lengths_.push_back(
        {0, 0, 0, 0, string_length(ref_10), string_length(ref_11)});
    // Add reference probabilities for 2nd example, padded by sys output zeros.
    denom = static_cast<double>(count_10 + count_11);
    double prob_10 = static_cast<double>(count_10) / denom;
    double prob_11 = static_cast<double>(count_11) / denom;
    probs2_.push_back({0, 0, 0, 0, prob_10, prob_11});
  }

  // Creates second file for testing tsv2json functionality (system output).
  // Also adds system output probabilities for later testing.
  void CreateFileTwo() {
    std::ofstream output_file(sys_output_);
    ASSERT_TRUE(output_file.good()) << "Failed to open: " << sys_output_;
    // System outputs for first example.
    double prob_00 = 0.6;
    double prob_01 = 0.4;
    output_file << absl::StrCat(0, "\t", "seeverling", "\t", -log(prob_00),
                                "\n");
    output_file << absl::StrCat(0, "\t", "siefelin", "\t", -log(prob_01), "\n");
   // Add sys output probabilities for 1st example, padded by reference zeros.
    probs1_.push_back({prob_00, prob_01, 0, 0});
    // System outputs for second example.
    double prob_10 = 0.4;
    double prob_11 = 0.3;
    double prob_12 = 0.2;
    double prob_13 = 0.1;
    output_file << absl::StrCat(1, "\t", "UFOship", "\t", -log(prob_10), "\n");
    output_file << absl::StrCat(1, "\t", "youFOsheep", "\t", -log(prob_11),
                                "\n");
    output_file << absl::StrCat(1, "\t", "UFOsheep", "\t", -log(prob_12), "\n");
    output_file << absl::StrCat(1, "\t", "youeffohship", "\t", -log(prob_13),
                                "\n");
    ASSERT_TRUE(output_file.good()) << "Failed to write to " << sys_output_;
    // Add sys output probabilities for 2nd example, padded by reference zeros.
    probs1_.push_back({prob_10, prob_11, prob_12, prob_13, 0, 0});
  }

  void CreateDistances() {
    // Distances (Levenshtein) for first example.
    // Distances between references and between system outputs are 0 (unused).
    // Distance between ref "sieberling" and sys "seeverling".
    int d_00_00 = 2;
    // Distance between ref "sieberling" and sys "siefelin".
    int d_00_01 = 3;
    // Distance between ref "zeeberlin" and sys "seeverling".
    int d_01_00 = 3;
    // Distance between ref "zeeberlin" and sys "siefelin".
    int d_01_01 = 4;
    distances_.push_back({0, 0, d_00_00, d_01_00});
    distances_.push_back({0, 0, d_00_01, d_01_01});
    distances_.push_back({d_00_00, d_00_01, 0, 0});
    distances_.push_back({d_01_00, d_01_01, 0, 0});
    // Distances (Levenshtein) for second example.
    // Distance between ref "UFOshipt" and sys "UFOship".
    int d_10_10 = 1;
    // Distance between ref "UFOshipt" and sys "youFOsheep".
    int d_10_11 = 6;
    // Distance between ref "UFOshipt" and sys "UFOsheep".
    int d_10_12 = 3;
    // Distance between ref "UFOshipt" and sys "youeffohship".
    int d_10_13 = 9;
    // Distance between ref "youeffOshp" and sys "UFOship".
    int d_11_10 = 7;
    // Distance between ref "youeffOshp" and sys "youFOsheep".
    int d_11_11 = 5;
    // Distance between ref "youeffOshp" and sys "UFOsheep".
    int d_11_12 = 8;
    // Distance between ref "youeffOshp" and sys "youeffohship".
    int d_11_13 = 3;
    distances_.push_back({0, 0, 0, 0, d_10_10, d_11_10});
    distances_.push_back({0, 0, 0, 0, d_10_11, d_11_11});
    distances_.push_back({0, 0, 0, 0, d_10_12, d_11_12});
    distances_.push_back({0, 0, 0, 0, d_10_13, d_11_13});
    distances_.push_back({d_10_10, d_10_11, d_10_12, d_10_13, 0, 0});
    distances_.push_back({d_11_10, d_11_11, d_11_12, d_11_13, 0, 0});
  }

  void SetUp() override {
    // Setup the input files.
    const std::filesystem::path tmp_dir =
        std::filesystem::temp_directory_path();
    std::filesystem::path file_path = tmp_dir / "file_one.txt";
    reference_ = file_path.string();
    CreateFileOne();

    file_path = tmp_dir / "file_two.txt";
    sys_output_ = file_path.string();
    CreateFileTwo();
    CreateDistances();
  }

  std::string reference_;   // File name for reference file.
  std::string sys_output_;  // File name for system output file.
  std::vector<std::vector<int>> distances_;  // String distances.
  std::vector<std::vector<int>> lengths_;  // Reference string lengths.
  std::vector<std::vector<double>> probs1_;  // System output probabilities.
  std::vector<std::vector<double>> probs2_;  // Reference probabilities.
};

TEST_F(EmdTsvToJsonTest, CorrectJsonDistancesLengthsAndProbs) {
  nisaba::translit::tools::MultiRefErrorRate emd_tsv2json(
      /*is_split_chars=*/true);
  emd_tsv2json.CalculateErrorRate(reference_, sys_output_,
                                  /*pairwise_edits=*/true);
  const std::filesystem::path tmp_dir = std::filesystem::temp_directory_path();
  std::filesystem::path file_path = tmp_dir / "test.json";
  const std::string json_file = file_path.string();
  emd_tsv2json.Write(json_file, /*pairwise_edits=*/true);
  int didx = 0;
  int idx = 0;
  const auto &input_lines_status = file::ReadLines(json_file, kMaxLine);
  QCHECK(input_lines_status.ok()) << "Failed to read " << json_file;
  const std::vector<std::string> input_lines = input_lines_status.value();
  for (const std::string &str : input_lines) {
    ::nlohmann::json parsed_json = ::nlohmann::json::parse(str);
    for (int i = 0; i < parsed_json["D"].size(); ++i) {
      for (int j = 0; j < parsed_json["D"].at(i).size(); ++j) {
        auto value = parsed_json["D"].at(i).at(j).template get<double>();
        ASSERT_EQ(std::lround(value), distances_[i + didx][j]);
      }
    }
    didx += parsed_json["D"].size();
    for (int i = 0; i < parsed_json["L"].size(); ++i) {
      auto value = parsed_json["L"].at(i).template get<double>();
      ASSERT_EQ(std::lround(value), lengths_[idx][i]);
    }
    for (int i = 0; i < parsed_json["p1"].size(); ++i) {
      auto value = parsed_json["p1"].at(i).template get<double>();
      ASSERT_NEAR(value, probs1_[idx][i], kFloatDelta);
    }
    for (int i = 0; i < parsed_json["p2"].size(); ++i) {
      auto value = parsed_json["p2"].at(i).template get<double>();
      ASSERT_NEAR(value, probs2_[idx][i], kFloatDelta);
    }
    ++idx;
  }
}

}  // namespace
}  // namespace tools
}  // namespace translit
}  // namespace nisaba
