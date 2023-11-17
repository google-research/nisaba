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

#include "nisaba/interim/grm2/thrax/rewrite-tester.h"

#include <iostream>
#include <memory>
#include <ostream>
#include <set>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include "fst/arc.h"
#include "fst/fst.h"
#include "fst/string.h"
#include "fst/symbol-table.h"
#include "fst/vector-fst.h"
#include "absl/flags/flag.h"
#include "absl/log/check.h"
#include "absl/log/log.h"
#include "absl/memory/memory.h"
#include "absl/strings/str_cat.h"
#include "absl/strings/str_split.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/grm2/paths/paths.h"
#include "nisaba/interim/grm2/thrax/grm-manager.h"
#include "nisaba/interim/grm2/thrax/walker/util/function/symbols.h"

ABSL_FLAG(std::string, far, "", "Path to the FAR.");
ABSL_FLAG(std::string, rules, "", "Names of the rewrite rules.");
ABSL_FLAG(std::string, input_mode, "byte",
          "Either \"byte\", \"utf8\", or the path to a "
          "symbol table for input parsing.");
ABSL_FLAG(std::string, output_mode, "byte",
          "Either \"byte\", \"utf8\", or the path to "
          "a symbol table for input parsing.");
ABSL_FLAG(int, noutput, 1,
          "Maximum number of output strings for each input.");
ABSL_FLAG(bool, show_details, false,
          "Show the output of each individual rule when"
          " multiple rules are specified.");
ABSL_FLAG(std::string, field_separator, "\t ",
          "Set of characters used as a separator between printed fields");

