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

// The AbstractGrmManager holds a set of FSTs in memory and performs rewrites
// via composition. The class is parametrized by the FST arc type.
// AbstractGrmManager is thread-compatible.

#ifndef NISABA_INTERIM_GRM2_THRAX_ABSTRACT_GRM_MANAGER_H_
#define NISABA_INTERIM_GRM2_THRAX_ABSTRACT_GRM_MANAGER_H_

#include <functional>
#include <map>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "fst/extensions/mpdt/compose.h"
#include "fst/extensions/mpdt/mpdt.h"
#include "fst/extensions/pdt/compose.h"
#include "fst/extensions/pdt/pdt.h"
#include "fst/extensions/pdt/shortest-path.h"
#include "fst/arc.h"
#include "fst/fst.h"
#include "fst/fstlib.h"
#include "fst/string.h"
#include "fst/vector-fst.h"
#include "absl/base/casts.h"
#include "absl/container/flat_hash_map.h"
#include "absl/log/log.h"
#include "absl/memory/memory.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/grm2/rewrite/parentheses.h"

namespace thrax {

template <typename Arc>
class AbstractGrmManager {
 public:
  using Transducer = ::::fst::Fst<Arc>;
  using MutableTransducer = ::::fst::VectorFst<Arc>;
  using FstMap =
      std::map<std::string, std::unique_ptr<const Transducer>, std::less<>>;
  using Label = typename Arc::Label;

  virtual ~AbstractGrmManager();

  // Read-only access to the underlying FST map.
  const FstMap& GetFstMap() const { return fsts_; }

  // Compile-time access to the FST table.
  FstMap* GetFstMap() { return &fsts_; }

  // ***************************************************************************
  // REWRITE: These functions perform the actual rewriting of inputs using the
  // named FSTs.

  // Rewrites the input to the output (in various parse modes). Returns false on
  // a failed rewrite (i.e., the input was not accepted by the rule's FST) and
  // true otherwise. Notably, a return value of true and an empty string output
  // is a deliberate rewrite to the empty string and not a failed match. If
  // pdt_parens_rule is not empty, then it the transducer associated with "rule"
  // is assumed to be a pushdown automaton, and that associated with
  // pdt_parens_rule is assumed to specify the parentheses. If
  // pdt_assignments_rule is not empty, then this is assumed to be an MPDT.

  bool RewriteBytes(absl::string_view rule, absl::string_view input,
                    std::string* output, absl::string_view pdt_parens_rule = "",
                    absl::string_view mpdt_assignments_rule = "") const;

  bool RewriteBytes(absl::string_view rule, const Transducer& input,
                    std::string* output, absl::string_view pdt_parens_rule = "",
                    absl::string_view mpdt_assignments_rule = "") const;

  // Unlike RewriteBytes(), The MutableTransducer output of Rewrite() contains
  // all the possible output paths. A Rewrite() call only returns false if the
  // specified rule(s) cannot be found. Notably, the call returns true even if
  // output transducer contains no accepting path.

  bool Rewrite(absl::string_view rule, absl::string_view input,
               MutableTransducer* output,
               absl::string_view pdt_parens_rule = "",
               absl::string_view mpdt_assignments_rule = "") const;

  bool Rewrite(absl::string_view rule, const Transducer& input,
               MutableTransducer* output,
               absl::string_view pdt_parens_rule = "",
               absl::string_view mpdt_assignments_rule = "") const;

  // This helper function (when given a potential string fst) takes the shortest
  // path, projects the output, and then removes epsilon arcs.
  static void StringifyFst(MutableTransducer* output);

  // ***************************************************************************
  // The following functions give access to, modify, or serialize internal data.

  // Returns the FST associated with the particular name. This class returns
  // the actual pointer to the FST (or nullptr if it is not found), so the
  // caller should not free the pointer.
  const Transducer* GetFst(absl::string_view name) const;

  // Gets the named FST, just like GetFst(), but this function doesn't lock
  // anything and is thread-safe because it returns a transducer safely
  // shallow-copied from the original.
  std::unique_ptr<Transducer> GetFstSafe(absl::string_view name) const;

  // Modify the transducer under the given name. If no such rule name exists,
  // returns false, otherwise returns true. Note: For thread-safety, it is
  // assumed this function will not be used in a multi-threaded context.
  bool SetFst(absl::string_view name, const Transducer& input);

