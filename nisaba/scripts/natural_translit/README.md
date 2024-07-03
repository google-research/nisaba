# Natural Transliteration

[TOC]

## Overview

This collection of [OpenGrm Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini) grammars provide rule based transliteration between scripts, currently [romanization](#romanization) and [deromanization](#deromanization), as well as a [phonological transcription](#g2p) in cases where a grapheme-to-phoneme grammar is used to inform the transliteration.

Natural transliteration refers to the way the users transliterate between scripts in daily use, as opposed to the official or reversible transliteration schemes such as the extended [ISO 15919](https://github.com/google-research/nisaba/blob/main/nisaba/nisaba/scripts/brahmic/README.md#iso) for Brahmic scripts, which is used for the examples below for readability.

In some cases natural transliteration is pronunciation-driven rather that reflecting the exact spelling in the source script. For example, Hindi, 'कांके' (`kāṁkē`) is transliterated as 'kanke', whereas 'चंबा' (`caṁbā`) is transliterated as 'chamba', reflecting different pronunciations of `ṁ` in different contexts.

Most natural transliteration exclusively uses the Basic Latin characters in the English alphabet, resulting in ambiguity where one to one mapping of characters is not possible. For example, the distinction between the native Brahmic letters `t` or `ṭ` are lost as they are both transliterated as 't'.

Natural transliteration can be non-standardized and highly variable. For example when transliterating Brahmic scripts to Latin, the vowel length of the long `ī` in the source script can be represented by 'ii' which repeats the short form, or using an English-like spelling such as 'ee'. The vowel length can also be completely dropped, using the short form 'i'.

In addition, natural transliteration can revert to the spelling of loanwords in the language of origin, even though their nativization is based on the pronunciation rather than the spelling in the original script. For example, the English words 'here' and 'hear' are transliterated as the same Devanagari string `hi.ara` (alternatively `hiyara`). When transliterating these Devanagari strings back to Latin, usually the English spelling of the intended word is used.

Moreover, there can be regional conventions. For example in Bengali or Hindi native words, 'th' almost exclusively represents the aspirated letters `tʰ` or `ṭʰ`, whereas in Malayalam and Tamil it can be used to distinguish letter `t` from letter `ṯ`.

Natural transliteration aims to capture these variances to the extent that they can be predicted by rule based grammars.

### Languages

* bn: Bengali
* gu: Gujarati
* hi: Hindi
* kn: Kannada
* ml: Malayalam
* mr: Marathi
* pa: Punjabi
* sd: Sindhi
* si: Sinhala
* ta: Tamil
* te: Telugu
* ur: Urdu

### Scripts

* arab: Arabic
* beng: Bengali
* deva: Devanagari
* gujr: Gujarati
* guru: Gurmukhi
* iso: Extended ISO 15919
* knda: Kannada
* latn: Latin
* mlym: Malayalam
* orya: Oriya
* sinh: Sinhala
* taml: Tamil
* telu: Telugu

### Phonological transcription

* ipa: [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet) (International phonetic alphabet)

## Grammars

### Deromanization

Deromanization is a special case of transliteration where the source script is Latin.

**Example**

```
atin -> अतिन
```

* Directory: [deromanization](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/deromanization)
* Naming format: `<language>_<target_script>`

For example, `hi_deva` is a deromanization grammar for Hindi where the source script is Latin and the target script is Devanagari, whereas `hi_iso` means the target script is ISO. Deromanization is currently available for Hindi and Tamil to ISO and the native scripts.

English spell-out grammars deromanize Latin strings by spelling out each letter.

**Example**

```
atin -> एटीआईएन (ēṭī.ā.ī.ēna)
```

* Directory: [deromanization](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/deromanization)
* Naming format: `en_spellout_<language>_<target_script>`

For example, `en_spellout_hi_deva` is an English spell-out grammar for Hindi where the source script is Latin and the target script is Devanagari. English spell-out is currently available for Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Oriya, Punjabi, Sindi, Sinhala, Tamil, Telugu, and Urdu.


### G2P

Grapheme to phoneme alignments are used to inform pronunciation-driven transliterations and therefore only aim to cover phonological phenomena to the extent that it is relevant to transliteration rather than offering a high-coverage, high accuracy grapheme to phoneme conversion for each language. The output of g2p modules are also exported as phonological transcription grammars.

**Example**

```
āṭīna -> aːʈiːn̪
```

* Directory: [g2p](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/g2p)
* Naming format: `<language>_<source_script>_<transcription_script>`

For example, `hi_iso_ipa` is a phonological transcription grammar for Hindi where the source script is ISO, and the phonological transcription is in IPA. G2p is currently available from ISO to IPA for Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Punjabi, Tamil, and Telugu.

### Romanization

Romanization is another special case of transliteration where the target script is Latin.

**Example**

```
āṭīna -> ateen
```

Due to the non-standardized nature of romanization in some languages, we provide more than one romanization scheme.

* Directory: [romanization](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/romanization)
* Naming format: `<language>_<source_script>_<romanization_scheme>`

For example, `hi_iso_nat` is the natural romanization grammar for Hindi where the source script is ISO. Romanization is currently available for Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Punjabi, Tamil, and Telugu, from ISO to natural romanization [NAT](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/README.md#nat), and Pan South Asian romanizations [PSAC](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/README.md#psac) and [PSAF](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic/README.md#psaf).

## Resource libraries

* [**brahmic:**](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/brahmic) Libraries for processing South Asian languages that use Brahmic scripts.
* [**language_params:**](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/language_params) Language parameters for compiling grammars using modular FST builders.
* [**phonology:**](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/phonology) Libraries for representing multilingual phonology and common phonological operations.
* [**script:**](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/script) Libraries for representing scripts and building script inventories.
* [**utils:**](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/natural_translit/utils) Libraries for constructing modular, parametrizable FST builders.

## Citing

If you use this software in a publication, please cite the accompanying [paper](http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.718.pdf) from [LREC 2022](https://lrec2022.lrec-conf.org/en/):

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
