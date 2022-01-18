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

// Testing utilities for working with absl::Status and absl::StatusOr.

#ifndef NISABA_PORT_STATUS_MATCHERS_H_
#define NISABA_PORT_STATUS_MATCHERS_H_

#include <ostream>
#include <string>
#include <type_traits>
#include <utility>

#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "gmock/gmock-matchers.h"
#include "gtest/gtest-matchers.h"
#include "gtest/gtest.h"
#include "nisaba/port/status_macros.h"

namespace testing {
namespace status {
namespace internal_status {

inline const absl::Status& GetStatus(const absl::Status& status) {
  return status;
}

template <typename T>
inline const absl::Status& GetStatus(const absl::StatusOr<T>& status) {
  return status.status();
}

////////////////////////////////////////////////////////////
// Implementation of IsOkAndHolds().

// Monomorphic implementation of matcher IsOkAndHolds(m).  StatusOrType can be
// either StatusOr<T> or a reference to it.
template <typename StatusOrType>
class IsOkAndHoldsMatcherImpl : public MatcherInterface<StatusOrType> {
 public:
  typedef typename std::remove_reference<StatusOrType>::type::element_type
      value_type;

  template <typename InnerMatcher>
  explicit IsOkAndHoldsMatcherImpl(InnerMatcher&& inner_matcher)
      : inner_matcher_(SafeMatcherCast<const value_type&>(
            std::forward<InnerMatcher>(inner_matcher))) {}

  void DescribeTo(std::ostream* os) const override {
    *os << "is OK and has a value that ";
    inner_matcher_.DescribeTo(os);
  }

  void DescribeNegationTo(std::ostream* os) const override {
    *os << "isn't OK or has a value that ";
    inner_matcher_.DescribeNegationTo(os);
  }

  bool MatchAndExplain(StatusOrType actual_value,
                       MatchResultListener* result_listener) const override {
    if (!actual_value.ok()) {
      *result_listener << "which has status " << actual_value.status();
      return false;
    }

    StringMatchResultListener inner_listener;
    const bool matches = inner_matcher_.MatchAndExplain(
        actual_value.ValueOrDie(), &inner_listener);
    const std::string inner_explanation = inner_listener.str();
    if (inner_explanation != "") {
      *result_listener << "which contains value "
                       << PrintToString(actual_value.ValueOrDie()) << ", "
                       << inner_explanation;
    }
    return matches;
  }

 private:
  const Matcher<const value_type&> inner_matcher_;
};

// Implements IsOkAndHolds(m) as a polymorphic matcher.
template <typename InnerMatcher>
class IsOkAndHoldsMatcher {
 public:
  explicit IsOkAndHoldsMatcher(InnerMatcher inner_matcher)
      : inner_matcher_(std::move(inner_matcher)) {}

  // Converts this polymorphic matcher to a monomorphic matcher of the
  // given type.  StatusOrType can be either StatusOr<T> or a
  // reference to StatusOr<T>.
  template <typename StatusOrType>
  operator Matcher<StatusOrType>() const {
    return MakeMatcher(
        new IsOkAndHoldsMatcherImpl<StatusOrType>(inner_matcher_));
  }

 private:
  const InnerMatcher inner_matcher_;
};

////////////////////////////////////////////////////////////
// Implementation of StatusIs().

// StatusIs() is a polymorphic matcher.  This class is the common
// implementation of it shared by all types T where StatusIs() can be
// used as a Matcher<T>.

MATCHER_P2(ErrorCodeEq, expected_error_code, error_space,
           (negation ? "isn't " : "is ") +
               error_space->String(expected_error_code)) {
  if (arg != expected_error_code) {
    *result_listener << error_space->String(arg);
    return false;
  }
  return true;
}

template <typename T>
Matcher<int> ToCodeMatcher(T m) {
  return Eq(m);
}
inline Matcher<int> ToCodeMatcher(const Matcher<int>& m) { return m; }

class StatusIsMatcherCommonImpl {
 public:
  StatusIsMatcherCommonImpl(Matcher<int> code_matcher,
                            Matcher<const std::string&> message_matcher)
      : code_matcher_(std::move(code_matcher)),
        message_matcher_(std::move(message_matcher)) {}

  void DescribeTo(std::ostream* os) const;

  void DescribeNegationTo(std::ostream* os) const;

  bool MatchAndExplain(const absl::Status& status,
                       MatchResultListener* result_listener) const;

 private:
  const Matcher<int> code_matcher_;
  const Matcher<const std::string&> message_matcher_;
};

// Monomorphic implementation of matcher StatusIs() for a given type
// T.  T can be Status, StatusOr<>, or a reference to either of them.
template <typename T>
class MonoStatusIsMatcherImpl : public MatcherInterface<T> {
 public:
  explicit MonoStatusIsMatcherImpl(StatusIsMatcherCommonImpl common_impl)
      : common_impl_(std::move(common_impl)) {}

