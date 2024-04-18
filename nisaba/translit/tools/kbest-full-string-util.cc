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

#include <algorithm>
#include <cmath>
#include <fstream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "fst/arc-map.h"
#include "fst/arc.h"
#include "fst/arcsort.h"
#include "fst/compose.h"
#include "fst/float-weight.h"
#include "fst/project.h"
#include "fst/shortest-path.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "ngram/ngram-count.h"
#include "absl/container/flat_hash_set.h"
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

using ::fst::ArcIterator;
using ::fst::Compose;
using ::fst::ILabelCompare;
using ::fst::Log64Weight;
using ::fst::LogArc;
using ::fst::OLabelCompare;
using ::fst::Project;
using ::fst::PROJECT_INPUT;
using ::fst::PROJECT_OUTPUT;
using ::fst::ShortestPath;
using ::fst::StdArc;
using ::fst::StdToLogMapper;
using ::fst::StdVectorFst;
using ::fst::SymbolTable;
using ::fst::VectorFst;

namespace impl {
namespace {

// Returns the most frequently found value in the vector.
int MostFreqValue(std::vector<int> input_vec, int *min_value = nullptr) {
  std::sort(input_vec.begin(), input_vec.end());
  if (min_value != nullptr && !input_vec.empty()) {
    *min_value = input_vec[0];
  }
  int curr_cnt = 0;
  int max_cnt = 0;
  int most_freq_val = -1;
  for (int i = 0; i < input_vec.size(); ++i) {
    if (i > 0 && input_vec[i] != input_vec[i - 1]) {
      if (curr_cnt >= max_cnt) {
        max_cnt = curr_cnt;
        most_freq_val = input_vec[i - 1];
      }
      curr_cnt = 0;
    }
    ++curr_cnt;
  }
  if (most_freq_val < 0 || curr_cnt >= max_cnt) {
    most_freq_val = input_vec.back();
  }
  return most_freq_val;
}

// Returns (whitespace delimited) word count for string.
int GetWordCount(const std::string &str) {
  const std::vector<std::string> seq = absl::StrSplit(
      str, nisaba::utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  return seq.size();
}

// Counts position-specific word occurrences in weighted k-best list.
StdVectorFst CountPosSyms(const StdVectorFst &fst) {
  std::unique_ptr<ngram::NGramCounter<Log64Weight>> ngram_counter(
      new ngram::NGramCounter<Log64Weight>(/*order=*/1, false));
  StdToLogMapper std2log_mapper;
  VectorFst<LogArc> log_fst;
  ArcMap(fst, &log_fst, std2log_mapper);
  CHECK(ngram_counter->Count(log_fst));
  StdVectorFst count_fst;
  ngram_counter->GetFst(&count_fst);
  ArcSort(&count_fst, ILabelCompare<StdArc>());
  return count_fst;
}

// Verifies and combines inputs for downstream processing.
std::vector<std::vector<std::pair<std::string, double>>>
VerifyCombineEnsembleInputs(
    const std::vector<std::vector<std::vector<std::pair<std::string, double>>>>
        &inputs_to_ensemble) {
  // Verifies that files have same number of examples.
  int num_items = inputs_to_ensemble[0].size();
  for (int i = 1; i < inputs_to_ensemble.size(); ++i) {
    QCHECK_EQ(inputs_to_ensemble[i].size(), num_items);
  }
  // Combines candidates in ensemble for easier subsequent processing.
  std::vector<std::vector<std::pair<std::string, double>>>
      inputs_to_ensemble_combined = inputs_to_ensemble[0];
  for (int j = 0; j < num_items; ++j) {
    for (int i = 1; i < inputs_to_ensemble.size(); ++i) {
      inputs_to_ensemble_combined[j].insert(
          inputs_to_ensemble_combined[j].end(),
          inputs_to_ensemble[i][j].begin(), inputs_to_ensemble[i][j].end());
    }
  }
  return inputs_to_ensemble_combined;
}

// Reads in input lengths from TXT file.
std::vector<int> ReadInputLengths(const std::string &ifile, int num_items) {
  std::vector<int> input_lengths(num_items, -1);
  if (!ifile.empty()) {
    const auto &input_lines_status = nisaba::file::ReadLines(ifile, kMaxLine);
    QCHECK_OK(input_lines_status) << "Failed to read " << ifile;
    const std::vector<std::string> input_lines = input_lines_status.value();
    QCHECK_EQ(num_items, static_cast<int>(input_lines.size()));
    for (int i = 0; i < num_items; ++i) {
      input_lengths[i] = std::stoi(input_lines[i]);
      QCHECK_GT(input_lengths[i], 0);
    }
  }
  return input_lengths;
}

// Reads in candidates from TSV file w/input, output and scores.
std::vector<std::vector<double>> ReadInputs(
    const std::string &ifile,
    std::vector<std::vector<std::string>> *system_outputs) {
  system_outputs->clear();
  std::vector<std::string> system_inputs;
  std::vector<std::vector<double>> system_scores;
  const auto &input_lines_status = nisaba::file::ReadLines(ifile, kMaxLine);
  QCHECK_OK(input_lines_status) << "Failed to read " << ifile;
  const std::vector<std::string> input_lines = input_lines_status.value();
  for (const auto &str : input_lines) {
    const std::vector<std::string> seq =
        absl::StrSplit(str, '\t', absl::SkipEmpty());
    QCHECK_EQ(seq.size(), 3) << "oops: " << str;
    if (system_inputs.empty() || system_inputs.back() != seq[0]) {
        system_inputs.push_back(seq[0]);
        system_outputs->push_back(std::vector<std::string>());
        system_scores.push_back(std::vector<double>());
    }
    // Removes extra whitespace at word boundaries.
    system_outputs->back().push_back(absl::StrJoin(
        absl::StrSplit(seq[1], nisaba::utf8::Utf8WhitespaceDelimiter(),
                       absl::SkipEmpty()),
        " "));
    system_scores.back().push_back(std::stod(seq[2]));
  }
  return system_scores;
}

// Normalizes candidate probabilities (softmax) and creates pairs.
std::vector<std::vector<std::pair<std::string, double>>> NormAndPairList(
    const std::vector<std::vector<std::string>> &system_outputs,
    const std::vector<std::vector<double>> &system_scores) {
  std::vector<std::vector<std::pair<std::string, double>>> input_to_ensemble(
      system_scores.size());
  for (int i = 0; i < system_scores.size(); ++i) {
    QCHECK_GT(system_scores[i].size(), 0);
    double tot = system_scores[i][0];
    input_to_ensemble[i].reserve(system_scores[i].size());
    for (int j = 1; j < system_scores[i].size(); ++j) {
        tot = -log(exp(-tot) + exp(-system_scores[i][j]));
    }
    for (int j = 0; j < system_scores[i].size(); ++j) {
      input_to_ensemble[i].push_back(
          std::make_pair(system_outputs[i][j], system_scores[i][j] - tot));
    }
  }
  return input_to_ensemble;
}

// Returns vector of candidate vectors, each entry a pair of string and score.
std::vector<std::vector<std::pair<std::string, double>>> ReadInputsToEnsemble(
    const std::string &ifiles) {
  std::vector<std::string> input_files =
      absl::StrSplit(ifiles, ':', absl::SkipEmpty());
  QCHECK_GE(input_files.size(), 2)
      << "Need at least 2 files in ifiles argument, which was not found in "
      << ifiles;
  std::vector<std::vector<std::vector<std::pair<std::string, double>>>>
      inputs_to_ensemble;
  for (const auto &ifile : input_files) {
    std::vector<std::vector<std::string>> system_outputs;
    std::vector<std::vector<double>> system_scores =
        ReadInputs(ifile, &system_outputs);
    inputs_to_ensemble.push_back(
        NormAndPairList(system_outputs, system_scores));
  }
  return VerifyCombineEnsembleInputs(inputs_to_ensemble);
}

// Returns k-best outputs from FST.
std::vector<std::pair<std::string, double>> GetOutputs(
    const StdVectorFst &infst, const SymbolTable &syms, int kbest) {
  if (infst.NumStates() == 0) {
    // Returns empty k-best outputs if FST is empty.
    return std::vector<std::pair<std::string, double>>();
  }
  StdVectorFst kbest_strings;
  ShortestPath(infst, &kbest_strings, kbest);
  std::vector<int> start_states;
  std::vector<double> kbest_scores;
  std::vector<std::vector<std::string>> kbest_words;
  if (kbest == 1) {
    start_states.push_back(kbest_strings.Start());
    kbest_scores.push_back(0.0);
    kbest_words.push_back(std::vector<std::string>());
  } else {
    for (ArcIterator<StdVectorFst> aiter(kbest_strings, kbest_strings.Start());
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      QCHECK_EQ(arc.ilabel, 0);
      QCHECK_EQ(arc.olabel, 0);
      start_states.push_back(arc.nextstate);
      kbest_scores.push_back(arc.weight.Value());
      kbest_words.push_back(std::vector<std::string>());
    }
  }
  double tot_cost;
  for (int i = 0; i < start_states.size(); ++i) {
    int curr_st = start_states[i];
    while (kbest_strings.NumArcs(curr_st) > 0) {
      ArcIterator<StdVectorFst> aiter(kbest_strings, curr_st);
      StdArc arc = aiter.Value();
      if (arc.ilabel > 0) {
        kbest_words[i].push_back(syms.Find(arc.ilabel));
      }
      kbest_scores[i] += arc.weight.Value();
      curr_st = arc.nextstate;
    }
    kbest_scores[i] += kbest_strings.Final(curr_st).Value();
    tot_cost =
        i == 0 ? kbest_scores[i] : -log(exp(-tot_cost) + exp(-kbest_scores[i]));
  }
  std::vector<std::pair<std::string, double>> result(start_states.size());
  for (int i = 0; i < start_states.size(); ++i) {
    result[i] = std::make_pair(absl::StrJoin(kbest_words[i], " "),
                               kbest_scores[i] - tot_cost);
  }
  return result;
}

// Makes a lattice FST from input representation.
StdVectorFst MakeLattice(
    absl::Span<const std::vector<std::pair<std::string, double>>> str_arcs,
    SymbolTable *syms) {
  StdVectorFst fst;
  int curr_state = fst.AddState();
  fst.SetStart(curr_state);
  for (const auto &pairs : str_arcs) {
    int next_state = fst.AddState();
    for (const auto &pair : pairs) {
      const std::string word_str = pair.first;
      int sym = syms->Find(word_str);
      if (sym < 0) {
        sym = syms->AddSymbol(word_str);
      }
      fst.AddArc(curr_state, StdArc(sym, sym, pair.second, next_state));
    }
    curr_state = next_state;
  }
  fst.SetFinal(curr_state, 0.0);
  return fst;
}

// Performs whitespace normalization required when rejoining lists.
std::vector<std::pair<std::string, double>> WhitespaceNorm(
    const std::vector<std::pair<std::string, double>> &rejoined_list) {
  std::vector<std::pair<std::string, double>> to_return(rejoined_list.size());
  for (int i = 0; i < rejoined_list.size(); ++i) {
    to_return[i] = std::make_pair(
        absl::StrJoin(absl::StrSplit(rejoined_list[i].first,
                                     nisaba::utf8::Utf8WhitespaceDelimiter(),
                                     absl::SkipEmpty()),
                      " "),
        rejoined_list[i].second);
  }
  return to_return;
}

// Recursively accumulates the best candidates into a single representation.
void GatherBestCands(const StdVectorFst &kbest_cands, int curr_state,
                     const std::vector<int> &input_vec,
                     std::vector<std::vector<int>> *to_return) {
  if (kbest_cands.NumArcs(curr_state) < 1) {
    to_return->push_back(input_vec);
  } else {
    for (ArcIterator<StdVectorFst> aiter(kbest_cands, curr_state);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (arc.ilabel > 0) {
        std::vector<int> next_vec = input_vec;
        next_vec.push_back(arc.ilabel);
        GatherBestCands(kbest_cands, arc.nextstate, next_vec, to_return);
      } else {
        GatherBestCands(kbest_cands, arc.nextstate, input_vec, to_return);
      }
    }
  }
}

// Iterates over k-best items and assembles them into easy-to-use vectors.
std::vector<std::vector<int>> GatherBestCands(const StdVectorFst &kbest_cands) {
  std::vector<std::vector<int>> to_return;
  for (ArcIterator<StdVectorFst> aiter(kbest_cands, kbest_cands.Start());
       !aiter.Done(); aiter.Next()) {
    StdArc arc = aiter.Value();
    std::vector<int> input_vec;
    if (arc.ilabel > 0) {
      input_vec.push_back(arc.ilabel);
    }
    GatherBestCands(kbest_cands, arc.nextstate, input_vec, &to_return);
  }
  return to_return;
}

// Combines multiple k-best lists into a single k-best list.
std::vector<std::pair<std::string, double>> RejoinList(
    absl::Span<const std::vector<std::pair<std::string, double>>> kbest_lists,
    int kbest) {
  if (kbest_lists.size() < 2) {
    QCHECK(!kbest_lists.empty());
    return kbest_lists[0];
  }
  StdVectorFst fst;
  int curr_state = fst.AddState();
  fst.SetStart(curr_state);
  for (int i = 0; i < kbest_lists.size(); ++i) {
    int next_state = fst.AddState();
    for (int j = 0; j < kbest_lists[i].size(); ++j) {
      fst.AddArc(curr_state,
                 StdArc(j + 1, j + 1, kbest_lists[i][j].second, next_state));
    }
    curr_state = next_state;
  }
  fst.SetFinal(curr_state, 0.0);
  StdVectorFst kbest_cands;
  ShortestPath(fst, &kbest_cands, kbest);
  const std::vector<std::vector<int>> best_cands = GatherBestCands(kbest_cands);
  QCHECK(!best_cands.empty());
  std::vector<std::pair<std::string, double>> return_vec;
  return_vec.reserve(best_cands.size());
  for (const auto &best_cand : best_cands) {
    QCHECK_EQ(best_cand.size(), kbest_lists.size());
    double score = 0.0;
    std::vector<std::string> cand_str;
    for (int i = 0; i < best_cand.size(); ++i) {
      cand_str.push_back(kbest_lists[i][best_cand[i] - 1].first);
      score += kbest_lists[i][best_cand[i] - 1].second;
    }
    return_vec.push_back(std::make_pair(absl::StrJoin(cand_str, " "), score));
  }
  return return_vec;
}

}  // namespace
}  // namespace impl

int EnsembleFullString::FindSymOrAdd(absl::string_view str) {
  int sym = syms_.Find(str);
  if (sym < 0) {
    sym = syms_.AddSymbol(str);
  }
  return sym;
}

int EnsembleFullString::AddSymToKbestWfst(int sym, int curr_state) {
  int next_st = kbest_wfst_.AddState();
  kbest_wfst_.AddArc(curr_state, StdArc(sym, sym, 0.0, next_st));
  return next_st;
}

void EnsembleFullString::BuildAlignWfst() {
  int align_fst_final_state = align_fst_.AddState();
  align_fst_.SetFinal(align_fst_final_state, 0.0);
  syms_.AddSymbol("<epsilon>");
  kbest_wfst_.SetStart(kbest_wfst_.AddState());
  absl::flat_hash_set<std::vector<int>> align_arcs;
  for (int i = 0; i < input_lists_.size(); ++i) {
    std::vector<std::string> seq = absl::StrSplit(
        input_lists_[i].first, nisaba::utf8::Utf8WhitespaceDelimiter(),
        absl::SkipEmpty());
    QCHECK_EQ(ws_states_[i].size() + 1, seq.size())
        << "here: " << input_lists_[i].first;
    ws_states_[i].push_back(align_fst_final_state);
    int curr_state = align_fst_.Start();
    int curr_kbest_st = kbest_wfst_.Start();
    int idx = 0;
    for (auto ws_pos : ws_states_[i]) {
      int sym = FindSymOrAdd(seq[idx++]);
      QCHECK_GE(ws_pos, 0);
      const std::vector<int> align_arc = {curr_state, ws_pos, sym};
      align_arcs.emplace(align_arc);
      curr_state = ws_pos;
      curr_kbest_st = AddSymToKbestWfst(sym, curr_kbest_st);
    }
    kbest_wfst_.SetFinal(curr_kbest_st, input_lists_[i].second);
  }
  ArcSort(&kbest_wfst_, ILabelCompare<StdArc>());
  SymbolTable pos_syms;
  pos_syms.AddSymbol("<epsilon>");
  for (const auto &align_arc : align_arcs) {
    int psym = pos_syms.Find(absl::StrJoin(align_arc, ":"));
    if (psym < 0) {
      psym = pos_syms.AddSymbol(absl::StrJoin(align_arc, ":"));
    }
    align_fst_.AddArc(align_arc[0],
                      StdArc(psym, align_arc[2], 0.0, align_arc[1]));
  }
  ArcSort(&align_fst_, OLabelCompare<StdArc>());
  StdVectorFst pos_sym_kbest;
  Compose(align_fst_, kbest_wfst_, &pos_sym_kbest);
  Project(&pos_sym_kbest, PROJECT_INPUT);
  ArcSort(&align_fst_, ILabelCompare<StdArc>());
  Compose(impl::CountPosSyms(pos_sym_kbest), align_fst_, &align_wfst_);
  Project(&align_wfst_, PROJECT_OUTPUT);
}

bool EnsembleFullString::PruneByInputLength(int input_length) {
  int most_freq_count =
      input_length > 0 ? input_length : impl::MostFreqValue(word_counts_);
  auto input_lists = input_lists_;
  auto word_counts = word_counts_;
  input_lists_.clear();
  word_counts_.clear();
  for (int i = 0; i < input_lists.size(); ++i) {
    if (word_counts[i] == most_freq_count) {
      input_lists_.push_back(input_lists[i]);
      word_counts_.push_back(word_counts[i]);
    }
  }
  return true;
}

void EnsembleFullString::SimpleAlign(int input_length) {
  if (input_lists_.empty()) {
    return;
  }
  bool all_same_count = true;
  for (int i = 0; i < input_lists_.size(); ++i) {
    word_counts_.push_back(impl::GetWordCount(input_lists_[i].first));
    if (all_same_count && word_counts_[i] != word_counts_[0]) {
      all_same_count = false;
    }
  }
  if (!all_same_count) {
    PruneByInputLength(input_length);
  }
  align_fst_.SetStart(align_fst_.AddState());
  ws_states_.clear();
  ws_states_.resize(input_lists_.size());
  int base_idx = -1;
  for (int i = 0; i < input_lists_.size(); ++i) {
    if (word_counts_[i] == word_counts_[0]) {
      if (base_idx < 0) {
        for (int j = 1; j < word_counts_[i]; ++j) {
          ws_states_[i].push_back(align_fst_.AddState());
        }
        base_idx = i;
      } else {
        ws_states_[i] = ws_states_[base_idx];
      }
    } else if (word_counts_[i] > 1) {
      ws_states_[i].resize(word_counts_[i] - 1, -1);
    }
  }
}

void EnsembleFullString::RunEnsemble(int input_length) {
  SimpleAlign(input_length);
  BuildAlignWfst();
}

std::vector<std::pair<std::string, double>> EnsembleFullString::GetOutputs(
    int kbest) {
  return impl::GetOutputs(align_wfst_, syms_, kbest);
}

void EnsembleFiles::InitializeEnsembleFiles(
    const std::string &ifiles, const std::string &input_length_file) {
  inputs_ = impl::ReadInputsToEnsemble(ifiles);
  input_lengths_ = impl::ReadInputLengths(input_length_file, inputs_.size());
}

void EnsembleFiles::RunEnsembleAndOutput(int kbest, const std::string &ofile) {
  std::ofstream output_file;
  output_file.open(ofile);
  QCHECK(output_file) << "Cannot open " << ofile << " for writing.";
  for (int j = 0; j < inputs_.size(); ++j) {
    EnsembleFullString input_ensemble(inputs_[j]);
    input_ensemble.RunEnsemble(input_lengths_[j]);
    const auto kbest_outputs = input_ensemble.GetOutputs(kbest);
    for (int i = 0; i < kbest_outputs.size(); i++) {
      output_file << absl::StrCat(
          absl::StrJoin({std::to_string(j), kbest_outputs[i].first,
                         std::to_string(kbest_outputs[i].second)},
                        "\t"),
          "\n");
      QCHECK(output_file);
    }
  }
}

std::vector<std::pair<std::string, double>> KbestExtractor::GetBest(
    const std::vector<std::vector<std::pair<std::string, double>>> &str_arcs,
    int kbest) {
  SymbolTable syms;
  syms.AddSymbol("<epsilon>");
  const StdVectorFst fst = impl::MakeLattice(str_arcs, &syms);
  return impl::GetOutputs(fst, syms, kbest);
}

std::vector<std::vector<std::pair<std::string, double>>>
KbestExtractor::GetBests(int kbest) {
  std::vector<std::vector<std::pair<std::string, double>>> bests;
  bests.reserve(input_arcs_.size());
  for (const auto &input_arcs : input_arcs_) {
    bests.push_back(GetBest(input_arcs, kbest));
  }
  return bests;
}

void KbestExtractor::InitializeKbestExtractor(const std::string &ifile) {
  const auto &input_lines_status = nisaba::file::ReadLines(ifile, kMaxLine);
  QCHECK_OK(input_lines_status) << "Failed to read " << ifile;;
  InitializeKbestExtractor(input_lines_status.value());
}

void KbestExtractor::InitializeKbestExtractor(
    const std::vector<std::string> &input_lines) {
  if (!input_lines.empty()) {
    std::vector<std::vector<std::pair<std::string, double>>> str_arcs;
    std::vector<std::string> input_words;
    int last_idx = -1;
    int last_pos = -1;
    for (const std::string &str : input_lines) {
      const std::vector<std::string> seq =
          absl::StrSplit(str, '\t', absl::SkipEmpty());
      QCHECK_EQ(seq.size(), 5);
      int idx = std::stoi(seq[0]);
      int pos = std::stoi(seq[1]);
      if (idx != last_idx && last_idx >= 0) {
        input_arcs_.push_back(str_arcs);
        input_words_.push_back(absl::StrJoin(input_words, " "));
        input_index_.push_back(last_idx);
        str_arcs.clear();
        input_words.clear();
      }
      if (idx != last_idx || pos != last_pos) {
        input_words.push_back(seq[2]);
        str_arcs.push_back(std::vector<std::pair<std::string, double>>());
      }
      QCHECK_EQ(str_arcs.size(), pos + 1);
      str_arcs[pos].push_back(std::make_pair(seq[3], std::stod(seq[4])));
      last_idx = idx;
      last_pos = pos;
    }
    input_arcs_.push_back(str_arcs);
    input_words_.push_back(absl::StrJoin(input_words, " "));
    input_index_.push_back(last_idx);
  }
}

void KbestExtractor::RunExtractorAndOutput(const std::string &ofile, int kbest,
                                           bool show_score,
                                           bool show_full_input_string) {
  std::ofstream output_file;
  output_file.open(ofile);
  QCHECK(output_file) << "Cannot open " << ofile << " for writing.";
  for (int idx = 0; idx < input_arcs_.size(); ++idx) {
    const auto results = GetBest(input_arcs_[idx], kbest);
    for (const auto &result : results) {
      const std::string result_str =
          show_score ? absl::StrCat(result.first, "\t", result.second)
                     : result.first;
      const std::string input_str = show_full_input_string
                                        ? input_words_[idx]
                                        : std::to_string(input_index_[idx]);
      const std::string to_output =
          kbest > 1 ? absl::StrCat(input_str, "\t", result_str, "\n")
                    : absl::StrCat(result_str, "\n");
      output_file << to_output;
      QCHECK(output_file);
    }
  }
}

void KbestRejoiner::InitializeKbestRejoiner(absl::string_view ifile,
                                            absl::string_view split_file,
                                            int kbest) {
  const auto &input_lines_status = nisaba::file::ReadLines(ifile, kMaxLine);
  QCHECK_OK(input_lines_status) << "Failed to read " << ifile;
  const auto &split_lines_status =
      nisaba::file::ReadLines(split_file, kMaxLine);
  QCHECK_OK(split_lines_status) << "Failed to read " << split_file;
  std::vector<int> output_indices;
  output_indices.reserve(split_lines_status.value().size());
  for (const auto &str : split_lines_status.value()) {
    output_indices.push_back(std::stoi(str));
  }
  InitializeKbestRejoiner(input_lines_status.value(), output_indices, kbest);
}

void KbestRejoiner::InitializeKbestRejoiner(
    const std::vector<std::string> &input_lines,
    const std::vector<int> &output_indices, int kbest) {
  output_indices_ = output_indices;
  for (int i = 1; i < output_indices_.size(); ++i) {
    // Checks that output index is equal to last value plus either 0 or 1.
    QCHECK_GE(output_indices_[i], output_indices_[i - 1]);
    QCHECK_LE(output_indices_[i], output_indices_[i - 1] + 1);
  }
  int max_kbest = 0;
  if (!input_lines.empty()) {
    std::vector<std::vector<std::pair<std::string, double>>> curr_list(1);
    std::string last_input;
    int output_idx = 0;
    for (const std::string &input_line : input_lines) {
      std::vector<std::string> seq =
          absl::StrSplit(input_line, '\t', absl::SkipEmpty());
      QCHECK_EQ(seq.size(), 3) << input_line;
      if (!last_input.empty() && seq[0] != last_input) {
        QCHECK_LT(output_idx, output_indices_.size() - 1);
        if (output_indices_[output_idx] != output_indices_[output_idx + 1]) {
          for (const auto &curr_set : curr_list) {
            if (curr_set.size() > max_kbest) {
              max_kbest = curr_set.size();
            }
          }
          kbest_lists_.push_back(curr_list);
          curr_list.clear();
        }
        ++output_idx;
        curr_list.push_back(std::vector<std::pair<std::string, double>>());
      }
      last_input = seq[0];
      curr_list.back().push_back(std::make_pair(seq[1], std::stod(seq[2])));
    }
    kbest_lists_.push_back(curr_list);
    QCHECK_EQ(kbest_lists_.size(), output_indices_.back() + 1);
  }
  kbest_ = kbest > 0 ? kbest : max_kbest;
}

std::vector<std::pair<std::string, double>> KbestRejoiner::GetRejoinedList(
    absl::Span<const std::vector<std::pair<std::string, double>>> kbest_list)
    const {
  return impl::WhitespaceNorm(impl::RejoinList(kbest_list, kbest_));
}

std::vector<std::pair<std::string, double>> KbestRejoiner::GetRejoinedList(
    int idx) const {
  if (idx < NumKbestLists()) {
    return GetRejoinedList(kbest_lists_[idx]);
  } else {
    // List associated with this index is empty.
    return std::vector<std::pair<std::string, double>>();
  }
}

void KbestRejoiner::RunRejoinerAndOutput(const std::string &ofile) {
  std::ofstream output_file;
  output_file.open(ofile);
  QCHECK(output_file) << "Cannot open " << ofile << " for writing.";
  int output_idx = 0;
  for (const auto &kbest_list_entry : kbest_lists_) {
    const auto kbest_list = GetRejoinedList(kbest_list_entry);
    for (const auto &list_pair : kbest_list) {
      output_file << absl::StrCat(
          absl::StrJoin({std::to_string(output_idx), list_pair.first,
                         std::to_string(list_pair.second)},
                        "\t"),
          "\n");
      QCHECK(output_file);
    }
    ++output_idx;
  }
}

}  // namespace tools
}  // namespace translit
}  // namespace nisaba
