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

"""Build rule for easier textproto testing.

Sample usage:

    grm_textproto_test(
        name = "example_test",
        grammar = ":example",
        testdata = ":testdata/example.textproto",
    )
"""

def _GetFarParams(basename, grammar):
    """Determine full FAR target/path."""
    if grammar:
        grammar_target = grammar
    else:
        grammar_target = ":" + basename + "_sstable"
    if grammar_target.endswith("_sstable"):
        grammar_base = grammar_target[:-8]
    elif grammar_target.endswith("_android"):
        grammar_base = grammar_target[:-10]
    else:
        grammar_base = grammar_target
    if grammar_base.startswith("//" + native.package_name()):
        grammar_package_absolute, far_name_relative = grammar_base.split(":", 1)
        far_name_relative += ".far"
    elif grammar_base.startswith(":"):
        grammar_package_absolute = "//" + native.package_name()
        far_name_relative = grammar_base[1:] + ".far"
    else:
        fail("Unhandled grammar: %s" % grammar)
    far_target = grammar_package_absolute + ":" + far_name_relative
    far_path = far_target[2:].replace(":", "/")
    return far_path, far_target

def _GetTextprotoParams(basename, textproto):
    """Determine full textproto target/path."""
    if textproto:
        textproto_target = textproto
    else:
        textproto_target = "testdata/" + basename + ".textproto"
    if textproto_target.startswith("//"):
        textproto_path = textproto_target[2:].replace(":", "/")
    else:
        textproto_path = native.package_name() + "/" + textproto_target.replace(":", "/")
    return textproto_path, textproto_target

def grm_textproto_test(
        name,
        grammar = None,
        textproto = None,
        token_type = "byte",
        size = "small",
        mode = "exact",
        extra_deps = [],
        **kwds):
    """Generates a textproto test for the specified grammar.

    Args:
       name: The BUILD rule name. (Ordinarily this has the _test suffix.)
       grammar: The rule defining the compiled grammar. If not specified,
          {current_package}:{name} is used.
      textproto: The test textproto. If not specified,
          testdata:{name}.textproto is used.
      size: Blaze test size.
      mode: The rewrite mode (one of: "exact", "subset", "top", "one_top").
      token_type: Token type (one of: "byte", "utf8").
      extra_deps: Additional dependencies.
      **kwds: Attributes passed to the underlying cc_test rule.
    """
    basename = name[:-5] if name.endswith("_test") else name
    far_path, far_target = _GetFarParams(basename, grammar)
    textproto_path, textproto_target = _GetTextprotoParams(basename, textproto)
    args = [
        "--far_path=" + far_path,
        "--textproto_path=" + textproto_path,
        "--token_type=" + token_type,
    ]

    tags = [
    ] + kwds.pop("tags", [])  # We pop to avoid providing tags twice.

    args.append("--mode=" + mode)
    native.cc_test(
        name = name,
        size = size,
        args = args,
        linkstatic = 1,
        tags = tags,
        data = [
            far_target,
            textproto_target,
        ],
        deps = [
            "//nisaba/interim/testing:test_textproto_lib",
            "//nisaba/port:status-matchers",
            "@com_google_googletest//:gtest_main",
        ] + extra_deps,
        **kwds
    )
