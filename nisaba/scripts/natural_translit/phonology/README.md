# Phonological representation

[TOC]

## txn

`txn` is an internal, high coverage, easily typable, byte-only representation for multilingual phoneme inventories.

For parsimony, `txn` uses a featurized representation for diphthongs, affricates, coarticulation, secondary articulation and features like phonation. Where a sequence of symbols need to be disambiguated, eg, a phoneme sequence vs diphthong or affricate, or distinguishing between nasalization that affects the whole phoneme vs. prenasalization and nasal release, the combining symbol `{+}` is used.

In order to keep the number of primitives to a minimum, features that can be present at different levels are modified by a shared set of qualifiers. For example, instead of using `{primary, secondary}` for stress, `{extra-short, short, half-long, long, extra-long}` for duration and various qualifiers for tone and intonation, there is a shared set of level modifiers `{bottom, low, middle, high, top}` and change modifiers `{rising, falling, interrupt}`.

With this scheme some suprasegmental features can be represented as:

* Rising tone: `[contour, rising]`
* Mid rising tone: `[pitch, mid] + [contour, rising]`
* Falling tone: `[contour, falling]`
* Global rise in intonation: `[intonation, rising]`
* Global fall in intonation: `[intonation, falling]`

The subset of modifiers are defined within feature. For example, primary stress is represented as `[stress, high]` and secondary stress is represented as `[stress, middle]`. However this doesn't necessarily imply the existence of `[stress, top]` since there is no need for an additional level of stress feature.

The default level of a feature is also defined within feature. For example, the default value for duration can be `[duration, low]` in order to accommodate other possible durations.

* Unmarked phoneme is implicitly `[duration, low]`
* Long phoneme: `[duration, high]`
* Extra-long phoneme: `[duration, top]`
* Half-long phoneme: `[duration, middle]`
* Extra-short phoneme: `[duration, bottom]`

For another feature, the default can be `[<feature>, bottom]` or `[<feature>, middle]` depending on the general usage of the feature and the semantics attributed to it.

## Phon

Phonemes and standalone features are represented as `Phon` objects with following attributes:

**alias:** A string that will be used to refer to the phoneme in grammars. For example, if the alias of a character is 'A', in the grammar file this Phon can be referred to as `ph.A`.

**txn:** An internal, byte-only string to represent the character.

**ftr:** A list of phonological features.

**ph:** The acceptor fst of the `Phon`. The ph of a simple phoneme is its `txn` enclosed in `{ }`.

**ipa:** The representation of the `Phon` in International Phonetic Alphabet.

**tr_dict:** A dictionary of transliteration strings as `tr` of a [`Char`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/script/README.md). Every `tr` dictionary has a `base` key. For a simple `Phon`, `base` is its default transliteration. Derived and composite phonemes can have additional `tr`s if they are commonly transliterated in a way that differs from the concatenation of its components.

**cmp:** The components of a derived or composite `Phon`.

  **Example:**

               | a            | u            | au
   ------------|:------------:|:------------:|:----------------:
   **alias**   | A            | U            | A_U
   **txn**     | a            | u            | a+u
   **ftr**     | vowel        | vowel        | diph, vowel, ...
   **ph**      | `{a}`        | `{u}`        | `{a}{+}{u}`
   **ipa**     | a            | u            | a͡u
   **tr_dict** |`base: ˋaˋ`   |`base: ˋuˋ`   |`base: ˋaˋ ˋuˋ`
               |              |              |`diph: ˋauˋ`
               |              |              |`semi: ˋawˋ`
               |              |              |`mono: ˋoˋ`

## Multilingual phoneme inventory

The [`phoneme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/phoneme_inventory.py) library contains a multilingual `Phon` inventory. The complete list of `Phon`s can be found [here](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/doc/phon_table.md) along with [IPA](https://www.internationalphoneticassociation.org/content/ipa-chart) mapping. The IPA symbols in this table are meant to be descriptive rather than definitive. Since related `Phon`s are derived from each other, the IPA strings are created dynamically during the derivation process. As a result, some phonemes with dedicated IPA symbols are represented as a symbol and diacritic instead. For example, the voiced bilabial implosive is represented as `bʼ` rather than the dedicated IPA symbol `ɓ`.

Language specific phoneme inventories can be built by importing phonemes from the multilingual inventory. For example, [brahmic/phoneme inventory](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/phoneme_inventory.py) contains the phonemes covering the unified South Asian phoneme inventory presented in [Demirsahin et al. (2018)](https://research.google/pubs/pub47341/).

## Phonological operations

The `g2p` grammars produce spelling-pronunciation alignments between `Char`s and `Phon`s. The format of an alignment is `<char_typ>={phon_txn}`.

**Example**

```
<a><tt><aa> -> <a>={a}<tt>={tt}<aa>={a}{:h}
```

Libraries such as [voicing](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology/operations/voicing.py) contain common phonological rules that can apply to a sequence of phonemes or a g2p alignment independent of the source language or script.

**Example**:

Common voicing rule

```
{tt} -> {dd}
```

Application of the Malayalam intervocalic voicing:

```
<a>={a}<tt>={tt}<aa>={a}{:h} -> <a>={a}<tt>={dd}<aa>={a}{:h}
```
