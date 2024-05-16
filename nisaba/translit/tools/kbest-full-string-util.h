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

#ifndef NISABA_TRANSLIT_TOOLS_KBEST_FULL_STRING_UTIL_H_
#define NISABA_TRANSLIT_TOOLS_KBEST_FULL_STRING_UTIL_H_

#include <map>
#include <string>
#include <utility>
#include <vector>

#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace translit {
namespace tools {

static const int kMaxLine = 51200;

// Class for ensembling k-best full string outputs from multiple systems.
class EnsembleFullString {
 public:
  explicit EnsembleFullString(
      const std::vector<std::pair<std::string, double>> &input_lists)
      : input_lists_(input_lists) {}

  // Runs ensembling over the set with a given input length. If this value is
  // less than or equal to zero, it sets the parameter for simple alignment to
  // be the most frequent length across the input set.
  void RunEnsemble(int input_length);

  // Returns k-best outputs from the ensembled candidates.
  std::vector<std::pair<std::string, double>> GetOutputs(int kbest);

 private:
  // Simple alignment aligns candidate via position in the string.
  void SimpleAlign(int input_length);

  // Prunes candidates that don't match input_length or (if input_length set to
  // zero) the most frequent candidate length.
  bool PruneByInputLength(int input_length);

  // Builds the FST to perform alignment.
  void BuildAlignWfst();

  // Adds symbol to symbol table.
  int FindSymOrAdd(absl::string_view str);

  // Adds symbol to the weighted FST for extracting k-best.
  int AddSymToKbestWfst(int sym, int curr_state);

  nlp_::fst::SymbolTable syms_;
  nlp_::fst::StdVectorFst align_wfst_;
  nlp_::fst::StdVectorFst align_fst_;
  nlp_::fst::StdVectorFst kbest_wfst_;
  std::vector<int> word_counts_;
  std::vector<std::vector<int>> ws_states_;
  std::vector<nlp_::fst::StdVectorFst> multi_aligns_;
  std::vector<std::pair<std::string, double>> input_lists_;
};

// Class for handling file I/O when using ensembling class.
class EnsembleFiles {
 public:
  EnsembleFiles(const std::string &ifiles,
                const std::string &input_length_file) {
    InitializeEnsembleFiles(ifiles, input_length_file);
  }

  void RunEnsembleAndOutput(int kbest, const std::string &ofile);

 private:
  void InitializeEnsembleFiles(const std::string &ifiles,
                               const std::string &input_length_file);
  std::vector<std::vector<std::pair<std::string, double>>> inputs_;
  std::vector<int> input_lengths_;
};

// Class for extracting k-best full string outputs from inputs.
class KbestExtractor {
 public:
  explicit KbestExtractor(const std::string &ifile) {
    InitializeKbestExtractor(ifile);
  }

  explicit KbestExtractor(const std::vector<std::string> &input_lines) {
    InitializeKbestExtractor(input_lines);
  }

  // Performs k-best extraction on the whole set and outputs to file.
  void RunExtractorAndOutput(const std::string &ofile, int kbest,
                             bool show_scores, bool show_full_input_string);

  // Performs k-best extraction on the whole set and returns vector.
  std::vector<std::vector<std::pair<std::string, double>>> GetBests(int kbest);

 private:
  // Initializes data structures from strings for kbest extraction.
  void InitializeKbestExtractor(const std::string &ifile);
  void InitializeKbestExtractor(const std::vector<std::string> &input_lines);

  // Returns kbest items with score.
  std::vector<std::pair<std::string, double>> GetBest(
      const std::vector<std::vector<std::pair<std::string, double>>> &str_arcs,
      int kbest);

  std::vector<std::vector<std::vector<std::pair<std::string, double>>>>
      input_arcs_;
  std::vector<int> input_index_;
  std::vector<std::string> input_words_;
};

// Class for rejoining k-best lists of full string outputs, for use when the
// input strings have been split into multiple substrings, usually to conform to
// maximum length constraints of systems.
class KbestRejoiner {
 public:
  KbestRejoiner(absl::string_view ifile, absl::string_view split_file,
                int kbest) {
    InitializeKbestRejoiner(ifile, split_file, kbest);
  }

  KbestRejoiner(const std::vector<std::string> &input_lines,
                const std::vector<int> &output_indices, int kbest) {
    InitializeKbestRejoiner(input_lines, output_indices, kbest);
  }

  int NumKbestLists() const { return kbest_lists_.size(); }

  // Returns the rejoined list corresponding to index.  Will return an empty
  // vector if the index does not correspond to any list.
  std::vector<std::pair<std::string, double>> GetRejoinedList(int idx) const;

  // Runs the rejoiner over the whole set and outputs to file.
  void RunRejoinerAndOutput(const std::string &ofile);

 private:
  // Initializes data structures from strings for kbest rejoining.
  void InitializeKbestRejoiner(absl::string_view ifile,
                               absl::string_view split_file, int kbest);
  void InitializeKbestRejoiner(const std::vector<std::string> &input_lines,
                               const std::vector<int> &output_indices,
                               int kbest);

  // Returns the rejoined list corresponding to the given list.
  std::vector<std::pair<std::string, double>> GetRejoinedList(
      absl::Span<const std::vector<std::pair<std::string, double>>> kbest_list)
      const;

  std::vector<int> output_indices_;
  std::vector<std::vector<std::vector<std::pair<std::string, double>>>>
      kbest_lists_;
  int kbest_;
};

}  // namespace tools
}  // namespace translit
}  // namespace nisaba

#endif  // NISABA_TRANSLIT_TOOLS_KBEST_FULL_STRING_UTIL_H_
