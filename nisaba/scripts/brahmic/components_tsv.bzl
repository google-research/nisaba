# Copyright 2022 Nisaba Authors.
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
    "DEFAULT_VISIBILITY",
    "component_tsv",
)

_COMMON_DIR = "//nisaba/scripts/brahmic/data/common"

# Empty string represents local directory as in ":consonant.textptoto"
_LOCAL_DIR = ""

# Wrapper over `component_tsv` with defaults meaningful for Brahmic scripts.
#
# The `uname_prefix_from` provides the path for `uname_prefix.textproto`.
# Default is the local directory path.
#
# The `text_protos_from` provides the default paths for the component.
# Default is both local and common directory paths.
#
# The `more_text_protos_from` provides the additional text proto paths for the
# component, along with the `text_protos_from`.
#
# Both of these path lists assume the presence of `<name>.textproto` in that
# path.
def component_tsv_with_defaults(
        name,
        uname_prefix_from = _LOCAL_DIR,
        text_protos_from = [_LOCAL_DIR, _COMMON_DIR],
        more_text_protos_from = []):
    component_tsv(
        name,
        ["%s:uname_prefix.textproto" % uname_prefix_from] +
        [
            "%s:%s.textproto" % (path, name)
            for path in text_protos_from + more_text_protos_from
        ],
    )

# The list of components which are defined by local files in the directory
# only. By default, they use local `uname_prefix.textproto` to get the prefix
# information.
def components_tsv_local(
        names,
        name = "components_local",
        uname_prefix_from = _LOCAL_DIR):
    for name in names:
        component_tsv_with_defaults(
            name,
            text_protos_from = [_LOCAL_DIR],
            uname_prefix_from = uname_prefix_from,
        )

# The list of components which are defined by local files in the directory and
# the corresponding ones in the `brahmic/data/common` as well.
# They use local `uname_prefix.textproto` to get the prefix information.
def components_tsv_local_with_common(
        names,
        name = "components_local_with_common"):
    for name in names:
        component_tsv_with_defaults(name)

# The list of components which do not have any local definitions and are
# exclusively defined by the corresponding ones in the `brahmic/data/common`.
# They use local `uname_prefix.textproto` to get the prefix information.
def components_tsv_from_common(names, name = "components_from_common"):
    for name in names:
        component_tsv_with_defaults(name, text_protos_from = [_COMMON_DIR])

def empty_components_tsv(names, name = "empties"):
    """Creates empty script data component files in TSV format.

    Args:
      names: The names of the script data components (e.g., `accept`).
      name: Name of the rule.
    """
    for component_name in names:
        native.genrule(
            name = "create_%s_tsv" % component_name,
            outs = ["%s.tsv" % component_name],
            visibility = [DEFAULT_VISIBILITY],
            # May not work in Windows. To be fixed when Windows support is added.
            cmd = "touch $@",
        )
