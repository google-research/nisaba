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

#ifndef NISABA_TRANSLIT_FST_WORDPIECE_SEGMENTER_H_
#define NISABA_TRANSLIT_FST_WORDPIECE_SEGMENTER_H_

#include <map>
#include <string>
#include <utility>
#include <vector>

#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/container/flat_hash_map.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace translit {
namespace fst {

class WordpieceSegmenter {
 public:
  // Initializes wordpiece segmenter from vector of wordpieces.
  explicit WordpieceSegmenter(const std::string &word_initial_prefix)
      : word_initial_prefix_(word_initial_prefix) {}

  // Initializes wordpieces from given text file, one wordpiece per line.
  // Assumes wordpiece file is sorted by priority, i.e., earlier in the file
  // indicates higher priority.
  absl::Status InitWordpieces(const std::string &wp_symbols);

  // Initializes wordpieces from vector of wordpieces. Assumes wordpiece vector
  // is sorted by priority, i.e., earlier in the vector indicates higher
  // priority.
  absl::Status InitWordpieces(const std::vector<std::string> &wp_symbols);

  // Returns a transducer from word indices to wordpiece indices for word
  // indices included in input_words vector.
  absl::StatusOr<::fst::StdVectorFst> GetWordpieceTransducer(
      const std::vector<int> &input_words, const ::fst::SymbolTable &word_syms,
      const ::fst::SymbolTable &wordpiece_syms,
      const std::string &wordpiece_unk) const;

  // Segments input string into vector of wordpieces.
  absl::StatusOr<std::vector<std::string>> GetWordpieces(
      const std::string &input_str) const;

  // Segments input string_view into vector of wordpieces.
  absl::StatusOr<std::vector<std::string>> GetWordpieces(
      absl::string_view input_sv) const;

  // Tokenizes input string and returns resulting string, whitespace delimited.
  absl::StatusOr<std::string> TokenizeInput(const std::string &input_str) const;

 private:
  // Looks for candidate, returns true and copies to wordpiece_pair if found.
  bool FindWordpiecePair(const std::string &cand_wordpiece,
                         std::pair<std::string, int> *wordpiece_pair) const;

  // Extracts wordpiece candidates for all positions over the input word.
  std::vector<std::vector<std::pair<std::string, int>>>
  ExtractWordpieceCands(const std::string &input_word) const;

  // Segments input vector of words into vector of wordpieces.
  absl::StatusOr<std::vector<std::string>> GetNoWhitespaceWordpieces(
      const std::vector<std::string> &input_words) const;

  // Vocabulary of wordpieces with rank in given list. The list is expected to
  // be sorted in order of priority.
  absl::flat_hash_map<std::string, int> wordpiece_ranks_;
  std::string word_initial_prefix_;
};

}  // namespace fst
}  // namespace translit
}  // namespace nisaba

#endif  // NISABA_TRANSLIT_FST_WORDPIECE_SEGMENTER_H_
