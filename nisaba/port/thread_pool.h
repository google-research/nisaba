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

// Portable thread pool implementation.
//
// This is taken from the absl synchronization internals and may not be the most
// optimal implementation. The reference implementation can be found here:
//   https://github.com/abseil/abseil-cpp/blob/master/absl/synchronization/internal/thread_pool.h

#ifndef NISABA_PORT_THREAD_POOL_H_
#define NISABA_PORT_THREAD_POOL_H_

#include <cassert>
#include <cstddef>
#include <functional>
#include <queue>
#include <thread>  // NOLINT(build/c++11)
#include <vector>

#include "absl/base/thread_annotations.h"
#include "absl/synchronization/mutex.h"

namespace nisaba {

// A simple thread pool implementation for tests.
class ThreadPool {
 public:
  explicit ThreadPool(int num_threads) : num_threads_(num_threads) {
    threads_.reserve(num_threads);
  }

  ThreadPool(const ThreadPool &) = delete;
  ThreadPool &operator=(const ThreadPool &) = delete;

  void StartWorkers() {
    for (int i = 0; i < num_threads_; ++i) {
      threads_.push_back(std::thread(&ThreadPool::WorkLoop, this));
    }
  }

  ~ThreadPool() {
    {
      absl::MutexLock l(&mu_);
      for (size_t i = 0; i < threads_.size(); i++) {
        queue_.push(nullptr);  // Shutdown signal.
      }
    }
    for (auto &t : threads_) {
      t.join();
    }
  }

  // Schedules a function to be run on a ThreadPool thread immediately.
  void Schedule(std::function<void()> func) {
    assert(func != nullptr);
    absl::MutexLock l(&mu_);
    queue_.push(std::move(func));
  }

 private:
  bool WorkAvailable() const ABSL_EXCLUSIVE_LOCKS_REQUIRED(mu_) {
    return !queue_.empty();
  }

  void WorkLoop() {
    while (true) {
      std::function<void()> func;
      {
        absl::MutexLock l(&mu_);
        mu_.Await(absl::Condition(this, &ThreadPool::WorkAvailable));
        func = std::move(queue_.front());
        queue_.pop();
      }
      if (func == nullptr) {  // Shutdown signal.
        break;
      }
      func();
    }
  }

  const int num_threads_;
  absl::Mutex mu_;
  std::queue<std::function<void()>> queue_ ABSL_GUARDED_BY(mu_);
  std::vector<std::thread> threads_;
};

}  // namespace nisaba

#endif  // NISABA_PORT_THREAD_POOL_H_
