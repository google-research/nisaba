# Text Processing Grammars for Brahmic scripts

This package is a collection of
[OpenGrm Thrax](http://www.openfst.org/twiki/bin/view/GRM/Thrax) and
[OpenGrm Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini) grammars to
work with the texts in Brahmic scripts of South and Southeast Asia. Respective
C++ and Python access APIs are also provided. The language scripts under
consideration and their [BCP-47](https://tools.ietf.org/rfc/bcp/bcp47.txt)
script tags are as below. When a script tag is used as a finite state transducer
(FST) name, it will be all uppercase; example: `DEVA`. FST Archive (FAR) names
are all lowercase (e.g., `iso`).

1.  Bengali (`Beng`)
1.  Lontara (`Bugi`)
1.  Devanagari (`Deva`)
1.  Gujarati (`Gujr`)
1.  Gurmukhi (`Guru`)
1.  Kannada (`Knda`)
1.  Lepcha (Róng) (`Lepc`)
1.  Limbu (`Limb`)
1.  Malayalam (`Mlym`)
1.  Meetei Mayek (`Mtei`)
1.  Newa (Prachalit) (`Newa`)
1.  Oriya (`Orya`)
1.  Sinhala (`Sinh`)
1.  Syloti Nagri (`Sylo`)
1.  Tagalog (Baybayin) (`Tglg`)
1.  Takri (`Takr`)
1.  Tamil (`Taml`)
1.  Telugu (`Telu`)
1.  Thaana (`Thaa`)
1.  Tirhuta (Maithili) (`Tirh`)

[TOC]

## NFC {#nfc}

OpenFst Thrax grammar has neither native support for
[Unicode NFC](http://unicode.org/charts/normalization/) nor access to ICU
libraries to apply NFC. These FSTs can be used to create FSTs that convert
Brahmic text to its NFC form. Example:

```
ড় <09DC (Bengali RRA)> ⇒ ড় <09A1 (DDA), 09BC (Nukta)>
```

Use the NFC FSTs in Thrax using, for example:

```
nfc_deva = LoadFstFromFar['nisaba/scripts/brahmic/nfc.far', 'DEVA'];
```

or in Pynini using, for example:

```python
import pynini
from rules_python.python.runfiles import runfiles
with pynini.Far(runfiles.Create().Rlocation(
                'nisaba/scripts/brahmic/nfc.far')) as far:
  nfc_deva = far['DEVA']
```

with the data dependency of:

```
"//nisaba/scripts/brahmic:nfc.far"
```

Following FSTs are available, per script:

```
nfc.BENG
nfc.DEVA
...
```

Single FST for all the supported scripts: `nfc.BRAHMIC`

## Visual Norm {#visual_norm}

*Visual Norm* of a text is the result of the normalization that rewrites the
text to its standard sequence of codepoints, preserving its visual fidelity. For
example, in Malayalam, following rewrite needs to be applied to get the standard
Chillu representation from the legacy one:

```
ന്‍ <0D28 NA, 0D4D VIRAMA, 200D ZWJ> ⇒ ൻ <0D7B CHILLU N>
```

Visual Normalization is a necessary text preprocessing step for multiple
reasons:

1.  Unicode has occasionally defined visually identical, but separate legacy and
    standard codepoint sequences for compatibility reasons. Examples: Devanagari
    eyelash-RA, Malayalam Chillus.
2.  Input methods can differ by how they produce a particular visual.
    1.  When two sequences have same visual in a common rendering system. For
        example in Devanagari, ऑं `<CANDRA O, ANUSVARA>` is rendered the same as
        आँ `<AA, CANDRABINDU>` in many fonts. Later sequence is the standard.
    2.  Sometimes input methods or native keyboards pad the text with
        unnecessary joiners, just to be safe. However, joiners cannot be blindly
        deleted.
        [UAX #31](https://www.unicode.org/reports/tr31/#Layout_and_Format_Control_Characters)
        defines where joiners have important rendering functions and need to be
        preserved.

Visual Normalization applies NFC normalization internally; so there is no need
to apply NFC separately, on visual norm rewrite.

Use the Visual Norm FSTs in Thrax using, for example:

```
vn_deva = LoadFstFromFar['nisaba/scripts/brahmic/visual_norm.far', 'DEVA'];
```

or in Pynini using, for example:

```python
import pynini
from rules_python.python.runfiles import runfiles
with pynini.Far(runfiles.Create().Rlocation(
                'nisaba/scripts/brahmic/visual_norm.far')) as far:
  vn_deva = far['DEVA']
```

with the data dependency of:

```
"//nisaba/scripts/brahmic:visual_norm.far"
```

Following FSTs are available, per script:

```
vn.BENG
vn.DEVA
...
```

Single FST for all the scripts is not available as the joiner preservation rules
are not compatible across scripts.

## Well-Formedness Acceptor {#wellformed}

Not every possible sequence of characters of a Brahmic script are well-formed;
nor, all illegal sequences can be visual norm'ed to valid sequences. For
example, a word starting with a Virama is not well-formed. Some illegal
sequences:

```
काु <0915 KA, 093E VOWEL SIGN AA, 0941 VOWEL SIGN U> (Devanagari)
്ന <0D4D VIRAMA, 0D28 NA> (Malayalam)
```

The `wellformed` acceptor accepts only well-formed character sequence of a given
script. Usually it is applied after rewriting the string using Visual Norm FST
separately.

Use the wellformedness FSTs in Thrax using, for example:

```
wf_deva = LoadFstFromFar['nisaba/scripts/brahmic/wellformed.far', 'DEVA'];
```

or in Pynini using, for example:

```python
import pynini
from rules_python.python.runfiles import runfiles
with pynini.Far(runfiles.Create().Rlocation(
                'nisaba/scripts/brahmic/wellformed.far')) as far:
  wf_deva = far['DEVA']
```

with the data dependency of:

```
"//nisaba/scripts/brahmic:wellformed.far"
```

Following FSTs are available, per script:

```
wf.BENG
wf.DEVA
...
```

Single FST for all the scripts is not available as the joiner behavior is not
compatible across scripts.

## ISO 15919 romanization {#iso}

Bidirectional converter between Brahmic script text and its
[ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) representation. Example:

```
ब्राह्मिक ⇄ brāhmika
```

This conversion between abugida and alphabetic script systems provides unified
representation for various Brahmic scripts. It is also developer friendly as
this unified representation is in Latin. Since the ISO representation is not
lossy, the original script text can be retrieved, with the original script ID.

For conversions in either direction, import the FSTs in Thrax using, for
example:

```
iso_from_deva = LoadFstFromFar['nisaba/scripts/brahmic/wellformed.far', 'FROM_DEVA'];
```

or in Pynini using, for example:

```python
import pynini
from rules_python.python.runfiles import runfiles
with pynini.Far(runfiles.Create().Rlocation(
                'nisaba/scripts/brahmic/iso.far')) as far:
  iso_from_deva = far['FROM_DEVA']
```

with the data dependency of:

```
"//nisaba/scripts/brahmic:iso.far"
```

### Brahmic to ISO

Following per script FSTs convert text to its ISO representation:

```
iso.FROM_BENG
iso.FROM_DEVA
...
```

The FST for all the scripts together: `iso.FROM_BRAHMIC`. This FST ignores
punctuation and unsupported scripts Latin. This rewrite never fails.

### ISO to Brahmic

Following per script FSTs convert ISO representation to corresponding script
text:

```
iso.TO_BENG
iso.TO_DEVA
...
```

A single FST to cover all Brahmic scripts is not possible, as the source script
information is lost on ISO romanization.

### Extensions to ISO 15919

Since ISO 15919 cannot represent recently encoded characters and some prevailing
textual conventions, it is enhanced with the conventions from other sources:

1.  [GitHub: language-resources](https://github.com/google/language-resources/blob/master/mul_034/indic_graphemes.tsv)

1.  [Richard Ishida's Docs](https://r12a.github.io/scripts/#scriptnotes)

Additionally following are incorporated:

#### Independent vowel at non-word-initial position {.leaf-numbered}

Independent vowel at non-word-initial position is represented with a preceding
`.`(dot). In the example below, independent Devanagari `u` at the end of the
word is represented by `.u`:

```
गहाउ ⇄ gahā.u
```

#### Vowel signs not following a consonant {.leaf-numbered}

Dangling vowel sign that does not follow a consonant is represented with a
preceding '-' (dash). Example:

```
ാം ⇄ -āṁ
```

#### Virama not following a consonant {.leaf-numbered}

Dangling Virama that does not follow a consonant is represented with a
'˘'(breve). In the example below, the Malayalam schwa is represented by VIRAMA
after SIGN U. This Virama is represented explicitly by a combining breve:

```
ത്തു് ⇄ ttŭ
```

#### Malayalam: Traditional au-sign {.leaf-numbered}

The contemporary usage of AU LENGTH MARKER to indicate /au/ vowel sign is
romanized as per ISO 15919. The traditional usage with VOWEL SIGN AU is
represented separately as `au̯`.

#### Religious symbol Om {.leaf-numbered}

Some Brahmic scripts have the religious symbol *Om* encoded as a separate
character. Strictly speaking, religious symbols need not to be transliterated.
However, as *Om* has a standard phonetic transcription, it is represented as
`ōm̐`, as an exception to this convention.

## Fixed rule transliteration {#fixed}

This FST converts fixed rule Brahmic romanization to corresponding native text.

By fixed rule romanization, we refer to the set of deterministic rules used
to unambiguously represent Brahmic scripts using ASCII characters, for input
purposes. [ITRANS](https://en.wikipedia.org/wiki/ITRANS) for Devanagari and
[Mozhi](https://sites.google.com/site/cibu/mozhi2) for Malayalam are examples.

The rules defined in the script specific `fixed.tsv` convert the ASCII text to
[ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) as per above schemes.
That ISO 15919 output is then converted to respective Brahmic text using
ISO-to-native conversion defined in [ISO 15919 romanization](#iso).

## C++ API {#cc}

### Higher level Grammar and Normalizer Classes

Include directive:

```
#include "nisaba/scripts/brahmic/grammar.h"
```

BUILD dependency:

```
"//nisaba/scripts/brahmic:cc"
```

This target is optimized for dependency size and uses FSTs in a compact format
and the FAR files are embedded in the library as a memfile.

#### Grammar Class

1.  To access individual grammars, create a `Grammar` instance like:
    `nisaba::brahmic::Grammar("iso", "FROM_DEVA")`. The parameters are the FAR
    file's basename and the FST name, respectively. Available FARs and their
    FSTs are indicated below and are described in the respective sub-sections:

    1.  [iso](#iso)

        1.  FROM_BENG
        1.  TO_BENG
        1.  FROM_DEVA
        1.  TO_DEVA
        1.  ...

    1.  [nfc](#nfc)

        1.  BENG
        1.  DEVA
        1.  ...

    1.  [visual_norm](#visual_norm)

        1.  BENG
        1.  DEVA
        1.  ...

    1.  [wellformed](#wellformed)

        1.  BENG
        1.  DEVA
        1.  ...

1.  The constructed `Grammar` instance needs to be initialized by `.Load()`.

1.  String rewrite by the FST is done as per this example: `.Rewrite("हिन्दी",
    &output_str)`. For the FAR `iso` and the FST `FROM_DEVA`, the `output_str`
    gets `hindī` as the result. Input and output strings can be the same
    `std::string` instance.

1.  Acceptance of a string by the FSA is indicated by the boolean value returned
    by: `.Accept("हिन्दी")`.

Please see nisaba/scripts/brahmic/grammar_test.cc as well to
learn the usage.

#### Normalizer Class

Normalizer rewrites an input string by applying visual norm; then, returns a
boolean indicating if that output string is well-formed or not.

1.  Create a `Normalizer` instance like: `nisaba::brahmic::Normalizer("Deva")`.
    Only parameter is the script tag.

1.  The constructed `Normalizer` instance needs to be initialized by `.Load()`.

1.  String rewrite by the FST is done as per this example: `bool isWellFormed =
    normalizer.Rewrite("हिन्दी", &output_str)`. Well-formedness of the output
    string is indicated by the boolean value returned. Even if the input cannot
    be well-formed, result of the visual norm is updated in the output string.
    Input and output strings can be the same `std::string` instance.

Please see nisaba/scripts/brahmic/grammar_test.cc as well to
learn the usage.

### Lower level Far Class to access FSTs directly

Include directive:

```
#include "nisaba/scripts/brahmic/far.h"
```

Build dependency:

```
"//nisaba/scripts/brahmic:far_cc"
```

This target is not optimized for dependency size and provides FSTs in default
Vector format. The FAR data dependencies are not embedded and are accessed from
the run files directory at runtime.

1.  The construct `Far` object with the FAR name as the only argument. Example
    for FAR names: *wellformed\_utf8* indicating `utf8` token type.
    Corresponding `byte` token type FAR name would be: *wellformed*. Apart from
    the token type, the FAR and FST names are as used in the `Grammar` class
    described above.

1.  Far object needs to be initialized by `.Load()` before accessing the
    contained FSTs; returns `absl::OkStatus()`, if successful.

1.  Unique pointer to the FST is available through `.Fst(FST name)`. Example for
    an FST name: `Deva`.

Please see `nisaba/scripts/brahmic/far_test.cc` as well to
learn the usage.

## Python API

Python API is accessible through following import:

```
from nisaba import brahmic
```

BUILD dependency:

```
"//nisaba/scripts/brahmic:py"
```

API calls to fetch an FST:

1.  NFC of all Brahmic scripts: `brahmic.Nfc()`

1.  Any Brahmic script to ISO: `brahmic.ToIso()`

1.  ISO to a specific Brahmic script: `brahmic.IsoTo(<script tag. e.g.:
    'Deva'>)`

1.  Visual Norm: `brahmic.VisualNorm(<script tag. e.g.: 'Deva'>)`

1.  Well-Formed: `brahmic.WellFormed(<script tag. e.g.: 'Deva'>)`

Following operations are defined on the above FST:

1.  `fst.ApplyOnText(<text>)`: Transduce the given text using the FST.

1.  `fst.AcceptText(<text>)`: Accept or reject the given text using the FST.

### Normalizing text

`brahmic.NormalizingAcceptor(<script tag. e.g.: 'Deva'>)` provides a class to
normalize text by applying visual norm, while rejecting it, if it is still
ill-formed. The `brahmic.IllFormedError` exception is thrown on rejection. This
class has following methods:

1.  `.ApplyOnText(<text>)`: Operates on text with words separated by
    punctuations or white spaces.
1.  `.ApplyOnWord(<text>)`: Operates at word level. It does not expect
    punctuations or white spaces and the entire word should be well-formed in
    the given script.

If the script tag is not supported `brahmic.ScriptError` exception is thrown.

## Commandline Access

Example for commandline access:

```
bazel build -c opt nlp/grm/language/util/rewrite-tester \
  nisaba/scripts/brahmic/visual_norm.far

cat deva-words.txt |
bazel-bin/external/org_opengrm_thrax/rewrite-tester \
  --far=bazel-bin/nisaba/scripts/brahmic/visual_norm.far \
  --rules=DEVA > visual_normed_deva_words.txt
```

Available FARs are:

1.  NFC: `nisaba/scripts/brahmic/nfc.far`

1.  ISO: `nisaba/scripts/brahmic/iso.far`

1.  Visual Norm: `nisaba/scripts/brahmic/visual_norm.far`

1.  Well-Formed: `nisaba/scripts/brahmic/wellformed.far`
