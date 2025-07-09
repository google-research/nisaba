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

// Main entry points to the decoder that are easy to test.

#ifndef NISABA_TRANSLIT_FST_PAIRLM_DECODER_RUNNER_H_
#define NISABA_TRANSLIT_FST_PAIRLM_DECODER_RUNNER_H_

#include "absl/status/status.h"
#include "absl/strings/string_view.h"
#include "nisaba/translit/fst/pairlm_decoder_options.pb.h"

namespace nisaba {
namespace translit {
namespace fst {

// Runs the pair LM decoder using the configuration provided in `config` on
// the input file `ifile` outputting the transliterations to `ofile`. The number
// of transliteration candidates per word is given by `k_best`. The number of
// parallel jobs is specified by `num_workers`. Please note, the decoder may
// perform its own parallelization in addition to line-by-line parallization
// specified by `num_workers`. Returns ok status in case of success, in case of
// internal errors will most likely abort the execution with a fatal message.
absl::Status RunPairLMDecoder(const PairLMDecoderOptions &config,
                              int k_best, int num_workers,
                              absl::string_view ifile, absl::string_view ofile);

}  // namespace fst
}  // namespace translit
}  // namespace nisaba

#endif  // NISABA_TRANSLIT_FST_PAIRLM_DECODER_RUNNER_H_
