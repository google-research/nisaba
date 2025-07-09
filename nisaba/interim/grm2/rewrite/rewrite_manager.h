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

// RewriteManager is a mapping between strings and FSTs stored in a FAR, with
// support for (finite-state, PDT, and MPDT) composition and rewriting.

#ifndef NISABA_INTERIM_GRM2_REWRITE_REWRITE_MANAGER_H_
#define NISABA_INTERIM_GRM2_REWRITE_REWRITE_MANAGER_H_

#include <cstdint>
#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "fst/extensions/far/far.h"
#include "fst/arcsort.h"
#include "fst/fst-decl.h"
#include "fst/intersect.h"
#include "fst/string.h"
#include "absl/container/flat_hash_map.h"
#include "absl/log/log.h"
#include "absl/memory/memory.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/grm2/rewrite/parentheses.h"
#include "nisaba/interim/grm2/rewrite/rewrite.h"
#include "google/protobuf/repeated_ptr_field.h"

namespace rewrite {

template <class Arc>
class RewriteManager {
 public:
  using Transducer = ::fst::Fst<Arc>;
  using MutableTransducer = ::fst::VectorFst<Arc>;
  using SymbolTable = ::fst::SymbolTable;

  // Do not use the manager until FSTs are loaded with Load.
  // TODO: Add symbol table support, or YAGNI?
  explicit RewriteManager(::fst::TokenType token_type = ::fst::TokenType::BYTE)
      : compiler_(token_type), token_type_(token_type) {}

  // FAR IO.

  // Loads rules from a FAR.
  bool Load(const std::string &filename);

  // Loads FSTs and keys directly, taking ownership of the FST pointers.
  void Load(const absl::flat_hash_map<std::string,
                                      std::unique_ptr<const Transducer>> &map);

  // SETTERS AND GETTERS.

  // Accesses an FST; caller does not own pointer.
  const Transducer *GetFst(absl::string_view rule) const;

  // Accesses an FST; caller owns pointer.
  std::unique_ptr<Transducer> GetFstSafe(absl::string_view rule) const;

  // Overwrites a given FST in the FAR, returning false if the rule is not
  // found. This is not thread-safe.
  bool SetFst(absl::string_view rule, const Transducer &input);

  // REWRITING.

  // Computes one top rewrite, returning false if the requested rule is not
  // found or if composition fails. Requires a semiring with the path property.

  bool TopRewrite(absl::string_view rule, absl::string_view input,
                  std::string *output, absl::string_view pdt_parens_rule = "",
                  absl::string_view mpdt_assignments_rule = "") const;

  // Computes one top rewrite, returning false if the requested rule is not
  // found, if composition fails, or if there's a tie for the top output.
  // Requires a semiring with the path property.

  bool OneTopRewrite(absl::string_view rule, absl::string_view input,
                     std::string *output,
                     absl::string_view pdt_parens_rule = "",
                     absl::string_view mpdt_assignments_rule = "") const;

  // Same, but computes all optimal rewrites. Requires a semiring with the path
  // property.

  bool TopRewrites(absl::string_view rule, absl::string_view input,
                   std::vector<std::string> *output,
                   absl::string_view pdt_parens_rule = "",
                   absl::string_view mpdt_assignments_rule = "") const;

#ifndef NO_GOOGLE
  bool TopRewrites(absl::string_view rule, absl::string_view input,
                   google::protobuf::RepeatedPtrField<std::string> *output,
                   absl::string_view pdt_parens_rule = "",
                   absl::string_view mpdt_assignments_rule = "") const;
#endif  // NO_GOOGLE

  // Same, but computes the top n rewrites; requires a semiring with the path
  // property.

  bool TopRewrites(absl::string_view rule, absl::string_view input,
                   int32_t nshortest, std::vector<std::string> *output,
                   absl::string_view pdt_parens_rule = "",
                   absl::string_view mpdt_assignments_rule = "") const;

#ifndef NO_GOOGLE
  bool TopRewrites(absl::string_view rule, absl::string_view input,
                   int32_t nshortest,
                   google::protobuf::RepeatedPtrField<std::string> *output,
                   absl::string_view pdt_parens_rule = "",
                   absl::string_view mpdt_assignments_rule = "") const;
#endif  // NO_GOOGLE

  // Computes all rewrites.

  bool Rewrites(absl::string_view rule, absl::string_view input,
                std::vector<std::string> *output,
                absl::string_view pdt_parens_rule = "",
                absl::string_view mpdt_assignments_rule = "") const;

#ifndef NO_GOOGLE
  bool Rewrites(absl::string_view rule, absl::string_view input,
                google::protobuf::RepeatedPtrField<std::string> *output,
                absl::string_view pdt_parens_rule = "",
                absl::string_view mpdt_assignments_rule = "") const;
#endif  // NO_GOOGLE

