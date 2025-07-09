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

// Tool to ensemble full string k-best system outputs.
//
// Given multiple system k-best output in TSV files, combine them and extract
// the k-best resulting outputs.
//
// Sample run:
// ./ensemble-full-string \
// --ifiles="sys1.out.tsv:sys2.out.tsv:sys3.out.tsv" \
// --ofile="sys1-3.ensembled.out.tsv" \
// --input_length_file="sys.input.length.txt" \
// --kbest=10
//
// All system output TSV files provided by the (colon-delimited) ifiles argument
// are expected to have the format:
//
// sys output columns: <input>, <output>, <negative log probability>
//
// The output will have the same format.
//
// If provided, the input length file should have the number of words in the
// input, one example per line.

#include <cstdint>
#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/log/check.h"
#include "nisaba/translit/tools/kbest-full-string-util.h"

ABSL_FLAG(std::string, ifiles, "", "Input text filenames, colon delimited");
ABSL_FLAG(std::string, ofile, "", "Output filename.");
ABSL_FLAG(std::string, input_length_file, "",
          "File identifying number or words in input.");
ABSL_FLAG(int32_t, kbest, 20, "Number of k-best to extract");

int main(int argc, char** argv) {
  std::string usage = "Usage: ";
  usage += argv[0];
  usage += " --ifiles=<infiles>";
  usage += " --ofile=<outfile>";
  usage += " --input_length_file=[lengths]";
  usage += " --kbest=[number_to_output]";

  absl::ParseCommandLine(argc, argv);
  QCHECK(!absl::GetFlag(FLAGS_ifiles).empty() &&
         !absl::GetFlag(FLAGS_ofile).empty())
      << "Required arguments empty.\n"
      << usage << "\n";
  nisaba::translit::tools::EnsembleFiles ensemble_files(
      absl::GetFlag(FLAGS_ifiles), absl::GetFlag(FLAGS_input_length_file));
  ensemble_files.RunEnsembleAndOutput(absl::GetFlag(FLAGS_kbest),
                                      absl::GetFlag(FLAGS_ofile));
  return 0;
}
