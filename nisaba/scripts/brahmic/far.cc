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

#include "nisaba/scripts/brahmic/far.h"

#include "fst/compat.h"
#include "absl/strings/ascii.h"
#include "nisaba/port/file_util.h"

namespace nisaba {
namespace brahmic {

bool Far::Load() {
  constexpr char kFarPath[] = "com_google_nisaba/nisaba/scripts/brahmic";
  const auto far_dir = file::GetRunfilesResourcePath(kFarPath);
  if (!far_dir.ok()) {
    LOG(ERROR) << far_dir.status();
    return false;
  }
  constexpr char kFarExtn[] = ".far";
  const auto far_file_path = file::JoinPath(
      far_dir.value(), absl::AsciiStrToLower(far_name_) + kFarExtn);
  return grm_mgr_->LoadArchive(far_file_path);
}

std::unique_ptr<fst::StdFst> Far::Fst(const std::string& fst_name) const {
  return grm_mgr_->GetFstSafe(absl::AsciiStrToUpper(fst_name));
}

}  // namespace brahmic
}  // namespace nisaba