  // Determines whether the input allows a given input/output pair; i.e.,
  // whether the intersection of the output string and the output lattice is
  // non-null.
  bool Matches(absl::string_view rule, absl::string_view input,
               absl::string_view output, absl::string_view pdt_parens_rule = "",
               absl::string_view mpdt_assignments_rule = "") const;

  // Looks up rule, compiles input string, and populates an epsilon-free output
  // lattice; returns false if the rule is not found or if composition fails.
  // Users may also specify a PDT parentheses rule and an MPDT assignment rule
  // if PDT or MPDT composition is desired.
  bool RewriteLattice(absl::string_view rule, absl::string_view input,
                      MutableTransducer *lattice,
                      absl::string_view pdt_parens_rule = "",
                      absl::string_view mpdt_assignments_rule = "") const;

  // Same, but with a transducer input.
  bool RewriteLattice(absl::string_view rule, const Transducer &input,
                      MutableTransducer *lattice,
                      absl::string_view pdt_parens_rule = "",
                      absl::string_view mpdt_assignments_rule = "") const;

  const SymbolTable *GeneratedSymbols() const { return gensyms_.get(); }

 private:
  // Adds rule/FST pair to map.
  void AddToMap(absl::string_view rule, const Transducer &fst);

  // Resets all the private fields.
  void Reset();

