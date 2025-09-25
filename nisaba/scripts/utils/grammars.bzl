# Copyright 2025 Nisaba Authors.
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

load(
    "@org_opengrm_pynini//pynini/export:grm_py_build_defs.bzl",
    "compile_grm_py",
    "compile_multi_grm_py",
)
load("//nisaba/interim/testing:build_defs.bzl", "grm_textproto_test")

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

def nisaba_grm_textproto_test(
        name,
        textproto = None,
        token_type = "byte",
        extra_deps = [],
        **kwds):
    """Generates a textproto test for the specified grammar.

    Args:
      name: The BUILD rule name, this should generally include a _test suffix.
      textproto: The textproto location, if you don't want it to be automatically inferred.
      token_type: Token type (one of "byte", "utf8").
      extra_deps: Extra attributes passed to the underlying cc_test rule.
      **kwds: Attributes passed to the underlying rule.
    """
    grm_textproto_test(
        name = name,
        textproto = textproto,
        token_type = token_type,
        extra_deps = extra_deps + [
        ],
        mode = "one_top",
        **kwds
    )

def nisaba_compile_script_lang_multi_grm_py(
        family,
        name,
        script_langs,
        data = [],
        data_per_lang = [],
        data_per_script = [],
        deps = [],
        **kwds):
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
        script_langs: Script-language tuples contributing to this build.
        deps: Deps for the <name>.py compilation.
        **kwds: Additional attributes for FAR file targets, e.g., visibility.
    """
    script_langs = sorted(script_langs, key = lambda x: "".join([x[1], x[0]]).lower())
    for token_type in ("byte", "utf8"):
        name_token_type = ("%s_%s" % (name, token_type)).replace("_byte", "")
        for script, lang in script_langs:
            # Generates copies of the .py with different flag value defaults for each
            # script, language and token-type values.
            # Example: reading_norm_utf8_Deva_hi.py.
            out_py_file = "%s_%s_%s.py" % (name_token_type, script, lang)
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
                src = out_py_file,
                data = data + [
                    "%s:%s.tsv" % (lang_dir, entry)
                    for entry in data_per_lang
                    if lang
                ] + [
                    "%s:%s.tsv" % (script_dir, entry)
                    for entry in data_per_script
                ],
                visibility = ["//visibility:public"],
                deps = deps,
            )

        # Aggregated FAR file targets for each token-type.
        # Generates separate reading norm FAR files for each token-type values,
        # by combining individual FAR files for that token-type, generated
        # above.
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
            **kwds
        )
