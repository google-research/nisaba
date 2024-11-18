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

// Command-line utility for transliterating input strings given transliteration
// models and/or language models in FST format.
//
// Example usage:
// --------------
// DATAPATH=/usr/local/google/home/${USER}/translit
// bazel-bin/third_party/nisaba/translit/fst/pairlm_decoder \
//   --ifile="${DATAPATH}"/input_file.txt \
//   --ofile="${DATAPATH}"/output_file.tsv \
//   --pairlm_config="lm_file: \"${DATAPATH}/lm.fst\" oov_symbol: \"<unk>\" \
//     pairlm_file: \"${DATAPATH}/pairlm.fst\" invert_pairlm: true" \
//   --kbest=3

#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/log/check.h"
#include "absl/log/initialize.h"
#include "absl/log/log.h"
#include "absl/status/status.h"
#include "nisaba/port/file_util.h"
#include "nisaba/translit/fst/pairlm_decoder_options.pb.h"
#include "nisaba/translit/fst/pairlm_decoder_runner.h"
#include "google/protobuf/text_format.h"

ABSL_FLAG(std::string, ifile, "",
          "Input filename in text format. One input item per line.");
ABSL_FLAG(std::string, ofile, "",
          "Output filename with transliterations, in text format.");
ABSL_FLAG(int, kbest, 1,
          "Number of candidates per word.");
ABSL_FLAG(std::string, pairlm_config, "",
          "Protocol buffer `PairLMDecoderOptions` in text format as string.");
ABSL_FLAG(std::string, pairlm_config_file, "",
          "Text file representing protocol buffer `PairLMDecoderOptions`.");
ABSL_FLAG(int, num_workers, 1,
          "Number of parallel workers to process the input text, where a unit "
          "work corresponds to a single line in an input text file.");
ABSL_FLAG(std::string, input_pairlm_fst_file, "",
          "FST file containing pair-LM model. Overrides the corresponding path "
          "specified in the configuration.");
ABSL_FLAG(std::string, input_lm_fst_file, "",
          "FST file specifying LM model. Overrides the corresponding path "
          "specified in the configuration.");

namespace nisaba {

bool Run() {
  // Read the configuration from string or file.
  translit::fst::PairLMDecoderOptions config;
  std::string config_contents;
  if (!absl::GetFlag(FLAGS_pairlm_config).empty()) {
    config_contents = absl::GetFlag(FLAGS_pairlm_config);
  } else if (!absl::GetFlag(FLAGS_pairlm_config_file).empty()) {
    const std::string config_file = absl::GetFlag(FLAGS_pairlm_config_file);
    LOG(INFO) << "Reading configuration from " << config_file;
    const auto status = file::ReadTextFile(config_file);
    QCHECK_OK(status) << "Failed to read proto file from " << config_file;
    config_contents = status.value();
  } else {
    LOG(WARNING) << "Configuration not specified. Using defaults.";
  }
  QCHECK(google::protobuf::TextFormat::ParseFromString(config_contents, &config))
      << "Failed to parse configuration from string";

  // Check if the model paths have been explicitly specified in addition to the
  // configuration.
  if (!absl::GetFlag(FLAGS_input_pairlm_fst_file).empty()) {
    config.set_pairlm_file(absl::GetFlag(FLAGS_input_pairlm_fst_file));
  }
  if (!absl::GetFlag(FLAGS_input_lm_fst_file).empty()) {
    config.set_pairlm_file(absl::GetFlag(FLAGS_input_lm_fst_file));
  }

  // Run the decoder.
  return translit::fst::RunPairLMDecoder(
      config, absl::GetFlag(FLAGS_kbest),
      absl::GetFlag(FLAGS_num_workers),
      absl::GetFlag(FLAGS_ifile), absl::GetFlag(FLAGS_ofile)).ok();
}

}  // namespace nisaba

int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  absl::InitializeLog();
  if (!nisaba::Run()) {
    LOG(ERROR) << "Decoder failed";
    return 1;
  }
  return 0;
}
