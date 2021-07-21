# Data tables

All the grammars are driven by data supplied through a handful of simple mapping
tables. Time to time, we do find new legitimate usages of script outside the
grammar provided and they need to be incorporated. Tables format makes these
maintenance tasks easy. Here are the list data tables per script as TSV files.

## `consonant.tsv`

Characters with an inherent schwa. This can be a cluster as well. The
corresponding Latin sequence does not have schwa. See Devanagari examples below:

Native | Codepoints              | Latin
------ | ----------------------- | -----
क      | `KA: 0915`              | `k`
ख      | `KA: 0916`              | `kh`
क़     | `KA: 0956, NUKTA: 093C` | `q`

## `vowel.tsv`

Characters (or character sequences) which act as independent vowels. They can be
optionally followed by the coda entries. The corresponding Latin entry should
match for the appropriate pairs of independent and dependent vowels. See
Devanagari examples below:

Native | Codepoints       | Latin
------ | ---------------- | -----
अ      | `A: 0905`        | `a`
आ      | `AA: 0906`       | `ā`
ॲ      | `CANDRA A: 0972` | `æ`

## `vowel_sign.tsv`

Characters that consume the inherent schwa in a consonant. They are usually the
vowel signs. _Virama_ is not included. See Devanagari examples below:

Native | Codepoints             | Latin
------ | ---------------------- | -----
ा      | `SIGN AA: 093E`        | `ā`
ि      | `SIGN I: 093F`         | `i`
ृ      | `SIGN VOCALIC R: 0943` | `r̥`

## `virama.tsv`

Contains only virama character for the script. Primary function of a virama
character is to remove the inherent schwa from consonants. See the Devanagari
example below:

Native | Codepoint
------ | --------------
्      | `VIRAMA: 094D`

## `coda.tsv`

Combining marks whose only legal placement is to come at the end (in the coda)
of the aksara. For example _anusvara_, _candrabindu_, and _visarga_. See the
Devanagari examples below:

Native | Codepoints          | Latin
------ | ------------------- | -----
ँ      | `CANDRABINDU: 0901` | `m̐`
ं      | `ANUSVARA: 0902`    | `ṁ`
ः      | `VISARGA: 0903`     | `ḥ`

## `standalone.tsv`

Contains standalone characters which cannot take the vowel signs, _virama_, or
codas of a script, such as the Devanagari _Om_ sign. See Devanagari examples
below:

Native | Codepoints       | Latin
------ | ---------------- | -----
ॐ      | `OM: 0950`       | `ōm̐`
ऽ      | `AVAGRAHA: 093D` | `’`

## `nfc.tsv`

The NFC normalized form of characters or sequences as defined in Unicode data
tables, for the given script. See Devanagari examples below:

| Native Legacy | Codepoints        | Native Canonical | Codepoints        |
| ------------- | ----------------- | ---------------- | ----------------- |
| क़             | `QA: 0958`        | क़               | `KA: 0915, NUKTA: |
:               :                   :                  : 093C`             :
| ऩ            | `NA: 0928, NUKTA: | ऩ                | `NNNA: 0929`      |
:               : 093C`             :                  :                   :

## `visual_rewrite.tsv`

The specific rewrites that are part of the Visual Norm rewrites. Example: In
Devanagari, eyelash-RA can be represented in two ways `<RA, VIRAMA, ZWJ>` and
`<RRA, VIRAMA>`, where the later being the standard (The Unicode Standard
§12.1). The former sequence is rewritten to this standard form. First column
represents the non-standard form and the second column is the corresponding
canonical form. See Devanagari examples:

| Native Legacy | Codepoints         | Native Canonical | Codepoints          |
| ------------- | ------------------ | ---------------- | ------------------- |
| अा            | `A: 0905, SIGN AA: | आ                | `AA: 0906`          |
:               : 093E`              :                  :                     :
| न्ा           | `NA: 0928, VIRAMA: | न                | `NA: 0928`          |
:               : 094D, SIGN AA\:    :                  :                     :
:               : 093E`              :                  :                     :
| र्‍           | `RA: 0930, VIRAMA: | ऱ्               | `RRA: 0931, VIRAMA: |
:               : 094D, ZWJ\: 200D`  :                  : 094D`               :

## `preserve.tsv`

Usually the zero width characters like Zero Width Joiner `(ZWJ: 200D)`, Zero
Width Non-Joiner `(ZWNJ: 200C)`, and Zero Width Space `(ZWS: 200B)` can be
deleted from the text. However, they are meaningful in some contexts for some
scripts. For example, the name of the country Sri Lanka (ශ්‍රී ලංකා) needs a
`ZWJ` between Sinhala `<SHA, VIRAMA>` and `<RA>` for the correct visual. This
file indicates which sequences that are sandwiched between two consonants, need
to be preserved while removing the zero width characters. The first column is
the sequence to be preserved and the second column is a unique representative
text as a placeholder during the rewrite. See Devanagari example below:

Native | Codepoints                 | Latin
------ | -------------------------- | ----------------
्‌     | `VIRAMA: 094D, ZWNJ: 200C` | `[VIRAMA, ZWNJ]`

## `dead_consonant.tsv`

Consonants without an inherent schwa. This is a subset of the coda and its ISO
mapping is specified only in coda.tsv. See Bengali and Malayalam examples below:

Native | Codepoints
------ | -----------------
ৎ      | `KHANDA TA: 09CE`
ൽ      | `CHILLU L: 0D7D`

## `accept.tsv`

Valid character sequences specific for a script. If not specified in this file,
these sequences will be invalid and will be rejected by the well-formedness
acceptor. This file for some scripts may be empty as they may not have any
exceptions from the general logic. See Malayalam examples below:

Native | Codepoints
------ | ------------------------------
അ്     | `A: 0D05, VIRAMA: 0D4D`
ാം     | `SIGN A: 0D3E, ANUSVARA: 0D02`
