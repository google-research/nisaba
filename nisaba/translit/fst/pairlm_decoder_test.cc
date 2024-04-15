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

#include <cmath>
#include <cstdlib>
#include <string>
#include <tuple>
#include <vector>

#include "fst/arc.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"
#include "nisaba/port/file_util.h"
#include "nisaba/translit/fst/pairlm_decoder_options.pb.h"

using ::fst::ArcIterator;
using ::fst::StdArc;
using ::fst::StdVectorFst;
using ::fst::SymbolTable;

namespace nisaba {
namespace translit {
namespace fst {
namespace {

constexpr float kFloatDelta = 0.00001;  // Delta for float comparisons.

class PairLMDecoderTest : public ::testing::Test {
 protected:
  // Creates pair language model of expected topology for lowercase to uppercase
  // conversion for letters a, b, c and d, with ambiguity for c: c;C and c;K.
  void CreatePairLMFile() {
    SymbolTable syms;
    syms.AddSymbol("<epsilon>");
    // Creates pairs of lowercase to upper case for ASCII 97-100 (a-d) plus c;K.
    syms.AddSymbol("97;65");
    syms.AddSymbol("98;66");
    syms.AddSymbol("99;67");
    syms.AddSymbol("99;75");
    syms.AddSymbol("100;68");

    // Creates 2-state automaton: a;A, b;B, c;C, d;D labeling arcs to/from start
    // state 0, c;K labeling arcs from state 1 to state 0. State 1 is reached by
    // <epsilon> (failure) from state 0 which is also the final state.
    StdVectorFst fst;
    fst.SetStart(fst.AddState());
    double cost = 1.0;
    fst.SetFinal(fst.Start(), 0.0);
    int other_state = fst.AddState();
    fst.AddArc(fst.Start(), StdArc(1, 1, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(2, 2, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(3, 3, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(5, 5, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(0, 0, cost, other_state));
    fst.AddArc(other_state, StdArc(4, 4, cost, fst.Start()));
    fst.SetInputSymbols(&syms);
    fst.SetOutputSymbols(&syms);
    fst.Write(pairlm_file_);
  }

  // Creates pair language model of expected transducer topology for lowercase
  // to uppercase conversion for letters a, b, c and d, with ambiguity for c:
  // c;C and c;K.
  void CreatePairLMTransducerFile() {
    // Creates 2-state transducer: a:A, b:B, c:C, d:D labeling arcs to/from
    // start state 0, c:K labeling arcs from state 1 to state 0. State 1 is
    // reached by <epsilon> (failure) from state 0 which is also the final
    // state.
    StdVectorFst fst;
    fst.SetStart(fst.AddState());
    double cost = 1.0;
    fst.SetFinal(fst.Start(), 0.0);
    int other_state = fst.AddState();
    fst.AddArc(fst.Start(), StdArc(97, 65, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(98, 66, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(99, 67, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(100, 68, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(0, 0, cost, other_state));
    fst.AddArc(other_state, StdArc(99, 75, cost, fst.Start()));
    fst.Write(pairlm_transducer_file_);
  }

  // Creates language model for small set of tokens plus <unk> for OOV handling.
  void CreateLMFile() {
    SymbolTable syms;
    syms.AddSymbol("<epsilon>");
    syms.AddSymbol("AB");
    syms.AddSymbol("CD");
    syms.AddSymbol("CA");
    syms.AddSymbol("DC");
    syms.AddSymbol("<unk>");

    // Creates 2-state automaton: AB, CA, CD, and DC labeling arcs to/from start
    // state 0, <unk> labeling arc from state 1 to state 0. State 1 is reached
    // by <epsilon> (failure) from state 0 which is also the final state.
    StdVectorFst fst;
    fst.SetStart(fst.AddState());
    double cost = 3.0;
    fst.SetFinal(fst.Start(), 0.0);
    int other_state = fst.AddState();
    fst.AddArc(fst.Start(), StdArc(1, 1, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(2, 2, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(3, 3, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(4, 4, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(0, 0, cost, other_state));
    fst.AddArc(other_state, StdArc(5, 5, cost, fst.Start()));
    fst.SetInputSymbols(&syms);
    fst.SetOutputSymbols(&syms);
    fst.Write(lm_file_);
  }

  // Creates wordpiece language model for character word pieces, with one
  // character (C) only occurring word-internally.
  void CreateWordpieceInternalLMFile() {
    SymbolTable syms;
    syms.AddSymbol("<epsilon>");
    syms.AddSymbol("A");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "A"));
    syms.AddSymbol("B");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "B"));
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "C"));
    syms.AddSymbol("D");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "D"));
    syms.AddSymbol("<unk>");

    // Creates 2-state automaton: everything but <unk> labeling arcs to/from
    // start state 0, <unk> labeling arc from state 1 to state 0. State 1 is
    // reached by <epsilon> (failure) from state 0 which is the final state.
    StdVectorFst fst;
    fst.SetStart(fst.AddState());
    double cost = 5.0;
    fst.SetFinal(fst.Start(), 0.0);
    int other_state = fst.AddState();
    fst.AddArc(fst.Start(), StdArc(1, 1, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(2, 2, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(3, 3, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(4, 4, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(5, 5, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(6, 6, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(7, 7, cost, fst.Start()));
    fst.AddArc(fst.Start(), StdArc(0, 0, cost, other_state));
    fst.AddArc(other_state, StdArc(8, 8, cost, fst.Start()));
    fst.SetInputSymbols(&syms);
    fst.SetOutputSymbols(&syms);
    fst.Write(lm_wp_internal_file_);
  }

  void CreateWordpieceModelFile() {
    // Wordpiece model that omits K, B has no word initial wordpiece, and there
    // are two two-character wordpieces starting with B.
    const std::string &file_contents = absl::StrJoin(
        std::make_tuple(wordpiece_prefix_, "A", "B", "C", "D",
                        absl::StrCat(wordpiece_prefix_, "A"),
                        absl::StrCat(wordpiece_prefix_, "C"),
                        absl::StrCat(wordpiece_prefix_, "D"), "BC", "BD"),
        "\n");
    ASSERT_OK(file::WriteTextFile(wordpiece_model_file_, file_contents));
  }

  // Creates wordpiece language model for character word pieces, with one
  // character (B) only occurring word-internally and 2 two-character word
  // pieces.
  void CreateWordpieceInitialLMFile() {
    SymbolTable syms;
    syms.AddSymbol("<epsilon>");
    syms.AddSymbol(wordpiece_prefix_);
    syms.AddSymbol("A");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "A"));
    syms.AddSymbol("B");
    syms.AddSymbol("C");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "C"));
    syms.AddSymbol("D");
    syms.AddSymbol(absl::StrCat(wordpiece_prefix_, "D"));
    syms.AddSymbol("BC");
    syms.AddSymbol("BD");
    syms.AddSymbol("<unk>");

    // Creates 2-state automaton: those with wordpiece_prefix_ (indices 1, 3, 6
    // and 8) from the start state 0 to state 1, everything else from state 1 to
    // state 1, which is the final state.
    StdVectorFst fst;
    fst.SetStart(fst.AddState());
    double cost = 5.0;
    int other_state = fst.AddState();
    fst.SetFinal(other_state, 0.0);
    fst.AddArc(fst.Start(), StdArc(1, 1, cost, other_state));
    fst.AddArc(fst.Start(), StdArc(3, 3, cost, other_state));
    fst.AddArc(fst.Start(), StdArc(6, 6, cost, other_state));
    fst.AddArc(fst.Start(), StdArc(8, 8, cost, other_state));
    fst.AddArc(other_state, StdArc(2, 2, cost, other_state));
    fst.AddArc(other_state, StdArc(4, 4, cost, other_state));
    fst.AddArc(other_state, StdArc(5, 5, cost, other_state));
    fst.AddArc(other_state, StdArc(7, 7, cost, other_state));
    fst.AddArc(other_state, StdArc(9, 9, cost, other_state));
    fst.AddArc(other_state, StdArc(10, 10, cost, other_state));
    fst.AddArc(other_state, StdArc(11, 11, cost, other_state));
    fst.SetInputSymbols(&syms);
    fst.SetOutputSymbols(&syms);
    fst.Write(lm_wp_initial_file_);
  }

  // Creates external transliteration candidates file, mapping input words to
  // output words with a score.  Here we have otherwise out-of-vocabulary ef
  // transliterating to EF, and ca mapping to the alternative CCA.
  void CreateTranslitCandsFile() {
    const std::string &file_contents = absl::StrCat(
        absl::StrJoin(std::make_tuple("ef", "EF", 0.0), "\t"), "\n",
        absl::StrJoin(std::make_tuple("ca", "CCA", 0.0), "\t"), "\n");
    ASSERT_OK(file::WriteTextFile(translit_cands_file_, file_contents));
  }

  void SetUp() override {
    pairlm_file_ = file::TempFilePath("pairlm.fst");
    CreatePairLMFile();
    pairlm_transducer_file_ = file::TempFilePath("pairlm-trans.fst");
    CreatePairLMTransducerFile();
    lm_file_ = file::TempFilePath("lm.fst");
    CreateLMFile();
    wordpiece_prefix_ = "##";
    lm_wp_internal_file_ = file::TempFilePath("wordpiece_internal_lm.fst");
    CreateWordpieceInternalLMFile();
    wordpiece_model_file_ = file::TempFilePath("wordpiece_model.txt");
    CreateWordpieceModelFile();
    lm_wp_initial_file_ = file::TempFilePath("wordpiece_initial_lm.fst");
    CreateWordpieceInitialLMFile();
    translit_cands_file_ = file::TempFilePath("translit_cands.tsv");
    CreateTranslitCandsFile();
  }

  std::string pairlm_file_;  // File name of created pair LM Fst.
  std::string
      pairlm_transducer_file_;  // File name of created pair LM Transducer.
  std::string lm_file_;      // File name of created word-based LM.
  std::string lm_wp_internal_file_;    // File name of internal word piece LM.
  std::string wordpiece_model_file_;   // File name of created word piece model.
  std::string lm_wp_initial_file_;     // File name of initial word piece LM.
  std::string translit_cands_file_;    // File name of created translit cands.
  std::string wordpiece_prefix_;  // Word piece prefix, internal or initial.
};

// Initializing with no model files results in outputs identical to inputs.
TEST_F(PairLMDecoderTest, NoModelsProducesIdentityTransform) {
  PairLMDecoderOptions pairlm_config;
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab", /*k_best=*/1);
  ASSERT_EQ(absl::StrJoin(std::make_tuple(0, "ab", "ab", 0), "\t"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Automaton and Transducer PairLMs produce same result.
TEST_F(PairLMDecoderTest, AutomatonAndTransducerSame) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst a_transliterations =
      pairlm_decoder.TransliterateString("ab", /*k_best=*/1);
  PairLMDecoderOptions pairlm_trans_config;
  pairlm_trans_config.set_pairlm_file(pairlm_transducer_file_);
  pairlm_trans_config.set_pairlm_is_transducer(true);
  PairLMDecoder pairlm_transducer_translit(pairlm_trans_config);
  StdVectorFst t_transliterations =
      pairlm_transducer_translit.TransliterateString("ab", /*k_best=*/1);
  ASSERT_EQ(pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", a_transliterations,
                /*include_final_endline=*/false),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", t_transliterations,
                /*include_final_endline=*/false));
}

// Symbol not covered by pair LM fails and returns input token as output.
TEST_F(PairLMDecoderTest, OOVInputSymbolsProduceIdentity) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("xy", /*k_best=*/1);
  ASSERT_EQ(absl::StrJoin(std::make_tuple(0, "xy", "xy", 0), "\t"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Symbol partially covered by pair LM segments into covered and uncovered
// strings and returns input token as output for uncovered string.
TEST_F(PairLMDecoderTest, MixedOOVInputSymbolsProduceMixedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("abxyba", /*k_best=*/1);
  ASSERT_EQ(absl::StrJoin(std::make_tuple(0, "abxyba", "ABxyBA", 0), "\t"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Single word translit works as advertised with failure-class pair LM.
TEST_F(PairLMDecoderTest, SingleWordStandardExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("abcdab", /*k_best=*/1);
  ASSERT_EQ(absl::StrJoin(std::make_tuple(0, "abcdab", "ABCDAB", 0), "\t"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM and
// word-based (non-word-piece) LM.
TEST_F(PairLMDecoderTest, MultiWordStandardExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  pairlm_config.set_lm_file(lm_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/2);

  // ef is out of vocabulary in the transliteration model, hence that token
  // fails and is in output unchanged. Only ambiguity is c:C and c:K, with cost
  // difference of 4, due to use of phi-arc in both pair LM (with cost of 1) and
  // in LM (with cost of 3).
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "AB"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "CA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "KA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "ef"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "DD"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    float sum_prob = 0.0;
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (sum_prob > 0.0) {
        // If more than one arc, this corresponds to the CA/KA ambigutity and
        // the difference between two costs should be ~4.0.
        ASSERT_NEAR(std::abs(arc.weight.Value() - output_scores.back()), 4.0,
                    kFloatDelta);
      }
      output_scores.push_back(arc.weight.Value());
      sum_prob += exp(-arc.weight.Value());
    }
    if (transliterations.NumArcs(s) > 0) {
      // Checks that probabilities of arcs leaving (non-final) state sum to 1.
      ASSERT_NEAR(sum_prob, 1.0, kFloatDelta);
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM and
// word-based (non-word-piece) LM, with transducer PairLM.
TEST_F(PairLMDecoderTest, MultiWordStandardTransducerPairLMExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_transducer_file_);
  pairlm_config.set_pairlm_is_transducer(true);
  pairlm_config.set_lm_file(lm_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/2);

  // ef is out of vocabulary in the transliteration model, hence that token
  // fails and is in output unchanged. Only ambiguity is c:C and c:K, with cost
  // difference of 4, due to use of phi-arc in both pair LM (with cost of 1) and
  // in LM (with cost of 3).
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "AB"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "CA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "KA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "ef"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "DD"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    float sum_prob = 0.0;
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (sum_prob > 0.0) {
        // If more than one arc, this corresponds to the CA/KA ambigutity and
        // the difference between two costs should be ~4.0.
        ASSERT_NEAR(std::abs(arc.weight.Value() - output_scores.back()), 4.0,
                    kFloatDelta);
      }
      output_scores.push_back(arc.weight.Value());
      sum_prob += exp(-arc.weight.Value());
    }
    if (transliterations.NumArcs(s) > 0) {
      // Checks that probabilities of arcs leaving (non-final) state sum to 1.
      ASSERT_NEAR(sum_prob, 1.0, kFloatDelta);
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM and
// word-piece (w/word_piece_internal_prefix) LM.
TEST_F(PairLMDecoderTest, MultiWordWordpieceInternalExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  pairlm_config.set_lm_file(lm_wp_internal_file_);
  pairlm_config.set_word_piece_internal_prefix(wordpiece_prefix_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/2);

  // ef is out of vocabulary in the transliteration model, hence that token
  // fails and is in output unchanged. Only ambiguity is c:C and c:K, with cost
  // difference of 1, due to use of phi-arc in pair LM (with cost of 1). Since C
  // is only seen word-internally, it has to use <unk> word-initially, hence
  // both K and C use <unk> and there's no LM difference in score.
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "AB"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "CA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "KA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "ef"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "DD"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    float sum_prob = 0.0;
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (sum_prob > 0.0) {
        // If more than one arc, this corresponds to the CA/KA ambigutity and
        // the difference between two costs should be ~1.0.
        ASSERT_NEAR(std::abs(arc.weight.Value() - output_scores.back()), 1.0,
                    kFloatDelta);
      }
      output_scores.push_back(arc.weight.Value());
      sum_prob += exp(-arc.weight.Value());
    }
    if (transliterations.NumArcs(s) > 0) {
      // Checks that probabilities of arcs leaving (non-final) state sum to 1.
      ASSERT_NEAR(sum_prob, 1.0, kFloatDelta);
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM and
// word-piece (w/word_piece_initial_prefix) LM.
TEST_F(PairLMDecoderTest, MultiWordWordpieceInitialExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  pairlm_config.set_lm_file(lm_wp_initial_file_);
  pairlm_config.set_apply_closure_to_lm(true);
  pairlm_config.set_word_piece_word_initial_prefix(wordpiece_prefix_);
  pairlm_config.set_word_piece_model(wordpiece_model_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab bca ef dd", /*k_best=*/2);

  // ef is out of vocabulary in the transliteration model, hence that token
  // fails and is in output unchanged. Only ambiguity is c:C and c:K, with cost
  // difference of 1 from the translit pair LM, due to use of phi-arc in pair LM
  // (with cost of 1), plus an additional difference of 5, due to an extra token
  // in the wordpiece tokenizer (each costs 5), for a total difference of 6.
  // BCA -> _ BC A  versus  BKA -> _ B K A  (since K is not in the wordpiece
  // model). K ends up being mapped to <unk>.
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "AB"), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(1, "bca", "BCA"), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(1, "bca", "BKA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "ef"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "DD"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    float sum_prob = 0.0;
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (sum_prob > 0.0) {
        // If more than one arc, this corresponds to the BCA/BKA ambigutity and
        // the difference between two costs should be ~6.0.
        ASSERT_NEAR(std::abs(arc.weight.Value() - output_scores.back()), 6.0,
                    kFloatDelta);
      }
      output_scores.push_back(arc.weight.Value());
      sum_prob += exp(-arc.weight.Value());
    }
    if (transliterations.NumArcs(s) > 0) {
      // Checks that probabilities of arcs leaving (non-final) state sum to 1.
      ASSERT_NEAR(sum_prob, 1.0, kFloatDelta);
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with external translit cands and LM.
TEST_F(PairLMDecoderTest, MultiWordTranslitCandsExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_translit_cands_file(translit_cands_file_);
  pairlm_config.set_lm_file(lm_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/2);

  // Only ca and ef are now in vocabulary, others left unchanged. There is no
  // ambiguity in the output, even with k_best=2.
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "ab"), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(1, "ca", "CCA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "EF"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "dd"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    ASSERT_LT(transliterations.NumArcs(s), 2);
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      ASSERT_NEAR(arc.weight.Value(), 0.0, kFloatDelta);
      output_scores.push_back(arc.weight.Value());
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM combined
// with external transliteration candidates and LM.
TEST_F(PairLMDecoderTest, MultiWordPairLMPlusExternalExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  pairlm_config.set_translit_cands_file(translit_cands_file_);
  pairlm_config.set_pairlm_translit_weight(0.5);
  pairlm_config.set_lm_file(lm_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/3);

  // ef is out of vocabulary in the pair LM transliteration model, but shows up
  // in the transliteration cands file, so only that candidate results. There is
  // now a 3-way ambiguity for input "ca", which is CCA from the cands file and
  // CA/KA from the pair LM. KA has 4 points higher cost than CA (1 from phi-arc
  // in pair LM, 3 from phi-arc in LM).  CCA also accrues an extra 3 from the
  // phi-arc in the LM, but has no cost from the transliteration candidate file.
  std::vector<std::string> output_strings;
  output_strings.push_back(absl::StrJoin(std::make_tuple(0, "ab", "AB"), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(1, "ca", "CCA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "CA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(1, "ca", "KA"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(2, "ef", "EF"), "\t"));
  output_strings.push_back(absl::StrJoin(std::make_tuple(3, "dd", "DD"), "\t"));
  std::vector<float> output_scores;
  for (int s = 0; s < transliterations.NumStates(); ++s) {
    float sum_prob = 0.0;
    for (ArcIterator<StdVectorFst> aiter(transliterations, s);
         !aiter.Done(); aiter.Next()) {
      StdArc arc = aiter.Value();
      if (sum_prob > 0.0) {
        if (output_scores.size() == 3) {
          // Measures the cost difference between ca:CA and ca:KA.
          ASSERT_NEAR(std::abs(arc.weight.Value() - output_scores.back()), 4.0,
                      kFloatDelta);
        } else {
          ASSERT_EQ(output_scores.size(), 2);  // Only other possible value.
        }
      }
      output_scores.push_back(arc.weight.Value());
      sum_prob += exp(-arc.weight.Value());
    }
    if (transliterations.NumArcs(s) > 0) {
      // Checks that probabilities of arcs leaving (non-final) state sum to 1.
      ASSERT_NEAR(sum_prob, 1.0, kFloatDelta);
    }
  }
  ASSERT_EQ(output_strings.size(), output_scores.size());
  for (int i = 0; i < output_strings.size(); ++i) {
    // Adds scores to candidate strings to compare with Print() method.
    output_strings[i] = absl::StrJoin(
        std::make_tuple(output_strings[i], output_scores[i]), "\t");
  }
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

// Multi word translit works as advertised with failure-class pair LM combined
// with external transliteration candidates with no mixing and LM.
TEST_F(PairLMDecoderTest, MultiWordPairLMPlusExternalNoMixExpectedOutput) {
  PairLMDecoderOptions pairlm_config;
  pairlm_config.set_pairlm_file(pairlm_file_);
  pairlm_config.set_translit_cands_file(translit_cands_file_);
  pairlm_config.set_translit_cands_override(true);
  pairlm_config.set_pairlm_translit_weight(0.5);
  pairlm_config.set_lm_file(lm_file_);
  pairlm_config.set_oov_symbol("<unk>");
  pairlm_config.set_oov_cost(0.0);
  PairLMDecoder pairlm_decoder(pairlm_config);
  StdVectorFst transliterations =
      pairlm_decoder.TransliterateString("ab ca ef dd", /*k_best=*/3);

  // ef is out of vocabulary in the pair LM transliteration model, but shows up
  // in the transliteration cands file, so only that candidate results. There is
  // now a 3-way ambiguity for input "ca", but the CCA from the cands file now
  // overrides the other candidates, so just one candidate each with 0.0 scores.
  std::vector<std::string> output_strings;
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(0, "ab", "AB", 0.0), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(1, "ca", "CCA", 0.0), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(2, "ef", "EF", 0.0), "\t"));
  output_strings.push_back(
      absl::StrJoin(std::make_tuple(3, "dd", "DD", 0.0), "\t"));
  ASSERT_EQ(absl::StrJoin(output_strings, "\n"),
            pairlm_decoder.PrintTransliterations(
                /*line_prefix=*/"", transliterations,
                /*include_final_endline=*/false));
}

}  // namespace
}  // namespace fst
}  // namespace translit
}  // namespace nisaba
