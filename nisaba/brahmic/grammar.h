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

// See the documentation on further information on this API.

#ifndef NISABA_BRAHMIC_GRAMMAR_H_
#define NISABA_BRAHMIC_GRAMMAR_H_

#include <memory>
#include <string>

#include "nisaba/utils/util.h"
#include "thrax/grm-manager.h"
#include "absl/strings/ascii.h"
#include "absl/memory/memory.h"

namespace nisaba {
namespace brahmic {

// 'far_files' is the name of the 'memfile_embed_data' target in BUILD.
constexpr char kFarPath[] = "com_google_nisaba/nisaba/brahmic/";
constexpr char kFarExtn[] = ".far";

// Generic wrapper around FST archive with Brahmic transducers.
class Grammar {
 public:
  Grammar(const std::string& far_path, const std::string& far_name,
          const std::string& fst_name)
      : far_file_path_(utils::JoinPath(
            far_path, absl::AsciiStrToLower(far_name) + kFarExtn)),
        fst_name_(absl::AsciiStrToUpper(fst_name)),
        grm_mgr_(absl::make_unique<thrax::GrmManager>()) {}

  Grammar(const std::string& far_name, const std::string& fst_name)
      : Grammar(kFarPath, far_name, fst_name){}

  bool Load();
  bool Rewrite(const std::string& input,
                     std::string *output) const;
  bool Accept(const std::string& input) const;

 private:
  const std::string far_file_path_;
  std::string fst_name_;
  const std::unique_ptr<thrax::GrmManager> grm_mgr_;
};

// Provides normalization of Brahmic text by composing multiple Grammar classes.
class Normalizer {
 public:
  explicit Normalizer(const std::string& far_path, const std::string& fst_name)
      : visual_norm_(far_path, "visual_norm", fst_name),
        wellformed_(far_path, "wellformed", fst_name){}

  explicit Normalizer(const std::string& fst_name):
                      visual_norm_("visual_norm", fst_name),
                      wellformed_("wellformed", fst_name){}

  bool Load();
  bool Rewrite(const std::string& input,
               std::string *output) const;
  bool NormalizeOnly(const std::string& input, std::string* output) const;

 private:
  Grammar visual_norm_;
  Grammar wellformed_;
};

}  // namespace brahmic
}  // namespace nisaba

#endif  // NISABA_BRAHMIC_GRAMMAR_H_
