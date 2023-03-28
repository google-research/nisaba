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

"""Rules for converting Unicode string protos to Pynini TSV format."""

load("@bazel_skylib//rules:build_test.bzl", "build_test")

DEFAULT_VISIBILITY = "//nisaba/scripts:__subpackages__"

# Empty string represents local directory as in ":consonant.textptoto"
_LOCAL_DIR = ""

def component_tsv(name, text_protos):
    """Converts script component text protos into TSV format.

    Args:
      name: The name of the script data component (e.g., `consonant`).
      text_protos: Text proto targets that make up this component.
    """

    proto_files = " ".join([("$(location %s)" % tgt) for tgt in text_protos])
    combined_text_proto = "combined_%s.textproto" % name
    native.genrule(
        name = "combine_%s_text_protos" % name,
        outs = [combined_text_proto],
        srcs = text_protos,
        visibility = [DEFAULT_VISIBILITY],
        cmd = "cat %s > $@" % proto_files,
    )

    converter_tool = "//nisaba/scripts/utils:unicode_strings_to_tsv"
    converter_rule_name = "generate_" + name
    native.genrule(
        name = converter_rule_name,
        outs = ["%s.tsv" % name],
        srcs = [combined_text_proto],
        exec_tools = [converter_tool],
        visibility = [DEFAULT_VISIBILITY],
        cmd = "$(location %s) --input_text_proto $(location %s) --output_tsv $@" % (
            converter_tool,
            combined_text_proto,
        ),
    )
    build_test(
        name = converter_rule_name + "_smoke_test",
        targets = [":" + converter_rule_name],
    )

def empty_components_tsv(names, name = "empty"):
    """Creates empty script data component files in TSV format.

    Args:
      names: The names of the script data components (e.g., `accept`).
      name: Name of the rule.
    """
    for component_name in names:
        native.genrule(
            name = "create_%s_%s_tsv" % (name, component_name),
            outs = ["%s.tsv" % component_name],
            visibility = [DEFAULT_VISIBILITY],
            # May not work in Windows. To be fixed when Windows support is added.
            cmd = "touch $@",
        )

# Generates component TSV files for a list of given names.
#
# The `uname_prefix_from` provides the path for `uname_prefix.textproto`.
# The `text_protos_from` provides the default paths for the component.
# The `name` parameter is unused.
def _components_tsv_for(name, names, uname_prefix_from, text_protos_from):
    for name in names:
        component_tsv(
            name,
            ["%s:uname_prefix.textproto" % uname_prefix_from] +
            [
                "%s:%s.textproto" % (path, name)
                for path in text_protos_from
            ],
        )

# List of components which are defined by local files in the directory only.
# By default, they use local `uname_prefix.textproto` to get the prefix
# information.
def components_tsv_local(
        names,
        name = "components_local",
        uname_prefix_from = _LOCAL_DIR,
        more_text_protos_from = []):
    _components_tsv_for(
        name,
        names,
        uname_prefix_from,
        text_protos_from = [_LOCAL_DIR] + more_text_protos_from,
    )

# List of components which are defined by local files in the directory and
# the corresponding ones in common directory (e.g.: `brahmic/data/common`).
# They use local `uname_prefix.textproto` to get the prefix information.
def components_tsv_local_with_common(
        names,
        name = "components_local_with_common",
        common_dir = _LOCAL_DIR,
        uname_prefix_from = _LOCAL_DIR,
        more_text_protos_from = []):
    _components_tsv_for(
        name,
        names,
        uname_prefix_from,
        text_protos_from = [_LOCAL_DIR, common_dir] + more_text_protos_from,
    )

# List of components which do not have any local definitions and are
# exclusively defined by the corresponding ones in common directory
# (e.g.: `brahmic/data/common`). By default, they use local
# `uname_prefix.textproto` to get the prefix information.
def components_tsv_from_common(
        names,
        name = "components_from_common",
        common_dir = _LOCAL_DIR,
        uname_prefix_from = _LOCAL_DIR,
        more_text_protos_from = []):
    _components_tsv_for(
        name,
        names,
        uname_prefix_from,
        text_protos_from = [common_dir] + more_text_protos_from,
    )

# Returns a function with the `args` already provided to the given function `fn`.
def add_args_to_fn(fn, args):
    return lambda **kwargs: fn(**dict(args, **kwargs))
