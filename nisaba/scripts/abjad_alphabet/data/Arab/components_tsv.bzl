# Copyright 2023 Nisaba Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rules to convert Unicode string protos to Pynini TSV format."""

load(
    "//nisaba/scripts/utils:unicode_strings_to_tsv.bzl",
    "add_args_to_fn",
    _components_tsv_from_common = "components_tsv_from_common",
    _components_tsv_local = "components_tsv_local",
    _components_tsv_local_with_common = "components_tsv_local_with_common",
    _empty_components_tsv = "empty_components_tsv",
)

_COMMON_DIR = "//nisaba/scripts/abjad_alphabet/data/Arab"

_COMMON_ARGS = {
    "common_dir": _COMMON_DIR,
    "uname_prefix_from": _COMMON_DIR,
}

empty_components_tsv = _empty_components_tsv
components_tsv_local = add_args_to_fn(_components_tsv_local, {"uname_prefix_from": _COMMON_DIR})
components_tsv_local_with_common = add_args_to_fn(_components_tsv_local_with_common, _COMMON_ARGS)
components_tsv_from_common = add_args_to_fn(_components_tsv_from_common, _COMMON_ARGS)
