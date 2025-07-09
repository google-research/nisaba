// Copyright 2025 Nisaba Authors.
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

#ifndef NISABA_TRANSLIT_FST_PAIRLM_DECODER_H_
#define NISABA_TRANSLIT_FST_PAIRLM_DECODER_H_

#include <memory>
#include <string>
#include <vector>

#include "fst/vector-fst.h"
#include "absl/container/flat_hash_map.h"
#include "absl/container/flat_hash_set.h"
#include "absl/strings/string_view.h"
#include "absl/synchronization/mutex.h"
#include "nisaba/translit/fst/pairlm_decoder_options.pb.h"
#include "nisaba/translit/fst/wordpiece-segmenter.h"

namespace nisaba {
namespace translit {
namespace fst {

// Default values for the common symbols: These will be used if the
// corresponding fields in the configuration proto are not set.
namespace symbols {
inline constexpr absl::string_view kEpsilonSymbol = "<epsilon>";
inline constexpr absl::string_view kUnknownSymbol = "<UNK>";
}  // symbols

constexpr int kMaxLineLength = 51200;  // For reading text with ReadLines.

// Class to perform inference with pair LM transliteration models.
class PairLMDecoder {
 public:
  explicit PairLMDecoder(const PairLMDecoderOptions &pairlm_config) {
    InitializePairLMDecoder(pairlm_config);
  }

  // Transliterates a full string, returning an Fst of results.
  ::fst::StdVectorFst TransliterateString(absl::string_view input_line,
                                          int k_best);

  // Prints output from transliteration along with user provided line prefix.
  std::string PrintTransliterations(
      absl::string_view line_prefix,
      const ::fst::StdVectorFst &transliteration_fst,
      bool include_final_endline = true) const;

  // Check if input word is in global cache.
  bool CheckCache(absl::string_view input_word) const;

 private:
  PairLMDecoder() = delete;

  // Nested class to store data applicable to each string transliteration.
  struct TranslitContext {
   public:
    TranslitContext(std::string epsilon_symbol) {
      cand_syms.AddSymbol(epsilon_symbol);
      input_syms.AddSymbol(epsilon_symbol);
      cands_to_lm_fst = std::make_unique<::fst::StdVectorFst>();
      cands_to_lm_fst->SetStart(cands_to_lm_fst->AddState());
      cands_to_lm_fst->SetFinal(cands_to_lm_fst->Start(), 0.0);
    }
    ::fst::SymbolTable cand_syms;
    ::fst::SymbolTable input_syms;
    std::unique_ptr<::fst::StdVectorFst> cands_to_lm_fst;
    absl::flat_hash_map<std::string, ::fst::StdVectorFst>
        word_transliteration_cache;
    absl::flat_hash_map<std::string, bool> mixed_with_precomputed;
    absl::Mutex mutex;
  };

  // Transliterates a segmented word, concatenating the result from each segment
  // and returning an Fst of results.
  ::fst::StdVectorFst TransliterateSegmentedWord(
      const std::vector<std::string> &segmented_word, int k_best,
      TranslitContext &fst_params);

  // Transliterates an unsegmented word, returning an Fst of results.
  ::fst::StdVectorFst TransliterateUnsegmentedWord(absl::string_view input_word,
                                                   int k_best,
                                                   TranslitContext &fst_params)
      ABSL_LOCKS_EXCLUDED(mutex_);

  // Transliterates a single word, returning an Fst of results.
  ::fst::StdVectorFst TransliterateWord(absl::string_view input_word,
                                        int k_best, TranslitContext &fst_params)
      ABSL_LOCKS_EXCLUDED(mutex_);

  // Initializes full class for transliteration.
  void InitializePairLMDecoder(const PairLMDecoderOptions &pairlm_config)
      ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Initializes transliteration model and associated structures if present.
  void InitializeTranslitModel(const PairLMDecoderOptions &pairlm_config)
      ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Initializes language model and associated structures if present.
  void InitializeLanguageModel(const PairLMDecoderOptions &pairlm_config)
      ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Initializes word-piece trie if word-piece internal prefix is non-empty.
  void InitializeWordPieceTrie(const PairLMDecoderOptions &pairlm_config)
      ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Initializes external transliterations and associated structures if present.
  void InitializeExternalTransliterations(
      const PairLMDecoderOptions &pairlm_config) ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Initializes hash set of input characters for later segmentation.
  void InitializeInputCharacterSet() ABSL_NO_THREAD_SAFETY_ANALYSIS;

  // Segments input word into substrings covered by translit and those not.
  // Returns a vector of segments, or an empty vector if input is unsegmented.
  // Hence a vector size < 2 indicates that the input word is not segmented.
  std::vector<std::string> SegmentCoveredChars(
      absl::string_view input_word) const;

  // Returns a lattice of possible single word transliterations.
  ::fst::StdVectorFst GetWordTransliterations(absl::string_view input_word,
                                              bool prune_lattice) const;

  // Puts arc in Fst that maps from candidate to lm_fst_ symbols.
  void AddToCandsToLMFst(absl::string_view new_symbol, int cand_sym,
                         TranslitContext &fst_params)
      ABSL_LOCKS_EXCLUDED(mutex_);