  void DescribeTo(std::ostream* os) const override {
    common_impl_.DescribeTo(os);
  }

  void DescribeNegationTo(std::ostream* os) const override {
    common_impl_.DescribeNegationTo(os);
  }

  bool MatchAndExplain(T actual_value,
                       MatchResultListener* result_listener) const override {
    return common_impl_.MatchAndExplain(GetStatus(actual_value),
                                        result_listener);
  }

 private:
  StatusIsMatcherCommonImpl common_impl_;
};

// Implements StatusIs() as a polymorphic matcher.
class StatusIsMatcher {
 public:
  template <typename StatusCodeMatcher>
  StatusIsMatcher(StatusCodeMatcher&& code_matcher,
                  Matcher<const std::string&> message_matcher)
      : common_impl_(
            ToCodeMatcher(std::forward<StatusCodeMatcher>(code_matcher)),
            std::move(message_matcher)) {}

  // Converts this polymorphic matcher to a monomorphic matcher of the
  // given type.  T can be StatusOr<>, Status, or a reference to
  // either of them.
  template <typename T>
  operator Matcher<T>() const {
    return MakeMatcher(new MonoStatusIsMatcherImpl<T>(common_impl_));
  }

 private:
  const StatusIsMatcherCommonImpl common_impl_;
};

// Monomorphic implementation of matcher IsOk() for a given type T.
// T can be Status, StatusOr<>, or a reference to either of them.
template <typename T>
class MonoIsOkMatcherImpl : public MatcherInterface<T> {
 public:
  void DescribeTo(std::ostream* os) const override { *os << "is OK"; }
  void DescribeNegationTo(std::ostream* os) const override {
    *os << "is not OK";
  }
  bool MatchAndExplain(T actual_value, MatchResultListener*) const override {
    return GetStatus(actual_value).ok();
  }
};

// Implements IsOk() as a polymorphic matcher.
class IsOkMatcher {
 public:
  template <typename T>
  operator Matcher<T>() const {  // NOLINT
    return MakeMatcher(new MonoIsOkMatcherImpl<T>());
  }
};
}  // namespace internal_status

#define ASSERT_OK_AND_ASSIGN_IMPL(statusor, lhs, rexpr) \
  auto statusor = (rexpr);                              \
  ASSERT_OK(statusor);                                  \
  lhs = std::move(statusor).ValueOrDie();

#define ASSERT_OK_AND_ASSIGN(lhs, rexpr) \
  ASSERT_OK_AND_ASSIGN_IMPL(             \
      STATUS_MACROS_CONCAT_NAME(_status_or_, __COUNTER__), lhs, rexpr);

// Macros for testing the results of functions that return absl::Status or
// absl::StatusOr<T> (for any type T).
#define EXPECT_OK(expression) EXPECT_THAT(expression, ::testing::status::IsOk())
#define ASSERT_OK(expression) ASSERT_THAT(expression, ::testing::status::IsOk())

// Returns a gMock matcher that matches a StatusOr<> whose status is
// OK and whose value matches the inner matcher.
template <typename InnerMatcher>
internal_status::IsOkAndHoldsMatcher<typename std::decay<InnerMatcher>::type>
IsOkAndHolds(InnerMatcher&& inner_matcher) {
  return internal_status::IsOkAndHoldsMatcher<
      typename std::decay<InnerMatcher>::type>(
      std::forward<InnerMatcher>(inner_matcher));
}

// Returns a gMock matcher that matches a Status or StatusOr<> whose
// status code matches code_matcher, and whose error message matches
// message_matcher.
template <typename StatusCodeMatcher>
internal_status::StatusIsMatcher StatusIs(
    StatusCodeMatcher&& code_matcher,
    Matcher<const std::string&> message_matcher) {
  return internal_status::StatusIsMatcher(
      std::forward<StatusCodeMatcher>(code_matcher),
      std::move(message_matcher));
}

// Returns a gMock matcher that matches a Status or StatusOr<> whose status code
// matches code_matcher.
template <typename StatusCodeMatcher>
internal_status::StatusIsMatcher StatusIs(StatusCodeMatcher&& code_matcher) {
  return StatusIs(std::forward<StatusCodeMatcher>(code_matcher), _);
}

// Returns a gMock matcher that matches a Status or StatusOr<> which is OK.
inline internal_status::IsOkMatcher IsOk() {
  return internal_status::IsOkMatcher();
}

}  // namespace status
}  // namespace testing

#endif  // NISABA_PORT_STATUS_MATCHERS_H_
