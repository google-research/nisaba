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

// Tool to rejoin k-best outputs when inputs were split to a max num of bytes.
//
// Sample run:
// ./rejoin-kbest-full-string \
// --ifile="sys.out.tsv" \
// --ofile="rejoined.out.tsv" \
// --split_file="split_file"
//
// if kbest flag is unspecified, then kbest is set to the maximum kbest found in
// the input set.

#include <cstdint>
#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/log/check.h"
#include "nisaba/translit/tools/kbest-full-string-util.h"

ABSL_FLAG(std::string, ifile, "", "Input text lattice file");
ABSL_FLAG(std::string, ofile, "", "Output filename.");
ABSL_FLAG(std::string, split_file, "", "Filename containing split ids");
ABSL_FLAG(int32_t, kbest, -1, "Number of k-best to extract");

int main(int argc, char** argv) {
  std::string usage = "Usage: ";
  usage += argv[0];
  usage += " --ifiles=<infile>";
  usage += " --ofile=<outfile>";
  usage += " --split_file=<splitfile>";

  absl::ParseCommandLine(argc, argv);
  QCHECK(!absl::GetFlag(FLAGS_ifile).empty() &&
         !absl::GetFlag(FLAGS_ofile).empty() &&
         !absl::GetFlag(FLAGS_split_file).empty())
      << "Required arguments empty.\n"
      << usage << "\n";

  nisaba::translit::tools::KbestRejoiner kbest_rejoiner(
      absl::GetFlag(FLAGS_ifile), absl::GetFlag(FLAGS_split_file),
      absl::GetFlag(FLAGS_kbest));
  kbest_rejoiner.RunRejoinerAndOutput(absl::GetFlag(FLAGS_ofile));
  return 0;
}
