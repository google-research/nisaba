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

#ifndef NISABA_PORT_TIMER_H_
#define NISABA_PORT_TIMER_H_

#include "absl/time/clock.h"
#include "absl/time/time.h"

namespace nisaba {

// A helper class for measuring elapsed times.
class Timer {
 public:
  Timer() : start_time_(absl::Now()) {}

  double ElapsedMillis() const {
    return absl::FDivDuration(absl::Now() - start_time_,
                              absl::Milliseconds(1));
  }

 private:
  const absl::Time start_time_;
};

}  // namespace nisaba

#endif  // NISABA_PORT_TIMER_H_
