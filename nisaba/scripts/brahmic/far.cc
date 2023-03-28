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

#include "nisaba/scripts/brahmic/far.h"

namespace nisaba {
namespace brahmic {
namespace {
constexpr char kFarPath[] = "com_google_nisaba/nisaba/scripts/brahmic";
}  // namespace

absl::Status Far::Load() {
  return FarBase::Load(kFarPath);
}

}  // namespace brahmic
}  // namespace nisaba
