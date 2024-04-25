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

// Tests that rules read from a FAR matches textproto-based testdata.
//
// More specifically, it tests that:
//
// * The textproto can be parsed
// * For each input in the testproto, there are zero or more expected outputs,
//   or the failure bit is set
//
// Sample usage:
//
//   cc_test(
//       name = "en_us_text_proto_test"
//       args = [
//           "--textproto_path=full/path/to/test/file",
//           "--far_path=full/path/to/far",
//       ],
//       linkstatic = 1,
//       data = [
//           ":path/to/test/file/relative/to/package,
//           ":far_label/relative/to/package,
//       ],
//       deps = [
//           "//third_party/nisaba/interim/testing:test_textproto_lib",
//           "//testing/base/public:gunit_main_no_heapcheck",
//       ],
//   )

#include <iterator>
#include <string>
#include <vector>

#include "fst/script/getters.h"
#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/algorithm/container.h"
#include "absl/flags/flag.h"
#include "absl/log/check.h"
#include "absl/log/log.h"
#include "absl/strings/str_join.h"
#include "absl/strings/string_view.h"
#include "nisaba/interim/grm2/rewrite/rule_cascade.h"
#include "nisaba/interim/testing/testdata.h"
#include "absl/flags/parse.h"

ABSL_FLAG(std::string, far_path, "", "Path of FAR to read rules from");
ABSL_FLAG(std::string, textproto_path, "", "Rewrites textproto path");
ABSL_FLAG(std::string, token_type, "byte",
          "Token type (one of \"byte\", \"utf8\")");
// See below to see how these modes are interpreted.
ABSL_FLAG(std::string, mode, "exact",
          "Rewrite mode (one of \"exact\", \"one_top\", \"subset\", \"top\")");

