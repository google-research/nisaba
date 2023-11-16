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

// BaseRuleCascade provides a rich class of member functions for rewriting
// string inputs for any implementation that provides the following interface:
//
// bool RewriteLattice(absl::string_view input,
//                     MutableTransducer *lattice) const;
//
// const ::fst::SymbolTable *GeneratedSymbols() const;

#ifndef NISABA_INTERIM_GRM2_REWRITE_BASE_RULE_CASCADE_H_
#define NISABA_INTERIM_GRM2_REWRITE_BASE_RULE_CASCADE_H_

#include <cstdint>
#include <ostream>
#include <sstream>
#include <string>
#include <vector>

#ifndef NO_GOOGLE
#include "google/protobuf/repeated_field.h"
#endif  // NO_GOOGLE
#include "fst/arcsort.h"
#include "fst/compose.h"
#include "fst/fst.h"
#include "fst/string.h"
#include "fst/symbol-table.h"
#include "fst/log.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/grm2/rewrite/rewrite.h"

namespace rewrite {

template <class Arc>
class BaseRuleCascade {
 public:
  using Label = typename Arc::Label;

  using Transducer = ::fst::Fst<Arc>;
  using MutableTransducer = ::fst::VectorFst<Arc>;

  // TODO: Add symbol table support, or YAGNI?
  explicit BaseRuleCascade(
      ::fst::TokenType token_type = ::fst::TokenType::BYTE)
      : compiler_(token_type), token_type_(token_type) {}

  virtual ~BaseRuleCascade() = default;

 public:
  // Rewrites the output tape of `input` and stores the result in `output`. The
  // output tape of `output` is the result of the rewrite; the contents of the
  // input tape of `output` is implemenation-defined.
  //
  // Note `input` and `output` may be the same object.
  virtual bool Rewrite(const Transducer &input,
                       MutableTransducer *output) const = 0;

  // Returns the symbol table for generated output symbols when available, or
  // nullptr otherwise.
  virtual const ::fst::SymbolTable *GeneratedSymbols() const {
    return nullptr;
  }

  // TopRewrite() computes one top rewrite, returning false if composition
  // fails. Requires a semiring with the path property.

  // Produces the top rewrite as an epsilon-free acceptor.
  bool TopRewrite(absl::string_view input, MutableTransducer *output) const;

  // Produces the top rewrite as a sequence of non-epsilon labels.
  bool TopRewrite(absl::string_view input, std::vector<Label> *output) const;

  // Produces the top rewrite string.
  bool TopRewrite(absl::string_view input, std::string *output) const;

  // Produces the top rewrite string, and the corresponding debug string.
  bool TopRewrite(absl::string_view input, std::string *output,
                  std::string *debug) const;

  // OneTopRewrite() computes one top rewrite, returning false if composition
  // fails or if there's a tie for the top rewrite. Requires a semiring with the
  // path property.

  // Produces the top rewrite as an epsilon-free acceptor.
  bool OneTopRewrite(absl::string_view input, MutableTransducer *output) const;

  // Produces the top rewrite as a sequence of non-epsilon labels.
  bool OneTopRewrite(absl::string_view input, std::vector<Label> *output) const;

  // Produces the top rewrite string.
  bool OneTopRewrite(absl::string_view input, std::string *output) const;

  // Produces the top rewrite string, and the corresponding debug string.
  bool OneTopRewrite(absl::string_view input, std::string *output,
                     std::string *debug) const;

  // TopRewrites() computes the top `nshortest` rewrites, returning false if
  // composition fails. Requires a semiring with the path property.

  // Produces the top `nshortest` rewrite as an acceptor. Epsilon arcs might be
  // added by the shortest path algorithm.
  bool TopRewrites(absl::string_view input, int32_t nshortest,
                   MutableTransducer *output) const;

  // Produces the top `nshortest` rewrite as sequences of labels. Epsilon labels
  // might be added by the shortest path algorithm.
  bool TopRewrites(absl::string_view input, int32_t nshortest,
                   std::vector<std::vector<Label>> *output) const;

  // Produces the top `nshortest` rewrite strings.
  bool TopRewrites(absl::string_view input, int32_t nshortest,
                   std::vector<std::string> *output) const;

