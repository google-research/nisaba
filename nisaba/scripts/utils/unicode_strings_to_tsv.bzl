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

def _convert_script_data_component(script_data_name):
    """Converts script data proto into TSV format.

    Args:
      script_data_name: The name of the script data (e.g., `consonant`).
    """
    input_proto_file = "%s.textproto" % script_data_name

    converter_tool = "//nisaba/scripts/utils:unicode_strings_to_tsv"
    converter_rule_name = "generate_" + script_data_name
    native.genrule(
        name = converter_rule_name,
        outs = ["%s.tsv" % script_data_name],
        srcs = [input_proto_file],
        exec_tools = [converter_tool],
        visibility = ["//visibility:public"],
        cmd = "$(location %s) --input_text_proto $(location %s) --output_tsv $@" % (
            converter_tool,
            ":" + input_proto_file,
        ),
    )
    build_test(
        name = converter_rule_name + "_smoke_test",
        targets = [":" + converter_rule_name],
    )

def setup_script_data(name, script_data_components):
    """Converts a list of script components to the corresponding TSV files.

    Args:
       name: Name of this macro.
       script_data_components: A list of script data component names.
    """
    for script_data in script_data_components:
        _convert_script_data_component(script_data)
