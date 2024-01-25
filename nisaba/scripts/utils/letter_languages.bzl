# Copyright 2024 Nisaba Authors.
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

"""Starlark utilities for letter registry."""

load("@pip_deps//:requirements.bzl", "requirement")

def setup_letter_languages(name):
    """Introduces several rules that deal with script letter language registry.

    Args:
      name: Name of this rule. Ideally should correspond to the name of the
        script, e.g. `Ethi` (for Ge`ez).
    """
    text_proto_name = "letter_languages.textproto"

    # Copy the test file from a common location to the current directory.
    test_src_file = "letter_languages_integrity_test.py"
    native.genrule(
        name = "letter_languages_generate_test",
        srcs = ["//nisaba/scripts/utils:%s" % test_src_file],
        outs = [test_src_file],
        cmd = "cp $(SRCS) $@",
    )

    # Introduce the integrity test target.
    native.py_test(
        name = "letter_languages_integrity_test",
        srcs = [":%s" % test_src_file],
        python_version = "PY3",
        srcs_version = "PY3",
        args = ["--input_text_proto=$(location :%s)" % text_proto_name],
        data = [":%s" % text_proto_name],
        deps = [
            "@io_abseil_py//absl/testing:absltest",
            "//nisaba/scripts/utils:letter_languages",
            "@io_abseil_py//absl/flags",
            requirement("pycountry"),
        ],
    )
