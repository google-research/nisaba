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

// Tool to k-best outputs from TSV lattice representation.
//
// Given TSV lattice representation, extracts k-best full string candidates.
//
// Sample run:
// ./extract-kbest-full-string \
// --ifile="lattice.out.tsv" \
// --ofile="sys.out.tsv" \
// --kbest=20 \
// --show_scores=true
//
// All input TSV files are expected to have the format:
//
// input columns: <example>, <position>, <input>, <output>, <neg log prob>
// where <example> is the sentence ID number and <position> is the word position
// number within <example>.  <input> is the input word, and <output> is the
// candidate output word, at <example, position>.
//
// The output TSV will include the example index, full output string and score
// (if show_score=true).
//
// If k=1, i.e., just one best, then the input string is omitted in the output.

#include <cstdint>
#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/log/check.h"
#include "nisaba/translit/tools/kbest-full-string-util.h"

ABSL_FLAG(std::string, ifile, "", "Input text lattice file");
ABSL_FLAG(std::string, ofile, "", "Output filename.");
ABSL_FLAG(int32_t, kbest, 20, "Number of k-best to extract");
ABSL_FLAG(bool, show_score, false, "Whether to show the score");
ABSL_FLAG(bool, show_full_input_string, false,
          "Whether to show the full input string or just the example index.");

int main(int argc, char** argv) {
  std::string usage = "Usage: ";
  usage += argv[0];
  usage += " --ifiles=<infile>";
  usage += " --ofile=<outfile>";
  usage += " --kbest=[number_to_output]";
  usage += " --show_score=[true/false]";

  absl::ParseCommandLine(argc, argv);
  QCHECK(!absl::GetFlag(FLAGS_ifile).empty() &&
         !absl::GetFlag(FLAGS_ofile).empty())
      << "Required arguments empty.\n"
      << usage << "\n";
  nisaba::translit::tools::KbestExtractor kbest_extractor(
      absl::GetFlag(FLAGS_ifile));
  kbest_extractor.RunExtractorAndOutput(
      absl::GetFlag(FLAGS_ofile), absl::GetFlag(FLAGS_kbest),
      absl::GetFlag(FLAGS_show_score),
      absl::GetFlag(FLAGS_show_full_input_string));
  return 0;
}
