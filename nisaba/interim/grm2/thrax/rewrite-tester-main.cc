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

// Stand-alone binary to load up a FAR and rewrite some strings.

#include <memory>

#include "absl/flags/parse.h"
#include "nisaba/interim/grm2/thrax/rewrite-tester.h"

int main(int argc, char **argv) {
  absl::ParseCommandLine(argc, argv);
  auto utils = std::make_unique<::thrax::RewriteTester>();
  utils->Initialize();
  utils->Run();

  return 0;
}
