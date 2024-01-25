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

#ifndef NISABA_INTERIM_TESTING_TESTDATA_H_
#define NISABA_INTERIM_TESTING_TESTDATA_H_

// Shared library code for rewrite testing.

#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/testing/testdata.pb.h"

namespace testing {

// Loads rewrites from textproto file.
absl::StatusOr<Rewrites> GetRewritesTextProto(absl::string_view filename);

// Serializes rewrites from file to textproto.
absl::Status SetRewritesTextProto(absl::string_view filename,
                                  const Rewrites &rewrites);

}  // namespace testing

#endif  // NISABA_INTERIM_TESTING_TESTDATA_H_
