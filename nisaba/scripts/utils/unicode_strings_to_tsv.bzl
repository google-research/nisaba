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

"""Rules for converting Unicode string protos to Pynini TSV format."""

load("@bazel_skylib//rules:build_test.bzl", "build_test")

def component_tsv(name, text_protos):
    """Converts script component text protos into TSV format.

    Args:
      name: The name of the script data component (e.g., `consonant`).
      text_protos: Text proto targets make up this component.
    """

    proto_files = " ".join([("$(location %s)" % tgt) for tgt in text_protos])
    combined_text_proto = "combined_%s.textproto" % name
    native.genrule(
        name = "combine_%s_text_protos" % name,
        outs = [combined_text_proto],
        srcs = text_protos,
        visibility = ["//nisaba/scripts:__subpackages__"],
        cmd = "cat %s > $@" % proto_files,
    )

    converter_tool = "//nisaba/scripts/utils:unicode_strings_to_tsv"
    converter_rule_name = "generate_" + name
    native.genrule(
        name = converter_rule_name,
        outs = ["%s.tsv" % name],
        srcs = [combined_text_proto],
        exec_tools = [converter_tool],
        visibility = ["//nisaba/scripts:__subpackages__"],
        cmd = "$(location %s) --input_text_proto $(location %s) --output_tsv $@" % (
            converter_tool,
            combined_text_proto,
        ),
    )
    build_test(
        name = converter_rule_name + "_smoke_test",
        targets = [":" + converter_rule_name],
    )

def empty_components_tsv(name, empty_component_names):
    """Creates empty script data component files in TSV format.

    Args:
      name: Name of the rule.
      empty_component_names: The names of the script data components (e.g.,
        `accept`).
    """
    for component_name in empty_component_names:
        native.genrule(
            name = "create_%s_tsv" % component_name,
            outs = ["%s.tsv" % component_name],
            visibility = ["//nisaba/scripts:__subpackages__"],
            # May not work in Windows. To be fixed when Windows support is added.
            cmd = "touch $@",
        )

def setup_script_data(
        name,
        script_data_components = (),
        empty_components = (),
        more_component_paths = {},
        export_script_data = True):
    """Converts a list of script components to the corresponding TSV files.

    Args:
      name: Name of this macro.
      script_data_components: A list of script data component names.
      empty_components: List of components without any items.
      more_component_paths: Map of component parts available at a path.
      export_script_data: Whether the script data should be exported. If
        the data is auto-generated set this argument to `False`.
    """

    # Export script data only if it's not auto-generated.
    if export_script_data:
        native.exports_files(
            [
                "%s.textproto" % component
                for component in script_data_components
            ],
        )

    # Creating the map from components to all their text proto targets.
    path_to_components = dict(more_component_paths)
    path_to_components[""] = script_data_components
    component_to_proto_tgts = {}
    for path, components in path_to_components.items():
        for component in components:
            proto_tgt = "%s:%s.textproto" % (path, component)
            component_to_proto_tgts.setdefault(component, []).append(proto_tgt)

    # Adding the build rules for each component.
    for component, proto_tgts in component_to_proto_tgts.items():
        component_tsv(component, depset(proto_tgts).to_list())

    # Add targets generating empty components.
    empty_components_tsv("%s_empties" % name, empty_components)
