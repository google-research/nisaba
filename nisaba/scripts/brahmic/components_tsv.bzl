# Copyright 2021 Nisaba Authors.
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

"""Rules to convert Unicode string protos for Brahmic to Pynini TSV format."""

load(
    "//nisaba/scripts/utils:unicode_strings_to_tsv.bzl",
    "component_tsv",
)

_COMMON_DIR = "//nisaba/scripts/brahmic/data/common"

# Wrapper over `component_tsv` with defaults meaningful for Brahmic scripts.
# The `text_protos_from` provides the list of default path for the component.
# Its default is local directory path which is the empty string.
# The `more_text_protos_from` provides the additional paths for the component.
# Both of these path lists assume the presence of `<name>.textproto` in that
# path. `uname_prefix.textproto` is always included from the local directory.
def _component_tsv_with_defaults(
        name,
        text_protos_from = [""],
        more_text_protos_from = []):
    component_tsv(name, [":uname_prefix.textproto"] +
                        [
                            "%s:%s.textproto" % (path, name)
                            for path in text_protos_from + more_text_protos_from
                        ])

# The list of components which are defined by local files in the directory
# only. They use `uname_prefix.textproto` to get the prefix information.
def components_tsv_local(name = "components_local", names = []):
    for name in names:
        _component_tsv_with_defaults(name)

# The list of components which are defined by local files in the directory and
# the corresponding ones in the `brahmic/data/common` as well.
# They use `uname_prefix.textproto` to get the prefix information.
def components_tsv_local_with_common(
        name = "components_local_with_common",
        names = []):
    for name in names:
        _component_tsv_with_defaults(name, more_text_protos_from = [_COMMON_DIR])

# The list of components which do not have any local definitions and are
# exclusively defined by the corresponding ones in the `brahmic/data/common`.
# They use `uname_prefix.textproto` in the local directory to get the prefix
# information.
def components_tsv_from_common(name = "components_from_common", names = []):
    for name in names:
        _component_tsv_with_defaults(name, text_protos_from = [_COMMON_DIR])
