# Natural Transliteration for Brahmic Scripts

This collection of [OpenGrm Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini) grammars takes the [ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) transliteration of a Brahmic script that is normalized and converted by the [Nisaba Brahmic library](https://github.com/google-research/nisaba/tree/main/nisaba/nisaba/scripts/brahmic/README.md), and converts it to a Latin transliteration based on language specific pronunciation. For example, the natural transliteration of the same ISO string `apa` would be `ap` in Hindi, and `aba` in Malayalam.

The natural transliteration grammars use internal notations that only contain extended ASCII characters for ease of input. All substrings are enclosed in type specific, asymmetrical boundary marks. `< >` donates a [grapheme](#typ-representation-and-iso-inventory), `{ }` donates a [phoneme](#txn-representation-and-phoneme-inventory), and `“ ”` donates a [transliteration](#transliteration-strings-and-ltn-inventory) substring.

## typ representation and script inventories
The characters of a script is defined as a `Char` with the following
attributes:

**alias:** A string that will be used to refer to the character in grammars. For
example, if the alias of a character is 'A', in the grammar file this character
will be referred to as `gr.A` or `tr.A`. The default value is the uppercase of
`typ` as this is the most common case.

**typ:** An internal, byte-only string to represent the character.

**gr:** `typ` enclosed in `< >`. It is used to represent the characters of the
source script.

**tr:** `typ` enclosed in `“ ”`. It is used to represent the characters of the
target script.

**glyph:** The glyph of the character in the original script.

**ph:** A default pronunciation assignment for the character. ph is optional.

**cmp:** Graphemes of the parts for composite characters.

tr and gr are the underlying representations for the rewrite rules. For
example, rules with `gr.A` apply to `<a>`, and rules with `tr.A` apply to `“a”`.

Conventions for assigning a `typ` to a character:

* `typ` of ASCII characters are the same as the letter.

* `typ` of non-ASCII characters are a sequence of lowercase letters.

* `typ` of the uppercase letters have `_uc` suffix.

* `typ` of substrings have `s_` prefix.

  **Example:**

             | a         | u         | ä         | Ä         | au        |
   ----------|:---------:|:---------:|:---------:|:---------:|:---------:|
   **alias** | A         | U         | AU        | AU_UC     | S_AU      |
   **typ**   | a         | u         | au        | au_uc     | s_au      |
   **gr**    | `<a>`     | `<u>`     | `<au>`    | `<au_uc>` | `<s_au>`  |
   **tr**    | `“a”`     | `“u”`     | `“au”`    | `“au_uc”` | `“s_au”`  |
   **glyph** | a         | u         | ä         | Ä         | au        |
   **ph**    | ph.A      | ph.U      | ph.E      | ph.E      | ph.AU     |

This scheme disambiguates substrings for grammars. For example, a rule that
changes the transliteration of the diphthong `ph.AU` from 'au' to 'o' only
applies to `“s_au”` substrings and not `“au”` or `“a”“u”`.

[`iso_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/iso_inventory.py) is a library that contains the `typ`-ISO mapping and makes `Char` for ISO characters.

[`ltn_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/latin/ltn_inventory.py) is a library that makes `Char` for Latin script characters and transliteration substrings for romanization grammars.

## iso2typ grammar

`iso2typ` grammar rewrites an ISO string as a series of `typ` characters.

**Examples**

* `ā` -> `<aa>`
* `ṭ` -> `<tt>`
* `nⸯ` -> `<n_chl>`
* `āṭānⸯ` -> `<aa><tt><aa><n_chl>`

## txn representation and phoneme_inventory

`txn` is an internal, high coverage, typable representation for multilingual phoneme inventories.

For parsimony, txn uses a featurised representation for  diphthongs, affricates,
coarticulation, secondary articulation and features like phonation. Where a sequence of symbols need to be disambiguated, eg, a phoneme
sequence vs diphthong or affricate, or distinguishing between nasalization that
affects the whole phoneme vs. prenasalization and nasal release,
the combining symbol {+} is used.

Phonemes and features are defined as `Phon` with the following attributes:

**alias:** A string that will be used to refer to the phoneme in grammars. For
example, if the alias of a character is 'A', in the grammar file this Phon
can be referred to as `ph.A`.

**txn:** An internal, byte-only string to represent the character.

**ftr:** A list of phonological features.

**ph:** The acceptor fst of the `Phon`. The ph of a simple phoneme is its `txn`
enclosed in `{ }`.

**ipa:** The representation of the `Phon` in International Phonetic Alphabet.

**tr_dict:** A dictionary of transliteration strings in `tr` format.
Every `tr` dictionary has a 'base' key. For a simple `Phon`, 'base' is its
default transliteration. Derived and composite phonemes can have additional `tr`s,
in addition to a 'base' that is composed from its components.

**cmp:** The components of a derived or composite `Phon`.

  **Example:**

               | a           | u           | a_l         | au               |
   ------------|:-----------:|:-----------:|:-----------:|:----------------:|
   **alias**   | A           | U           | A_L         | A_U              |
   **txn**     | a           | u           | a_l         | a+u              |
   **ftr**     | vowel       | vowel       | vowel, long | diph, vowel, ... |
   **ph**      | `{a}`       | `{u}`       | `{a_l}`     | `{a}{+}{u}`      |
   **ipa**     | a           | u           | aː          | a͡u               |
   **tr_dict** | `base: “a”` | `base: “u”` | `base: “a”` | `base: “a”“u”`   |
               |             |             | `long: “aa”`| `diph: “au”`     |
               |             |             |             | `semi: “aw”`     |
               |             |             |             | `mono: “o”`      |


[`phoneme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/brahmic/natural_translit/phoneme_inventory.py) is a library that contains the `txn`-[IPA](https://www.internationalphoneticassociation.org/content/ipa-chart) mapping and forms the `txn` symbols covering the unified South Asian phoneme inventory presented in [Demirsahin et al. (2018)](https://research.google/pubs/pub47341/).

## iso2txn grammars

`iso2txn` grammar assigns a naive orthography to phonology mapping for iso graphemes prior to the phonological operations. The format of an assignment is `<iso_graphemes>={txn_phonemes}`.

**Example**

* `<aa><tt><aa><n_chl>` -> `<aa>={a_l}<tt>={tt}<aa>={a_l}<n_chl>={n}`

`iso2txn_ops` grammar contains phonological operations that depend on the iso graphemes that are on the left side of the alignment, and therefore don't fit the language agnostic phonological operations in the `phon_ops` grammar.

## phon_ops grammar

`phon_ops` grammar contains common phonological operations on the pronunciation side, independent of the source language or script.

**Example**: Malayalam voicing

* `<aa>={a_l}<tt>={tt}<aa>={a_l}<n_chl>={n}` -> `<aa>={a_l}<tt>={dd}<aa>={a_l}<n_chl>={n}`

## txn2ltn and iso2ltn_ops grammars

`txn2ltn` grammar contains a default txn pronunciation romanization.

`iso2ltn_ops` grammar contains romanization rules that depend on the iso graphemes that are on the left side of the alignment. In addition to providing rules for the language specific natural transliteration rules imported by the end to end grammar of each language, it has two Pan South Asian romanization outputs.

**PSAF**: Fine grained Pan South Asian representation. Fine grained in this context means that for characters that have more than one conventional transliteration, it uses the most informative one. For example, long vowels can be transliterated as one or two characters. PSAF uses the two character version to retain the vowel length information.

**Example**

* `<aa>={a_l}<tt>={dd}<aa>={a_l}<n_chl>={n}` ->

 `<aa>=“aa”<tt>=“d”<aa>=“aa”<n_chl>=“n”` ->

   `aadaan`

In this format different spellings of the same word in one language are likely to have closer romanizations, but they may differ across languages. For example, two Hindi spellings of the word "hindi", `hiṁdī` and `hindī` in ISO, will retain the long vowel ii and have the same PSAF, `hindii`. Whereas the Malayalam spelling of the same word will have a different PSAF `hindi` because the word ends with a short vowel in the native spelling, `hindi` in ISO.

**PSAC**: Coarse grained Pan South Asian representation. Coarse grained in this context means that PSAC conflates some transliteration substrings in order to simplify the romanization as much as possible. Fine details such as vowel length are lost in this format.

**Example**

* `<aa>={a_l}<tt>={dd}<aa>={a_l}<n_chl>={n}` ->

 `<aa>=“a”<tt>=“d”<aa>=“a”<n_chl>=“n”` ->

   `aadaan`

Discarding finer details makes it possible to have much closer PSAC romanizations of the same word across languages. For example, PSAC for "hindi" will be `hindi` for both Hindi and Malayalam, regardless of the vowel length in the source language.

## txn2ipa grammar

`txn2ipa` grammar converts the `txn` pronunciation to IPA using the mapping in the [`phoneme_inventory`](#txn-representation-and-phoneme-inventory).

**Example**

* `<aa>{a_l}<tt>{dd}<aa>{a_l}<n_chl>{ni}` ->

 `<aa>aː<tt>ɖ<aa>aː<n_chl>n` ->

   `aːɖaːn`

## e2e grammars

These are end-to-end grammars for individual languages.

**Example**

* `hi_e2e`: End-to-end grammar for Hindi

* `ml_e2e`: End-to-end grammar for Malayalam

End-to-end grammars compose the relevant fsts from grammars and pass arguments to functions where necessary.

**Example**

* `voicing` is a phon_ops function that takes the preceding and following phonological context as arguments. The ml_e2e grammar passes the arguments `ph.VOWEL, ph.NASAL, ph.APPROXIMANT` for the phonological context, so that voicing happens between vowels, nasals, and approximants.

```
_VOICING = ops.voicing(
    pyn.union(ph.VOWEL, ph.NASAL, ph.APPROXIMANT).optimize(),  # Preceding context
    rw.concat_r(
        ph.ASP.ques,
        pyn.union(ph.VOWEL, ph.NASAL, ph.APPROXIMANT)).optimize())  # Following context
```

Natural transliteration, which aims to capture the romanization of the source language by the users, is composed in the end to end grammar of the specific language. For example, the users of a language might prefer to use a long aa at the beginning of a word, but shorten it in other positions.

**NAT**: Regional natural transliteration.

**Example**

* `<aa>={a_l}<tt>={dd}<aa>={a_l}<n_chl>={n}` ->

 `<aa>“aa”<tt>“d”<aa>“a”<n_chl>“n”` ->

   `aadan`

The natural transliteration of the same word might differ for each language and might include conventions that don't directly match the pronunciation of the word in the conventional sense. For example, some languages might favour using `ee` for a long i or `oo` for a long u, while in other languages `ee` could only mean a long e. The guideline for the natural transliteration grammars is to approximate the most conventional way the users of that language in the appropriate context. For example, if the ISO string `ēpʰabī.ā.ī` will be `eephbiiaaii` in PSAF and `ephbiai` in PSAC, but the natural romanization could be `FBI` if it's the native spelling of the English acronym FBI and it's the way most users would romanize it. This acronym conversion is handled by the `typ2acr` grammar.

## util library

This library holds most common constants such as SIGMA_STAR and boundary signs for enclosing different types of strings, as well as basic operations for aligning and assigning strings.

## rewrite_functions library

This library contains common rewrite functions shared across grammars, which modify an alignment dependent on the context.

## Citing

If you use this software in a publication, please cite the accompanying
[paper](http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.718.pdf) from
[LREC 2022](https://lrec2022.lrec-conf.org/en/):

```bibtex
@InProceedings{demirsahin-natural2022,
  author = {Işın Demirşahin and Cibu Johny and Alexander Gutkin and Brian Roark},
  title = {Criteria for Useful Automatic Romanization in South Asian Languages},
  booktitle = {Proceedings of the 13th Conference on Language Resources and Evaluation (LREC 2022)},
  month = {June},
  year = {2022},
  address = {Marseille, France},
  publisher = {European Language Resources Association (ELRA)},
  pages = {6662--6673},
  url = {https://aclanthology.org/2022.lrec-1.718},
}
```
