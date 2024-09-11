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

#include "nisaba/translit/fst/pairlm_decoder.h"

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "nisaba/port/integral_types.h"
#include "fst/arc-map.h"
#include "fst/arc.h"
#include "fst/arcsort.h"
#include "fst/cache.h"
#include "fst/closure.h"
#include "fst/compose.h"
#include "fst/concat.h"
#include "fst/determinize.h"
#include "fst/float-weight.h"
#include "fst/fst.h"
#include "fst/icu.h"
#include "fst/invert.h"
#include "fst/matcher.h"
#include "fst/project.h"
#include "fst/prune.h"
#include "fst/push.h"
#include "fst/rational.h"
#include "fst/reweight.h"
#include "fst/rmepsilon.h"
#include "fst/shortest-path.h"
#include "fst/symbol-table.h"
#include "fst/union.h"
#include "fst/vector-fst.h"
#include "fst/weight.h"
#include "ngram/ngram-count.h"
#include "absl/log/check.h"
#include "absl/log/log.h"
#include "absl/strings/numbers.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "absl/synchronization/mutex.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/utf8_util.h"
#include "nisaba/translit/fst/wordpiece-segmenter.h"
#include "nisaba/port/thread_pool.h"

using ::fst::ArcIterator;
using ::fst::ArcMap;
using ::fst::CacheOptions;
using ::fst::Closure;
using ::fst::CLOSURE_PLUS;
using ::fst::Compose;
using ::fst::ComposeFstOptions;
using ::fst::Concat;
using ::fst::Connect;
using ::fst::Invert;
using ::fst::kDelta;
using ::fst::kNoLabel;
using ::fst::kNoStateId;
using ::fst::LabelsToUTF8String;
using ::fst::Log64Weight;
using ::fst::LogArc;
using ::fst::LogToStdMapper;
using ::fst::MATCH_INPUT;
using ::fst::MATCH_NONE;
using ::fst::Matcher;
using ::fst::MATCHER_REWRITE_NEVER;
using ::fst::MutableArcIterator;
using ::fst::OLabelCompare;
using ::fst::PhiMatcher;
using ::fst::Project;
using ::fst::Prune;
using ::fst::Push;
using ::fst::REWEIGHT_TO_INITIAL;
using ::fst::RmEpsilon;
using ::fst::ShortestPath;
using ::fst::StdArc;
using ::fst::StdComposeFst;
using ::fst::StdFst;
using ::fst::StdILabelCompare;
using ::fst::StdToLogMapper;
using ::fst::StdVectorFst;
using ::fst::SymbolTable;
using ::fst::TopSort;
using ::fst::Union;
using ::fst::VectorFst;

