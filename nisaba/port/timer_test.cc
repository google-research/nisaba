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

#include "nisaba/port/timer.h"

#include "gmock/gmock.h"
#include "nisaba/port/status-matchers.h"
#include "gtest/gtest.h"
#include "absl/time/clock.h"

namespace nisaba {
namespace {

// Timeout in milliseconds.
constexpr int kTimeoutMsec = 100;

TEST(TimerTest, BasicCheck) {
  Timer timer;
  absl::SleepFor(absl::Milliseconds(kTimeoutMsec));
  EXPECT_LT(0.0, timer.ElapsedMillis());
}

}  // namespace
}  // namespace nisaba
