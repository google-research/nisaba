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

#ifndef NISABA_PORT_STATUS_MACROS_H_
#define NISABA_PORT_STATUS_MACROS_H_

#include <utility>

#include "absl/base/optimization.h"
#include "absl/status/status.h"
#include "google/protobuf/stubs/logging.h"

namespace mozolm {

#define STATUS_MACROS_CONCAT_NAME(x, y) \
  STATUS_MACROS_CONCAT_IMPL(x, y)
#define STATUS_MACROS_CONCAT_IMPL(x, y) x##y

#define ASSIGN_OR_RETURN(lhs, rexpr)                                 \
  ASSIGN_OR_RETURN_IMPL(                                             \
      STATUS_MACROS_CONCAT_NAME(_status_or_value, __COUNTER__), lhs, \
      rexpr)

#define ASSIGN_OR_RETURN_IMPL(statusor, lhs, rexpr) \
  do {                                              \
    const auto statusor = (rexpr);                  \
    if (ABSL_PREDICT_FALSE(!statusor.ok())) {       \
      return statusor.status();                     \
    }                                               \
    lhs = std::move(statusor.value());              \
  } while (false)

#define RETURN_IF_ERROR_IMPL(__local_status, __status) \
  do {                                                 \
    const auto __local_status = __status;              \
    if (ABSL_PREDICT_FALSE(!__local_status.ok())) {    \
      return __local_status;                           \
    }                                                  \
  } while (false)

#define RETURN_IF_ERROR(status) \
  RETURN_IF_ERROR_IMPL(         \
      STATUS_MACROS_CONCAT_NAME(_local_status, __COUNTER__), status)

#define RETURN_IF_NULL(ptr)                                              \
  do {                                                                   \
    if (!(ptr)) {                                                        \
      return absl::InvalidArgumentError(absl::StrCat(#ptr, " is null")); \
    }                                                                    \
  } while (false)

// We need dependency on logging to import the core GOOGLE_CHECK macros.
#if !defined(GOOGLE_CHECK_OK)
#define GOOGLE_CHECK_OK(value) GOOGLE_CHECK((value).ok())
#endif  // GOOGLE_CHECK_OK

}  // namespace mozolm

#endif  // NISABA_PORT_STATUS_MACROS_H_
