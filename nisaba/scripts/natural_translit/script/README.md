# Script representation

[TOC]

## typ

`typ` is an internal, easily typable, byte-only representation for characters in a script.

**Example**

```
āṭānⸯ -> <aa><tt><aa><n_chl>
```

## Char

The characters of a script is defined as a `Char` with the following attributes:

**alias:** A string that will be used to refer to the character in grammars. For example, if the alias of a character is 'A', in the grammar file this character will be referred to as `gr.A` or `tr.A`. The default value is the uppercase of `typ` as this is the most common case.

**typ:** An internal, byte-only string to represent the character.

**gr:** `typ` enclosed in `< >`, used for representing the characters of the source script.

**tr:** `typ` enclosed in `ˋ ˋ`, used for representing the characters of the target script.

**glyph:** The glyph of the character in the original script.

**ph:** A default pronunciation assignment for the character, as the `ph` of a [`Phon`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/README.md). This field is optional.

**cmp:** The list of `gr` of the parts for composite characters.

`tr` and `gr` are the underlying representations for the rewrite rules. For example, rules for `gr.A` apply to `<a>`, and rules for `tr.A` apply to `ˋaˋ`.

Conventions for assigning a `typ` to a character:

* `typ` of ASCII characters are the same as the letter.

* `typ` of non-ASCII characters are a sequence of lowercase letters.

* `typ` of the uppercase letters have `_uc` suffix.

* `typ` of substrings have `s_` prefix.

  **Example:**

             | a         | u         | ä         | Ä           | au
   ----------|:---------:|:---------:|:---------:|:-----------:|:----------:
   **alias** | A         | U         | AU        | AU_UC       | S_AU
   **typ**   | a         | u         | au        | au_uc       | s_au
   **gr**    | `<a>`     | `<u>`     | `<au>`    | `<au_uc>`   | `<s_au>`
   **tr**    | `ˋaˋ`     | `ˋuˋ`     |`ˋauˋ`     |`ˋau_ucˋ`    |`ˋs_auˋ`
   **glyph** | a         | u         | ä         | Ä           | au
   **ph**    | `ph.A`    | `ph.U`    | `ph.E`    | `ph.E`      | `ph.AU`

This scheme disambiguates substrings for grammars. For example, a rule that changes the transliteration of the diphthong `ph.AU` from 'au' to 'o' only applies to `ˋs_auˋ` substrings and not `ˋauˋ` or `ˋa` `uˋ`.

## Script inventories

* [`brahmic/grapheme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/grapheme_inventory.py) is a library that contains the `typ`-ISO mapping and `Char`s for ISO characters.

* [`latin/ltn_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/latin/ltn_inventory.py) is a library that contains `Char`s for Latin script characters and common transliteration substrings for romanization grammars.
