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

DEFAULT_VISIBILITY = "//nisaba/scripts:__subpackages__"

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
