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

#ifndef NISABA_TRANSLIT_TOOLS_CALCULATE_ERROR_RATE_H_
#define NISABA_TRANSLIT_TOOLS_CALCULATE_ERROR_RATE_H_

#include <cstdint>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/strings/str_cat.h"
#include "absl/types/span.h"

namespace nisaba {
namespace translit {
namespace tools {

static const int kMaxLine = 51200;

// Edit distance components (int) storage.
struct EditDistanceInt {
  int reference_length = 0;
  int substitutions = 0;
  int insertions = 0;
  int deletions = 0;

  int Edits() const { return substitutions + insertions + deletions; }
};

// Edit distance components (double) storage.
struct EditDistanceDouble {
  double reference_length = 0.;
  double substitutions = 0.;
  double insertions = 0.;
  double deletions = 0.;

  EditDistanceDouble() {}

  explicit EditDistanceDouble(const EditDistanceInt &x)
      : reference_length(x.reference_length),
        substitutions(x.substitutions),
        insertions(x.insertions),
        deletions(x.deletions) {}

  EditDistanceDouble &operator=(const EditDistanceInt &x) {
    this->reference_length = x.reference_length;
    this->substitutions = x.substitutions;
    this->insertions = x.insertions;
    this->deletions = x.deletions;
    return *this;
  }

  EditDistanceDouble &operator+=(const EditDistanceInt &x) {
    this->reference_length += x.reference_length;
    this->substitutions += x.substitutions;
    this->insertions += x.insertions;
    this->deletions += x.deletions;
    return *this;
  }

  EditDistanceDouble &operator+=(const EditDistanceDouble &x) {
    this->reference_length += x.reference_length;
    this->substitutions += x.substitutions;
    this->insertions += x.insertions;
    this->deletions += x.deletions;
    return *this;
  }

  void Normalize(double norm) {
    reference_length /= norm;
    substitutions /= norm;
    insertions /= norm;
    deletions /= norm;
  }

  double Edits() const { return substitutions + insertions + deletions; }
  double ErrorRate() const { return Edits() / reference_length; }

  std::string ToString() const {
    return absl::StrCat("reference length=", reference_length,
                        " substitutions=", substitutions,
                        " deletions=", deletions, " insertions=", insertions);
  }
};

// Class for calculating error rates possibly from multiple references.
class MultiRefErrorRate {
 public:
  MultiRefErrorRate() = default;

  explicit MultiRefErrorRate(bool is_split_chars)
      : is_split_chars_(is_split_chars) {
    output_syms_.AddSymbol("<epsilon>");
  }

  // Calculates multi reference error rate for given test file. If pairwise_edit
  // is set to true, provides pairwise edits between all reference and test
  // outputs for the same input.
  void CalculateErrorRate(absl::string_view reffile, absl::string_view testfile,
                          bool pairwise_edits);

  // Writes results to output file.
  void Write(absl::string_view ofile, bool pairwise_edits);

  // Calculates error rate and optionally writes to provide file pointer.
  double CalcErrorRate();

 private:
  // Reads in TSV input file, either reference or test file.
  // Column 1 should be the example index, starting from 0.
  // Column 2 should be the reference/test output string.
  // Optional column 3 is the value associated with the output.
  // For the reference file this is a count; for test a -log prob.
  void ReadInputs(absl::string_view input_file, bool is_reference);

  // Returns tokenized string associated with idx and k-th item from test_input_
  // if is_test_item is true, otherwise references_.
  std::vector<std::string> GetTokenizedString(int idx, int k,
                                              bool is_test_item) const;

  // Scans through data set and calculates error rate.
  void CalculateErrorRate(bool pairwise_edits);

  // Calculates error rate for one example.
  void CalculateErrorRate(int idx, bool pairwise_edits);

  // Calculates minimum error rate for one example.
  void CalculateMinErrorRate(int idx);

  // Calculates pairwise edits for all reference and test outputs for item idx.
  void CalculatePairwiseErrors(int idx);

  // Writes error rates to output file.
  void WriteErrorRate(std::ofstream &output_file);

  // Writes pairwise edits to output file.
  void WritePairwiseEdits(std::ofstream &output_file);

  ::fst::SymbolTable output_syms_;
  std::vector<std::vector<std::pair<int, double>>> references_;
  std::vector<std::vector<std::pair<int, double>>> test_input_;
  std::vector<EditDistanceDouble> total_ed_double_;
  std::vector<std::vector<std::vector<int>>> pairwise_edits_;
  bool is_split_chars_;
};

}  // namespace tools
}  // namespace translit
}  // namespace nisaba

#endif  // NISABA_TRANSLIT_TOOLS_CALCULATE_ERROR_RATE_H_