  // Produces the top `nshortest` rewrite strings, and the corresponding debug
  // strings.
  bool TopRewrites(absl::string_view input, int32_t nshortest,
                   std::vector<std::string> *output,
                   std::vector<std::string> *debug) const;

#ifndef NO_GOOGLE
  // Produces the top `nshortest` rewrite strings.
  bool TopRewrites(absl::string_view input, int32_t nshortest,
                   google::protobuf::RepeatedPtrField<std::string> *output) const;
#endif  // NO_GOOGLE

  // TopRewrites() computes all optimal rewrites, returning false if composition
  // fails. Requires a semiring with the path property.

  // Produces all optimal rewrites as an epsilon-free acceptor.
  bool TopRewrites(absl::string_view input, MutableTransducer *output) const;

  // Produces all optimal rewrites as sequences of labels.
  bool TopRewrites(absl::string_view input,
                   std::vector<std::vector<Label>> *output) const;

  // Produces all optimal rewrite strings.
  bool TopRewrites(absl::string_view input,
                   std::vector<std::string> *output) const;

  // Produces all optimal rewrite strings, and the corresponding debug strings.
  bool TopRewrites(absl::string_view input, std::vector<std::string> *output,
                   std::vector<std::string> *debug) const;

#ifndef NO_GOOGLE
  // Produces all optimal rewrite strings.
  bool TopRewrites(absl::string_view input,
                   google::protobuf::RepeatedPtrField<std::string> *output) const;
#endif  // NO_GOOGLE

  // Rewrites() computes all rewrites, returning false if composition fails.

  // Produces all rewrites as an epsilon-free acceptor.
  bool Rewrites(absl::string_view input, MutableTransducer *output) const;

  // Produces all rewrites as sequences of labels.
  bool Rewrites(absl::string_view input,
                std::vector<std::vector<Label>> *output) const;

  // Produces all rewrite strings.
  bool Rewrites(absl::string_view input,
                std::vector<std::string> *output) const;

  // Produces all rewrite strings, and the corresponding debug strings.
  bool Rewrites(absl::string_view input, std::vector<std::string> *output,
                std::vector<std::string> *debug) const;

#ifndef NO_GOOGLE
  // Produces all rewrite strings.
  bool Rewrites(absl::string_view input,
                google::protobuf::RepeatedPtrField<std::string> *output) const;
#endif  // NO_GOOGLE

  // Determines whether the rule cascade allows a given input/output pair; i.e.,
  // whether the intersection of the output string and the output lattice is
  // non-null.
  bool Matches(absl::string_view input, absl::string_view output) const;

 private:
  bool LabelsToDebugString(const std::string &output,
                           const std::vector<Label> &labels,
                           std::string *debug) const;

  void PrintDebugSymbol(Label label, std::ostream &ostrm) const;

  bool RewriteLattice(absl::string_view input,
                      MutableTransducer *lattice) const;

  const ::fst::StringCompiler<Arc> compiler_;
  const ::fst::TokenType token_type_;
};

// Computes one top rewrite, returning false if composition fails. Requires a
// semiring with the path property.

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrite(absl::string_view input,
                                      MutableTransducer *output) const {
  if (!RewriteLattice(input, output)) return false;
  LatticeToShortest(output);
  return true;
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrite(
    absl::string_view input, std::vector<typename Arc::Label> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrite(input, &lattice)) return false;
  return ::fst::StringFstToOutputLabels(lattice, output);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrite(absl::string_view input,
                                      std::string *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrite(input, &lattice)) return false;
  return LatticeToTopString(lattice, output, token_type_);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrite(absl::string_view input,
                                      std::string *output,
                                      std::string *debug) const {
  output->clear();
  debug->clear();
  std::vector<Label> labels;
  if (!TopRewrite(input, &labels)) return false;
  if (!::fst::LabelsToString(labels, output, token_type_)) return false;
  LabelsToDebugString(*output, labels, debug);
  return true;
}

// Computes one top rewrite, returning false if composition fails or if there's
// a tie for the top rewrite. Requires a semiring with the path property.

template <class Arc>
bool BaseRuleCascade<Arc>::OneTopRewrite(absl::string_view input,
                                         MutableTransducer *output) const {
  if (!RewriteLattice(input, output)) return false;
  LatticeToDfa(output, /*optimal_only=*/true);
  // Make sure there is only one path.
  for (::fst::StateIterator<MutableTransducer> siter(*output);
       !siter.Done(); siter.Next()) {
    if (output->NumArcs(siter.Value()) > 1) return false;
  }
  return true;
}

template <class Arc>
bool BaseRuleCascade<Arc>::OneTopRewrite(
    absl::string_view input, std::vector<typename Arc::Label> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!OneTopRewrite(input, &lattice)) return false;
  return ::fst::StringFstToOutputLabels(lattice, output);
}

template <class Arc>
bool BaseRuleCascade<Arc>::OneTopRewrite(absl::string_view input,
                                         std::string *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!OneTopRewrite(input, &lattice)) return false;
  return LatticeToOneTopString(lattice, output, token_type_);
}

