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


#include "nisaba/port/thread_pool.h"

#include <chrono>  // NOLINT(build/c++11)
#include <memory>
#include <thread>  // NOLINT(build/c++11)

#include "absl/base/thread_annotations.h"
#include "absl/synchronization/mutex.h"
#include "gtest/gtest.h"

namespace nisaba {
namespace {

constexpr int kNumThreads = 100;
constexpr int kDurationMSec = 50;
constexpr int kNumIterations = 1000;

class SecureInteger {
 public:
  explicit SecureInteger(int initial) : value_(initial) {}
  SecureInteger(const SecureInteger &other) = delete;
  SecureInteger& operator=(const SecureInteger &other) = delete;

  void Increment() {
    absl::MutexLock lock(&mutex_);
    ++value_;
    changed_.SignalAll();
  }

  int value() {
    absl::MutexLock lock(&mutex_);
    return value_;
  }

 private:
  absl::Mutex mutex_;
  absl::CondVar changed_;
  int value_ ABSL_GUARDED_BY(mutex_);
};

// Increments a given integer.
void IncrementIntegerWorker(SecureInteger *value) {
  std::this_thread::sleep_for(std::chrono::milliseconds(kDurationMSec));
  value->Increment();
}

TEST(ThreadPoolTest, CheckIncrement) {
  std::unique_ptr<ThreadPool> thread_pool(new ThreadPool(kNumThreads));
  thread_pool->StartWorkers();
  SecureInteger count(0);
  for (int i = 0; i < kNumIterations; ++i) {
    thread_pool->Schedule([&count]() { IncrementIntegerWorker(&count); });
  }
  thread_pool.reset(nullptr);
  EXPECT_EQ(count.value(), kNumIterations);
}

TEST(ThreadPoolTest, CheckFIFO) {
  int count = 0;
  ThreadPool pool(1);
  pool.StartWorkers();
  for (int i = 0; i < kNumIterations; ++i) {
    pool.Schedule([&count, i]() {
      EXPECT_EQ(count, i);
      count++;
    });
  }
}

}  // namespace
}  // namespace nisaba