  // Adds a hypothesized transliteration with cost to transliterations fst. Arc
  // will have the correct language model symbol on the olabel if required.
  void AddCandSymArc(absl::string_view new_symbol, double cost,
                     int destination_state, TranslitContext &fst_params,
                     ::fst::StdVectorFst *word_transliterations)
      ABSL_LOCKS_EXCLUDED(mutex_);

  // Segments candidate word symbol into word pieces in language model and
  // returns any out-of-vocabulary costs.
  double SegmentCandWordPiece(absl::string_view new_symbol,
                              std::vector<int> *lm_syms) const;

  // Parses candidate word symbol into word pieces in language model and returns
  // any out-of-vocabulary costs.
  double ParseCandWordPiece(absl::string_view new_symbol,
                            std::vector<int> *lm_syms) const;

  // Builds Fst mapping from candidate transliteration to lm_fst_ symbol(s).
  void BuildCandToLMFst(absl::string_view new_symbol,
                        ::fst::StdVectorFst *cand_to_lm);

  // Build FST containing transliterations from global cache
  void ExtractCachedWordTransliterations(absl::string_view input_word,
                                         TranslitContext &fst_params,
                                         ::fst::StdVectorFst &cached);

  // Builds the transliteration Fst word-by-word from input_line string.
  ::fst::StdVectorFst BuildTransliterationFst(absl::string_view input_line,
                                              int k_best,
                                              TranslitContext &fst_params,
                                              std::vector<int> *unique_arc_id);

  // Composes input word lattice with n-gram language model.
  ::fst::StdVectorFst ComposeLatticeWithLM(
      const ::fst::StdVectorFst &transliteration_fst) const;

  // Collects the costs for each unique arc in the transliteration Fst lattice,
  // which, because it is pushed, represents the arc's posterior probability.
  std::vector<double> CollectUniqueArcCosts(
      const ::fst::StdVectorFst &string_lm_composed_fst,
      const std::vector<int> &unique_arc_id) const;

  // Puts posterior probabilities and output labels on arcs of transliteration
  // lattice.
  void AssignLabelsAndCostsToTranslitLattice(
      const std::vector<int> &unique_arc_id,
      const std::vector<double> &unique_arc_cost, int k_best,
      absl::string_view input_line, TranslitContext &fst_params,
      ::fst::StdVectorFst *transliteration_fst) const;

  // Performs a final pruning of transliterations per word position.
  void ApplyFinalKBestFilter(int k_best,
                             ::fst::StdVectorFst *transliteration_fst) const;

  std::unique_ptr<::fst::StdVectorFst> translit_fst_;  // PairLM model.
  bool translit_fst_is_transducer_;  // Whether PairLM model is transducer.
  bool add_to_cache_;  // Whether to cache word transliterations internally.

  // FSTs for mapping from unicode codepoints to/from pair symbols.
  std::unique_ptr<::fst::StdVectorFst> unicode_to_pair_fst_;
  std::unique_ptr<::fst::StdVectorFst> pair_to_unicode_fst_;
  absl::flat_hash_set<int> covered_input_chars_;   // Set of input characters.
  std::unique_ptr<::fst::StdVectorFst> lm_fst_;    // Language model fst.
  int lm_oov_index_;  // Index of OOV symbol in language model.
  double oov_cost_;  // Cost of OOV beyond that given by language model.
  std::string word_piece_internal_prefix_;  // Word-internal word-piece prefix.
  bool apply_lm_at_word_level_;  // Whether to apply LM at word level or not.

  // FST that encodes a trie of word-piece symbols.
  std::unique_ptr<::fst::StdVectorFst> word_piece_trie_fst_;

  // Word-piece model.
  std::unique_ptr<const WordpieceSegmenter> wpm_;

  // Start state for matching word-pieces word-internally, i.e., after prefix.
  int word_internal_cands_to_lm_start_state_;

  absl::flat_hash_map<std::string, absl::flat_hash_map<std::string, double>>
      global_word_transliteration_cache_ ABSL_GUARDED_BY(mutex_);

  double pairlm_translit_weight_;  // Mixture weight of pair LM w/ precomputed.

  absl::flat_hash_set<std::string> mix_overrides_ ABSL_GUARDED_BY(mutex_);

  int max_word_cands_;   // Maximum alternative transliterations per word.
  int max_parallel_tokens_;    // Maximum number of parallel words to
                               // transliterate.
  double word_cand_thresh_;    // Threshold on word candidates.
  double min_cand_posterior_;  // Minimum posterior candidate probability.
  bool sample_from_k_best_;  // Whether to sample from (vs. returning) k-best.
  uint64_t random_seed_;     // Random seed for sampling.

  std::string epsilon_symbol_;

  // Mutex to keep class-wide data thread-safe.
  mutable absl::Mutex mutex_;
};

}  // namespace fst
}  // namespace translit
}  // namespace nisaba

#endif  // NISABA_TRANSLIT_FST_PAIRLM_DECODER_H_
