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

// The GrmManager holds a set of FSTs in memory and performs rewrites via
// composition as well as various I/O functions. GrmManager is
// thread-compatible.

#ifndef NISABA_INTERIM_GRM2_THRAX_GRM_MANAGER_H_
#define NISABA_INTERIM_GRM2_THRAX_GRM_MANAGER_H_

#include <memory>
#include <string>

#include "fst/extensions/far/far.h"
#include "fst/symbol-table.h"
#include "absl/flags/declare.h"
#include "absl/flags/flag.h"
#include "absl/memory/memory.h"
#include "nisaba/interim/grm2/thrax/abstract-grm-manager.h"

ABSL_DECLARE_FLAG(std::string, outdir);

namespace thrax {

template <typename Arc>
class GrmManagerSpec : public AbstractGrmManager<Arc> {
  using Base = AbstractGrmManager<Arc>;
 public:
  using Base::GetFst;
  using typename Base::FstMap;

  GrmManagerSpec() : Base() {}

  ~GrmManagerSpec() override {}

  // Loads FSTs from a FAR file, returning true on success.
  bool LoadArchive(const std::string &filename);

  // Returns the generated symbol table.
  std::unique_ptr<::fst::SymbolTable> GetGeneratedSymbolTable() const;

 private:
  GrmManagerSpec(const GrmManagerSpec &) = delete;
  GrmManagerSpec &operator=(const GrmManagerSpec &) = delete;
};

template <typename Arc>
bool GrmManagerSpec<Arc>::LoadArchive(const std::string &filename) {
  std::unique_ptr<::fst::FarReader<Arc>> reader(
     ::fst::STTableFarReader<Arc>::Open(filename));
  if (!reader) {
    LOG(ERROR) << "Unable to open FAR: " << filename;
    return false;
  }
  return Base::LoadArchive(reader.get(), filename);
}

template <typename Arc>
std::unique_ptr<::fst::SymbolTable>
GrmManagerSpec<Arc>::GetGeneratedSymbolTable() const {
  const auto *symbolfst = GetFst("*StringFstSymbolTable");
  return symbolfst ? absl::WrapUnique(symbolfst->InputSymbols()->Copy())
                   : nullptr;
}

// A lot of code outside this build uses GrmManager with the old meaning of
// GrmManagerSpec<::fst::StdArc>, forward-declaring it as a class. To
// obviate the need to change all that outside code, we provide this derived
// class:

class GrmManager : public GrmManagerSpec<::fst::StdArc> {};

}  // namespace thrax

#endif  // NISABA_INTERIM_GRM2_THRAX_GRM_MANAGER_H_
