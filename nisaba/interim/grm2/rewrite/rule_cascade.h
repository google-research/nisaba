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

// RuleCascade is an implementation of BaseRuleCascade that wraps around a
// RewriteManager. RuleCascade can be used to apply a cascade of rules in a FAR
// to strings.

#ifndef NISABA_INTERIM_GRM2_REWRITE_RULE_CASCADE_H_
#define NISABA_INTERIM_GRM2_REWRITE_RULE_CASCADE_H_

#include <array>
#include <string>
#include <utility>
#include <vector>

#include "absl/log/log.h"
#include "nisaba/interim/grm2/rewrite/base_rule_cascade.h"
#include "nisaba/interim/grm2/rewrite/rewrite_manager.h"

namespace rewrite {
namespace internal {

// Helper class for rule triples (rule name, optional PDT parentheses rule name,
// optional MPDT assignment rule name).
class RuleTriple {
 public:
  explicit RuleTriple(const std::string &rule_def)
      : RuleTriple(RuleTriple::ParseRuleDef(rule_def)) {}

  const std::string &Rule() const { return rules_[0]; }

  bool HasPdtParens() const { return !rules_[1].empty(); }

  const std::string &PdtParens() const { return rules_[1]; }

  bool HasMPdtAssignments() const { return !rules_[2].empty(); }

  const std::string &MPdtAssignments() const { return rules_[2]; }

 private:
  explicit RuleTriple(std::array<std::string, 3> rules)
      : rules_(std::move(rules)) {}

  // Actually parses the rules into the pieces we need.
  static std::array<std::string, 3> ParseRuleDef(const std::string &rule_def) {
    std::array<std::string, 3> result;
    auto main_pos = rule_def.find('$');
    if (main_pos == std::string::npos) main_pos = rule_def.find(':');
    result[0] = rule_def.substr(0, main_pos);
    if (main_pos == std::string::npos) return result;
    auto pdt_parens_pos = rule_def.find('$', main_pos + 1);
    if (pdt_parens_pos == std::string::npos) {
      pdt_parens_pos = rule_def.find(':', main_pos + 1);
    }
    if (pdt_parens_pos == std::string::npos) {
      result[1] = rule_def.substr(main_pos + 1);
      return result;
    }
    result[1] = rule_def.substr(main_pos + 1, pdt_parens_pos - main_pos - 1);
    result[2] = rule_def.substr(pdt_parens_pos + 1);
    return result;
  }

  const std::array<std::string, 3> rules_;
};

}  // namespace internal

template <class Arc>
class RuleCascade : public BaseRuleCascade<Arc> {
 public:
  using Transducer = ::fst::Fst<Arc>;
  using MutableTransducer = ::fst::VectorFst<Arc>;
  using SymbolTable = ::fst::SymbolTable;

  // Do not use the manager until FSTs are loaded (with Load) and rules are
  // set (with SetRules).
  explicit RuleCascade(
      ::fst::TokenType token_type = ::fst::TokenType::BYTE)
      : BaseRuleCascade<Arc>(token_type), manager_(token_type) {}

  // Loads rules from a FAR.
  bool Load(const std::string &filename);

  // Sets up rule spec; can be called repeatedly.
  bool SetRules(const std::vector<std::string> &rules);

#ifndef NO_GOOGLE
  bool SetRules(const google::protobuf::RepeatedPtrField<std::string> &rules);
#endif  // NO_GOOGLE

  bool Rewrite(
      const typename BaseRuleCascade<Arc>::Transducer &input,
      typename BaseRuleCascade<Arc>::MutableTransducer *output) const final;

  const SymbolTable *GeneratedSymbols() const final {
    return manager_.GeneratedSymbols();
  }

 private:
  bool ValidateRules();

  RewriteManager<Arc> manager_;
  std::vector<internal::RuleTriple> triples_;
};

template <class Arc>
bool RuleCascade<Arc>::Load(const std::string &filename) {
  return manager_.Load(filename);
}

template <class Arc>
bool RuleCascade<Arc>::SetRules(const std::vector<std::string> &rules) {
  triples_.clear();
  for (const auto &rule : rules) triples_.emplace_back(rule);
  return ValidateRules();
}

#ifndef NO_GOOGLE
template <class Arc>
bool RuleCascade<Arc>::SetRules(
    const google::protobuf::RepeatedPtrField<std::string> &rules) {
  triples_.clear();
  for (const auto &rule : rules) triples_.emplace_back(rule);
  return ValidateRules();
}
#endif  // NO_GOOGLE

template <class Arc>
bool RuleCascade<Arc>::Rewrite(
    const typename BaseRuleCascade<Arc>::Transducer &input,
    typename BaseRuleCascade<Arc>::MutableTransducer *output) const {
  *output = input;
  for (const auto &triple : triples_) {
    if (!manager_.RewriteLattice(triple.Rule(), *output, output,
                                 triple.PdtParens(),
                                 triple.MPdtAssignments())) {
      return false;
    }
  }
  return true;
}

// Private methods.

template <class Arc>
bool RuleCascade<Arc>::ValidateRules() {
  if (triples_.empty()) {
    LOG(ERROR) << "No rules defined";
    return false;
  }
  for (const auto &triple : triples_) {
    if (!manager_.GetFst(triple.Rule())) {
      LOG(ERROR) << "Cannot find rule: " << triple.Rule();
      return false;
    }
    if (triple.HasPdtParens() && !manager_.GetFst(triple.PdtParens())) {
      LOG(ERROR) << "Cannot find PDT parens: " << triple.PdtParens();
      return false;
    }
    if (triple.HasMPdtAssignments() &&
        !manager_.GetFst(triple.MPdtAssignments())) {
      LOG(ERROR) << "Cannot find MPDT assignments: "
                 << triple.MPdtAssignments();
      return false;
    }
  }
  return true;
}

using StdRuleCascade = RuleCascade<::fst::StdArc>;

}  // namespace rewrite

#endif  // NISABA_INTERIM_GRM2_REWRITE_RULE_CASCADE_H_
