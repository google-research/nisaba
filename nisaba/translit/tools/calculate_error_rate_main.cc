// Copyright 2023 Nisaba Authors.
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

// Tool to calculate error rates with (possibly) multiple references.
//
// Given a set of attested references, finds the reference that minimizes the
// example's error rate.  Note that, if only one reference is provided, this is
// equivalent to standard error rate.
//
// Sample run:
// translit/tools/calculate_error_rate \
// --reference=gold_attested_with_counts.tsv       \
// --testfile=system_k_best_output.tsv      \
// --ofile=error_rate_by_line.txt
//
// reference columns: <input>, <output>, <count>
// testfile columns: <input>, <output>, <negative log probability>
//
// The third column is optional. If omitted, count is 1 by default, and negative
// log probability is 0.0 by default.
//
// Output is space separated 4 columns for each line in the input:
//     reference count, substitutions, deletions, and insertions.
// At the very end there will be summary statistics for the whole input file.
//
// Sample output:
//
// reference length=5 substitutions=1 deletions=1 insertions=0
// Summary CER
// total statistics: reference length=5 substitutions=1 deletions=1 insertions=0
// overall CER: 0.4

#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/log/check.h"
#include "nisaba/translit/tools/calculate_error_rate.h"

ABSL_FLAG(std::string, reference, "",
          "Reference filename, tab delimited input, output, count.");
ABSL_FLAG(std::string, testfile, "",
          "System output filename, tab delimited input, output, -logP.");
ABSL_FLAG(std::string, ofile, "", "Output filename.");
ABSL_FLAG(bool, split_chars, true,
          "Whether to split at character level or at whitespace separated "
          "token level.");

int main(int argc, char** argv) {
  std::string usage = "Usage: ";
  usage += argv[0];
  usage += " --reference=<infile>";
  usage += " --testfile=<outfile>";
  usage += " --ofile=<outfile>";

  absl::ParseCommandLine(argc, argv);
  QCHECK(!absl::GetFlag(FLAGS_reference).empty() &&
         !absl::GetFlag(FLAGS_testfile).empty() &&
         !absl::GetFlag(FLAGS_ofile).empty())
      << "Required argument empty.\n"
      << usage << "\n";

  nisaba::translit::tools::MultiRefErrorRate error_rate_calc(
      absl::GetFlag(FLAGS_split_chars));
  error_rate_calc.CalculateErrorRate(absl::GetFlag(FLAGS_reference),
                                    absl::GetFlag(FLAGS_testfile));
  error_rate_calc.Write(absl::GetFlag(FLAGS_ofile));
  return 0;
}
