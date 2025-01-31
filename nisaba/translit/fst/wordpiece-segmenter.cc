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

#include "nisaba/translit/fst/wordpiece-segmenter.h"

#include <fstream>
#include <string>
#include <utility>
#include <vector>

#include "fst/arc.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/container/flat_hash_map.h"
#include "absl/log/check.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "nisaba/port/utf8_util.h"

constexpr char kWordInitPrefix[] = "▁";

namespace nisaba {
namespace translit {
namespace fst {

using ::fst::StdArc;
using ::fst::StdVectorFst;
using ::fst::SymbolTable;
using ::fst::kNoSymbol;

namespace impl {
namespace {

// Returns vector of best wordpiece lengths beginning at each string position.
absl::StatusOr<std::vector<int>> CalculateBestWordpieceLengths(
    const std::vector<std::vector<std::pair<std::string, int>>>
        &wordpiece_cands) {
  // All wordpieces begin at length 1, i.e., individual unicode codepoints.
  std::vector<int> wp_lengths(wordpiece_cands.size(), 1);
  int min_b = 0;
  while (min_b >= 0) {  // While wordpiece merges are found.
    min_b = -1;
    int min_l = -1;
    int min_r = -1;
    for (int b = 0; b < wp_lengths.size(); ++b) {  // For each position.
      int test_len = wp_lengths[b];  // Current length of wordpiece at b.
      if (test_len > 0 && test_len < wp_lengths.size() - b) {
        // Wordpiece exists here but covers less than the rest of the string.
        if (wp_lengths[b + test_len] < 1) {
          return absl::InternalError(
              "Second item for the merge does not exist.");
        }
        int new_len = test_len + wp_lengths[b + test_len];
        const auto &new_cand = wordpiece_cands[b][new_len];
        if (!new_cand.first.empty() && (min_b < 0 || new_cand.second < min_r)) {
          // Merge exists and has the top rank of all merges found so far.
          min_b = b;
          min_l = new_len;
          min_r = new_cand.second;
        }
      }
    }
    if (min_b >= 0) {  // Updates wordpiece lengths at merge positions.
      wp_lengths[min_b + wp_lengths[min_b]] = 0;  // Removes this wordpiece.
      wp_lengths[min_b] = min_l;  // Updates this wordpiece to new merged one.
    }
  }
  return wp_lengths;
}

// Returns vector of wordpieces given input candidates.
absl::StatusOr<std::vector<std::string>> GetWordpieceTokenization(
    const std::vector<std::vector<std::pair<std::string, int>>>
        &wordpiece_cands) {
  const auto wp_length_status = CalculateBestWordpieceLengths(wordpiece_cands);
  if (!wp_length_status.ok()) return wp_length_status.status();
  const auto &wp_lengths = wp_length_status.value();
  std::vector<std::string> wordpiece_tokenization;
  for (int b = 0; b < wp_lengths.size(); ++b) {
    if (wp_lengths[b] > 0) {  // Pushes wordpiece that begins at this position.
      wordpiece_tokenization.push_back(wordpiece_cands[b][wp_lengths[b]].first);
    }
  }
  return wordpiece_tokenization;
}

// Appends the best wordpiece tokenization from candidates to existing tokens.
absl::Status AppendBestWordpieces(
    const std::vector<std::vector<std::pair<std::string, int>>>
        &wordpiece_cands,
    std::vector<std::string> *wordpieces) {
  const auto tokenization_status = GetWordpieceTokenization(wordpiece_cands);
  if (!tokenization_status.ok()) return tokenization_status.status();
  const auto &wordpiece_tokenization = tokenization_status.value();
  wordpieces->insert(wordpieces->end(), wordpiece_tokenization.begin(),
                     wordpiece_tokenization.end());
  return absl::OkStatus();
}

}  // namespace
}  // namespace impl

absl::Status WordpieceSegmenter::InitWordpieces(
    const std::vector<std::string> &wp_symbols) {
  wordpiece_ranks_.clear();
  if (word_initial_prefix_.empty()) {
    // Requires a non-empty word initial prefix.
    word_initial_prefix_ = kWordInitPrefix;
  }
  for (int rank = 0; rank < wp_symbols.size(); ++rank) {
    wordpiece_ranks_.insert({wp_symbols[rank], rank});
  }
  return absl::OkStatus();
}

absl::Status WordpieceSegmenter::InitWordpieces(const std::string &wp_symbols) {
  std::vector<std::string> wordpieces;
  std::ifstream infile(wp_symbols);
  if (!infile.is_open()) {
    return absl::InternalError(
        absl::StrCat("Wordpiece file ", wp_symbols, " could not be accessed."));
  }
  std::string str;
  while (std::getline(infile, str)) {
    const std::vector<std::string> line_tokens =
        absl::StrSplit(str, utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty());
    if (!line_tokens.empty()) {
      wordpieces.push_back(line_tokens[0]);
    }
  }
  if (infile.is_open()) {
    infile.close();
  }
  return InitWordpieces(wordpieces);
}

bool WordpieceSegmenter::FindWordpiecePair(
    const std::string &cand_wordpiece,
    std::pair<std::string, int> *wordpiece_pair) const {
  const auto sym_result = wordpiece_ranks_.find(cand_wordpiece);
  if (sym_result != wordpiece_ranks_.end()) {
    *wordpiece_pair = std::make_pair(sym_result->first, sym_result->second);
    return true;
  }
  return false;
}

std::vector<std::vector<std::pair<std::string, int>>>
WordpieceSegmenter::ExtractWordpieceCands(const std::string &input_word) const {
  const std::vector<std::string> input_chars =
      utf8::StrSplitByChar(absl::StrCat(word_initial_prefix_, input_word));
  std::vector<std::vector<std::pair<std::string, int>>> wordpiece_cands(
      input_chars.size());
  for (int b = 0; b < input_chars.size(); ++b) {
    std::vector<std::pair<std::string, int>> b_wordpieces(
        input_chars.size() - b + 1, std::make_pair("", 0));
    std::string cand_wordpiece = "";
    for (int l = 1; l <= input_chars.size() - b; ++l) {
      absl::StrAppend(&cand_wordpiece, input_chars[b + l - 1]);
      std::pair<std::string, int> wordpiece_pair;
      bool found_wordpiece = FindWordpiecePair(cand_wordpiece, &wordpiece_pair);
      if (found_wordpiece) {
        b_wordpieces[l] = wordpiece_pair;
      } else if (l == 1) {
        // All single unicode codepoints should be present as wordpieces.
        b_wordpieces[l] = std::make_pair(input_chars[b], 0);
      }
    }
    wordpiece_cands[b] = b_wordpieces;
  }
  return wordpiece_cands;
}

absl::StatusOr<std::vector<std::string>>
WordpieceSegmenter::GetNoWhitespaceWordpieces(
    const std::vector<std::string> &input_words) const {
  std::vector<std::string> wordpieces;
  for (const auto &input_word : input_words) {
    const std::vector<std::vector<std::pair<std::string, int>>>
        wordpiece_cands = ExtractWordpieceCands(input_word);
    absl::Status append_status =
        impl::AppendBestWordpieces(wordpiece_cands, &wordpieces);
    if (!append_status.ok()) {
      return append_status;
    }
  }
  return wordpieces;
}

absl::StatusOr<std::vector<std::string>> WordpieceSegmenter::GetWordpieces(
    const std::string &input_str) const {
  return GetNoWhitespaceWordpieces(absl::StrSplit(
      input_str, utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty()));
}

absl::StatusOr<std::vector<std::string>> WordpieceSegmenter::GetWordpieces(
    absl::string_view input_sv) const {
  return GetNoWhitespaceWordpieces(absl::StrSplit(
      input_sv, utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty()));
}

absl::StatusOr<StdVectorFst> WordpieceSegmenter::GetWordpieceTransducer(
    const std::vector<int> &input_words, const SymbolTable &word_syms,
    const SymbolTable &wordpiece_syms, const std::string &wordpiece_unk) const {
  int unk_label = wordpiece_syms.Find(wordpiece_unk);
  const auto cost = StdArc::Weight::One();  // Everything is free!
  StdVectorFst fst;
  fst.SetStart(fst.AddState());
  fst.SetFinal(fst.Start(), cost);
  for (auto input_word : input_words) {
    const auto wordpiece_status = GetWordpieces(word_syms.Find(input_word));
    if (!wordpiece_status.ok()) return wordpiece_status.status();
    const auto &wordpieces = wordpiece_status.value();
    int curr_state = fst.Start();
    for (const auto &wordpiece : wordpieces) {
      int wordpiece_idx = wordpiece_syms.Find(wordpiece);
      if (wordpiece_idx == kNoSymbol) {
        // Wordpiece is not in vocabulary, hence replaced with <unk>.
        if (unk_label == kNoSymbol) {
          return absl::InternalError("Need OOV in wordpiece syms.");
        }
        wordpiece_idx = unk_label;
      }
      int next_state = fst.AddState();
      fst.AddArc(curr_state, StdArc(0, wordpiece_idx, cost, next_state));
      curr_state = next_state;
    }
    fst.AddArc(curr_state, StdArc(input_word, 0, cost, fst.Start()));
  }
  return fst;
}

absl::StatusOr<std::string> WordpieceSegmenter::TokenizeInput(
    const std::string &input_str) const {
  const auto wordpiece_status = GetWordpieces(input_str);
  if (!wordpiece_status.ok()) return wordpiece_status.status();
  return absl::StrJoin(wordpiece_status.value(), " ");
}

}  // namespace fst
}  // namespace translit
}  // namespace nisaba
