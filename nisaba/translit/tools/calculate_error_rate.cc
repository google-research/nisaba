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

#include "nisaba/translit/tools/calculate_error_rate.h"

#include <cmath>
#include <fstream>
#include <string>
#include <utility>
#include <vector>

#include "fst/arc.h"
#include "fst/arcsort.h"
#include "fst/compose.h"
#include "fst/shortest-path.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/log/check.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "absl/types/span.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/utf8_util.h"

namespace nisaba {
namespace translit {
namespace tools {

namespace impl {
namespace {

// Uses composition and shortest path to return min cost alignment.
::fst::StdVectorFst GetMinErrorAlignment(const ::fst::StdVectorFst &ifst,
                                           const ::fst::StdVectorFst &ofst,
                                           ::fst::StdVectorFst *align_mod) {
  ArcSort(align_mod, ::fst::ILabelCompare<::fst::StdArc>());
  ::fst::StdVectorFst ifst_o_align_mod;
  ::fst::Compose(ifst, *align_mod, &ifst_o_align_mod);
  ::fst::ArcSort(&ifst_o_align_mod,
                   ::fst::OLabelCompare<::fst::StdArc>());
  ::fst::StdVectorFst ifst_o_align_mod_o_ofst;
  ::fst::Compose(ifst_o_align_mod, ofst, &ifst_o_align_mod_o_ofst);
  ::fst::StdVectorFst alignment;
  ::fst::ShortestPath(ifst_o_align_mod_o_ofst, &alignment);
  return alignment;
}

// Prints 1-4 items in a line to the output file.
void LineToFile(std::ofstream &output_file, const absl::AlphaNum &a,
                bool newline, const absl::AlphaNum &b = "",
                const absl::AlphaNum &c = "", const absl::AlphaNum &d = "") {
  if (newline) {
    output_file << absl::StrCat(a, b, c, d, "\n");
  } else {
    output_file << absl::StrCat(a, b, c, d);
  }
  QCHECK(output_file);
}

// Returns true if first edit distance components yields better error rate than
// second.
bool BetterErrorValues(const EditDistanceDouble &this_min_error_values,
                       const EditDistanceDouble &min_error_values) {
  return this_min_error_values.ErrorRate() < min_error_values.ErrorRate();
}

// Creates linear string Fst from vector of symbols, adding to symbol table.
::fst::StdVectorFst GetStringFst(absl::Span<const std::string> token_string,
                                   ::fst::SymbolTable *syms) {
  ::fst::StdVectorFst fst;
  fst.SetStart(fst.AddState());
  int curr_state = fst.Start();
  for (const auto &token : token_string) {
    int sym = syms->Find(token);
    if (sym < 0) {
      sym = syms->AddSymbol(token);
    }
    int next_state = fst.AddState();
    fst.AddArc(curr_state, ::fst::StdArc(sym, sym, 0.0, next_state));
    curr_state = next_state;
  }
  fst.SetFinal(curr_state, 0.0);
  return fst;
}

// Finds minimum cost alignment between two string automata.
::fst::StdVectorFst AlignStringFsts(const ::fst::StdVectorFst &ref_fst,
                                      const ::fst::StdVectorFst &test_fst,
                                      int num_symbols) {
  ::fst::StdVectorFst align_mod;
  align_mod.SetStart(align_mod.AddState());
  align_mod.SetFinal(align_mod.Start(), 0.0);
  for (int sym = 1; sym < num_symbols; ++sym) {
    // Adds insertion, deletion and substitution arcs for all symbols.
    align_mod.AddArc(align_mod.Start(),
                     ::fst::StdArc(sym, 0, 1.0, align_mod.Start()));
    align_mod.AddArc(align_mod.Start(),
                     ::fst::StdArc(0, sym, 1.0, align_mod.Start()));
    for (int sub_sym = 1; sub_sym < num_symbols; ++sub_sym) {
      // If sym == sub_sym, cost is 0.0, otherwise 1.0.
      align_mod.AddArc(align_mod.Start(),
                       ::fst::StdArc(sym, sub_sym, sym == sub_sym ? 0.0 : 1.0,
                                       align_mod.Start()));
    }
  }
  return impl::GetMinErrorAlignment(test_fst, ref_fst, &align_mod);
}

// Returns the counts for deriving the string-to-string edit distance.
EditDistanceInt CalculatePairEditDistance(const ::fst::StdVectorFst &ref_fst,
                                          const ::fst::StdVectorFst &test_fst,
                                          int num_symbols) {
  const ::fst::StdVectorFst min_cost_alignment =
      AlignStringFsts(ref_fst, test_fst, num_symbols);
  int curr_state = min_cost_alignment.Start();
  EditDistanceInt ed_int;
  ed_int.reference_length = ref_fst.NumStates() - 1;
  while (curr_state >= 0 && min_cost_alignment.NumArcs(curr_state) > 0) {
    QCHECK_EQ(min_cost_alignment.NumArcs(curr_state), 1);
    ::fst::ArcIterator<::fst::StdVectorFst> aiter(min_cost_alignment,
                                                      curr_state);
    ::fst::StdArc arc = aiter.Value();
    if (arc.ilabel != arc.olabel) {  // This is an edit in the alignment.
      if (arc.ilabel == 0) {
        // Reference token aligns with nothing in the test string: deletion.
        ++ed_int.deletions;
      } else if (arc.olabel == 0) {
        // Test token aligns with nothing in the reference string: insertion.
        ++ed_int.insertions;
      } else {
        ++ed_int.substitutions;
      }
    }
    curr_state = arc.nextstate;
  }
  return ed_int;
}

// Returns the counts for deriving the string-to-string edit distance.
EditDistanceInt CalculatePairEditDistance(
    const std::vector<std::string> &ref_string,
    const std::vector<std::string> &test_string) {
  ::fst::SymbolTable syms;
  syms.AddSymbol("<epsilon>");
  const ::fst::StdVectorFst ref_fst = GetStringFst(ref_string, &syms);
  const ::fst::StdVectorFst test_fst = GetStringFst(test_string, &syms);
  return CalculatePairEditDistance(ref_fst, test_fst, syms.NumSymbols());
}

// Returns the number of edits in the distance between the pairs.
int CalculatePairEditDistanceValue(
    const std::vector<std::string> &ref_string,
    const std::vector<std::string> &test_string) {
  return CalculatePairEditDistance(ref_string, test_string).Edits();
}

// Splits string on either whitespace or characters.
std::vector<std::string> MaybeSplitChars(absl::string_view str,
                                         bool split_chars) {
  std::vector<std::string> tokenized_string =
      absl::StrSplit(str, utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  if (split_chars) {
    // Rejoins with a single whitespace prior to splitting on single unicode
    // codepoints, thus normalizing the whitespace in the strings.
    tokenized_string =
        utf8::StrSplitByChar(absl::StrJoin(tokenized_string, " "));
  }
  return tokenized_string;
}

// Accumulates a normalizer from a vector of pairs including -log weights.
double GetNormalizer(const std::vector<std::pair<int, double>> &input_pairs) {
  double exp_sum = 0.0;
  for (const auto input_pair : input_pairs) {
    exp_sum += exp(-input_pair.second);
  }
  return -log(exp_sum);
}

// Writes vector of candidates to output file in expected json format, after
// normalizing the weights, and returns vector of probabilities.
std::vector<double> WriteCands(std::ofstream &output_file,
                               const std::vector<std::pair<int, double>> &cands,
                               const ::fst::SymbolTable &syms) {
  double norm = impl::GetNormalizer(cands);
  std::vector<double> probs;
  probs.reserve(cands.size());
  for (int i = 0; i < cands.size(); ++i) {
    const std::string hyp_word = syms.Find(cands[i].first);
    probs.push_back(exp(-cands[i].second + norm));
    const std::string delim = i > 0 ? ", \"" : "\"";
    impl::LineToFile(output_file,
                     absl::StrCat(delim, hyp_word, "\": ", probs[i]),
                     /*newline=*/false);
  }
  return probs;
}

// Produces a square bracket vector string concatenating two vectors of type T.
template <class T>
std::string GetBracketedVectorString(const std::vector<T> &vector_a,
                                     const std::vector<T> &vector_b) {
  return absl::StrCat(
      "[",
      absl::StrJoin(
          {absl::StrJoin(vector_a, ", "), absl::StrJoin(vector_b, ", ")}, ", "),
      "]");
}

// Transposes matrix of ints.
std::vector<std::vector<int>> TransposeMatrix(
    const std::vector<std::vector<int>> &matrix) {
  if (matrix.empty()) {
    return matrix;
  }
  std::vector<std::vector<int>> transposed;
  int rows = matrix.size();
  int cols = matrix[0].size();
  transposed.reserve(cols);
  for (int i = 0; i < cols; ++i) {
    std::vector<int> this_row;
    this_row.reserve(rows);
    for (int j = 0; j < rows; ++j) {
      this_row.push_back(matrix[j][i]);
    }
    transposed.push_back(this_row);
  }
  return transposed;
}

// Returns string showing pairwise distances between refs/hyps in json format.
std::string GetDistances(const std::vector<std::vector<int>> &dists) {
  std::vector<std::string> dist_arrays;
  if (!dists.empty()) {
    int rows = dists.size();
    int cols = dists[0].size();
    const auto transposed = TransposeMatrix(dists);
    dist_arrays.reserve(rows + cols);
    for (const auto &dist : dists) {
      dist_arrays.push_back(
          GetBracketedVectorString(std::vector<int>(rows, 0), dist));
    }
    for (const auto &trans_dist : transposed) {
      dist_arrays.push_back(
          GetBracketedVectorString(trans_dist, std::vector<int>(cols, 0)));
    }
  }
  return absl::StrJoin(dist_arrays, ", ");
}

// Returns vector of lengths of strings in cands.
std::vector<int> GetLengths(const std::vector<std::pair<int, double>> &cands,
                            const ::fst::SymbolTable &syms) {
  std::vector<int> lengths;
  lengths.reserve(cands.size());
  for (const auto cand : cands) {
    lengths.push_back(utf8::StrSplitByChar(syms.Find(cand.first)).size());
  }
  return lengths;
}

}  // namespace
}  // namespace impl

double MultiRefErrorRate::CalcErrorRate() {
  EditDistanceDouble tot_ed_double;
  for (int i = 0; i < total_ed_double_.size(); ++i) {
    tot_ed_double += total_ed_double_[i];
  }
  return tot_ed_double.ErrorRate();
}

void MultiRefErrorRate::WriteErrorRate(std::ofstream &output_file) {
  EditDistanceDouble tot_ed_double;
  for (int i = 0; i < total_ed_double_.size(); ++i) {
    impl::LineToFile(output_file, total_ed_double_[i].ToString(),
                     /*newline=*/true);
    tot_ed_double += total_ed_double_[i];
  }
  std::string error_rate_label = is_split_chars_ ? "CER" : "WER";
  impl::LineToFile(output_file, "Summary ", /*newline=*/true, error_rate_label);
  impl::LineToFile(output_file, "total statistics: ", /*newline=*/true,
                   tot_ed_double.ToString());
  impl::LineToFile(output_file, "overall ", /*newline=*/true, error_rate_label,
                   ": ", tot_ed_double.ErrorRate());
}

void MultiRefErrorRate::WritePairwiseEdits(std::ofstream &output_file) {
  for (int idx = 0; idx < references_.size(); ++idx) {
    // Writes system outputs with probabilities.
    impl::LineToFile(output_file, "{\"hyp\": {", /*newline=*/false);
    const auto p1 =
        impl::WriteCands(output_file, test_input_[idx], output_syms_);
    // Writes references with probabilities.
    impl::LineToFile(output_file, "}, \"ref\": {", /*newline=*/false);
    const auto p2 =
        impl::WriteCands(output_file, references_[idx], output_syms_);
    // Writes system output probabilities.
    impl::LineToFile(output_file, "}, \"p1\": ", /*newline=*/false);
    impl::LineToFile(output_file,
                     impl::GetBracketedVectorString(
                         p1, std::vector<double>(references_[idx].size(), 0)),
                     /*newline=*/false);
    // Writes reference probabilities.
    impl::LineToFile(output_file, ", \"p2\": ", /*newline=*/false);
    impl::LineToFile(
        output_file,
        impl::GetBracketedVectorString(
            std::vector<double>(test_input_[idx].size(), 0), p2),
        /*newline=*/false);
    // Writes distances all system/reference pairs, (zeros for
    // reference/reference or system/system distances, not used).
    impl::LineToFile(output_file, ", \"D\": [", /*newline=*/false);
    impl::LineToFile(output_file, impl::GetDistances(pairwise_edits_[idx]),
                     /*newline=*/false);
    // Writes lengths of references (zeros for system items, not used).
    impl::LineToFile(output_file, "], \"L\": ", /*newline=*/false);
    impl::LineToFile(output_file,
                     impl::GetBracketedVectorString(
                         std::vector<int>(test_input_[idx].size(), 0),
                         impl::GetLengths(references_[idx], output_syms_)),
                     /*newline=*/false);
    impl::LineToFile(output_file, "}", /*newline=*/true);
  }
}

void MultiRefErrorRate::Write(absl::string_view ofile, bool pairwise_edits) {
  std::ofstream output_file;
  output_file.open(std::string(ofile));
  QCHECK(output_file) << "Cannot open " << ofile << " for writing.";
  if (pairwise_edits) {
    WritePairwiseEdits(output_file);
  } else {
    WriteErrorRate(output_file);
  }
}

void MultiRefErrorRate::ReadInputs(absl::string_view input_file,
                                   bool is_reference) {
  if (is_reference) {
    references_.clear();
  } else {
    test_input_.clear();
  }
  const auto &input_lines_status = file::ReadLines(input_file, kMaxLine);
  QCHECK(input_lines_status.ok()) << "Failed to read " << input_file;
  const std::vector<std::string> input_lines = input_lines_status.value();
  for (const std::string &str : input_lines) {
    const std::vector<std::string> seq =
        absl::StrSplit(str, '\t', absl::SkipEmpty());
    QCHECK_GE(seq.size(), 2);
    int input_idx = std::stoi(seq[0]);
    int osym = 0;
    if (!seq[1].empty()) {
      osym = output_syms_.Find(seq[1]);
      if (osym < 0) {
        osym = output_syms_.AddSymbol(seq[1]);
      }
    }
    // Default count (in reference) is 1.0; otherwise default (-logP) is 0.0.
    double item_value = is_reference ? 1.0 : 0.0;
    if (seq.size() > 2) {
      QCHECK_LE(seq.size(), 3);
      item_value = std::stod(seq[2]);
    }
    if (is_reference) {
      // Converts raw count to -log count for references.
      item_value = -log(item_value);
      if (input_idx >= references_.size()) {
        references_.resize(input_idx + 1);
      }
      references_[input_idx].push_back(std::make_pair(osym, item_value));
    } else {
      if (input_idx >= test_input_.size()) {
        test_input_.resize(input_idx + 1);
      }
      test_input_[input_idx].push_back(std::make_pair(osym, item_value));
    }
  }
}

std::vector<std::string> MultiRefErrorRate::GetTokenizedString(
    int idx, int k, bool is_test_item) const {
  const auto &inputs = is_test_item ? test_input_ : references_;
  if (idx >= inputs.size() || k >= inputs[idx].size()) {
    // If requested string does not exist in collection.
    return std::vector<std::string>();
  }
  const auto input_pair = inputs[idx][k];
  return input_pair.first == 0
             ? std::vector<std::string>()
             : impl::MaybeSplitChars(output_syms_.Find(input_pair.first),
                                     is_split_chars_);
}

void MultiRefErrorRate::CalculateMinErrorRate(int idx) {
  int min_cost_test_item = 0;
  for (int i = 1; i < test_input_[idx].size(); ++i) {
    if (test_input_[idx][i].second <
        test_input_[idx][min_cost_test_item].second) {
      min_cost_test_item = i;
    }
  }
  EditDistanceDouble min_error_values;
  // If minimum cost test item is empty string, empty vector; otherwise
  // tokenize string as requested.
  const std::vector<std::string> test_string =
      GetTokenizedString(idx, min_cost_test_item, /*is_test_item=*/true);
  for (int i = 0; i < references_[idx].size(); ++i) {
    const std::vector<std::string> ref_string =
        GetTokenizedString(idx, i, /*is_test_item=*/false);
    auto this_min_error_values =
        impl::CalculatePairEditDistance(ref_string, test_string);
    if (i == 0 || impl::BetterErrorValues(
                      static_cast<EditDistanceDouble>(this_min_error_values),
                      min_error_values)) {
      min_error_values = this_min_error_values;
    }
  }
  total_ed_double_.push_back(min_error_values);
}

void MultiRefErrorRate::CalculatePairwiseErrors(int idx) {
  std::vector<std::vector<int>> pairwise_edits;
  pairwise_edits.reserve(test_input_[idx].size());
  for (int i = 0; i < test_input_[idx].size(); ++i) {
    const std::vector<std::string> test_string =
        GetTokenizedString(idx, i, /*is_test_item=*/true);
    std::vector<int> these_edits;
    these_edits.reserve(references_[idx].size());
    for (int j = 0; j < references_[idx].size(); ++j) {
      const std::vector<std::string> ref_string =
          GetTokenizedString(idx, j, /*is_test_item=*/false);
      these_edits.push_back(
          impl::CalculatePairEditDistanceValue(ref_string, test_string));
    }
    pairwise_edits.push_back(these_edits);
  }
  pairwise_edits_.push_back(pairwise_edits);
}

void MultiRefErrorRate::CalculateErrorRate(int idx, bool pairwise_edits) {
  if (references_[idx].empty()) {
    // Nothing to do for this example.
    return;
  }
  if (pairwise_edits) {
    CalculatePairwiseErrors(idx);
  } else {
    CalculateMinErrorRate(idx);
  }
}

void MultiRefErrorRate::CalculateErrorRate(bool pairwise_edits) {
  QCHECK_EQ(references_.size(), test_input_.size());
  if (pairwise_edits) {
    pairwise_edits_.clear();
    pairwise_edits_.reserve(references_.size());
  } else {
    total_ed_double_.clear();
    total_ed_double_.reserve(references_.size());
  }
  for (int idx = 0; idx < references_.size(); ++idx) {
    // Either both are empty or reference is non-empty.
    QCHECK(!references_[idx].empty() || test_input_[idx].empty());
    if (test_input_[idx].empty()) {
      // Creates empty string test input if none given for reference item.
      test_input_[idx].push_back(std::make_pair(0, 0.0));
    }
    CalculateErrorRate(idx, pairwise_edits);
  }
}

void MultiRefErrorRate::CalculateErrorRate(absl::string_view reffile,
                                           absl::string_view testfile,
                                           bool pairwise_edits) {
  ReadInputs(reffile, /*is_reference=*/true);
  ReadInputs(testfile, /*is_reference=*/false);
  CalculateErrorRate(pairwise_edits);
}

}  // namespace tools
}  // namespace translit
}  // namespace nisaba