template <class Arc>
bool BaseRuleCascade<Arc>::OneTopRewrite(absl::string_view input,
                                         std::string *output,
                                         std::string *debug) const {
  output->clear();
  debug->clear();
  std::vector<Label> labels;
  if (!OneTopRewrite(input, &labels)) return false;
  if (!::fst::LabelsToString(labels, output, token_type_)) return false;
  LabelsToDebugString(*output, labels, debug);
  return true;
}

// Computes the top `nshortest` rewrites, returning false if composition fails.
// Requires a semiring with the path property.

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       int32_t nshortest,
                                       MutableTransducer *output) const {
  if (!RewriteLattice(input, output)) return false;
  LatticeToShortest(output, nshortest);
  return true;
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(
    absl::string_view input, int32_t nshortest,
    std::vector<std::vector<Label>> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, nshortest, &lattice)) return false;
  return LatticeToLabels(lattice, output);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       int32_t nshortest,
                                       std::vector<std::string> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, nshortest, &lattice)) return false;
  return LatticeToStrings(lattice, output, token_type_);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       int32_t nshortest,
                                       std::vector<std::string> *output,
                                       std::vector<std::string> *debug) const {
  output->clear();
  debug->clear();
  std::vector<std::vector<Label>> labelss;
  if (!TopRewrites(input, nshortest, &labelss)) return false;
  output->reserve(labelss.size());
  debug->reserve(labelss.size());
  for (const auto &labels : labelss) {
    output->emplace_back();
    debug->emplace_back();
    if (!::fst::LabelsToString(labels, &output->back(), token_type_)) {
      return false;
    }
    LabelsToDebugString(output->back(), labels, &debug->back());
  }
  return true;
}

#ifndef NO_GOOGLE
template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(
    absl::string_view input, int32_t nshortest,
    google::protobuf::RepeatedPtrField<std::string> *output) const {
  output->Clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, nshortest, lattice)) return false;
  return LatticeToStrings(lattice, output, token_type_);
}
#endif  // NO_GOOGLE

// Computes all optimal rewrites, returning false if composition fails. Requires
// a semiring with the path property.

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       MutableTransducer *output) const {
  if (!RewriteLattice(input, output)) return false;
  LatticeToDfa(output, /*optimal_only=*/true);
  return true;
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(
    absl::string_view input, std::vector<std::vector<Label>> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, &lattice)) return false;
  return LatticeToLabels(lattice, output);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       std::vector<std::string> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, &lattice)) return false;
  return LatticeToStrings(lattice, output, token_type_);
}

template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(absl::string_view input,
                                       std::vector<std::string> *output,
                                       std::vector<std::string> *debug) const {
  output->clear();
  debug->clear();
  std::vector<std::vector<Label>> labelss;
  if (!TopRewrites(input, &labelss)) return false;
  output->reserve(labelss.size());
  debug->reserve(labelss.size());
  for (const auto &labels : labelss) {
    output->emplace_back();
    debug->emplace_back();
    if (!::fst::LabelsToString(labels, &output->back(), token_type_)) {
      return false;
    }
    LabelsToDebugString(output->back(), labels, &debug->back());
  }
  return true;
}

#ifndef NO_GOOGLE
template <class Arc>
bool BaseRuleCascade<Arc>::TopRewrites(
    absl::string_view input,
    google::protobuf::RepeatedPtrField<std::string> *output) const {
  output->Clear();
  MutableTransducer lattice;
  if (!TopRewrites(input, &lattice)) return false;
  return LatticeToStrings(lattice, output, token_type_);
}
#endif  // NO_GOOGLE

// Computes all rewrites, returning false if composition fails.