namespace nisaba {
namespace translit {
namespace fst {
namespace {

constexpr int kPhiSymbol = -2;   // Symbol used for phi-arcs.
constexpr int kMaxWordCands = 100;     // Default for max_word_cands_.
constexpr float kWordCandThresh = 12;  // Default for word_cand_thresh_.
constexpr float kMinCandPosterior = 0.0;  // Default for min_cand_posterior_.
constexpr float kDefaultMixWeight = 0.0;  // Default pairlm_translit_weight_.
constexpr float kOOVCost = 10;         // Default for oov_cost_.
constexpr int kDefaultMaxParallelTokens = 4;  // Maximum number of cores to use.

}  // namespace

namespace impl {
namespace {

// Returns digital unicode codepoint for given single character string.
int GetUtf8Codepoint(absl::string_view letter_str) {
  char32 utf8_code;
  QCHECK(utf8::DecodeSingleUnicodeChar(letter_str, &utf8_code))
      << "Couldn't decode " << letter_str;
  return static_cast<int>(utf8_code);
}

bool Utf8Check(absl::string_view word_str) {
  for (absl::string_view letter_str : utf8::StrSplitByChar(word_str)) {
    char32 utf8_code;
    if (!utf8::DecodeSingleUnicodeChar(letter_str, &utf8_code)) {
      return false;
    }
  }
  return true;
}

// Returns the backoff state for a given state, also backoff cost if needed.
int GetBackoff(const StdVectorFst &lm_fst, int st, double *bo_cost) {
  ArcIterator<StdVectorFst> aiter(lm_fst, st);
  const StdArc arc = aiter.Value();
  if (arc.ilabel != 0) {
    if (bo_cost) *bo_cost = StdArc::Weight::Zero().Value();
    return kNoStateId;
  }
  if (bo_cost) *bo_cost = arc.weight.Value();
  return arc.nextstate;
}

// Returns the final cost of the state, following backoff if required. Sets the
// state's final cost to the calculated backoff value if state is non-final.
double GetStateFinalCost(StdVectorFst *lm_fst, int st) {
  if (st < 0) return StdArc::Weight::Zero().Value();
  if (lm_fst->Final(st) != StdArc::Weight::Zero())
    return lm_fst->Final(st).Value();
  double fcost;
  int backoff_state = GetBackoff(*lm_fst, st, &fcost);
  fcost += GetStateFinalCost(lm_fst, backoff_state);
  lm_fst->SetFinal(st, fcost);
  return fcost;
}

// Converts given language model into one that works with PhiMatcher.
void MakePhiMatcherLM(StdVectorFst *lm_fst) {
  for (int st = 0; st < lm_fst->NumStates(); ++st) {
    if (lm_fst->Final(st) == StdArc::Weight::Zero() && st != lm_fst->Start()) {
      // Updates final cost for non-final states using backoff.
      GetStateFinalCost(lm_fst, st);
    }
  }
  for (int st = 0; st < lm_fst->NumStates(); ++st) {
    // Updates backoff arc label to kPhiSymbol.
    MutableArcIterator<StdVectorFst> aiter(lm_fst, st);
    StdArc arc = aiter.Value();
    if (arc.ilabel == 0) {
      arc.ilabel = arc.olabel = kPhiSymbol;
      aiter.SetValue(arc);
    }
  }
  ArcSort(lm_fst, StdILabelCompare());
}

// Builds transducers from pair symbols, mapping input symbols to pairs and
// pairs to output symbols. Pair symbols are assumed to be of the form N;M where
// N and M are decimal unicode values. If the invert_pairlm bool is true, then M
// is treated as the input symbol and N the output symbol; otherwise N is input
// and M output. If the flip_transducer bool is true, then the resulting
// transducer is inverted.
StdVectorFst BuildUnicodeToPairTransducer(const SymbolTable *syms,
                                          bool invert_pairlm,
                                          bool flip_transducer) {
  QCHECK(syms != nullptr) << "Symbol table is empty";
  StdVectorFst unicode_to_pair_fst;
  const int input_idx = invert_pairlm ? 1 : 0;
  const int single_state = unicode_to_pair_fst.AddState();
  unicode_to_pair_fst.SetStart(single_state);
  unicode_to_pair_fst.SetFinal(single_state, 0.0);
  for (const auto &sym : *syms) {
    if (sym.Label() > 0) {
      // Iterates through all symbols other than <epsilon>.
      const std::string symbol = sym.Symbol();
      const std::vector<absl::string_view> pairs =
          absl::StrSplit(symbol, ';', absl::SkipEmpty());
      if (pairs.size() != 2) {
        // If symbol is not of the form N;M (e.g., <UNK>).
        LOG(WARNING) << "Symbol table contained non-pair symbol (" << symbol
                     << "), which will be ignored.";
      } else {
        int32_t isym;
        QCHECK(absl::SimpleAtoi(pairs[input_idx], &isym))
            << "Cannot convert " << std::string(pairs[input_idx]) << " to int";
        unicode_to_pair_fst.AddArc(
            single_state, StdArc(isym, sym.Label(), 0.0, single_state));
      }
    }
  }
  if (flip_transducer) Invert(&unicode_to_pair_fst);
  ArcSort(&unicode_to_pair_fst, StdILabelCompare());
  return unicode_to_pair_fst;
}

// Creates a linear FST with unicode codepoints as arc labels for word.
// Takes FST to modify as argument, to allow also building word trie, i.e., add
// a linear path from start state of existing FST.
void WordToFst(absl::string_view input_word, StdVectorFst *string_fst) {
  QCHECK_NE(string_fst, nullptr);
  int curr_state = string_fst->Start();
  QCHECK_GE(curr_state, 0);  // Provided string_fst must have start state.
  for (absl::string_view letter_str : utf8::StrSplitByChar(input_word)) {
    // Splits word into individual codepoints.
    const int token_idx = GetUtf8Codepoint(letter_str);
    const int next_state = string_fst->AddState();
    string_fst->AddArc(curr_state,
                       StdArc(token_idx, token_idx, 0.0, next_state));
    curr_state = next_state;
  }
  string_fst->SetFinal(curr_state, 0.0);
}

// Reads the string from ilabels of linear (string automaton) and returns cost.
double GetTextString(const StdVectorFst &best_pair_strings, int curr_state,
                     std::string *new_symbol) {
  double cost = 0.0;
  std::vector<int> text_labels;
  while (best_pair_strings.NumArcs(curr_state) > 0) {
    QCHECK_EQ(best_pair_strings.NumArcs(curr_state), 1);
    ArcIterator<StdVectorFst> aiter(best_pair_strings, curr_state);
    const StdArc arc = aiter.Value();
    if (arc.ilabel != 0) {
      // Skips any epsilon arcs, should they occur.
      text_labels.push_back(arc.ilabel);
    }
    cost += arc.weight.Value();
    curr_state = arc.nextstate;
  }
  cost += best_pair_strings.Final(curr_state).Value();
  QCHECK(LabelsToUTF8String(text_labels, new_symbol));
  return cost;
}

// Applies weight pushing in log semiring, then returns fst to std semiring.
// Optionally determinizes the input FST as well.
void PushInLogSemiring(StdVectorFst *fst, bool determinize = false) {
  VectorFst<LogArc> log_fst;
  ArcMap(*fst, &log_fst, StdToLogMapper());
  if (determinize) {
    // Determinizes in log semiring, hence log-summing probabilities.
    Determinize(log_fst, &log_fst);
  }
  Push(&log_fst, REWEIGHT_TO_INITIAL, kDelta,
       /*remove_total_weight=*/true);
  ArcMap(log_fst, fst, LogToStdMapper());
}

// Derives the cutoff score for k_best extraction from the state.
std::vector<bool> ApplyArcScoreThresh(const StdVectorFst &fst, int state,
                                      int k_best, double min_cand_posterior,
                                      const std::vector<double> *costs) {
  QCHECK_LT(k_best, fst.NumArcs(state));
  std::vector<bool> keep_arc(fst.NumArcs(state), false);
  std::vector<std::pair<double, size_t>> scores;
  size_t arc_idx = 0;
  for (ArcIterator<StdVectorFst> aiter(fst, state); !aiter.Done();
       aiter.Next()) {
    const StdArc arc = aiter.Value();
    QCHECK_GT(arc.ilabel, 0);
    if (costs != nullptr) {
      QCHECK_LT(arc.ilabel, costs->size());
      scores.push_back(std::make_pair((*costs)[arc.ilabel], arc_idx));
    } else {
      scores.push_back(std::make_pair(arc.weight.Value(), arc_idx));
    }
    ++arc_idx;
  }
  std::sort(scores.begin(), scores.end());
  for (int i = 0; i < k_best; ++i) {
    if (i == 0 || min_cand_posterior <= 0.0 ||
        scores[i].first <= -log(min_cand_posterior)) {
      // Always takes the lowest cost item; otherwise only adds if cost less
      // than -log(min_cand_posterior) threshold.
      arc_idx = scores[i].second;
      QCHECK_GE(arc_idx, 0);
      QCHECK_LT(arc_idx, keep_arc.size());
      keep_arc[arc_idx] = true;
    }
  }
  return keep_arc;
}

// Returns the next state in the trie if label matches, otherwise kNoStateId.
int GetNextTrieState(const StdVectorFst &word_piece_trie_fst, int curr_state,
                     int label) {
  Matcher<StdFst> matcher(word_piece_trie_fst, MATCH_INPUT);
  matcher.SetState(curr_state);
  if (matcher.Find(label)) {
    const StdArc arc = matcher.Value();
    return arc.nextstate;
  }
  return kNoStateId;
}

// Returns vector of characters that as a string match an item in the lexicon.
std::vector<int> GetMatchedTokens(
    const std::vector<std::string> &new_sym_letters,
    int string_start_position, const StdVectorFst &word_piece_trie_fst,
    int curr_state) {
  int match_length = 0;
  std::vector<int> matched_items;
  for (int i = string_start_position; i < new_sym_letters.size(); ++i) {
    int token_idx = GetUtf8Codepoint(new_sym_letters[i]);
    int next_state =
        GetNextTrieState(word_piece_trie_fst, curr_state, token_idx);
    if (next_state >= 0) {
      curr_state = next_state;
      matched_items.push_back(token_idx);
      if (word_piece_trie_fst.Final(curr_state) != StdArc::Weight::Zero()) {
        // Extends match length only if destination state is a final state.
        match_length = i - string_start_position + 1;
      }
    } else {
      break;
    }
  }
  if (match_length < matched_items.size()) {
    matched_items.resize(match_length);
  }
  return matched_items;
}

// Produces a two-state transducer with the same arcs as the incoming
// lattice_fst, which effectively removes the context.
StdVectorFst RemoveContext(const StdVectorFst &lattice_fst) {
  StdVectorFst contextless_fst;
  const int start_st = contextless_fst.AddState();
  contextless_fst.SetStart(start_st);
  const int final_st = contextless_fst.AddState();
  contextless_fst.SetFinal(final_st, 0.0);
  for (int st = 0; st < lattice_fst.NumStates(); ++st) {
    for (ArcIterator<StdVectorFst> aiter(lattice_fst, st); !aiter.Done();
         aiter.Next()) {
      const StdArc arc = aiter.Value();
      contextless_fst.AddArc(
          start_st, StdArc(arc.ilabel, arc.olabel, arc.weight, final_st));
    }
  }
  return contextless_fst;
}

}  // namespace
}  // namespace impl

bool PairLMDecoder::CheckCache(absl::string_view input_word) const {
  absl::ReaderMutexLock lock(&mutex_);
  return global_word_transliteration_cache_.contains(input_word);
}

void PairLMDecoder::InitializePairLMDecoder(
    const PairLMDecoderOptions &pairlm_config) {
  InitializeTranslitModel(pairlm_config);
  InitializeLanguageModel(pairlm_config);
  epsilon_symbol_ = pairlm_config.epsilon_symbol().empty()
                        ? symbols::kEpsilonSymbol
                        : pairlm_config.epsilon_symbol();
  add_to_cache_ =
      pairlm_config.has_add_to_cache() ? pairlm_config.add_to_cache() : true;
  max_parallel_tokens_ = pairlm_config.has_max_parallel_tokens()
                             ? pairlm_config.max_parallel_tokens()
                             : kDefaultMaxParallelTokens;
  oov_cost_ =
      pairlm_config.has_oov_cost() ? pairlm_config.oov_cost() : kOOVCost;
  InitializeExternalTransliterations(pairlm_config);
  max_word_cands_ = pairlm_config.has_max_word_cands()
                        ? pairlm_config.max_word_cands()
                        : kMaxWordCands;
  word_cand_thresh_ = pairlm_config.has_word_cand_thresh()
                          ? pairlm_config.word_cand_thresh()
                          : kWordCandThresh;
  min_cand_posterior_ = pairlm_config.has_min_cand_posterior()
                            ? pairlm_config.min_cand_posterior()
                            : kMinCandPosterior;
  pairlm_translit_weight_ = kDefaultMixWeight;
}

void PairLMDecoder::InitializeTranslitModel(
    const PairLMDecoderOptions &pairlm_config) {
  if (!pairlm_config.pairlm_file().empty()) {
    // Reads in pair LM transliteration model and builds related transducers.
    translit_fst_.reset(StdVectorFst::Read(pairlm_config.pairlm_file()));
    QCHECK(translit_fst_ != nullptr)
        << "Failed to read pair-LM translit model from "
        << pairlm_config.pairlm_file();
    translit_fst_is_transducer_ = pairlm_config.pairlm_is_transducer();
    if (translit_fst_is_transducer_) {
      unicode_to_pair_fst_ = nullptr;
      pair_to_unicode_fst_ = nullptr;
      if (pairlm_config.invert_pairlm()) {
        Invert(translit_fst_.get());
      }
    } else {
      impl::MakePhiMatcherLM(translit_fst_.get());
      unicode_to_pair_fst_ =
          std::make_unique<StdVectorFst>(impl::BuildUnicodeToPairTransducer(
              translit_fst_->InputSymbols(), pairlm_config.invert_pairlm(),
              /*flip_transducer=*/false));
      pair_to_unicode_fst_ =
          std::make_unique<StdVectorFst>(impl::BuildUnicodeToPairTransducer(
              translit_fst_->InputSymbols(), !pairlm_config.invert_pairlm(),
              /*flip_transducer=*/true));
    }
    InitializeInputCharacterSet();
  }
}

void PairLMDecoder::InitializeLanguageModel(
    const PairLMDecoderOptions &pairlm_config) {
  if (!pairlm_config.lm_file().empty()) {
    // Reads in language model FST and initializes related auxiliary resources.
    lm_fst_.reset(StdVectorFst::Read(pairlm_config.lm_file()));
    QCHECK(lm_fst_ != nullptr) << "Failed to read LM FST from "
                               << pairlm_config.lm_file();
    impl::MakePhiMatcherLM(lm_fst_.get());
    if (pairlm_config.apply_closure_to_lm()) {
      Closure(lm_fst_.get(), CLOSURE_PLUS);
      ArcSort(lm_fst_.get(), StdILabelCompare());
    }
    apply_lm_at_word_level_ = pairlm_config.apply_lm_at_word_level();
    const absl::string_view oov_symbol = pairlm_config.oov_symbol().empty()
                                         ? symbols::kUnknownSymbol
                                         : pairlm_config.oov_symbol();
    lm_oov_index_ = lm_fst_->InputSymbols()->Find(oov_symbol);
    if (pairlm_config.has_word_piece_model()) {
      auto wpm = std::make_unique<WordpieceSegmenter>(
          pairlm_config.word_piece_word_initial_prefix());
      QCHECK_OK(wpm->InitWordpieces(pairlm_config.word_piece_model()))
          << "Failed to read wordpiece model from "
          << pairlm_config.word_piece_model();
      wpm_ = std::move(wpm);
    } else if (pairlm_config.has_word_piece_internal_prefix() &&
               !pairlm_config.word_piece_internal_prefix().empty()) {
      // Only follow word_piece_internal_prefix methods if no word piece model.
      // Builds a special purpose word piece trie for these cases. Included for
      // backwards compatibility.
      InitializeWordPieceTrie(pairlm_config);
    }
  }
}

void PairLMDecoder::InitializeWordPieceTrie(
    const PairLMDecoderOptions &pairlm_config) {
  word_piece_internal_prefix_ = pairlm_config.word_piece_internal_prefix();
  QCHECK(!word_piece_internal_prefix_.empty());
  word_piece_trie_fst_ = std::make_unique<StdVectorFst>();
  word_piece_trie_fst_->SetStart(word_piece_trie_fst_->AddState());
  for (const auto &sym : *lm_fst_->InputSymbols()) {
    if (sym.Label() > 0 && sym.Label() != lm_oov_index_) {
      impl::WordToFst(sym.Symbol(), word_piece_trie_fst_.get());
    }
  }
  Determinize(*word_piece_trie_fst_, word_piece_trie_fst_.get());
  ArcSort(word_piece_trie_fst_.get(), StdILabelCompare());

  // Finds the internal state in the trie corresponding to internal prefix.
  word_internal_cands_to_lm_start_state_ = word_piece_trie_fst_->Start();
  for (absl::string_view prefix_letter : utf8::StrSplitByChar(
           word_piece_internal_prefix_)) {
    // Finds destination state for each letter in the prefix, checks non-zero.
    word_internal_cands_to_lm_start_state_ = impl::GetNextTrieState(
        *word_piece_trie_fst_, word_internal_cands_to_lm_start_state_,
        impl::GetUtf8Codepoint(prefix_letter));
    QCHECK_GE(word_internal_cands_to_lm_start_state_, 0);
  }
}

void PairLMDecoder::InitializeInputCharacterSet() {
  // Looks at input side of model transducer, which is the translit_fst_ itself
  // if the bool translit_fst_is_transducer_ is set to true; otherwise the input
  // side of unicode_to_pair_fst_.
  const StdVectorFst *input_transducer = translit_fst_is_transducer_
                                             ? translit_fst_.get()
                                             : unicode_to_pair_fst_.get();
  if (input_transducer != nullptr) {
    for (StdArc::StateId s = 0; s < input_transducer->NumStates(); ++s) {
      for (ArcIterator<StdVectorFst> aiter(*input_transducer, s); !aiter.Done();
           aiter.Next()) {
        const StdArc arc = aiter.Value();
        if (arc.ilabel > 0 && !covered_input_chars_.contains(arc.ilabel)) {
          // Adds new non-epsilon unicode codepoints to the hash set.
          covered_input_chars_.insert(arc.ilabel);
        }
      }
    }
  }
}

void PairLMDecoder::InitializeExternalTransliterations(
    const PairLMDecoderOptions &pairlm_config) {
  if (!pairlm_config.translit_cands_file().empty()) {
    // Reads in externally provided word transliterations. Assumes three column
    // format: input word; transliteration; negative log cost.
    const auto read_lines_status = file::ReadLines(
        pairlm_config.translit_cands_file(), kMaxLineLength);
    QCHECK_OK(read_lines_status) << "Failed to read lines from "
                                 << pairlm_config.translit_cands_file();
    const std::vector<std::string> &input_lines = read_lines_status.value();
    for (const auto &input_line : input_lines) {
      const std::vector<absl::string_view> input_cols =
          absl::StrSplit(input_line, '\t', absl::SkipEmpty());
      QCHECK_EQ(input_cols.size(), 3);
      double cost;
      QCHECK(absl::SimpleAtod(input_cols[2], &cost))
          << "Cannot covert cost to double in " << input_line;
      if (impl::Utf8Check(input_cols[0]) && impl::Utf8Check(input_cols[1])) {
        // Checks that input and output decompose into valid UTF8 strings.
        global_word_transliteration_cache_[input_cols[0]][input_cols[1]] = cost;

        if (pairlm_config.translit_cands_override()) {
          mix_overrides_.emplace(input_cols[0]);
        }
      }
    }

    if (translit_fst_ != nullptr) {
      // Initializes tracking for mixing, only needed if both precomputed and
      // fst transliterations. Sets mixture cost for Fst transliterations when
      // combining with external transliterations.  When mixing \lambda p_f + (1
      // - \lambda) p_e where p_f is the Fst probability and p_e is the external
      // probability, we weight the -log Fst cost by -log(\lambda/(1-\lambda)).
      if (pairlm_config.has_pairlm_translit_weight()) {
        double lambda = pairlm_config.pairlm_translit_weight();
        lambda /= 1.0 - lambda;
        pairlm_translit_weight_ = -log(lambda);
      } else {
        pairlm_translit_weight_ = kDefaultMixWeight;
      }
    }
  }
}

StdVectorFst PairLMDecoder::GetWordTransliterations(
    absl::string_view input_word, bool prune_lattice) const {
  StdVectorFst pair_lm_composed_output;
  if (translit_fst_ == nullptr) {
    // Returns an empty Fst if translit_fst_ is not available.
    return pair_lm_composed_output;
  }
  // Encodes string as linear fst and composes with unicode_to_pair fst to
  // create lattice of possible pair strings.
  StdVectorFst string_fst;
  string_fst.SetStart(string_fst.AddState());
  impl::WordToFst(input_word, &string_fst);
  if (translit_fst_is_transducer_) {
    Compose(string_fst, *translit_fst_, &pair_lm_composed_output);
  } else {
    StdVectorFst pair_lattice;
    Compose(string_fst, *unicode_to_pair_fst_, &pair_lattice);
    Project(&pair_lattice, ::fst::ProjectType::OUTPUT);
    ArcSort(&pair_lattice, OLabelCompare<StdArc>());

    // Composes lattice of pair strings with pair language model.
    StdVectorFst pair_lm_composed_fst;
    pair_lm_composed_fst = StdComposeFst(
        pair_lattice, *translit_fst_,
        ComposeFstOptions<StdArc, PhiMatcher<Matcher<StdFst>>>(
            CacheOptions(),
            new PhiMatcher<Matcher<StdFst>>(pair_lattice, MATCH_NONE, kNoLabel),
            new PhiMatcher<Matcher<StdFst>>(*translit_fst_, MATCH_INPUT,
                                            kPhiSymbol, true,
                                            MATCHER_REWRITE_NEVER)));

    // Composes result with pair_to_unicode fst and prunes to produce pruned
    // lattice of unicode strings.
    Compose(pair_lm_composed_fst, *pair_to_unicode_fst_,
            &pair_lm_composed_output);
  }
  if (prune_lattice) {
    Prune(&pair_lm_composed_output, /*weight_threshold=*/word_cand_thresh_);
  }
  Project(&pair_lm_composed_output, ::fst::ProjectType::OUTPUT);
  return pair_lm_composed_output;
}

double PairLMDecoder::ParseCandWordPiece(absl::string_view new_symbol,
                                         std::vector<int> *lm_syms) const {
  double cost = 0.0;
  const std::vector<std::string> new_sym_letters = utf8::StrSplitByChar(
      new_symbol);
  int string_position = 0;
  int curr_state = word_piece_trie_fst_->Start();
  std::string prefix = "";  // Gets set to word internal prefix later.
  while (string_position < new_sym_letters.size()) {
    const std::vector<int> text_labels = impl::GetMatchedTokens(
        new_sym_letters, string_position, *word_piece_trie_fst_, curr_state);
    int lm_sym;
    if (text_labels.empty()) {
      // No input symbols matched, so use <unk> symbol in lm_fst_ and advance by
      // one character.  Also adds to the cost as parameterized.
      lm_sym = lm_oov_index_;
      ++string_position;
      cost += oov_cost_;
    } else {
      std::string word_piece_str;
      QCHECK(LabelsToUTF8String(text_labels, &word_piece_str));
      lm_sym =
          lm_fst_->InputSymbols()->Find(absl::StrCat(prefix, word_piece_str));
      string_position += text_labels.size();
    }
    QCHECK_GT(lm_sym, 0);  // Checks that symbol is found and not <epsilon>.
    lm_syms->push_back(lm_sym);
    curr_state = word_internal_cands_to_lm_start_state_;
    if (prefix.empty()) {
      // Sets prefix for word internal word pieces.
      prefix = word_piece_internal_prefix_;
    }
  }
  return cost;
}

double PairLMDecoder::SegmentCandWordPiece(absl::string_view new_symbol,
                                           std::vector<int> *lm_syms) const {
  double cost = 0;
  const auto wp_status = wpm_->GetWordpieces(new_symbol);
  QCHECK_OK(wp_status);
  for (const auto &wordpiece : wp_status.value()) {
    int lm_sym = lm_fst_->InputSymbols()->Find(wordpiece);
    if (lm_sym < 0) {
      lm_sym = lm_oov_index_;
      cost += oov_cost_;
    } else {
      QCHECK_GT(lm_sym, 0);  // Checks that found symbol is not epsilon.
    }
    lm_syms->push_back(lm_sym);
  }
  return cost;
}

void PairLMDecoder::AddToCandsToLMFst(absl::string_view new_symbol,
                                      int cand_sym,
                                      TranslitContext &fst_params) {
  if (lm_fst_ == nullptr) return;
  double cost = 0.0;
  std::vector<int> lm_syms;
  if (wpm_ != nullptr) {
    cost = SegmentCandWordPiece(new_symbol, &lm_syms);
  } else if (word_piece_trie_fst_ != nullptr) {
    // Legacy word piece methods included for backwards compatibility.
    cost = ParseCandWordPiece(new_symbol, &lm_syms);
  } else {
    int lm_sym = lm_fst_->InputSymbols()->Find(new_symbol);
    if (lm_sym < 0) {
      // Assigns OOV symbol and cost if token not found in LM.
      lm_syms.push_back(lm_oov_index_);
      cost += oov_cost_;
    } else {
      lm_syms.push_back(lm_sym);
    }
  }
  int cand_ilabel = cand_sym;
  int curr_state = fst_params.cands_to_lm_fst->Start();
  for (int i = 0; i < lm_syms.size(); ++i) {
    int dest_state;
    if (i < lm_syms.size() - 1) {
      dest_state = fst_params.cands_to_lm_fst->AddState();
    } else {
      dest_state = fst_params.cands_to_lm_fst->Start();
    }
    fst_params.cands_to_lm_fst->AddArc(
        curr_state, StdArc(cand_ilabel, lm_syms[i], cost, dest_state));
    curr_state = dest_state;
    cand_ilabel = 0;
    cost = 0.0;  // Accrues cost only on initial arc.
  }
}

void PairLMDecoder::AddCandSymArc(absl::string_view new_symbol, double cost,
                                  int destination_state,
                                  TranslitContext &fst_params,
                                  StdVectorFst *word_transliterations) {
  // Look for candidate symbol in the symbol list, add if not there.
  int cand_sym = fst_params.cand_syms.Find(new_symbol);
  if (cand_sym == ::fst::kNoSymbol) {
    cand_sym = fst_params.cand_syms.AddSymbol(new_symbol);
    AddToCandsToLMFst(new_symbol, cand_sym, fst_params);
  }
  word_transliterations->AddArc(
      word_transliterations->Start(),
      StdArc(cand_sym, cand_sym, cost, destination_state));
}

std::vector<std::string> PairLMDecoder::SegmentCoveredChars(
    absl::string_view input_word) const {
  std::vector<std::string> input_word_tokens;
  if (!input_word.empty()) {
    // Splits word into individual unicode codepoints.
    const std::vector<std::string> input_codepoints = utf8::StrSplitByChar(
        input_word);
    std::vector<bool> covered_codepoints(input_codepoints.size());
    int non_covered_count = 0;
    for (int i = 0; i < input_codepoints.size(); ++i) {
      covered_codepoints[i] = covered_input_chars_.contains(
          impl::GetUtf8Codepoint(input_codepoints[i]));
      if (!covered_codepoints[i]) non_covered_count++;
    }
    if (non_covered_count == 0 ||
        non_covered_count == input_codepoints.size()) {
      // No segmentation required, so can return empty vector, saves time.
      return input_word_tokens;
    }
    std::string this_token =
        input_codepoints[0];  // Initializes token with first codepoint.
    for (int i = 1; i < input_codepoints.size(); ++i) {
      if (covered_codepoints[i] != covered_codepoints[i - 1]) {
        // Segments where coverage bool changes value.
        input_word_tokens.push_back(this_token);
        this_token = input_codepoints[i];
      } else {
        // Appends codepoint to current token since they match in coverage.
        absl::StrAppend(&this_token, input_codepoints[i]);
      }
    }
    input_word_tokens.push_back(this_token);
  }
  return input_word_tokens;
}

StdVectorFst PairLMDecoder::TransliterateSegmentedWord(
    const std::vector<std::string> &segmented_word, int k_best,
    TranslitContext &fst_params) {
  StdVectorFst translit_result;
  if (!segmented_word.empty()) {
    // Transliterates each segment as an independent word.
    StdVectorFst transliterated_lattice =
        TransliterateUnsegmentedWord(segmented_word[0], k_best, fst_params);
    for (int i = 1; i < segmented_word.size(); ++i) {
      // Concatenates results from each token into full lattice.
      Concat(
          &transliterated_lattice,
          TransliterateUnsegmentedWord(segmented_word[i], k_best, fst_params));
    }
    // Extracts final k-best from resulting concatenated lattice and converts to
    // single tokens to be returned in final lattice.
    StdVectorFst best_concat_strings;
    ShortestPath(transliterated_lattice, &best_concat_strings, k_best,
                 /*unique=*/true);
    translit_result.SetStart(translit_result.AddState());
    int word_final_state = translit_result.AddState();
    translit_result.SetFinal(word_final_state, 0.0);
    int curr_state = best_concat_strings.Start();
    QCHECK_GE(curr_state, 0) << "Each segment should have non-empty output.";
    for (ArcIterator<StdVectorFst> aiter(best_concat_strings, curr_state);
         !aiter.Done(); aiter.Next()) {
      // Initializes new_symbol and cost with first arc in path, then
      // concatenates along the path. Only non-epsilon labels added to
      // new_symbol.
      const StdArc arc = aiter.Value();
      std::string new_symbol =
          arc.ilabel > 0 ? fst_params.cand_syms.Find(arc.ilabel) : "";
      double cost = arc.weight.Value();
      int next_state = arc.nextstate;
      while (best_concat_strings.NumArcs(next_state) > 0) {
        QCHECK_EQ(best_concat_strings.NumArcs(next_state), 1);
        ArcIterator<StdVectorFst> next_aiter(best_concat_strings, next_state);
        const StdArc next_arc = next_aiter.Value();
        if (next_arc.ilabel > 0) {
          // Skips any epsilon arcs, should they occur.
          absl::StrAppend(&new_symbol,
                          fst_params.cand_syms.Find(next_arc.ilabel));
        }
        cost += next_arc.weight.Value();
        next_state = next_arc.nextstate;
      }
      cost += best_concat_strings.Final(next_state).Value();
      fst_params.mutex.Lock();
      AddCandSymArc(new_symbol, cost, word_final_state, fst_params,
                    &translit_result);
      fst_params.mutex.Unlock();
    }
  }
  return translit_result;
}

void PairLMDecoder::ExtractCachedWordTransliterations(
    absl::string_view input_word, TranslitContext &fst_params,
    ::fst::StdVectorFst &cached) {
  mutex_.ReaderLock();
  const auto cached_pairs = global_word_transliteration_cache_.at(input_word);
  mutex_.ReaderUnlock();
  for (const auto &pair : cached_pairs) {
    AddCandSymArc(pair.first, pair.second,
                  /*destination_state=*/1, fst_params, &(cached));
  }
  impl::PushInLogSemiring(&(cached),
                          /*determinize=*/true);
}

StdVectorFst PairLMDecoder::TransliterateUnsegmentedWord(
    absl::string_view input_word, int k_best, TranslitContext &fst_params) {
  // Extracts k-best transliterations and adds them to the fst.
  StdVectorFst transliterated_lattice =
      GetWordTransliterations(input_word, /*prune_lattice=*/k_best > 1);
  StdVectorFst best_pair_strings;
  ShortestPath(transliterated_lattice, &best_pair_strings, k_best,
               /*unique=*/true);
  const bool vocab_check = CheckCache(input_word);
  if (best_pair_strings.Start() < 0 && vocab_check) {
    // No transliteration from pair LM (empty result) but some external ones.
    // Returns cached word transliterations.
    absl::MutexLock lock(&fst_params.mutex);
    StdVectorFst cached;
    cached.SetStart(cached.AddState());
    cached.SetFinal(cached.AddState(), 0.0);
    ExtractCachedWordTransliterations(input_word, fst_params, cached);
    fst_params.mixed_with_precomputed.insert_or_assign(input_word, true);
    fst_params.word_transliteration_cache.insert_or_assign(input_word, cached);
    return cached;
  }
  StdVectorFst word_transliterations;
  word_transliterations.SetStart(word_transliterations.AddState());
  int word_final_state = word_transliterations.AddState();
  word_transliterations.SetFinal(word_final_state, 0.0);
  int curr_state = best_pair_strings.Start();
  if (curr_state < 0) {
    // No valid transliterations, outputs input word output unchanged.
    absl::MutexLock lock(&fst_params.mutex);
    AddCandSymArc(input_word, /*cost=*/0.0, word_final_state, fst_params,
                  &word_transliterations);
  } else if (best_pair_strings.NumArcs(curr_state) == 1) {
    // Just one path, start that path at start state.
    std::string new_symbol;
    const double cost =
        impl::GetTextString(best_pair_strings, curr_state, &new_symbol);
    fst_params.mutex.Lock();
    AddCandSymArc(new_symbol, cost, word_final_state, fst_params,
                  &word_transliterations);
    fst_params.mutex.Unlock();
  } else {
    // Multiple paths, start each at destination of epsilon transition w/cost.
    for (ArcIterator<StdVectorFst> aiter(best_pair_strings, curr_state);
         !aiter.Done(); aiter.Next()) {
      const StdArc arc = aiter.Value();
      std::string new_symbol;
      const double cost =
          arc.weight.Value() +
          impl::GetTextString(best_pair_strings, arc.nextstate, &new_symbol);
      fst_params.mutex.Lock();
      AddCandSymArc(new_symbol, cost, word_final_state, fst_params,
                    &word_transliterations);
      fst_params.mutex.Unlock();
    }
  }
  return word_transliterations;
}

StdVectorFst PairLMDecoder::TransliterateWord(absl::string_view input_word,
                                              int k_best,
                                              TranslitContext &fst_params) {
  fst_params.mutex.Lock();
  // We haven't seen this word, so initialize it in indexes.
  if (!fst_params.word_transliteration_cache.contains(input_word)) {
    // Adds input_word since it has not been seen before.
    fst_params.input_syms.AddSymbol(input_word);
    // Add premixed.
    mutex_.ReaderLock();
    const bool override = mix_overrides_.contains(input_word);
    mutex_.ReaderUnlock();
    fst_params.mixed_with_precomputed.insert_or_assign(input_word, override);
    //  Add global cache.
    StdVectorFst cached;
    cached.SetStart(cached.AddState());
    cached.SetFinal(cached.AddState(), 0.0);
    const bool vocab_check = CheckCache(input_word);
    if (vocab_check) {
      ExtractCachedWordTransliterations(input_word, fst_params, cached);
    }
    fst_params.word_transliteration_cache.insert_or_assign(input_word, cached);
  }
  fst_params.mutex.Unlock();
  fst_params.mutex.ReaderLock();
  const bool no_fst_decoding_required =
      CheckCache(input_word) &&
      fst_params.mixed_with_precomputed.at(input_word);
  fst_params.mutex.ReaderUnlock();
  if (no_fst_decoding_required) {
    // If the word is in the global cache and is marked as already mixed (or not
    // requiring mixture), no need to mix or cache again, so returns cached word
    // transliterations right away.
    absl::ReaderMutexLock lock(&fst_params.mutex);
    return fst_params.word_transliteration_cache.at(input_word);
  }

  // Obtain up to k_best additional transliterations from PairLM.
  const std::vector<std::string> segmented_input_word =
      SegmentCoveredChars(input_word);
  StdVectorFst word_transliterations;
  if (segmented_input_word.size() > 1) {
    // There are non-covered segments in the input_word. Transliterates multiple
    // segments independently and concatenates.
    word_transliterations =
        TransliterateSegmentedWord(segmented_input_word, k_best, fst_params);
  } else {
    word_transliterations =
        TransliterateUnsegmentedWord(input_word, k_best, fst_params);
  }

  // If the word is marked as mixed, no need to mix or cache again, so return
  // right away.
  fst_params.mutex.ReaderLock();
  const bool override = fst_params.mixed_with_precomputed.at(input_word);
  fst_params.mutex.ReaderUnlock();
  if (override) {
    // Returns cached word transliterations.
    absl::ReaderMutexLock lock(&fst_params.mutex);
    return fst_params.word_transliteration_cache.at(input_word);
  }

  fst_params.mutex.Lock();
  // Adds Fst weighting to final state of Fst automaton prior to union.
  QCHECK_EQ(word_transliterations.NumStates(), 2);
  QCHECK_EQ(word_transliterations.Start(), 0);
  word_transliterations.SetFinal(1, pairlm_translit_weight_);

  // Combine any cached transliterations with output from PairLM composition.
  // Result will be a superset that contains at most
  // word_transliteration_cache[input_word].size() + k_best
  // transliterations.
  Union(&word_transliterations,
        fst_params.word_transliteration_cache.at(input_word));
  RmEpsilon(&word_transliterations);
  impl::PushInLogSemiring(&word_transliterations, /*determinize=*/true);

  // Update sentence-level transliterations and mark word as mixed.
  fst_params.word_transliteration_cache.insert_or_assign(input_word,
                                                         word_transliterations);
  fst_params.mixed_with_precomputed.insert_or_assign(input_word, true);

  // Add union to global cache if requested. Adds input word to mix_overrides,
  // which will trigger a return earlier in this function on subsequent calls,
  // preventing this caching code from being reached twice for the same input
  // word.
  if (add_to_cache_) {
    absl::MutexLock lock(&mutex_);
    const int curr_state = word_transliterations.Start();
    for (ArcIterator<StdVectorFst> aiter(word_transliterations, curr_state);
         !aiter.Done(); aiter.Next()) {
      const StdArc arc = aiter.Value();
      global_word_transliteration_cache_[input_word][fst_params.cand_syms.Find(
          arc.olabel)] = arc.weight.Value();
    }
    mix_overrides_.emplace(input_word);
  }
  fst_params.mutex.Unlock();

  return word_transliterations;
}

StdVectorFst PairLMDecoder::BuildTransliterationFst(
    absl::string_view input_line, int k_best, TranslitContext &fst_params,
    std::vector<int> *unique_arc_id) {
  // Initialize the transducer.
  StdVectorFst transliteration_fst;
  int curr_state = transliteration_fst.AddState();
  transliteration_fst.SetStart(curr_state);

  // Retrieves more word candidates than the requested k_best only if composing
  // with lm_fst_ afterwards.
  const int word_k_best = lm_fst_ == nullptr ? k_best : max_word_cands_;

  // Do the actual transliteration in parallel.
  const std::vector<std::string> input_words = absl::StrSplit(
      input_line, utf8::Utf8WhitespaceDelimiter(), absl::SkipEmpty());
  std::vector<StdVectorFst> translit_fsts(input_words.size());
  {
     ThreadPool pool(max_parallel_tokens_);
     pool.StartWorkers();
     for (int i = 0; i < input_words.size(); ++i) {
       pool.Schedule([this, i, word_k_best, &translit_fsts, &input_words,
         &fst_params] {
         translit_fsts[i] = TransliterateWord(input_words[i], word_k_best,
                                              fst_params);
       });
     }
     // Wait until all threads are complete.
  }

  // Loop through the fsts produced, joining them into a sentence lattice.
  for (int i = 0; i < input_words.size(); ++i) {
    const auto &word_transliterations = translit_fsts[i];
    const int next_state = transliteration_fst.AddState();
    QCHECK_GE(word_transliterations.NumArcs(word_transliterations.Start()), 1);
    for (ArcIterator<StdVectorFst> aiter(word_transliterations,
                                         word_transliterations.Start());
         !aiter.Done(); aiter.Next()) {
      const StdArc arc = aiter.Value();
      int ilabel;
      if (lm_fst_ != nullptr) {
        // Only creates unique index for arc if later composing with lm_fst_.
        ilabel = unique_arc_id->size();
        unique_arc_id->push_back(arc.ilabel);
      } else {
        // Sets ilabel to input word index if no later composition with lm_fst_.
        ilabel = fst_params.input_syms.Find(input_words[i]);
        QCHECK_GT(ilabel, 0);  // Checks that symbol is found and not <epsilon>.
      }
      transliteration_fst.AddArc(
          curr_state, StdArc(ilabel, arc.olabel, arc.weight, next_state));
    }
    curr_state = next_state;
  }
  transliteration_fst.SetFinal(curr_state, 0.0);
  ArcSort(&transliteration_fst, OLabelCompare<StdArc>());

  return transliteration_fst;
}

StdVectorFst PairLMDecoder::ComposeLatticeWithLM(
    const StdVectorFst &transliteration_fst) const {
  StdVectorFst string_lm_composed_fst(StdComposeFst(
      transliteration_fst, *lm_fst_,
      ComposeFstOptions<StdArc, PhiMatcher<Matcher<StdFst>>>(
          CacheOptions(),
          new PhiMatcher<Matcher<StdFst>>(transliteration_fst, MATCH_NONE, -1),
          new PhiMatcher<Matcher<StdFst>>(*lm_fst_, MATCH_INPUT, kPhiSymbol,
                                          true, MATCHER_REWRITE_NEVER))));
  Project(&string_lm_composed_fst, ::fst::ProjectType::INPUT);
  Connect(&string_lm_composed_fst);
  impl::PushInLogSemiring(&string_lm_composed_fst);
  TopSort(&string_lm_composed_fst);
  return string_lm_composed_fst;
}

std::vector<double> PairLMDecoder::CollectUniqueArcCosts(
    const StdVectorFst &string_lm_composed_fst,
    const std::vector<int> &unique_arc_id) const {
  QCHECK_GT(string_lm_composed_fst.NumStates(), 0)
      << "input string fst is empty.";
  // Initializes costs to 9999 (i.e., probability ~ 0) for all indices.
  std::vector<double> unique_arc_cost(unique_arc_id.size(), 9999);

  // For each index, counts the probability mass of paths with that index.
  // Counting must happen in the log semiring to sum probabilities.
  auto ngram_counter =
      std::make_unique<ngram::NGramCounter<Log64Weight>>(/*order=*/1, false);
  StdToLogMapper std2log_mapper;
  VectorFst<LogArc> log_string_fst;
  ArcMap(string_lm_composed_fst, &log_string_fst, std2log_mapper);
  CHECK(ngram_counter->Count(log_string_fst));
  StdVectorFst count_fst;
  ngram_counter->GetFst(&count_fst);
  for (ArcIterator<StdVectorFst> aiter(count_fst, count_fst.Start());
       !aiter.Done(); aiter.Next()) {
    // For every counted index, collect the count of that arc.
    const StdArc arc = aiter.Value();
    QCHECK_LT(arc.ilabel, unique_arc_cost.size());
    QCHECK_GT(arc.ilabel, 0);
    unique_arc_cost[arc.ilabel] = arc.weight.Value();
  }
  return unique_arc_cost;
}

void PairLMDecoder::ApplyFinalKBestFilter(
    int k_best,
    StdVectorFst *transliteration_fst) const {
  int dead_state = kNoStateId;
  for (int s = 0; s < transliteration_fst->NumStates(); ++s) {
    if (transliteration_fst->NumArcs(s) > k_best) {
      // Calculates score threshold if some pruning required at state. If
      // pruning required, makes sure that a sink state has been created.
      std::vector<bool> keep_arc =
          impl::ApplyArcScoreThresh(*transliteration_fst, s, k_best,
                                    min_cand_posterior_, /*costs=*/nullptr);
      if (dead_state < 0) dead_state = transliteration_fst->AddState();
      size_t arc_idx = 0;
      for (MutableArcIterator<StdVectorFst> aiter(transliteration_fst, s);
           !aiter.Done(); aiter.Next()) {
        StdArc arc = aiter.Value();
        if (!keep_arc[arc_idx++]) {
          // Points arcs below threshold to non-final sink state for removal
          // later.
          QCHECK_GE(dead_state, 0);
          arc.nextstate = dead_state;
        }
        aiter.SetValue(arc);
      }
    }
  }
  // Connects the lattice to remove pruned arcs.
  Connect(transliteration_fst);
}

void PairLMDecoder::AssignLabelsAndCostsToTranslitLattice(
    const std::vector<int> &unique_arc_id,
    const std::vector<double> &unique_arc_cost, int k_best,
    absl::string_view input_line, TranslitContext &fst_params,
    StdVectorFst *transliteration_fst) const {
  int dead_state = kNoStateId;
  const std::vector<absl::string_view> input_string =
      absl::StrSplit(input_line, utf8::Utf8WhitespaceDelimiter(),
                     absl::SkipEmpty());
  QCHECK_EQ(input_string.size(), transliteration_fst->NumStates() - 1);
  for (int s = 0; s < input_string.size(); ++s) {
    int input_sym = fst_params.input_syms.Find(input_string[s]);
    QCHECK_GT(input_sym, 0);  // Checks that symbol is found and not <epsilon>.
    std::vector<bool> keep_arc;
    if (transliteration_fst->NumArcs(s) > k_best) {
      // Calculates score threshold if some pruning required at state. If
      // pruning required, makes sure that a sink state has been created.
      keep_arc =
          impl::ApplyArcScoreThresh(*transliteration_fst, s, k_best,
                                    min_cand_posterior_, &unique_arc_cost);
      if (dead_state < 0) dead_state = transliteration_fst->AddState();
    }
    size_t arc_idx = 0;
    for (MutableArcIterator<StdVectorFst> aiter(transliteration_fst, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (keep_arc.empty() || keep_arc[arc_idx]) {
        // Updates arc weights and labels if keeping arc.
        arc.weight = unique_arc_cost[arc.ilabel];
        arc.olabel = unique_arc_id[arc.ilabel];
        arc.ilabel = input_sym;
      } else {
        // Points arcs below threshold to non-final sink state for removal
        // later.
        QCHECK_GE(dead_state, 0);
        arc.nextstate = dead_state;
      }
      aiter.SetValue(arc);
      ++arc_idx;
    }
  }
  // Connects the lattice to remove pruned arcs.
  Connect(transliteration_fst);
}

StdVectorFst PairLMDecoder::TransliterateString(absl::string_view input_line,
                                                int k_best) {
  // Holds arc indices for minimum Bayes risk counting.
  std::vector<int> unique_arc_id(1, kNoLabel);
  // Prepare FST symbol tables.
  TranslitContext fst_params(epsilon_symbol_);
  StdVectorFst transliteration_fst =
      BuildTransliterationFst(input_line, k_best, fst_params, &unique_arc_id);
  if (lm_fst_ != nullptr) {
    StdVectorFst lm_labels_lattice_fst;
    auto cands_ptr = *(fst_params.cands_to_lm_fst);
    if (apply_lm_at_word_level_) {
      // Since each arc has a unique arc id on the input side, we can remove
      // context while still accruing the correct arc weights via the existing
      // mechanism, by faithfully including all information from each arc.
      // This saves downstream computation in the composition and counting.
      Compose(impl::RemoveContext(transliteration_fst), cands_ptr,
              &lm_labels_lattice_fst);
    } else {
      Compose(transliteration_fst, cands_ptr, &lm_labels_lattice_fst);
    }
    ArcSort(&lm_labels_lattice_fst, OLabelCompare<StdArc>());
    AssignLabelsAndCostsToTranslitLattice(
        unique_arc_id,
        CollectUniqueArcCosts(ComposeLatticeWithLM(lm_labels_lattice_fst),
                              unique_arc_id),
        k_best, input_line, fst_params, &transliteration_fst);
  } else {
    ApplyFinalKBestFilter(k_best, &transliteration_fst);
  }
  transliteration_fst.SetInputSymbols(&fst_params.input_syms);
  transliteration_fst.SetOutputSymbols(&fst_params.cand_syms);
  return transliteration_fst;
}

std::string PairLMDecoder::PrintTransliterations(
    absl::string_view line_prefix, const StdVectorFst &transliteration_fst,
    bool include_final_endline) const {
  int curr_state = transliteration_fst.Start();
  std::vector<std::string> state_cands;
  while (transliteration_fst.NumArcs(curr_state) > 0) {
    int next_state = kNoStateId;
    for (ArcIterator<StdVectorFst> aiter(transliteration_fst, curr_state);
         !aiter.Done(); aiter.Next()) {
      const StdArc arc = aiter.Value();
      const std::string common_columns = absl::StrJoin(
          std::make_tuple(curr_state,
                          transliteration_fst.InputSymbols()->Find(arc.ilabel),
                          transliteration_fst.OutputSymbols()->Find(arc.olabel),
                          arc.weight.Value()),
          "\t");
      if (line_prefix.empty()) {
        state_cands.push_back(common_columns);
      } else {
        state_cands.push_back(
            absl::StrJoin(std::make_tuple(line_prefix, common_columns), "\t"));
      }
      if (next_state < 0) {
        next_state = arc.nextstate;
      } else {
        // Checks that lattice format is sausage.
        QCHECK_EQ(next_state, arc.nextstate);
      }
    }
    curr_state = next_state;
  }
  if (include_final_endline) state_cands.push_back("");
  return absl::StrJoin(state_cands, "\n");
}

}  // namespace fst
}  // namespace translit
}  // namespace nisaba
