# Description of data files

## Script specific directories

Data files corresponding to the scripts are kept under `script`. Script specific
directory names follow [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924)
convention of four letter script codes in lowercase with the initial letter
capitalized. Example: `Deva` for Devanagari.

1.  `consonant.textproto`: Characters with an inherent schwa. This can be a
    cluster as well. The corresponding Latin sequence does not have schwa.
    Example: `क ⇥ k`
1.  `dead_consonant.textproto`: Consonants without an inherent schwa. Examples:
    Malayalam Chillus, Bengali KHANDA TA. This is a subset of the coda and its
    ISO mapping is specified only in `coda.textproto`.
1.  `vowel_sign.textproto`: Characters that consume the inherent schwa in a
    consonant. They are usually the vowel signs. Virama is not included.
    Example: `ा ⇥ ā`
1.  `virama.textproto`: Contains only virama character for the script. Primary
    function of a virama character is to remove the inherent schwa from
    consonants.
1.  `vowel.textproto`: Characters (or character sequences) which act as
    independent vowels. They can be optionally followed by the coda entries. The
    corresponding Latin entry should match for the appropriate pairs of
    independent and dependent vowels. Example: `आ ⇥ ā`
1.  `coda.textproto`: Combining marks whose only legal placement is to come at
    the end (in the coda) of the akshara. For example anusvara, chandrabindu,
    and visarga in most scripts. Example: `ँ ⇥ m̐`
1.  `standalone.textproto`: Contains standalone characters which cannot take the
    vowel signs, virama, or codas of a script, such as the Devanagari Om sign.
    Example: `ॐ ⇥ ōm̐`
1.  `nfc.textproto`: The NFC normalized form of characters or sequences as
    defined in Unicode data tables, for the given script. Example: `क़(U+0958) ⇥
    क़(U+0915 U+093C)`
1.  `visual_rewrite.textproto`: The specific rewrites that are part of the
    visual normalization rewrites. Example: In Devanagari, eyelash-RA can be
    represented in two ways <RA, VIRAMA, ZWJ> and <RRA, VIRAMA>, where the later
    being the standard
    ([The Unicode Standard](http://www.unicode.org/versions/latest/) §12.1). The
    former sequence is rewritten to this standard form. First column represents
    the non-standard form and the second column is the corresponding standard
    form.
1.  `preserve.textproto`: Usually the zero width characters like Zero Width
    Joiner (ZWJ U+200D), Zero Width Non-Joiner (ZWNJ U+200C), and Zero Width
    Space (ZWS U+200B) can be deleted from the text. However, they are
    meaningful in some contexts for some scripts. For example, the name of the
    country Sri Lanka (ශ්‍රී ලංකා) needs a ZWJ between Sinhala `<SHA, VIRAMA>`
    and `<RA>` for the correct visual. This file indicates which sequences that
    are sandwiched between two consonants, need to be preserved while removing
    the zero width characters. The first column is the sequence and the second
    column is a unique representative text as a placeholder during the rewrite.
1.  `accept.textproto`: Valid character sequences specific for a script. If not
    specified in this file, these sequences will be invalid and will be rejected
    by the well-formedness acceptor. This file for some scripts may be empty as
    they may not have any exceptions from the general logic.
1.  `fixed.textproto`: Rewrites for fixed rule romanization for the script to
    its ISO representation.

## Language specific directories

The data for languages that use a particular script are kept under
subdirectories inside the corresponding script directory. These directory names
follow [BCP 47](https://tools.ietf.org/html/bcp47). For example, the data files
for Bangla in Bengali script are located in `Beng/bn` directory.

1.  `before_consonant.textproto` and `after_consonant.textproto`: The specific
    rewrites are part of the visual normalization rewrites specific to the
    language on top of the corresponding script specific ones. For example, the
    rewrites in `bn` will be applied on top of the corresponding `Beng` script
    rewrites. These rewrites are applied with *before-consonant* and
    *after-consonant* contexts respectively.

## Common directory

1.  `symbol.textproto`: Symbols common to all scripts. Examples: `ZWJ(U+200D)`
    and `ZWNJ(U+200C)`