namespace thrax {

using ::fst::kNoStateId;
using ::fst::LabelsToUTF8String;
using ::fst::PathIterator;
using ::fst::Project;
using ::fst::ProjectType;
using ::fst::RmEpsilon;
using ::fst::ShortestPath;
using ::fst::StdArc;
using ::fst::StdVectorFst;
using ::fst::StringCompiler;
using ::fst::SymbolTable;
using ::fst::TokenType;
using ::thrax::RuleTriple;

using Label = StdArc::Label;

RewriteTester::RewriteTester() : type_(TokenType::BYTE) {}

void RewriteTester::Initialize() {
  CHECK(grm_.LoadArchive(absl::GetFlag(FLAGS_far)));
  rules_ = absl::StrSplit(absl::GetFlag(FLAGS_rules), ',');
  byte_symtab_ = nullptr;
  utf8_symtab_ = nullptr;
  if (rules_.empty()) LOG(FATAL) << "--rules must be specified";
  for (size_t i = 0; i < rules_.size(); ++i) {
    RuleTriple triple(rules_[i]);
    const auto* fst = grm_.GetFst(triple.main_rule);
    if (!fst) {
      LOG(FATAL) << "grm.GetFst() must be non nullptr for rule: "
                 << triple.main_rule;
    }
    StdVectorFst vfst(*fst);
    // If the input transducers in the FAR have symbol tables then we need to
    // add the appropriate symbol table(s) to the input strings, according to
    // the parse mode.
    if (vfst.InputSymbols()) {
      if (!byte_symtab_ &&
          vfst.InputSymbols()->Name() ==
              ::thrax::function::kByteSymbolTableName) {
        byte_symtab_ = absl::WrapUnique(vfst.InputSymbols()->Copy());
      } else if (!utf8_symtab_ &&
                 vfst.InputSymbols()->Name() ==
                     ::thrax::function::kUtf8SymbolTableName) {
        utf8_symtab_ = absl::WrapUnique(vfst.InputSymbols()->Copy());
      }
    }
    if (!triple.pdt_parens_rule.empty()) {
      fst = grm_.GetFst(triple.pdt_parens_rule);
      if (!fst) {
        LOG(FATAL) << "grm.GetFst() must be non nullptr for rule: "
                   << triple.pdt_parens_rule;
      }
    }
    if (!triple.mpdt_assignments_rule.empty()) {
      fst = grm_.GetFst(triple.mpdt_assignments_rule);
      if (!fst) {
        LOG(FATAL) << "grm.GetFst() must be non nullptr for rule: "
                   << triple.mpdt_assignments_rule;
      }
    }
  }
  generated_symtab_ = grm_.GetGeneratedSymbolTable();
  if (absl::GetFlag(FLAGS_input_mode) == "byte") {
    compiler_ = std::make_unique<StringCompiler<StdArc>>(TokenType::BYTE);
  } else if (absl::GetFlag(FLAGS_input_mode) == "utf8") {
    compiler_ = std::make_unique<StringCompiler<StdArc>>(TokenType::UTF8);
  } else {
    input_symtab_ = absl::WrapUnique(
        SymbolTable::ReadText(absl::GetFlag(FLAGS_input_mode)));
    if (!input_symtab_) {
      LOG(FATAL) << "Invalid mode or symbol table path.";
    }
    compiler_ = std::make_unique<StringCompiler<StdArc>>(TokenType::SYMBOL,
                                                         input_symtab_.get());
  }
  output_symtab_ = nullptr;
  if (absl::GetFlag(FLAGS_output_mode) == "byte") {
    type_ = TokenType::BYTE;
  } else if (absl::GetFlag(FLAGS_output_mode) == "utf8") {
    type_ = TokenType::UTF8;
  } else {
    type_ = TokenType::SYMBOL;
    output_symtab_ = absl::WrapUnique(
        SymbolTable::ReadText(absl::GetFlag(FLAGS_output_mode)));
    if (!output_symtab_) {
      LOG(FATAL) << "Invalid mode or symbol table path.";
    }
  }
}

// Run() for interactive mode.
void RewriteTester::Run() {
  std::string input;
  while (ReadInput(&input)) std::cout << ProcessInput(input) << std::endl;
}

std::string RewriteTester::ProcessInput(absl::string_view input,
                                        bool prepend_output) const {
  StdVectorFst input_fst;
  StdVectorFst output_fst;
  if (!compiler_->operator()(input, &input_fst)) {
    return "Unable to parse input string.";
  }
  std::ostringstream sstrm;
  // Set symbols for the input, if appropriate
  if (byte_symtab_ && type_ == TokenType::BYTE) {
    input_fst.SetInputSymbols(byte_symtab_.get());
    input_fst.SetOutputSymbols(byte_symtab_.get());
  } else if (utf8_symtab_ && type_ == TokenType::UTF8) {
    input_fst.SetInputSymbols(utf8_symtab_.get());
    input_fst.SetOutputSymbols(utf8_symtab_.get());
  } else if (input_symtab_ && type_ == TokenType::SYMBOL) {
    input_fst.SetInputSymbols(input_symtab_.get());
    input_fst.SetOutputSymbols(input_symtab_.get());
  }
  bool succeeded = true;
  for (size_t i = 0; i < rules_.size(); ++i) {
    RuleTriple triple(rules_[i]);
    if (grm_.Rewrite(triple.main_rule, input_fst, &output_fst,
                     triple.pdt_parens_rule, triple.mpdt_assignments_rule)) {
      if (absl::GetFlag(FLAGS_show_details) && rules_.size() > 1) {
        std::vector<std::pair<std::string, float>> outputs;
        FstToStrings(output_fst, &outputs, absl::GetFlag(FLAGS_noutput));
        for (const auto &pair : outputs) {
          sstrm << "output of rule[" << triple.main_rule
                << "] is: " << pair.first << std::endl;
        }
      }
      input_fst = output_fst;
    } else {
      succeeded = false;
      break;
    }
  }
  std::vector<std::pair<std::string, float>> outputs;
  if (succeeded &&
      FstToStrings(output_fst, &outputs, absl::GetFlag(FLAGS_noutput))) {
    for (const auto &pair : outputs) {
      if (prepend_output) sstrm << "Output string: ";
      sstrm << pair.first;
      if (absl::GetFlag(FLAGS_noutput) != 1 && pair.second != 0) {
        sstrm << " <cost=" << pair.second << '>';
      }
      sstrm << std::endl;
    }
    return sstrm.str();
  } else {
    return absl::StrCat("Rewrite failed for \"", input, "\"");
  }
}

bool RewriteTester::ReadInput(std::string *s) {
  std::cout << "Input string: ";
  return static_cast<bool>(getline(std::cin, *s));
}

bool RewriteTester::FstToStrings(
    const StdVectorFst &fst,
    std::vector<std::pair<std::string, float>> *strings, size_t n) const {
  StdVectorFst shortest_path;
  if (n == 1) {
    ShortestPath(fst, &shortest_path, n);
  } else {
    // The uniqueness feature of ShortestPath requires us to have an acceptor,
    // so we project and remove epsilon arcs.
    StdVectorFst temp(fst);
    Project(&temp, ProjectType::OUTPUT);
    RmEpsilon(&temp);
    ShortestPath(temp, &shortest_path, n, /*unique=*/true);
  }
  if (shortest_path.Start() == kNoStateId) return false;
  for (PathIterator<StdArc> iter(shortest_path, /*check_acyclic=*/false);
       !iter.Done(); iter.Next()) {
    std::string path;
    for (const auto label : iter.OLabels()) {
      if (!AppendLabel(label, &path)) return false;
    }
    strings->emplace_back(std::move(path), iter.Weight().Value());
  }
  return true;
}

bool RewriteTester::AppendLabel(Label label, std::string *path) const {
  if (label != 0) {
    // Check first to see if this label is in the generated symbol set. Note
    // that this should not conflict with a user-provided symbol table since
    // the parser used by GrmCompiler doesn't generate extra labels if a
    // string is parsed using a user-provided symbol table.
    if (generated_symtab_ && !generated_symtab_->Find(label).empty()) {
      const auto &sym = generated_symtab_->Find(label);
      *path += "[" + sym + "]";
    } else if (type_ == TokenType::SYMBOL) {
      const auto &sym = output_symtab_->Find(label);
      if (sym.empty()) {
        LOG(ERROR) << "Missing symbol in symbol table for id: " << label;
        return false;
      }
      // For non-byte, non-UTF8 symbols, one overwhelmingly wants these to be
      // space-separated.
      if (!path->empty()) *path += absl::GetFlag(FLAGS_field_separator);
      *path += sym;
    } else if (type_ == TokenType::BYTE) {
      path->push_back(label);
    } else if (type_ == TokenType::UTF8) {
      std::string utf8_string;
      std::vector<Label> labels;
      labels.push_back(label);
      if (!LabelsToUTF8String(labels, &utf8_string)) {
        LOG(ERROR) << "LabelsToUTF8String: Bad code point: " << label;
        return false;
      }
      *path += utf8_string;
    }
  }
  return true;
}

}  // namespace thrax
