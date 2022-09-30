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

"""Starlark utilities for dealing with Pynini targets."""

load("@org_opengrm_thrax//:src/bazel/regression_test_build_defs.bzl", "grm_regression_test")
load(
    "@org_opengrm_pynini//pynini/export:grm_py_build_defs.bzl",
    "compile_grm_py",
    "compile_multi_grm_py",
)

# FST type for compile_grm_py and compile_multi_grm_py; depend on
# //nisaba/scripts/utils:fst_types to read such FSTs.
_FST_TYPE = "const"

def nisaba_compile_grm_py(
        name,
        deps = None,
        data = None,
        out = None,
        **kwds):
    """Provides a target to convert a Pynini file into a (portable) FAR file.

    Turns a Pynini file into a FAR file with the specified FAR and FST types.

    Args:
      name: The BUILD rule name and the file prefix for the generated output.
      deps: A list of other grammar targets that we'll need for this grammar.
      data: Extra data dependencies used in the Pynini file.
      out: Far file to be generated. If not present, then we'll use the `name`
           followed by ".far".
      **kwds: Attributes common to all BUILD rules, e.g., testonly, visibility.
    """
    compile_grm_py(
        name = name,
        fst_type = _FST_TYPE,
        deps = deps + [
        ],
        data = data,
        out = out,
        **kwds
    )

def nisaba_compile_multi_grm_py(
        name,
        outs,
        deps = None,
        data = None,
        **kwds):
    """Provides a target to convert a Pynini file into multiple (portable) FAR files.

    Turns a Pynini file into a FAR file with the specified FAR and FST types.

    Args:
      name: The BUILD rule name and the file prefix for the generated output.
      outs: A dictionary mapping designators to files, where designator
            is the designating name used in the Pynini file to refer to the
            corresponding file. The designated files must have extension ".far".
      deps: A list of other compile_grm rules that we'll need for this grammar.
      data: Extra data dependencies used in the Pynini file.
      **kwds: Attributes common to all BUILD rules, e.g., testonly, visibility.
    """
    compile_multi_grm_py(
        name = name,
        fst_type = _FST_TYPE,
        outs = outs,
        data = data,
        deps = deps + [
        ],
        **kwds
    )

def nisaba_grm_regression_test(
        name,
        grammar = None,
        test_file = None,
        size = "small",
        test_file_target = None,
        test_file_path = None,
        far_file_target = None,
        token_type = "byte",
        extra_deps = [],
        **kwds):
    """Generates a regression test for the specified grammar.

    Args:
      name: The BUILD rule name, this should generally include a _test suffix.
      grammar: The rule defining the compiled grammar. If absent,
               <current package>:<name - '_test'>_sstable is used.
      test_file: A file containing test data in the format expected by
                 regression_test.cc. If absent, testdata/<name - '_test'>.tsv
                 is used.
      size: Size of the test, e.g. "large".
      test_file_target: Path to the target which contains testdata files.
                        This should be set together with test_file_path parameter.
      test_file_path: Path to the grammar testdata file.
                      This should be set together with test_file_target parameter.
      far_file_target: The target of the FAR file to test. If absent, <grammar>.far
                      is used.
      token_type: TokenType to use when parsing the text examples that are to
                be composed with rule FSTs in the FAR. One of 'byte' or 'utf8'.
      extra_deps: Extra dependencies list.
      **kwds: Attributes passed to the underlying cc_test rule.
    """
    grm_regression_test(
        name = name,
        grammar = grammar,
        test_file = test_file,
        testdata_packaged = True,
        size = size,
        test_file_target = test_file_target,
        test_file_path = test_file_path,
        far_file_target = far_file_target,
        token_type = token_type,
        extra_deps = extra_deps + [
        ],
        **kwds
    )

def nisaba_compile_script_lang_multi_grm_py(
        family,
        name,
        script_langs,
        data = [],
        data_per_lang = [],
        data_per_script = [],
        deps = []):
    """Generates multiple FAR and test targets for given script and language pairs.

    The source file used is <name>.py and corresponding testdata/<name>.tsv as
    the test file. From these this rule generates following targets:
    <name>.far (for byte token type)
    <name>_utf8.far
    <name>_test
    <name>_utf8_test

    <name>.py Expects 3 optional flags, 'token_type', 'script' and 'lang' and
    generates FAR file for this combination. Its dependencies and data files are
    listed in 'data', 'data_per_lang' and 'data_per_script' parameters.

    Args:
        name: Name of this rule, dictating the the source and test files and
              the generated FAR and test targets.
        data: The language or script agnostic part of the data parameter for
              <name>.py compilation.
        data_per_script: The script specific part of the data parameter for
                         <name>.py compilation.
        data_per_lang: The language specific part of the data parameter for
                       <name>.py compilation.
        family: The container directory name indicating the script family
                (e.g., 'brahmic').
        script_langs: Script-langauge tuples contributing to this build.
        deps: Deps for the <name>.py compilation.
    """
    for token_type in ("byte", "utf8"):
        name_token_type = ("%s_%s" % (name, token_type)).replace("_byte", "")
        for script, lang in script_langs:
            # Generates copies of the .py with different flag value defaults for each
            # script, language and token-type values.
            # Example: reading_norm_utf8.Deva.hi.py.
            out_py_file = "%s.%s.%s.py" % (name_token_type, script, lang)
            native.genrule(
                name = "make_%s" % out_py_file,
                srcs = ["%s.py" % name],
                outs = [out_py_file],
                cmd = "sed -r 's/(.script., .)/\\1%s/g' $< | \
                   sed -r 's/(.lang., .)/\\1%s/g' | \
                   sed -r 's/(.token_type., .)/\\1%s/g' > $@" % (script, lang, token_type),
                visibility = ["//visibility:private"],
            )

            # From script, language and token-type specific generated py file,
            # generates the corresponding FAR file.
            # Example: reading_norm_utf8.Deva.hi.far
            data_dir = "//nisaba/scripts/%s/data" % family
            script_dir = "%s/%s" % (data_dir, script)
            lang_dir = "%s/%s" % (script_dir, lang)
            nisaba_compile_grm_py(
                name = "%s.%s.%s" % (name_token_type, script, lang),
                data = data + [
                    ("%s:%s.tsv" % (lang_dir, entry)).replace("/:", ":")
                    for entry in data_per_lang + [name]
                ] + [
                    "%s:%s.tsv" % (script_dir, entry)
                    for entry in data_per_script
                ],
                visibility = ["//visibility:public"],
                deps = deps,
            )

        # Aggreated FAR file targets for each token-type.
        # Generates separate reading norm FAR files for each token-type values,
        # by combining individual FAR files for that token-type,
        # generated above.
        native.genrule(
            name = name_token_type,
            srcs = [
                "%s.%s.%s.far" % (name_token_type, script, lang)
                for script, lang in script_langs
            ],
            outs = ["%s.far" % name_token_type],

            cmd = "$(location @org_openfst//:farextract) $(SRCS) ; \
               $(location @org_openfst//:farcreate) %s $@" % " ".join(
                [
                    lang.upper() if lang else script.upper()
                    for script, lang in script_langs
                ],
            ),
            tools = [
                "@org_openfst//:farcreate",
                "@org_openfst//:farextract",
            ],
            visibility = ["//visibility:private"],
        )

        # Tests token-type specific FAR files.
        nisaba_grm_regression_test(
            name = "%s_test" % name_token_type,
            grammar = ":%s" % name_token_type,
            test_file = "testdata:%s.tsv" % name,
            token_type = token_type,
        )
