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

#include "nisaba/scripts/brahmic/grammar.h"

#include <cstddef>
#include <memory>
#include <string>
#include <vector>

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/log/check.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace brahmic {
namespace {

using ::testing::NotNull;

class GrammarTest : public ::testing::Test {
 public:
  void TestRewrite(absl::string_view input,
                   absl::string_view expected_output) const {
    std::string actual_output;
    EXPECT_OK(rewriter_->Rewrite(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
  }

  void TestAccept(absl::string_view input) const {
    EXPECT_OK(accepter_->Accept(input));
  }

  void TestReject(absl::string_view input) const {
    EXPECT_FALSE(accepter_->Accept(input).ok());
  }

  void TestNormalize(absl::string_view input,
                     absl::string_view expected_output) const {
    std::string actual_output;
    EXPECT_OK(normalizer_->Rewrite(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
    EXPECT_OK(normalizer_->NormalizeOnly(input, &actual_output));
    EXPECT_EQ(expected_output, actual_output);
  }

  void TestNormalizeReject(absl::string_view input) const {
    std::string actual_output;
    EXPECT_FALSE(normalizer_->Rewrite(input, &actual_output).ok());
  }

 protected:
  void SetUp() override {
    rewriter_ = std::make_unique<Grammar>("ISO", "FROM_DEVA");
    ASSERT_OK(rewriter_->Load());

    accepter_ = std::make_unique<Grammar>("WellFormed", "Deva");
    ASSERT_OK(accepter_->Load());

    normalizer_ = std::make_unique<Normalizer>("Deva");
    ASSERT_OK(normalizer_->Load());
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

TEST_F(GrammarTest, DoubleLoadNormalizeTest) {
  EXPECT_OK(normalizer_->Load());
  EXPECT_OK(normalizer_->Load());
}

TEST_F(GrammarTest, MultiLanguageNormalizeLoadTest) {
  const std::vector<std::string> languages = {
    "bn", "gu", "hi", "kn", "ml", "mr", "or", "pa", "si", "ta", "te" };
  std::vector<std::unique_ptr<Normalizer>> normalizers(languages.size());
  for (int i = 0; i < normalizers.size(); ++i) {
    normalizers[i] = std::make_unique<Normalizer>(languages[i]);
    EXPECT_OK(normalizers[i]->Load());
  }
}

TEST(NormalizerTest, SupportsFstTest) {
  EXPECT_TRUE(Normalizer::SupportsFst("Deva"));
  EXPECT_FALSE(Normalizer::SupportsFst("NotARealFst"));
}

TEST(PreLoadedGrammarTest, LoadVisualNormManager) {
  auto manager = LoadVisualNormManager();
  ASSERT_OK(manager);
  ASSERT_THAT(manager.value(), NotNull());
  EXPECT_OK(Grammar("visual_norm", "deva", *manager).VerifyLoad());
}

TEST(PreLoadedGrammarTest, LoadWellformedNormManager) {
  auto manager = LoadWellformedManager();
  ASSERT_OK(manager);
  ASSERT_THAT(manager.value(), NotNull());
  EXPECT_OK(Grammar("wellformed", "deva", *manager).VerifyLoad());
}

TEST(PreLoadedNormalizerTest, MakeFarFilePath) {
  EXPECT_EQ(MakeFarFilePath("/foo/bar", "baz"), "/foo/bar/baz.far");
}

TEST(PreLoadedGrammarTest, GrammarWithPreLoadedManager) {
  auto manager = LoadWellformedManager();
  ASSERT_OK(manager);
  ASSERT_THAT(manager.value(), NotNull());
  Grammar grammar("wellformed", "deva", *manager);
  ASSERT_OK(grammar.VerifyLoad());

  EXPECT_OK(grammar.Accept("हिन्दी"));
  EXPECT_FALSE(grammar.Accept("काु").ok());
}

TEST(PreLoadedNormalizerTest, NormalizerWithPreLoadedManagers) {
  auto visual_norm_manager = LoadVisualNormManager();
  auto wellformed_manager = LoadWellformedManager();
  ASSERT_OK(visual_norm_manager);
  ASSERT_THAT(visual_norm_manager.value(), NotNull());
  ASSERT_OK(wellformed_manager);
  ASSERT_THAT(wellformed_manager.value(), NotNull());

  Normalizer normalizer("deva", *visual_norm_manager, *wellformed_manager);
  ASSERT_OK(normalizer.VerifyLoad());

  std::string output;
  EXPECT_OK(normalizer.Rewrite("गोल्‍डबर्ग", &output));
  EXPECT_EQ(output, "गोल्डबर्ग");
  EXPECT_OK(
      normalizer.NormalizeOnly("गोल्‍डबर्ग", &output));
  EXPECT_EQ(output, "गोल्डबर्ग");
  EXPECT_FALSE(normalizer.Rewrite("काु", &output).ok());
}

void CheckReadingNormLoadOk(absl::string_view language_or_script) {
  ReadingNorm reading_norm(language_or_script);
  EXPECT_OK(reading_norm.Load());
}

void CheckReadingNormLoadError(absl::string_view language_or_script) {
  ReadingNorm reading_norm(language_or_script);
  EXPECT_EQ(reading_norm.Load().code(), absl::StatusCode::kInternal);
}

TEST(ReadingNorm, CheckLoad) {
  // For language.
  CheckReadingNormLoadOk("bn");
  CheckReadingNormLoadOk("hi");
  CheckReadingNormLoadOk("ml");
  // For script.
  CheckReadingNormLoadOk("Beng");
  CheckReadingNormLoadOk("Mlym");
  CheckReadingNormLoadOk("Lepc");
  // No reading norm.
  CheckReadingNormLoadError("Deva");
  CheckReadingNormLoadError("mr");
}

// TODO: Consider adding tests based on the data from the file
// nisaba/scripts/brahmic/testdata/reading_norm.tsv file.
void TestReadingNorm(absl::string_view language,
                     const std::vector<std::string>& inputs,
                     const std::vector<std::string>& expected_outputs) {
  ReadingNorm reading_norm(language);
  ASSERT_OK(reading_norm.Load());
  for (size_t n = 0; n < inputs.size(); ++n) {
    std::string output_word;
    EXPECT_OK(reading_norm.Rewrite(inputs[n], &output_word));
    EXPECT_EQ(output_word, expected_outputs[n]);
  }
}

TEST(ReadingNorm, bn) {
  const std::vector<std::string> inputs({"সংগে"});
  const std::vector<std::string> expected_outputs({"সঙ্গে"});
  TestReadingNorm("bn", inputs, expected_outputs);
}

TEST(ReadingNorm, hi) {
  const std::vector<std::string> inputs({"काङ्ग्रेस"});
  const std::vector<std::string> expected_outputs({"कांग्रेस"});
  TestReadingNorm("hi", inputs, expected_outputs);
}

TEST(ReadingNorm, ml) {
  // clang-format off
  const std::vector<std::string> inputs({"​സ​ന്യാ​സി​വ​ൎയ്യ​ന്മാ​ർ​ക്ക"});
  const std::vector<std::string> expected_outputs({"സന്യാസിവര്യന്മാർക്ക"});
  // clang-format on
  TestReadingNorm("ml", inputs, expected_outputs);
}

}  // namespace
}  // namespace brahmic
}  // namespace nisaba
