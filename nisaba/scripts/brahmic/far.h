// Copyright 2021 Nisaba Authors.
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

// See the documentation on further information on this API.

#ifndef NISABA_SCRIPTS_BRAHMIC_FAR_H_
#define NISABA_SCRIPTS_BRAHMIC_FAR_H_

#include <memory>
#include <string>

#include "fst/fstlib.h"
#include "thrax/grm-manager.h"
#include "absl/memory/memory.h"

namespace nisaba {
namespace brahmic {

// Generic wrapper around FST archive with Brahmic transducers.
// TODO: Instead of far_name, allow the FAR to be specified by
// Grammar type (iso, wellformed, etc.), Token type (utf8, byte) and
// compactness. This needs to done together here and in Grammar classes.
class Far {
 public:
  explicit Far(const std::string& far_name)
      : far_name_(far_name),
        grm_mgr_(absl::make_unique<::thrax::GrmManager>()){}

  bool Load();
  std::unique_ptr<::fst::StdFst> Fst(const std::string& fst_name) const;

 private:
  const std::string far_name_;
  const std::unique_ptr<::thrax::GrmManager> grm_mgr_;
};

}  // namespace brahmic
}  // namespace nisaba

#endif  // NISABA_SCRIPTS_BRAHMIC_FAR_H_
