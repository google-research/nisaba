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

#include "nisaba/brahmic/grammar.h"

#include "nisaba/utils/util.h"

namespace nisaba {
namespace brahmic {

bool Grammar::Load() {
  const auto far_path = utils::GetRunfilesResourcePath(far_file_path_);
  if (!far_path.ok()) {
    LOG(ERROR) << far_path.status();
    return false;
  }
  return grm_mgr_->LoadArchive(far_path.value());
}

bool Grammar::Rewrite(const std::string& input, std::string *output) const {
  return grm_mgr_->RewriteBytes(fst_name_, input, output);
}

bool Grammar::Accept(const std::string& input) const {
  std::string output;
  return grm_mgr_->RewriteBytes(fst_name_, input, &output);
}

bool Normalizer::Load() {
  return visual_norm_.Load() && wellformed_.Load();
}

bool Normalizer::Rewrite(const std::string& input, std::string *output) const {
  return visual_norm_.Rewrite(input, output) && wellformed_.Accept(*output);
}

bool Normalizer::NormalizeOnly(const std::string& input,
                               std::string* output) const {
  return visual_norm_.Rewrite(input, output);
}

}  // namespace brahmic
}  // namespace nisaba