  const ::fst::StringCompiler<Arc> compiler_;
  const ::fst::TokenType token_type_;
  absl::flat_hash_map<std::string, std::unique_ptr<const Transducer>> map_;
  std::unique_ptr<const SymbolTable> gensyms_;
};

template <class Arc>
bool RewriteManager<Arc>::Load(const std::string &filename) {
  Reset();
  std::unique_ptr<::fst::STTableFarReader<Arc>> reader(
      ::fst::STTableFarReader<Arc>::Open(filename));
  if (!reader) {
    LOG(ERROR) << "Unable to read FAR: " << filename;
    return false;
  }
  for (; !reader->Done(); reader->Next()) {
    AddToMap(reader->GetKey(), *reader->GetFst());
  }
  return true;
}

template <class Arc>
void RewriteManager<Arc>::Load(
    const absl::flat_hash_map<std::string, std::unique_ptr<const Transducer>>
        &map) {
  Reset();
  for (const auto &kv : map) {
    AddToMap(kv.first, *kv.second);
  }
}

template <class Arc>
const typename RewriteManager<Arc>::Transducer *RewriteManager<Arc>::GetFst(
    absl::string_view rule) const {
  const auto it = map_.find(rule);
  return it == map_.end() ? nullptr : it->second.get();
}

template <class Arc>
std::unique_ptr<typename RewriteManager<Arc>::Transducer>
RewriteManager<Arc>::GetFstSafe(absl::string_view rule) const {
  const auto it = map_.find(rule);
  return absl::WrapUnique(it == map_.end() ? nullptr : it->second->Copy(true));
}

template <class Arc>
bool RewriteManager<Arc>::SetFst(
    absl::string_view rule,
    const typename RewriteManager<Arc>::Transducer &input) {
  auto it = map_.find(rule);
  if (it == map_.end()) return false;
  it->second.reset(input.Copy(true));
  return true;
}

template <class Arc>
bool RewriteManager<Arc>::TopRewrite(
    absl::string_view rule, absl::string_view input, std::string *output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  return LatticeToTopString(lattice, output, token_type_);
}

template <class Arc>
bool RewriteManager<Arc>::OneTopRewrite(
    absl::string_view rule, absl::string_view input, std::string *output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToDfa(&lattice, /*optimal_only=*/true);
  return LatticeToOneTopString(lattice, output, token_type_);
}

template <class Arc>
bool RewriteManager<Arc>::TopRewrites(
    absl::string_view rule, absl::string_view input,
    std::vector<std::string> *output, absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToDfa(&lattice, /*optimal_only=*/true);
  return LatticeToStrings(lattice, output, token_type_);
}

#ifndef NO_GOOGLE
template <class Arc>
bool RewriteManager<Arc>::TopRewrites(
    absl::string_view rule, absl::string_view input,
    google::protobuf::RepeatedPtrField<std::string> *output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToDfa(&lattice, /*optimal_only=*/true);
  return LatticeToStrings(lattice, output, token_type_);
}
#endif  // NO_GOOGLE

template <class Arc>
bool RewriteManager<Arc>::TopRewrites(
    absl::string_view rule, absl::string_view input, int32_t nshortest,
    std::vector<std::string> *output, absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToShortest(&lattice, nshortest);
  return LatticeToStrings(lattice, output, token_type_);
}

#ifndef NO_GOOGLE
template <class Arc>
bool RewriteManager<Arc>::TopRewrites(
    absl::string_view rule, absl::string_view input, int32_t nshortest,
    google::protobuf::RepeatedPtrField<std::string> *output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToShortest(&lattice, nshortest);
  return LatticeToStrings(lattice, output, token_type_);
}
#endif  // NO_GOOGLE

template <class Arc>
bool RewriteManager<Arc>::Rewrites(
    absl::string_view rule, absl::string_view input,
    std::vector<std::string> *output, absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToDfa(&lattice, /*optimal_only=*/false);
  return LatticeToStrings(lattice, output, token_type_);
}

template <class Arc>
bool RewriteManager<Arc>::Rewrites(
    absl::string_view rule, absl::string_view input,
    google::protobuf::RepeatedPtrField<std::string> *output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  LatticeToDfa(&lattice, /*optimal_only=*/false);
  return LatticeToStrings(lattice, output, token_type_);
}

template <class Arc>
bool RewriteManager<Arc>::Matches(
    absl::string_view rule, absl::string_view input, absl::string_view output,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  MutableTransducer lattice;
  if (!RewriteLattice(rule, input, &lattice, pdt_parens_rule,
                      mpdt_assignments_rule)) {
    return false;
  }
  static const ::fst::OLabelCompare<Arc> ocomp;
  ::fst::ArcSort(&lattice, ocomp);
  MutableTransducer output_fst;
  compiler_(output, &output_fst);
  static const ::fst::IntersectOptions opts(true, ::fst::SEQUENCE_FILTER);
  ::fst::Intersect(lattice, output_fst, &lattice, opts);
  return lattice.Start() != ::fst::kNoStateId;
}

template <class Arc>
bool RewriteManager<Arc>::RewriteLattice(
    absl::string_view rule, absl::string_view input, MutableTransducer *lattice,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  // Input string compilation.
  MutableTransducer input_fst;
  compiler_(input, &input_fst);
  return RewriteLattice(rule, input_fst, lattice, pdt_parens_rule,
                        mpdt_assignments_rule);
}

template <class Arc>
bool RewriteManager<Arc>::RewriteLattice(
    absl::string_view rule, const Transducer &input, MutableTransducer *lattice,
    absl::string_view pdt_parens_rule,
    absl::string_view mpdt_assignments_rule) const {
  using Label = typename Arc::Label;
  // Rule lookup.
  std::unique_ptr<Transducer> rule_fst(GetFstSafe(rule));
  if (!rule_fst) {
    LOG(ERROR) << "Rule " << rule << " not found";
    return false;
  }
  if (!pdt_parens_rule.empty()) {
    std::unique_ptr<Transducer> pdt_parens_fst(GetFstSafe(pdt_parens_rule));
    if (!pdt_parens_fst) {
      LOG(ERROR) << "PDT parentheses rule " << pdt_parens_rule << " not found";
      return false;
    }
    std::vector<std::pair<Label, Label>> pdt_parens;
    MakeParenthesesVector(*pdt_parens_fst, &pdt_parens);
    if (!mpdt_assignments_rule.empty()) {  // MPDT composition.
      std::unique_ptr<Transducer> mpdt_assignments_fst(
          GetFstSafe(mpdt_assignments_rule));
      if (!mpdt_assignments_fst) {
        LOG(ERROR) << "MPDT assignments rule " << mpdt_assignments_rule
                   << " not found";
        return false;
      }
      std::vector<Label> mpdt_assignments;
      MakeAssignmentsVector(*mpdt_assignments_fst, pdt_parens,
                            &mpdt_assignments);
      return ::rewrite::RewriteLattice(input, *rule_fst, lattice, pdt_parens,
                                       mpdt_assignments);
    } else {  // PDT composition.
      return ::rewrite::RewriteLattice(input, *rule_fst, lattice, pdt_parens);
    }
  } else {  // FST composition.
    return ::rewrite::RewriteLattice(input, *rule_fst, lattice);
  }
}

template <class Arc>
void RewriteManager<Arc>::AddToMap(absl::string_view rule,
                                   const Transducer &fst) {
  if (rule == "*StringFstSymbolTable") {
    gensyms_.reset(fst.InputSymbols()->Copy());
  } else {
    auto sorted_fst = std::make_unique<MutableTransducer>(fst);
    static const ::fst::ILabelCompare<Arc> icomp;
    ::fst::ArcSort(sorted_fst.get(), icomp);
    map_[rule] = std::move(sorted_fst);
  }
}

template <class Arc>
void RewriteManager<Arc>::Reset() {
  map_.clear();
  gensyms_.reset();
}

using StdRewriteManager = RewriteManager<::fst::StdArc>;

}  // namespace rewrite

#endif  // NISABA_INTERIM_GRM2_REWRITE_REWRITE_MANAGER_H_
