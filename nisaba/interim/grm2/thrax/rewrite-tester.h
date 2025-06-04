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

#ifndef NISABA_INTERIM_GRM2_THRAX_REWRITE_TESTER_H_
#define NISABA_INTERIM_GRM2_THRAX_REWRITE_TESTER_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "fst/arc.h"
#include "fst/fst.h"
#include "fst/string.h"
#include "fst/symbol-table.h"
#include "nisaba/interim/grm2/thrax/grm-manager.h"

namespace thrax {

class RewriteTester {
 public:
  RewriteTester();

  ~RewriteTester() = default;

  void Initialize();

  void Run();

  // Runs the input through the FSTs. Prepends "Output string:" to each line if
  // prepend_output is true
  std::string ProcessInput(absl::string_view input,
                           bool prepend_output = true) const;

 private:
  // Reader for the input in interactive version.
  bool ReadInput(std::string* s);

  bool FstToStrings(const ::fst::StdVectorFst &fst,
                    std::vector<std::pair<std::string, float>> *strings,
                    size_t n) const;

  bool AppendLabel(::fst::StdArc::Label label, std::string *path) const;

  ::fst::TokenType type_;
  GrmManagerSpec<::fst::StdArc> grm_;
  std::vector<std::string> rules_;
  std::unique_ptr<::fst::StringCompiler<::fst::StdArc>> compiler_;
  std::unique_ptr<::fst::SymbolTable> byte_symtab_;
  std::unique_ptr<::fst::SymbolTable> utf8_symtab_;
  std::unique_ptr<::fst::SymbolTable> generated_symtab_;
  std::unique_ptr<::fst::SymbolTable> input_symtab_;
  std::unique_ptr<::fst::SymbolTable> output_symtab_;

  RewriteTester(const RewriteTester&) = delete;
  RewriteTester& operator=(const RewriteTester&) = delete;
};

}  // namespace thrax

#endif  // NISABA_INTERIM_GRM2_THRAX_REWRITE_TESTER_H_
