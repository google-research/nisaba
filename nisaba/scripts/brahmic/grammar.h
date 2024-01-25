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

// See the documentation on further information on this API.

#ifndef NISABA_SCRIPTS_BRAHMIC_GRAMMAR_H_
#define NISABA_SCRIPTS_BRAHMIC_GRAMMAR_H_

#include <memory>
#include <string>

#include "nisaba/interim/grm2/thrax/grm-manager.h"
#include "absl/status/status.h"
#include "absl/status/statusor.h"
#include "absl/strings/ascii.h"
#include "absl/strings/string_view.h"

namespace nisaba {
namespace brahmic {

// 'far_files' is the name of the 'memfile_embed_data' target in BUILD.
inline constexpr char kFarPath[] = "com_google_nisaba/nisaba/scripts/brahmic/";
inline constexpr char kFarExtn[] = ".far";

// Creates and loads visual_norm manager from memfile.
absl::StatusOr<::thrax::GrmManager *> LoadVisualNormManager();

// Creates and loads wellformed manager from memfile.
absl::StatusOr<::thrax::GrmManager *> LoadWellformedManager();

// Makes the full file path for a far file.
std::string MakeFarFilePath(absl::string_view far_path,
                            absl::string_view far_name);

// Generic wrapper around FST archive with Brahmic transducers.
class Grammar {
 public:
  Grammar(absl::string_view far_path, absl::string_view far_name,
          absl::string_view fst_name)
      : far_file_path_(MakeFarFilePath(far_path, far_name)),
        fst_name_(absl::AsciiStrToUpper(fst_name)),
        grm_mgr_(std::make_shared<::thrax::GrmManager>()) {}

  Grammar(absl::string_view far_name, absl::string_view fst_name)
      : Grammar(kFarPath, far_name, fst_name) {}

  // Takes a GrmManager that was previously created and loaded from a file. The
  // same manager can be shared with other Grammars.
  Grammar(absl::string_view far_name, absl::string_view fst_name,
          ::thrax::GrmManager *grm_manager)
      : far_file_path_(MakeFarFilePath(kFarPath, far_name)),
        fst_name_(absl::AsciiStrToUpper(fst_name)),
        grm_mgr_(grm_manager) {}

  // Loads the FAR file and verifies that the FST is found.
  absl::Status Load();

  // Verifies that the FST is found in the loaded grammar.
  // There is no need to call this method if calling Load().
  absl::Status VerifyLoad();

  absl::Status Rewrite(absl::string_view input, std::string *output) const;
  absl::Status Accept(absl::string_view input) const;

 private:
  Grammar() = delete;

  const std::string far_file_path_;
  std::string fst_name_;
  const std::shared_ptr<::thrax::GrmManager> grm_mgr_;
};

// Provides normalization of Brahmic text by composing multiple Grammar classes.
class Normalizer {
 public:
  Normalizer(absl::string_view far_path, absl::string_view fst_name)
      : visual_norm_(far_path, "visual_norm", fst_name),
        wellformed_(far_path, "wellformed", fst_name) {}

  explicit Normalizer(absl::string_view fst_name)
      : visual_norm_("visual_norm", fst_name),
        wellformed_("wellformed", fst_name) {}

  // Takes a visual_norm and a wellformed GrmManagers, that are assumed to be
  // already loaded.
  Normalizer(absl::string_view fst_name, ::thrax::GrmManager *visual_norm_manager,
             ::thrax::GrmManager *wellformed_manager)
      : visual_norm_("visual_norm", fst_name, visual_norm_manager),
        wellformed_("wellformed", fst_name, wellformed_manager) {}

  // Loads the FAR files and verifies that the FSTs are found.
  absl::Status Load();

  // Verifies that the FSTs are found in the loaded grammars.
  // There is no need to call this method if calling Load().
  absl::Status VerifyLoad();

  absl::Status Rewrite(absl::string_view input, std::string *output) const;
  absl::Status NormalizeOnly(absl::string_view input,
                             std::string *output) const;

  // Checks if a given fst_path (e.g. a given script) is available.
  static bool SupportsFst(absl::string_view fst_name);

 private:
  Normalizer() = delete;

  Grammar visual_norm_;
  Grammar wellformed_;
};

}  // namespace brahmic
}  // namespace nisaba

#endif  // NISABA_SCRIPTS_BRAHMIC_GRAMMAR_H_
