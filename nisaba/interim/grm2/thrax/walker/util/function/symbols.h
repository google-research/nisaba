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

// Builds the symbol tables needed for byte and utf8.

#ifndef NISABA_INTERIM_GRM2_THRAX_WALKER_UTIL_FUNCTION_SYMBOLS_H_
#define NISABA_INTERIM_GRM2_THRAX_WALKER_UTIL_FUNCTION_SYMBOLS_H_

#include <cstdint>
#include <memory>
#include <string>

#include "fst/symbol-table.h"
#include "absl/synchronization/mutex.h"

namespace thrax {
namespace function {

const ::fst::SymbolTable* GetByteSymbolTable();
const ::fst::SymbolTable* GetUtf8SymbolTable();

void AddToByteSymbolTable(std::string symbol, int64_t label);
void AddToUtf8SymbolTable(std::string symbol, int64_t label);

static const char kByteSymbolTableName[] = "**Byte symbols";
static const char kUtf8SymbolTableName[] = "**UTF8 symbols";

class SymbolTableBuilder {
 public:
  SymbolTableBuilder();

  const ::fst::SymbolTable* GetByteSymbolTable();
  const ::fst::SymbolTable* GetUtf8SymbolTable();

  void AddToByteSymbolTable(std::string symbol, int64_t label);

  void AddToUtf8SymbolTable(std::string symbol, int64_t label);

 private:
  void GenerateByteSymbolTable();

  inline void GenerateUtf8SymbolTable();

  absl::Mutex map_mutex_;
  std::unique_ptr<::fst::SymbolTable> byte_symbols_;
  std::unique_ptr<::fst::SymbolTable> utf8_symbols_;
};

}  // namespace function
}  // namespace thrax

#endif  // NISABA_INTERIM_GRM2_THRAX_WALKER_UTIL_FUNCTION_SYMBOLS_H_
