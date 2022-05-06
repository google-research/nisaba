# Description of language-specific data for Arabic script

## Data files

This directory contain following data files:

1.  `letter_languages.textproto`: Contains mapping from each abjad / alphabet
    character to language code indicating valid characters in that language.
1.  `reversible_roman.tsv`: Contains mapping from abjad / alphabet characters to
    Latin characters for reversible romanization.

## Language directories

Language specific directory names follow
[BCP-47](https://tools.ietf.org/rfc/bcp/bcp47.txt) Example: `ur` for Urdu. Each
language directory contain following data files:

1.  `visual_norm.textproto`: Contains rewrite rules for visual normalization of
    text in Arabic script.
1.  `reading_norm.textproto`: Contains rewrite rules that modify the visual
    Arabic script text.