template <class Arc>
bool BaseRuleCascade<Arc>::Rewrites(absl::string_view input,
                                    MutableTransducer *output) const {
  if (!RewriteLattice(input, output)) return false;
  LatticeToDfa(output, /*optimal_only=*/false);
  return true;
}

template <class Arc>
bool BaseRuleCascade<Arc>::Rewrites(
    absl::string_view input, std::vector<std::vector<Label>> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!Rewrites(input, &lattice)) return false;
  return LatticeToLabels(lattice, output);
}

template <class Arc>
bool BaseRuleCascade<Arc>::Rewrites(absl::string_view input,
                                    std::vector<std::string> *output) const {
  output->clear();
  MutableTransducer lattice;
  if (!Rewrites(input, &lattice)) return false;
  return LatticeToStrings(lattice, output, token_type_);
}

template <class Arc>
bool BaseRuleCascade<Arc>::Rewrites(absl::string_view input,
                                    std::vector<std::string> *output,
                                    std::vector<std::string> *debug) const {
  output->clear();
  debug->clear();
  std::vector<std::vector<Label>> labelss;
  if (!Rewrites(input, &labelss)) return false;
  output->reserve(labelss.size());
  debug->reserve(labelss.size());
  for (const auto &labels : labelss) {
    output->emplace_back();
    debug->emplace_back();
    if (!::fst::LabelsToString(labels, &output->back(), token_type_)) {
      return false;
    }
    LabelsToDebugString(output->back(), labels, &debug->back());
  }
  return true;
}

#ifndef NO_GOOGLE
template <class Arc>
bool BaseRuleCascade<Arc>::Rewrites(
    absl::string_view input,
    google::protobuf::RepeatedPtrField<std::string> *output) const {
  output->Clear();
  MutableTransducer lattice;
  if (!RewriteLattice(input, &lattice)) return false;
  LatticeToDfa(&lattice, /*optimal_only=*/false);
  return LatticeToStrings(lattice, output, token_type_);
}
#endif  // NO_GOOGLE

// Determines whether the rule cascade allows a given input/output pair; i.e.,
// whether the intersection of the output string and the output lattice is
// non-null.
template <class Arc>
bool BaseRuleCascade<Arc>::Matches(absl::string_view input,
                                   absl::string_view output) const {
  MutableTransducer lattice;
  if (!RewriteLattice(input, &lattice)) return false;
  MutableTransducer output_fst;
  compiler_(output, &output_fst);
  static const ::fst::OLabelCompare<Arc> ocomp;
  ArcSort(&lattice, ocomp);
  static const ::fst::ComposeOptions opts(true, ::fst::SEQUENCE_FILTER);
  ::fst::Compose(lattice, output_fst, &lattice, opts);
  return lattice.Start() != ::fst::kNoStateId;
}

// Private methods.

template <class Arc>
bool BaseRuleCascade<Arc>::LabelsToDebugString(const std::string &output,
                                               const std::vector<Label> &labels,
                                               std::string *debug) const {
  debug->clear();
  // This really only makes sense in BYTE mode.
  if (token_type_ != ::fst::TokenType::BYTE) {
    *debug = output;
    return true;
  }
  std::stringstream sstrm;
  auto it = labels.begin();
  if (it == labels.end()) return true;
  PrintDebugSymbol(*it, sstrm);
  for (++it; it != labels.end(); ++it) PrintDebugSymbol(*it, sstrm);
  *debug = sstrm.str();
  return true;
}

template <class Arc>
void BaseRuleCascade<Arc>::PrintDebugSymbol(Label label,
                                            std::ostream &ostrm) const {
  if (const auto *gensyms = GeneratedSymbols()) {
    // First check the symbol table, then back off to bytes.
    const auto &symbol = gensyms->Find(label);
    if (symbol.empty()) {
      ostrm << static_cast<unsigned char>(label);
    } else {
      ostrm << '[' << symbol << ']';
    }
  } else {
    // No symbol table.
    ostrm << static_cast<unsigned char>(label);
  }
}

template <class Arc>
bool BaseRuleCascade<Arc>::RewriteLattice(absl::string_view input,
                                          MutableTransducer *lattice) const {
  compiler_(input, lattice);
  if (!Rewrite(*lattice, lattice)) return false;
  return internal::CheckNonEmptyAndCleanup(lattice);
}

}  // namespace rewrite

#endif  // NISABA_INTERIM_GRM2_REWRITE_BASE_RULE_CASCADE_H_
