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

#ifndef NISABA_INTERIM_GRM2_REWRITE_PARENS_H_
#define NISABA_INTERIM_GRM2_REWRITE_PARENS_H_

#include <map>
#include <set>
#include <utility>
#include <vector>

#include "fst/fst.h"
#include "absl/log/log.h"

// This is used by (M)PdtCompose and and associated grammar managers when they
// express parentheses and/or assignments as transducers.

namespace rewrite {

template <class Arc>
void MakeParenthesesVector(
    const ::::fst::Fst<Arc> &parens_transducer,
    std::vector<std::pair<typename Arc::Label, typename Arc::Label>> *parens) {
  using Label = typename Arc::Label;
  std::set<Label> seen_labels;
  for (::::fst::StateIterator<::::fst::Fst<Arc>> siter(parens_transducer);
       !siter.Done(); siter.Next()) {
    const auto state = siter.Value();
    for (::::fst::ArcIterator<::::fst::Fst<Arc>> aiter(parens_transducer, state);
         !aiter.Done(); aiter.Next()) {
      const auto &arc = aiter.Value();
      if (!arc.ilabel && !arc.olabel) {
      } else if (!arc.ilabel) {
        LOG(WARNING) << "MakeParensVector: left parenthesis corresponding to "
                     << arc.olabel << " is null";
      } else if (!arc.olabel) {
        LOG(WARNING) << "MakeParensVector: right parenthesis corresponding to "
                     << arc.ilabel << " is null";
      } else {
        {
          const auto it = seen_labels.find(arc.ilabel);
          if (it != seen_labels.end()) {
            LOG(FATAL) << "MakeParensVector: risky reuse of left paren "
                       << arc.ilabel;
          }
        }
        {
          const auto it = seen_labels.find(arc.olabel);
          if (it != seen_labels.end()) {
            LOG(FATAL) << "MakeParensVector: risky reuse of right paren "
                       << arc.olabel;
          }
        }
        if (arc.ilabel == arc.olabel) {
          LOG(FATAL) << "MakeParensVector: left parenthesis " << arc.ilabel
                     << " is identical to right parenthesis " << arc.olabel;
        }
        parens->emplace_back(arc.ilabel, arc.olabel);
      }
    }
  }
}

template <class Arc>
void MakeAssignmentsVector(
    const ::::fst::Fst<Arc> &assignments_transducer,
    const std::vector<std::pair<typename Arc::Label, typename Arc::Label>>
        &parens,
    std::vector<typename Arc::Label> *assignments) {
  using Label = typename Arc::Label;
  std::map<Label, Label> assignment_map;
  for (::::fst::StateIterator<::::fst::Fst<Arc>> siter(assignments_transducer);
       !siter.Done(); siter.Next()) {
    for (::::fst::ArcIterator<::::fst::Fst<Arc>> aiter(assignments_transducer,
                                                   siter.Value());
         !aiter.Done(); aiter.Next()) {
      const auto &arc = aiter.Value();
      if (!arc.ilabel && !arc.olabel) {
      } else if (!arc.ilabel) {
        LOG(WARNING) << "MakeAssignmentsVector: left parenthesis"
                     << "corresponding to assignment " << arc.olabel
                     << " is null";
      } else if (!arc.olabel) {
        LOG(WARNING) << "MakeAssignmentsVector: assignment corresponding"
                     << " to left parenthesis " << arc.ilabel << " is null";
      } else {
        assignment_map[arc.ilabel] = arc.olabel;
      }
    }
  }
  for (const auto &paren : parens) {
    const auto it = assignment_map.find(paren.first);
    if (it == assignment_map.end()) {
      LOG(FATAL) << "MakeAssignmentsVectors: left parenthesis " << paren.first
                 << " has no statck assignment";
    }
    assignments->emplace_back(it->second);
  }
}

}  // namespace rewrite.

#endif  // NISABA_INTERIM_GRM2_REWRITE_PARENS_H_
