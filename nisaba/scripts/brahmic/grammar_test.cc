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

#include "nisaba/scripts/brahmic/grammar.h"

#include <memory>
#include <string>

#include "gtest/gtest.h"
#include "absl/memory/memory.h"

namespace nisaba {
namespace brahmic {
namespace {

class GrammarTest : public ::testing::Test {
 public:
  void TestRewrite(const std::string& input,
                   const std::string& expected_output) const {
    std::string actual_output;
    EXPECT_TRUE(rewriter_->Rewrite(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
  }

  void TestAccept(const std::string& input) const {
    EXPECT_TRUE(accepter_->Accept(input));
  }

  void TestReject(const std::string& input) const {
    EXPECT_FALSE(accepter_->Accept(input));
  }

  void TestNormalize(const std::string& input,
                     const std::string& expected_output) const {
    std::string actual_output;
    EXPECT_TRUE(normalizer_->Rewrite(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
    EXPECT_TRUE(normalizer_->NormalizeOnly(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
  }

  void TestNormalizeReject(const std::string& input) const {
    std::string actual_output;
    EXPECT_FALSE(normalizer_->Rewrite(input, &actual_output));
  }

 protected:
  void SetUp() override {
    rewriter_ = absl::make_unique<Grammar>("ISO", "FROM_DEVA");
    rewriter_->Load();

    accepter_ = absl::make_unique<Grammar>("WellFormed", "Deva");
    accepter_->Load();

    normalizer_ = absl::make_unique<Normalizer>("Deva");
    normalizer_->Load();
  }

  std::unique_ptr<Grammar> rewriter_;
  std::unique_ptr<Grammar> accepter_;
  std::unique_ptr<Normalizer> normalizer_;
};

TEST_F(GrammarTest, SimpleTest) {
  TestRewrite("हिन्दी", "hindī");
  TestAccept("हिन्दी");
  TestReject("काु");  // Two adjacent vowel signs are illegal.
}

TEST_F(GrammarTest, NormalizeTest) {
  TestNormalize("गोल्‍डबर्ग", "गोल्डबर्ग");
  TestNormalizeReject("काु");
}

}  // namespace
}  // namespace brahmic
}  // namespace nisaba
