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

#include "nisaba/scripts/brahmic/far.h"

#include <memory>
#include <string>

#include "fst/fstlib.h"
#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"

using fst::StdFst;
using fst::StdVectorFst;
using StringCompiler = fst::StringCompiler<fst::StdArc>;

namespace nisaba {
namespace brahmic {
namespace {

bool UTF8AcceptsString(const StdFst &fsa, const std::string &s) {
  StringCompiler string_compiler(fst::TokenType::UTF8);
  StdVectorFst string_fst;
  string_compiler(s, &string_fst);

  StdVectorFst output;
  fst::Compose(string_fst, fsa, &output);
  return output.Start() != fst::kNoStateId;
}

TEST(WellformedFarTest, Basic) {
  Far far("wellformed_utf8");
  ASSERT_OK(far.Load());
  std::unique_ptr<const StdFst> deva = far.Fst("Deva");
  ASSERT_TRUE(deva != nullptr);

  EXPECT_TRUE(UTF8AcceptsString(*deva, "\u0905"));
  EXPECT_FALSE(UTF8AcceptsString(*deva, "A"));
}

}  // namespace
}  // namespace brahmic
}  // namespace nisaba
