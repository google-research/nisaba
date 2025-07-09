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

// See the documentation on further information on this API.

#ifndef NISABA_SCRIPTS_BRAHMIC_FAR_H_
#define NISABA_SCRIPTS_BRAHMIC_FAR_H_

#include "absl/status/status.h"
#include "absl/strings/string_view.h"
#include "nisaba/scripts/utils/far_base.h"

namespace nisaba {
namespace brahmic {

// Generic wrapper around FST archive with Brahmic transducers. This class
// injects the Brahmic-specific data path as well as the corresponding Brahmic
// script FARs.
//
// TODO: Instead of far_name, allow the FAR to be specified by
// Grammar type (iso, wellformed, etc.), Token type (utf8, byte) and
// compactness. This needs to done together here and in Grammar classes.
class Far : public FarBase{
 public:
  explicit Far(absl::string_view far_name) : FarBase(far_name) {}

  absl::Status Load();

 private:
  Far() = delete;
};

}  // namespace brahmic
}  // namespace nisaba

#endif  // NISABA_SCRIPTS_BRAHMIC_FAR_H_
