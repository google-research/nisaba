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

#include "nisaba/translit/tools/calculate_error_rate.h"

#include <filesystem>
#include <fstream>
#include <string>

#include "gtest/gtest.h"
#include "absl/strings/str_cat.h"

namespace nisaba {
namespace translit {
namespace tools {
namespace {

constexpr float kFloatDelta = 0.00001;  // Delta for float comparisons.

class MultiRefErrorRateTest : public ::testing::Test {
 protected:
  // Creates first file for testing error rate.
  void CreateFileOne() {
    std::ofstream output_file(file_one_);
    ASSERT_TRUE(output_file.good()) << "Failed to open: " << file_one_;
    output_file << absl::StrCat(0, "\t", "aabac", "\t", 1, "\n");
    output_file << absl::StrCat(0, "\t", "aabab", "\t", 2, "\n");
    output_file << absl::StrCat(1, "\t", "babac", "\t", 3, "\n");
    output_file << absl::StrCat(1, "\t", "babab", "\n");
    output_file << absl::StrCat(2, "\t", "bcdef", "\t", 2, "\n");
    ASSERT_TRUE(output_file.good()) << "Failed to write to " << file_one_;
  }

  // Creates second file for testing error rate.
  void CreateFileTwo() {
    std::ofstream output_file(file_two_);
    ASSERT_TRUE(output_file.good()) << "Failed to open: " << file_two_;
    output_file << absl::StrCat(0, "\t", "abac", "\t", 1, "\n");
    output_file << absl::StrCat(0, "\t", "aabb", "\t", 2, "\n");
    output_file << absl::StrCat(1, "\t", "bb", "\t", 3, "\n");
    output_file << absl::StrCat(1, "\t", "bbcbbc", "\t", 2, "\n");
    output_file << absl::StrCat(1, "\t", "babab", "\t", 5, "\n");
    output_file << absl::StrCat(2, "\t", "z", "\n");
    ASSERT_TRUE(output_file.good()) << "Failed to write to " << file_two_;
  }
  void SetUp() override {
    // Setup the input files.
    const std::filesystem::path tmp_dir =
        std::filesystem::temp_directory_path();
    std::filesystem::path file_path = tmp_dir / "file_one.txt";
    file_one_ = file_path.string();
    CreateFileOne();

    file_path = tmp_dir / "file_two.txt";
    file_two_ = file_path.string();
    CreateFileTwo();
  }

  std::string file_one_;  // File name for first k-best output.
  std::string file_two_;  // File name for second k-best output.
};

// TODO: create test of GetTokenizedString to test bad indices.
// Verifies minimum error rate calculation in both directions.
TEST_F(MultiRefErrorRateTest, CorrectMinErrorRates) {
  // Initializing calculator for use with file_one_ as reference.
  nisaba::translit::tools::MultiRefErrorRate multi_ref_calc_one(
      /*is_split_chars=*/true);
  multi_ref_calc_one.CalculateErrorRate(/*reffile=*/file_one_,
                                        /*testfile=*/file_two_,
                                        /*pairwise_edits=*/false);
  // If file two is the test file, then the minimum cost hypotheses in the
  // k-best list are "abac", "bbcbbc" and "z" for items 0, 1 and 2 respectively.
  // The closest matching reference to "abac" for item 0 is "aabac" which
  // results in reference length 5 and 1 deletion. The closest matching
  // reference to "bbcbbc" for item 1 is "babac" which results in reference
  // length 5 and 2 substitutions + 1 insertion. For item 2 there are 4
  // deletions and a substitution for reference length 5. That yields a total
  // reference length of 15 and 9 edits for an error rate of 9/15.
  double CER_one = multi_ref_calc_one.CalcErrorRate();
  ASSERT_NEAR(CER_one, static_cast<double>(9.0) / static_cast<double>(15.0),
              kFloatDelta);

  // Initializing calculator for use with file_two_ as reference.
  nisaba::translit::tools::MultiRefErrorRate multi_ref_calc_two(
      /*is_split_chars=*/true);
  multi_ref_calc_two.CalculateErrorRate(/*reffile=*/file_two_,
                                        /*testfile=*/file_one_,
                                        /*pairwise_edits=*/false);
  // If file one is the test file, then the minimum cost hypotheses in the
  // k-best list are "aabac", "babab" and "bcdef" for items 0, 1 and 2
  // respectively. "babab" is the min cost hypothesis because it does not have
  // a cost column, which is taken by convention to be free cost (0.0) hence
  // minimum from among the alternatives. The closest matching reference to
  // "aabac" for item 0 is "abac" which results in reference length 4 and 1
  // insertion. The closest matching reference to "babab" for item 1 is "babab"
  // which results in reference length 5 and no edits. For item 2 there are 4
  // insertions and a substitution for reference length 1. That yields a total
  // reference length of 10 and 6 edits for an error rate of 0.6.
  double CER_two = multi_ref_calc_two.CalcErrorRate();
  ASSERT_NEAR(CER_two, static_cast<double>(0.6), kFloatDelta);
}

}  // namespace
}  // namespace tools
}  // namespace translit
}  // namespace nisaba
