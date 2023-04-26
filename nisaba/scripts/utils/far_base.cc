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

#include "nisaba/scripts/utils/far_base.h"

#include "absl/strings/ascii.h"
#include "absl/strings/str_cat.h"
#include "nisaba/port/file_util.h"

namespace nisaba {

absl::Status FarBase::Load(absl::string_view far_path) {
  const auto far_dir = file::GetRunfilesResourcePath(far_path);
  if (!far_dir.ok()) return far_dir.status();

  const auto far_file_path = file::JoinPath(
      far_dir.value(), absl::AsciiStrToLower(far_name_) + kFarExtn);
  if (!grm_mgr_.LoadArchive(far_file_path)) {
    return absl::NotFoundError(absl::StrCat("Failed to load archive from ",
                                            far_file_path));
  }
  return absl::OkStatus();
}

std::unique_ptr<fst::StdFst> FarBase::Fst(
    absl::string_view fst_name) const {
  return grm_mgr_.GetFstSafe(absl::AsciiStrToUpper(fst_name));
}

}  // namespace nisaba