  // Sorts input labels of all FSTs in the archive.
  void SortRuleInputLabels();

  // Alternative to LoadArchive, allowing you to provide the FSTs and keys
  // directly.
  void LoadFstMap(FstMap named_fsts);

 protected:
  AbstractGrmManager();

  // Loads up the FSTs given the supplied reader. Returns true on success and
  // false otherwise.
  template <typename FarReader>
  bool LoadArchive(FarReader* reader, absl::string_view filename = "");

  // The list of FSTs held by this manager.
  FstMap fsts_;

 private:
  AbstractGrmManager(const AbstractGrmManager&) = delete;
  AbstractGrmManager& operator=(const AbstractGrmManager&) = delete;
};

template <typename Arc>
AbstractGrmManager<Arc>::AbstractGrmManager() {}

template <typename Arc>
AbstractGrmManager<Arc>::~AbstractGrmManager() {
}

template <typename Arc>
template <typename FarReader>
bool AbstractGrmManager<Arc>::LoadArchive(FarReader* reader,
                                          absl::string_view filename) {
  fsts_.clear();
  int num_read_fsts = 0;
  for (reader->Reset(); !reader->Done(); reader->Next()) {
    const auto& name = reader->GetKey();
    fsts_[name] = std::make_unique<MutableTransducer>(*reader->GetFst());
    ++num_read_fsts;
  }
  if (fsts_.size() != num_read_fsts) {
      LOG(ERROR) << num_read_fsts << " Fsts read but only " << fsts_.size()
                 << " Fsts saved.";
  }
  if (fsts_.size() == 0) {
    LOG(ERROR) << filename << " is an empty FAR: Did you `export` any rules?";
    return false;
  }
  SortRuleInputLabels();
  return true;
}

template <typename Arc>
void AbstractGrmManager<Arc>::LoadFstMap(FstMap named_fsts) {
  for (const auto& key_and_fst : named_fsts) {
    CHECK_NE(key_and_fst.second, nullptr);
  }
  fsts_ = std::move(named_fsts);
  SortRuleInputLabels();
}

template <typename Arc>
void AbstractGrmManager<Arc>::SortRuleInputLabels() {
  for (auto &pair : fsts_) {
    const auto& fst = *pair.second;
    // Arc-sorts if the FST is not known to be input-sorted.
    if (fst.Properties(::::fst::kILabelSorted, false) != ::::fst::kILabelSorted) {
      auto sorted_fst = std::make_unique<MutableTransducer>(fst);
      static const ::::fst::ILabelCompare<Arc> icomp;
      ::::fst::ArcSort(sorted_fst.get(), icomp);
      pair.second = std::move(sorted_fst);
    }
  }
}

template <typename Arc>
const typename AbstractGrmManager<Arc>::Transducer*
AbstractGrmManager<Arc>::GetFst(absl::string_view name) const {
  const auto it = fsts_.find(name);
  return it == fsts_.end() ? nullptr : it->second.get();
}

template <typename Arc>
std::unique_ptr<typename AbstractGrmManager<Arc>::Transducer>
AbstractGrmManager<Arc>::GetFstSafe(absl::string_view name) const {
  const auto* fst = GetFst(name);
  return absl::WrapUnique(fst ? fst->Copy(true) : nullptr);
}

template <typename Arc>
bool AbstractGrmManager<Arc>::SetFst(absl::string_view name,
                                     const Transducer& input) {
  auto it = fsts_.find(name);
  if (it != fsts_.end()) {
    it->second = absl::WrapUnique(input.Copy(true));
    return true;
  }
  return false;
}

template <typename Arc>
bool AbstractGrmManager<Arc>::RewriteBytes(
    absl::string_view rule, absl::string_view input, std::string* output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  static const ::::fst::StringCompiler<Arc> compiler(::::fst::TokenType::BYTE);
  MutableTransducer str_fst;
  if (!compiler(input, &str_fst)) return false;
  return RewriteBytes(rule, str_fst, output, pdt_parens_rule,
                      mpdt_assignments_rule);
}

template <typename Arc>
bool AbstractGrmManager<Arc>::RewriteBytes(
    absl::string_view rule, const Transducer& input, std::string* output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer output_fst;
  if (!Rewrite(rule, input, &output_fst, pdt_parens_rule,
               mpdt_assignments_rule)) {
    return false;
  }
  StringifyFst(&output_fst);
  if (output_fst.Start() == ::::fst::kNoStateId) return false;
  static const ::::fst::StringPrinter<Arc> printer(::::fst::TokenType::BYTE);
  return printer(output_fst, output);
}

template <typename Arc>
bool AbstractGrmManager<Arc>::Rewrite(
    absl::string_view rule, absl::string_view input, MutableTransducer* output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  static const ::::fst::StringCompiler<Arc> compiler(::::fst::TokenType::BYTE);
  MutableTransducer str_fst;
  if (!compiler(input, &str_fst)) return false;
  return Rewrite(rule, str_fst, output, pdt_parens_rule,
                 mpdt_assignments_rule);
}

template <typename Arc>
bool AbstractGrmManager<Arc>::Rewrite(
    absl::string_view rule, const Transducer& input, MutableTransducer* output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  const std::unique_ptr<const Transducer> rule_fst = GetFstSafe(rule);
  if (!rule_fst) {
    LOG(ERROR) << "Rule " << rule << " not found.";
    return false;
  }
  std::unique_ptr<const Transducer> pdt_parens_fst;
  if (!pdt_parens_rule.empty()) {
    pdt_parens_fst = GetFstSafe(pdt_parens_rule);
    if (!pdt_parens_fst) {
      LOG(ERROR) << "PDT parentheses rule " << pdt_parens_rule << " not found.";
      return false;
    }
  }
  std::unique_ptr<const Transducer> mpdt_assignments_fst;
  if (!mpdt_assignments_rule.empty()) {
    mpdt_assignments_fst = GetFstSafe(mpdt_assignments_rule);
    if (!mpdt_assignments_fst) {
      LOG(ERROR) << "MPDT assignments rule " << mpdt_assignments_rule
                 << " not found.";
      return false;
    }
  }
  if (pdt_parens_fst) {
    MutableTransducer mut_pdt_parens_fst(*pdt_parens_fst);
    std::vector<std::pair<Label, Label>> pdt_parens;
    ::rewrite::MakeParenthesesVector(mut_pdt_parens_fst, &pdt_parens);
    // PdtComposeFilter::EXPAND removes the parentheses, allowing for subsequent
    // application of PDTs. At the end (in StringifyFst() we use ordinary
    // ShortestPath().
    if (mpdt_assignments_fst) {
      MutableTransducer mut_mpdt_assignments_fst(*mpdt_assignments_fst);
      std::vector<Label> mpdt_assignments;
      ::rewrite::MakeAssignmentsVector(mut_mpdt_assignments_fst, pdt_parens,
                                       &mpdt_assignments);
      static const ::::fst::MPdtComposeOptions opts(
          true, ::::fst::PdtComposeFilter::EXPAND);
      ::::fst::Compose(input, *rule_fst, pdt_parens, mpdt_assignments, output,
                     opts);
    } else {
      static const ::::fst::PdtComposeOptions opts(
          true, ::::fst::PdtComposeFilter::EXPAND);
      ::::fst::Compose(input, *rule_fst, pdt_parens, output, opts);
    }
  } else {
    static const ::::fst::ComposeOptions opts(true, ::::fst::ALT_SEQUENCE_FILTER);
    ::::fst::Compose(input, *rule_fst, output, opts);
  }
  return true;
}

template <typename Arc>
void AbstractGrmManager<Arc>::StringifyFst(MutableTransducer* fst) {
  MutableTransducer temp;
  ::::fst::ShortestPath(*fst, &temp);
  ::::fst::Project(&temp, ::::fst::ProjectType::OUTPUT);
  ::::fst::RmEpsilon(&temp);
  *fst = temp;
}

// Triple of main rule, pdt_parens and mpdt assignments

struct RuleTriple {
  std::string main_rule, pdt_parens_rule, mpdt_assignments_rule;