namespace testing {
namespace {

using ::::fst::TokenType;
using ::::fst::script::GetTokenType;
using ::rewrite::StdRuleCascade;
using ::testing::IsSupersetOf;
using ::testing::SizeIs;
using ::testing::UnorderedElementsAreArray;

// Helper for computing set difference; C1 and C2 are containers (e.g., STL
// vectors, or protocol buffer repeated pointer fields) of strings.
template <class C1, class C2>
std::string StringSetDifference(const C1 &output1, const C2 &output2,
                                absl::string_view delimiter = ", ") {
  std::vector<std::string> difference;
  absl::c_set_difference(output1, output2, std::back_inserter(difference));
  return difference.empty() ? "" : absl::StrJoin(difference, delimiter);
}

TEST(TestTextProto, TextProtoTest) {
  // Reads textproto.
  const auto rewrites =
      GetRewritesTextProto(absl::GetFlag(FLAGS_textproto_path)).value();

  // Reads token type.
  TokenType token_type;
  QCHECK(GetTokenType(absl::GetFlag(FLAGS_token_type), &token_type));

  // Reads FAR.
  StdRuleCascade cascade(token_type);
  QCHECK(cascade.Load(absl::GetFlag(FLAGS_far_path)));

  // Reads mode.
  const auto mode = absl::GetFlag(FLAGS_mode);

  for (const auto &rewrite : rewrites.rewrite()) {
    QCHECK(cascade.SetRules(rewrite.rule()));
    const auto rules = absl::StrJoin(rewrite.rule(), ", ");
    const auto &input = rewrite.input();
    const auto &expected = rewrite.output();
    if (expected.empty()) {
      std::string actual;
      std::string debug;
      EXPECT_FALSE(cascade.TopRewrite(input, &actual, &debug))
          << "Rule(s): " << rules << "\n"
          << "Expected rewrite failure for input: " << input << "\n"
          << "Actual output: " << actual << "\n"
          << "Debug output: " << debug << "\n"
          << "Rewrite mode: " << mode;
    } else if (mode == "exact") {
      std::vector<std::string> actual;
      std::vector<std::string> debug;
      EXPECT_TRUE(cascade.Rewrites(input, &actual, &debug))
          << "Rule(s): " << rules << "\n"
          << "Unexpected rewrites failure for input: " << input << "\n"
          << "Expected output: " << absl::StrJoin(expected, ", ") << "\n"
          << "Actual output: " << absl::StrJoin(actual, ", ") << "\n"
          << "Debug output: " << absl::StrJoin(debug, ", ");
      EXPECT_THAT(actual, UnorderedElementsAreArray(expected))
          << "Rule(s): " << rules << "\n"
          << "Failed for input: " << input << "\n"
          << "Expected output: " << absl::StrJoin(expected, ", ") << "\n"
          << "Actual output: " << absl::StrJoin(actual, ", ") << "\n"
          << "Debug output: " << absl::StrJoin(debug, ", ") << "\n"
          << "Extra elements: " << StringSetDifference(actual, expected) << "\n"
          << "Missing elements: " << StringSetDifference(expected, actual);
    } else if (mode == "one_top") {
      std::string actual;
      std::string debug;
      EXPECT_THAT(expected, SizeIs(1))
          << "Rule(s): " << rules << "\n"
          << "Expected one top rewrite for input: " << input << "\n"
          << "but more than one output is listed: "
          << absl::StrJoin(expected, ", ");
      EXPECT_TRUE(cascade.OneTopRewrite(input, &actual, &debug))
          << "Rule(s): " << rules << "\n"
          << "Expected one top rewrite for input: " << input << "\n"
          << "Actual output: " << actual << "\n"
          << "Debug output: " << debug;
      EXPECT_EQ(actual, expected[0])
          << "Rule(s): " << rules << "\n"
          << "Unexpected one top rewrite result input: " << input << "\n"
          << "Expected output: " << expected[0] << "\n"
          << "Actual output: " << actual << "\n"
          << "Debug output: " << debug;
    } else if (mode == "subset") {
      std::vector<std::string> actual;
      std::vector<std::string> debug;
      EXPECT_TRUE(cascade.Rewrites(input, &actual, &debug))
          << "Rule(s): " << rules << "\n"
          << "Unexpected rewrites failure for input: " << input << "\n"
          << "Expected output: " << absl::StrJoin(expected, ", ") << "\n"
          << "Actual output: " << absl::StrJoin(actual, ", ") << "\n"
          << "Debug output: " << absl::StrJoin(debug, ", ");
      EXPECT_THAT(actual, IsSupersetOf(expected))
          << "Rule(s): " << rules << "\n"
          << "Failed for input: " << input << "\n"
          << "Expected output: " << absl::StrJoin(expected, ", ") << "\n"
          << "Actual output: " << absl::StrJoin(actual, ", ") << "\n"
          << "Debug output: " << absl::StrJoin(debug, ", ") << "\n"
          << "Extra elements: " << StringSetDifference(actual, expected);
    } else if (mode == "top") {
      std::string actual;
      std::string debug;
      EXPECT_THAT(expected, SizeIs(1))
          << "Rule(s): " << rules << "\n"
          << "Expected top rewrite for input: " << input << "\n"
          << "but more than one output is listed: "
          << absl::StrJoin(expected, ", ");
      EXPECT_TRUE(cascade.TopRewrite(input, &actual, &debug))
          << "Rule(s): " << rules << "\n"
          << "Unexpected top rewrite failure for input: " << input << "\n"
          << "Expected output: " << expected[0] << "\n"
          << "Actual output: " << actual << "\n"
          << "Debug output: " << debug;
      EXPECT_EQ(actual, expected[0])
          << "Rule(s): " << rules << "\n"
          << "Unexpected top rewrite result input: " << input << "\n"
          << "Expected output: " << expected[0] << "\n"
          << "Actual output: " << actual << "\n"
          << "Debug output: " << debug;
    } else {
      FAIL() << "Unknown mode: " << mode;
    }
  }
}

}  // namespace
}  // namespace testing

// The `main` function here is necessary in OSS mode in order to use absl
// flags in OSS C++ tests because OSS gtest_main intercepts argc and argv
// but does not parse absl flags. For details, see google/googletest#3646.
GTEST_API_ int main(int argc, char **argv) {
 printf("Running main() from %s\n", __FILE__);
 testing::InitGoogleTest(&argc, argv);
 absl::ParseCommandLine(argc, argv);
 return RUN_ALL_TESTS();
}
