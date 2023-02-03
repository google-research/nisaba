# Text Processing Grammars for Languages using Abjad or Alphabet Writing Systems

This package is a collection of
[OpenGrm Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini) grammars to
work with the texts in abjad / alphabet script. The language scripts under
consideration and their [BCP-47](https://tools.ietf.org/rfc/bcp/bcp47.txt)
script tags are as below. When a language tag is used as a finite state
transducer (FST) name, it will be all uppercase; example: `UR`. FST Archive
(FAR) names are all lowercase (e.g., `reversible_roman`). Supported languages
(sorted by language code):

1.  Arabic (MSA) (`ar`)
1.  Balochi (`bal`)
1.  Dari (`prs`)
1.  Kashmiri (`ks`)
1.  Pashto (`ps`)
1.  Persian (`fa`)
1.  Punjabi (Shahmukhi) (`pa`)
1.  Sindhi (`sd`)
1.  Sorani (Central Kurdish) (`ckb`)
1.  South Azerbaijani (`azb`)
1.  Standard Malay (Jawi orthography) (`ms`)
1.  Uighur (`ug`)
1.  Urdu (`ur`)
1.  Uzbek (`uz`)

## Reversible romanization

Bidirectional converter between abjad / alphabet script text and its
romanization. Example:

```
اردو ⇄ ârdv
```

This romanization attempts a unified representation for various abjad / alphabet
languages and their Brahmic counterparts, if exists (for example, Gurmukhi and
Shahmukhi for Punjabi). However, it is not guaranteed to be phonemic as an abjad
generally omits vowels. For example, گورنمنٹ gets romanized to `gvrnmnṭ`
representing the word `government` but without much indication about its vowels.

This representation is also developer friendly as it is a representation in
Latin. Since the reversible romanization is not lossy, the original script text
can be retrieved, with the original language ID.

For conversions in either direction, import the FSTs in Pynini as follows:

```python
import pynini
from rules_python.python.runfiles import runfiles
with pynini.Far(runfiles.Create().Rlocation(
                'nisaba/scripts/abjad_alphabet/reversible_roman.far')) as far:
  latin_from_arab = far['FROM_ARAB']
```

with the data dependency of:

```
"//nisaba/scripts/abjad_alphabet:reversible_roman.far"
```

Following per language FSTs romanize abjad / alphabet text:

```
reversible_roman.FROM_ARAB
...
```

Similarly, following per language FSTs convert romanization to corresponding
abjad / alphabet text:

```
reversible_roman.TO_ARAB
...
```

For Thrax, the FSTs could be imported as follows:

```
latin_from_arab = LoadFstFromFar['nisaba/scripts/abjad_alphabet/reversible_roman.far', 'FROM_ARAB'];
```

## Citation

If you use this software in a publication, please cite the accompanying
[paper](https://aclanthology.org/2022.wanlp-1.36.pdf) from
[WANLP 2022](https://sites.google.com/corp/view/wanlp2022/):

```bibtex
@inproceedings{gutkin-etal-2022-beyond,
    title = "Beyond {A}rabic: Software for {P}erso-{A}rabic Script Manipulation",
    author = "Gutkin, Alexander  and
      Johny, Cibu  and
      Doctor, Raiomond  and
      Roark, Brian  and
      Sproat, Richard",
    booktitle = "Proceedings of the Seventh Arabic Natural Language Processing Workshop (WANLP)",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, United Arab Emirates (Hybrid)",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.wanlp-1.36",
    pages = "381--387",
}
```


