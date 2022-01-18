// Copyright 2022 Nisaba Authors.
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

#include "nisaba/scripts/brahmic/grammar.h"

#include "absl/strings/str_cat.h"
#include "nisaba/port/file_util.h"
#include "nisaba/port/status_macros.h"

namespace nisaba {
namespace brahmic {

absl::Status Grammar::Load() {
  const auto far_path = file::GetRunfilesResourcePath(far_file_path_);
  if (!far_path.ok()) return far_path.status();
  if (!grm_mgr_->LoadArchive(far_path.value())) {
    return absl::InternalError(absl::StrCat("Failed to load archive from \"",
                                            far_path.value(), "\""));
  }

  static const std::map<std::string, std::string>& lang_script_map =
      {{"bn", "Beng"}, {"gu", "Gujr"}, {"hi", "Deva"}, {"kn", "Knda"},
       {"ml", "Mlym"}, {"mr", "Deva"}, {"or", "Orya"}, {"pa", "Guru"},
       {"si", "Sinh"}, {"ta", "Taml"}, {"te", "Telu"}};

  if (grm_mgr_->GetFstMap()->count(fst_name_) == 0) {
    const auto entry = lang_script_map.find(absl::AsciiStrToLower(fst_name_));
    if (entry == lang_script_map.end()) {
      return absl::InternalError(absl::StrCat(
          "FST \"", fst_name_, "\" not found in lowercase inside FAR \"",
          far_path.value(), "\""));
    }
    fst_name_ = absl::AsciiStrToUpper(entry->second);
    if (grm_mgr_->GetFstMap()->count(fst_name_) == 0) {
      return absl::InternalError(absl::StrCat(
          "FST \"", fst_name_, "\" not found in uppercase inside FAR \"",
          far_path.value(), "\""));
    }
  }
  return absl::OkStatus();
}

absl::Status Grammar::Rewrite(absl::string_view input,
                              std::string *output) const {
  if (!grm_mgr_->RewriteBytes(fst_name_, input, output)) {
    return absl::InternalError(absl::StrCat(
        "Rewrite failed for \"", input, "\""));
  }
  return absl::OkStatus();
}

absl::Status Grammar::Accept(absl::string_view input) const {
  std::string output;
  if (!grm_mgr_->RewriteBytes(fst_name_, input, &output)) {
    return absl::InternalError(absl::StrCat(
        "Rewrite failed for \"", input, "\""));
  }
  return absl::OkStatus();
}

absl::Status Normalizer::Load() {
  RETURN_IF_ERROR(visual_norm_.Load());
  RETURN_IF_ERROR(wellformed_.Load());
  return absl::OkStatus();
}

absl::Status Normalizer::Rewrite(absl::string_view input,
                                 std::string *output) const {
  RETURN_IF_ERROR(NormalizeOnly(input, output));
  RETURN_IF_ERROR(wellformed_.Accept(*output));
  return absl::OkStatus();
}

absl::Status Normalizer::NormalizeOnly(absl::string_view input,
                                       std::string *output) const {
  return visual_norm_.Rewrite(input, output);
}

}  // namespace brahmic
}  // namespace nisaba
