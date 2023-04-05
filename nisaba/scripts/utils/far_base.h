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

#ifndef NISABA_SCRIPTS_UTILS_FAR_BASE_H_
#define NISABA_SCRIPTS_UTILS_FAR_BASE_H_

#include <memory>
#include <string>

#include "fst/fstlib.h"
#include "thrax/grm-manager.h"
#include "absl/status/status.h"
#include "absl/strings/string_view.h"

namespace nisaba {

constexpr char kFarExtn[] = ".far";

// Generic wrapper around FST archive with transducers from a given directory.
// TODO: Instead of far_name, allow the FAR to be specified by
// Grammar type (iso, wellformed, etc.), Token type (utf8, byte) and
// compactness. This needs to done together here and in Grammar classes.
class FarBase {
 public:
  // Fetches FST given by its name.
  std::unique_ptr<::fst::StdFst> Fst(absl::string_view fst_name) const;

 protected:
  explicit FarBase(absl::string_view far_name) : far_name_(far_name) {}

  // Loads FAR from the supplied directory `far_path`.
  absl::Status Load(absl::string_view far_path);

 private:
  FarBase() = delete;

  const std::string far_name_;
  ::thrax::GrmManager grm_mgr_;
};

}  // namespace nisaba

#endif  // NISABA_SCRIPTS_UTILS_FAR_BASE_H_
