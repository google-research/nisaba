# Description of data files

## Script specific directories

Data files corresponding to the scripts are kept under `script`. Script specific
directory names follow [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)
convention of four letter script codes in lowercase with the initial letter
capitalized. Example: `Deva` for Devanagari.


1.  `consonant.tsv`: Characters with an inherent schwa. This can be a cluster as
    well. The corresponding Latin sequence does not have schwa. Example: `क ⇥ k`
1.  `dead_consonant.tsv`: Consonants without an inherent schwa. Examples:
    Malayalam Chillus, Bengali KHANDA TA. This is a subset of the coda and its
    ISO mapping is specified only in coda.tsv.
1.  `vowel_sign.tsv`: Characters that consume the inherent schwa in a consonant.
    They are usually the vowel signs. Virama is not included. Example: `ा ⇥ ā`
1.  `virama.tsv`: Contains only virama character for the script. Primary
    function of a virama character is to remove the inherent schwa from
    consonants.
1.  `vowel.tsv`: Characters (or character sequences) which act as independent
    vowels. They can be optionally followed by the coda entries. The
    corresponding Latin entry should match for the appropriate pairs of
    independent and dependent vowels. Example: `आ ⇥ ā`
1.  `coda.tsv`: Combining marks whose only legal placement is to come at the end
    (in the coda) of the akshara. For example anusvara, chandrabindu, and
    visarga in most scripts. Example: `ँ ⇥ m̐`
1.  `standalone.tsv`: Contains standalone characters which cannot take the vowel
    signs, virama, or codas of a script, such as the Devanagari Om sign.
    Example: `ॐ ⇥ ōm̐`
1.  `nfc.tsv`: The NFC normalized form of characters or sequences as defined in
    Unicode data tables, for the given script. Example: `क़(U+0958) ⇥ क़(U+0915
    U+093C)`
1.  `visual_rewrite.tsv`: The specific rewrites that are part of the Visual Norm
    rewrites. Example: In Devanagari, eyelash-RA can be represented in two ways
    <RA, VIRAMA, ZWJ> and <RRA, VIRAMA>, where the later being the standard
    ([The Unicode Standard](http://www.unicode.org/versions/latest/) §12.1). The
    former sequence is rewritten to this standard form. First column represents
    the non-standard form and the second column is the corresponding standard
    form.
1.  `preserve.tsv`: Usually the zero width characters like Zero Width Joiner
    (ZWJ U+200D), Zero Width Non-Joiner (ZWNJ U+200C), and Zero Width Space (ZWS
    U+200B) can be deleted from the text. However, they are meaningful in some
    contexts for some scripts. For example, the name of the country Sri Lanka
    (ශ්‍රී ලංකා) needs a ZWJ between Sinhala `<SHA, VIRAMA>` and `<RA>` for the
    correct visual. This file indicates which sequences that are sandwiched
    between two consonants, need to be preserved while removing the zero width
    characters. The first column is the sequence and the second column is a
    unique representative text as a placeholder during the rewrite.
1.  `accept.tsv`: Valid character sequences specific for a script. If not
    specified in this file, these sequences will be invalid and will be rejected
    by the well-formedness acceptor. This file for some scripts may be empty as
    they may not have any exceptions from the general logic.
1.  `fixed.tsv`: Rewrites for fixed rule romanization for the script to its ISO
    representation.

## Language specific directories

Data files corresponding to the specific languages are kept under `lang`.
These directory names follow [BCP 47](https://tools.ietf.org/html/bcp47).
Example: `bn` for Bengali.

1.  `before_consonant.tsv` and `after_consonant.tsv`: The specific rewrites are
    part of the Visual Norm rewrites specific to the language on top of the
    corresponding script specific ones. For example, the rewrites in `bn`
    will be applied on top of the corresponding `Beng` script rewrites. These
    rewrites are applied with _before-consonant_ and _after-consonant_ contexts
    respectively.

## Common directory

1.  `symbol.tsv`: Symbols common to all scripts. Examples: `ZWJ(U+200D)` and
    `ZWNJ(U+200C)`
