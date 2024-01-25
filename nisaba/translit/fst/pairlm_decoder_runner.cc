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

#include "nisaba/translit/fst/pairlm_decoder_runner.h"

#include <algorithm>
#include <fstream>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "fst/vector-fst.h"
#include "absl/log/log.h"
#include "absl/status/status.h"
#include "absl/strings/match.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_join.h"
#include "absl/strings/string_view.h"
#include "absl/synchronization/mutex.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/timer.h"
#include "nisaba/translit/fst/pairlm_decoder.h"
#include "nisaba/port/thread_pool.h"
#include "nisaba/port/status_macros.h"

namespace nisaba {
namespace translit {
namespace fst {
namespace {

// Transliterates a given line and converts the result to string.
std::string Transliterate(absl::string_view input_line, int k_best, int index,
                          PairLMDecoder *decoder) {
  const ::fst::StdVectorFst translit_fst =
      decoder->TransliterateString(input_line, k_best);
  return decoder->PrintTransliterations(std::to_string(index++), translit_fst);
}

// Runs the decoder sequentially line-by-line.
absl::Status SequentialDecoding(const PairLMDecoderOptions &config,
                                const std::vector<std::string> &input_lines,
                                int k_best,
                                std::ofstream &output_file) {
  std::unique_ptr<PairLMDecoder> pair_lm =
      std::make_unique<PairLMDecoder>(config);
  int index = 0;
  for (const auto &input_line : input_lines) {
    if (absl::StartsWith(input_line, "#")) continue;
    output_file << Transliterate(input_line, k_best, index++, pair_lm.get());
    if (!output_file) {
      return absl::InternalError("Failed to write to the output file");
    }
  }
  return absl::OkStatus();
}

// Runs the decoder parallelizing the execution using thread pool.
absl::Status ParallelDecoding(const PairLMDecoderOptions &config,
                              const std::vector<std::string> &input_lines,
                              int k_best, int num_workers,
                              std::ofstream &output_file) {
  // Perform all transliterations and save the results to `outputs`.
  absl::Mutex outputs_mutex;
  std::vector<std::pair<std::string, int>> outputs;
  outputs.reserve(input_lines.size());

  std::unique_ptr<PairLMDecoder> pair_lm =
      std::make_unique<PairLMDecoder>(config);
  std::unique_ptr<ThreadPool> thread_pool =
      std::make_unique<ThreadPool>(num_workers);
  thread_pool->StartWorkers();
  int index = 0;
  for (const auto &input_line : input_lines) {
    if (absl::StartsWith(input_line, "#")) continue;
    thread_pool->Schedule([&input_line, k_best, index, &pair_lm, &outputs,
                           &outputs_mutex] {
      const std::string &result = Transliterate(input_line, k_best, index,
                                                pair_lm.get());
      absl::WriterMutexLock lock(&outputs_mutex);
      outputs.push_back({result, index});
    });
    index++;
  }
  thread_pool.reset();  // Waits till all complete.

  // Write the results to a file. The returned string already contains a
  // newline.
  std::sort(outputs.begin(), outputs.end(),
            [](const auto &entry_a, const auto &entry_b) {
              return entry_a.second < entry_b.second;
            });
  output_file << absl::StrJoin(
      outputs, "", [](std::string *output, const auto &entry) {
        absl::StrAppend(output, entry.first);
      });
  if (!output_file) {
    return absl::InternalError("Failed to write to the output file");
  } else {
    return absl::OkStatus();
  }
}

}  // namespace

absl::Status RunPairLMDecoder(const PairLMDecoderOptions &config,
                              int k_best, int num_workers,
                              absl::string_view ifile,
                              absl::string_view ofile) {
  if (ifile.empty() || ofile.empty()) {
    return absl::InternalError(absl::StrCat("ifile (", ifile, ") or ofile (",
                                            ofile, ") empty"));
  }
  const auto &input_lines_status = file::ReadLines(ifile, kMaxLineLength);
  if (!input_lines_status.ok()) {
    return absl::InternalError("Failed to read lines");
  }
  const std::vector<std::string> input_lines = input_lines_status.value();
  std::ofstream output_file;
  output_file.open(std::string(ofile));
  if (!output_file) {
    return absl::InternalError(absl::StrCat("Can't open for writing: ", ofile));
  }
  LOG(INFO) << "Transliterating " << input_lines.size() << " input lines ...";
  Timer timer;
  if (num_workers <= 1) {
    RETURN_IF_ERROR(SequentialDecoding(config, input_lines, k_best,
                                       output_file));
  } else {
    RETURN_IF_ERROR(ParallelDecoding(config, input_lines, k_best, num_workers,
                                     output_file));
  }
  LOG(INFO) << absl::StrCat("Done in ", timer.ElapsedMillis(),
                            " msec. Saved results to ", ofile);
  return absl::OkStatus();
}

}  // namespace fst
}  // namespace translit
}  // namespace nisaba
