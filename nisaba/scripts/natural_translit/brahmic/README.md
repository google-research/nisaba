# Libraries for processing Brahmic scripts and unified South Asian phonology

[TOC]

This directory contains libraries that contain common resources such as the input and output symbol inventories and a superset of rules for building parameterizable g2p, romanization, and deromanization grammars for a group of South Asian languages, hereon referred to as PSA (Pan South Asian).

The individual grammars are built according to the [language parameters](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/language_params) provided for each language. See this [file](https://github.com/google-research/nisaba/tree/main/nisaba/nisaba/scripts/natural_translit/README.md) for the exact locations of the grammars for individual languages.

## Common inventories

### Grapheme inventory

[ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) transliteration as normalized by [Nisaba Brahmic library](https://github.com/google-research/nisaba/tree/main/nisaba/nisaba/scripts/brahmic/README.md) provides an underlying unified representation for Brahmic scripts. The [`grapheme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/grapheme_inventory.py) library contains the [`Char`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/script/README.md) inventory that represents ISO as a script.

### Phoneme inventory

The [`phoneme inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/phoneme_inventory.py) library contains the PSA [`Phon`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/README.md) inventory that covers the unified South Asian phoneme inventory presented in [Demirsahin et al. (2018)](https://research.google/pubs/pub47341/). The `Phon`s are imported from the [multilingual phoneme inventory](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/phoneme_inventory.py) and are given PSA-specific romanization labels where it differs from the multilingual inventory.

## Grammars builders

### Deromanization

The [`deromanizer`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/deromanizer.py) library contains transliteration rules from Latin to native script. Due to the underspecification of romanization in Brahmic languages, for example the loss of distinction between a dental `t` and the retroflex `ṭ`, it is not always possible to capture the intended native script using rule based grammars. Therefore, the main aim of deromanization is to generate a plausible string in the native script or ISO, which never fails for any string of Latin letters.

**Example**

```
atin -> atina and अतिन
```

### G2P

The [`g2p`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/g2p.py) library contains rules for generating ISO - pronunciation alignments in `<iso_char_typ>={phon_txn}` format, which is used as input for pronunciation-driven transliteration grammars. In addition, the phonological transcriptions of the g2p output are exported as light-weight phonological transcription grammars.

**Example**

```
āṭīna -> <aa><tt><ii><n><a> ->

<aa>={a}{:h}<tt>={tt}<ii>={i}{:h}<n>={ni}<a>={sil} -> aːʈiːn̪
```

### Romanization

The [`romanizer`]((https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/romanizer.py)) library contains common romanization rules that take the g2p alignments as input. It is used for building natural romanization grammars as well as two levels of PSA romanization as described below.

#### NAT

Natural transliteration aims to capture the romanization of the source language by the users following the most frequent conventions observed in daily use.

**Example**

```
āṭīna ->

<aa>={a}{:h}<tt>={tt}<ii>={i}{:h}<n>={ni}<a>={sil} -> ateen
```

For non standardized cases, for example when choosing between the 'ii', 'ee' or 'i' transliteration of the long vowel `ī`, NAT follows the most frequent romanization observed in a given context.

The intended romanization of loanwords, for example the Hindi strings `hi.ara` (or `hiyara`) for the English words 'here' and 'hear', cannot be predicted by the current rule based grammars. They are romanized using the same rules as the native strings, resulting in 'hiar' or 'hiyar', respectively. When there are more recognizable patterns, NAT generates the intended romanization where possible. For example, `ēpʰabī.ā.ī` is romanized as 'FBI' rather than 'ephbiai' since this pattern is highly unlikely in native words and it can be easily recognized by the acronym rules.

NAT takes regional conventions into account. For example, in Malayalam and Tamil, the dental `t` is romanized as 'th', as opposed to only 't' like other PSA languages such as Bengali or Hindi where 'th' almost exclusively represents the aspirated letters `tʰ` or `ṭʰ`.

In some cases, these varying conventions result in very different NAT romanizations of the same word within and across languages, obscuring the similarity or the common origin of the native spellings. We provide two additional PSA schemes for multilingual applications where these commonalities might be useful. These schemes still deviate from the strictly reversible representations such as ISO due to the pronunciation-driven nature of Brahmic romanization and the lack of one to one relation between Brahmic scripts and Basic Latin, but they are not as highly tailored for daily use as NAT.

#### PSAC

PSAC is the coarse grained PSA representation. Coarse grained in this context means that when there are multiple possible romanizations, PSAC chooses the simplest option, losing finer distinctions such as vowel length.

**Example**

```
āṭīna ->

<aa>={a}{:h}<tt>={tt}<ii>={i}{:h}<n>={ni}<a>={sil} -> atin
```

Discarding finer details makes it possible to have much closer PSAC romanizations of the same word across languages. For example, the native spellings for the English loanword 'political' is `pôliṭikala` and `pōliṭikala` in Hindi and `poḷiṟṟikkalⸯ` in Malayalam. The PSAC romanization of all three ISO strings is 'politikal' despite the differences in vowel and consonant lengths and places of articulation in native scripts.

#### PSAF

PSAF is the fine grained PSA representation. Fine grained in this context means that when there are multiple possible romanizations, PSAF chooses the most informative one. For example, the long vowels and geminations are always romanized to reflect the length.

**Example**

```
āṭīna ->

<aa>={a}{:h}<tt>={tt}<ii>={i}{:h}<n>={ni}<a>={sil} -> aatiin
```

In this format, different spellings of the same word in one language are likely to have closer romanizations, but they may differ more across languages. For example, the PSAF romanization of the two Hindi spellings `pôliṭikala` and `pōliṭikala` are 'poolitikal', retaining the vowel length. The PSAF romanization of the Malayalam spelling `poḷiṟṟikkalⸯ` is 'politikkal' reflecting the consonant length. The differences between the native letters such as `ô` and `ō` within Hindi and `l` and `ḷ` or `lⸯ` between Hindi and Malayalam are still lost due to the restrictions of the Basic Latin script.