  explicit RuleTriple(absl::string_view rule_def) {
    auto main_pos = rule_def.find('$');
    if (main_pos == std::string::npos) main_pos = rule_def.find(':');
    main_rule = std::string(rule_def.substr(0, main_pos));
    if (main_pos == std::string::npos) return;
    auto pdt_parens_pos = rule_def.find('$', main_pos + 1);
    if (pdt_parens_pos == std::string::npos) {
      pdt_parens_pos = rule_def.find(':', main_pos + 1);
    }
    if (pdt_parens_pos == std::string::npos) {
      pdt_parens_rule = std::string(rule_def.substr(main_pos + 1));
      return;
    }
    pdt_parens_rule = std::string(
        rule_def.substr(main_pos + 1, pdt_parens_pos - main_pos - 1));
    mpdt_assignments_rule = std::string(rule_def.substr(pdt_parens_pos + 1));
  }
};

// Does not own the grm pointer.
template <typename Arc>
class RuleCascade {
  using Transducer = ::::fst::Fst<Arc>;
  using MutableTransducer = ::::fst::VectorFst<Arc>;

 public:
  RuleCascade() : grm_(nullptr) {}

  // Initializes the cascade from rule triples.
  bool Init(const AbstractGrmManager<Arc>* grm,
            std::vector<RuleTriple> rule_triples);

