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

"""Starlark utilities for dealing with Pynini targets."""

load("@org_opengrm_thrax//:src/bazel/regression_test_build_defs.bzl", "grm_regression_test")
load(
    "@org_opengrm_pynini//pynini/export:grm_py_build_defs.bzl",
    "compile_grm_py",
    "compile_multi_grm_py",
)

# FST type for compile_grm_py and compile_multi_grm_py; depend on
# //nisaba/utils:fst_types to read such FSTs.
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
        deps = None,
        data = None,
        **kwds):
    """Provides a target to convert a Pynini file into multiple (portable) FAR files.

    Turns a Pynini file into a FAR file with the specified FAR and FST types.

    Assumes that there are exactly two output files, and that they are "byte"
    and "utf8" mode versions of the created FSTs.

    Args:
      name: The BUILD rule name and the file prefix for the generated output.
      deps: A list of other compile_grm rules that we'll need for this grammar.
      data: Extra data dependencies used in the Pynini file.
      **kwds: Attributes common to all BUILD rules, e.g., testonly, visibility.
    """
    compile_multi_grm_py(
        name = name,
        fst_type = _FST_TYPE,
        outs = {"byte": name + ".far", "utf8": name + "_utf8.far"},
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