  // Parses the rule definitions and initializes the cascade.
  bool InitFromDefs(const AbstractGrmManager<Arc>* grm,
                    const std::vector<std::string>& rule_defs);

  bool RewriteBytes(absl::string_view input, std::string* output) const;

  bool Rewrite(absl::string_view input, MutableTransducer* output) const;

  bool Rewrite(const Transducer& input, MutableTransducer* output) const;

 private:
  // Validates all rules.
  bool ValidateRules();
  const AbstractGrmManager<Arc>* grm_;
  std::vector<RuleTriple> rule_triples_;
};

template <typename Arc>
bool RuleCascade<Arc>::ValidateRules() {
  for (auto& rule_triple : rule_triples_) {
    if (!grm_->GetFst(rule_triple.main_rule)) {
      LOG(ERROR) << "Cannot find rule: " << rule_triple.main_rule;
      return false;
    }
    if (!rule_triple.pdt_parens_rule.empty() &&
        !grm_->GetFst(rule_triple.pdt_parens_rule)) {
      LOG(ERROR) << "Cannot find rule: " << rule_triple.pdt_parens_rule;
      return false;
    }
    if (!rule_triple.mpdt_assignments_rule.empty() &&
        !grm_->GetFst(rule_triple.mpdt_assignments_rule)) {
      LOG(ERROR) << "Cannot find rule: " << rule_triple.mpdt_assignments_rule;
      return false;
    }
  }
  return true;
}

template <typename Arc>
bool RuleCascade<Arc>::Init(const AbstractGrmManager<Arc>* grm,
                            std::vector<RuleTriple> rule_triples) {
  grm_ = grm;
  rule_triples_ = std::move(rule_triples);
  return ValidateRules();
}

template <typename Arc>
bool RuleCascade<Arc>::InitFromDefs(const AbstractGrmManager<Arc>* grm,
                                    const std::vector<std::string>& rules) {
  grm_ = grm;
  for (auto& rule : rules) rule_triples_.emplace_back(rule);
  return ValidateRules();
}

template <typename Arc>
bool RuleCascade<Arc>::RewriteBytes(absl::string_view input,
                                    std::string* output) const {
  static const ::::fst::StringCompiler<Arc> compiler(::::fst::TokenType::BYTE);
  MutableTransducer input_fst;
  if (!compiler(input, &input_fst)) return false;
  MutableTransducer output_fst;
  if (!Rewrite(input_fst, &output_fst)) return false;
  AbstractGrmManager<Arc>::StringifyFst(&output_fst);
  if (output_fst.Start() == ::::fst::kNoStateId) return false;
  static const ::::fst::StringPrinter<Arc> printer(::::fst::TokenType::BYTE);
  return printer(output_fst, output);
}

template <typename Arc>
bool RuleCascade<Arc>::Rewrite(absl::string_view input,
                               MutableTransducer* output) const {
  static const ::::fst::StringCompiler<Arc> compiler(::::fst::TokenType::BYTE);
  MutableTransducer str_fst;
  if (!compiler(input, &str_fst)) return false;
  return Rewrite(str_fst, output);
}

template <typename Arc>
bool RuleCascade<Arc>::Rewrite(const Transducer& input,
                               MutableTransducer* output) const {
  MutableTransducer tmp_input(input);
  for (auto& rule_triple : rule_triples_) {
    if (!grm_->Rewrite(rule_triple.main_rule, tmp_input, output,
                       rule_triple.pdt_parens_rule,
                       rule_triple.mpdt_assignments_rule)) {
      return false;
    }
    tmp_input = *output;
  }
  return true;
}

}  // namespace thrax

#endif  // NISABA_INTERIM_GRM2_THRAX_ABSTRACT_GRM_MANAGER_H_
