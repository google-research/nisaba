# Phonological features

[TOC]

## Descriptive features

This inventory defines a set of descriptive phonological features that can be
used to build phonological profiles based on where a phonological symbol is
located on an[IPA chart](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart).

### How to build a feature profile

The ph_class and airstream aspects show which chart the symbol is located on.

* ph_class = vowel: vowel chart (all vowels are pulmonic.)
* ph_class = consonant:
  * airstream = pulmonic: pulmonic consonant chart.
  * airstream = ejective, implosive: non-pulmonic consonant chart.
  * airstream = click: non-pulmonic consonant chart or a separate click chart.

The supplemental sets in the inventory contain the default values for the rows
and columns of the consonant charts that represent more than one aspect, such as
articulators and airflow, or have another default value for an aspect such as
voicing. Rows that are defined only by the manner aspect are not included in the
supplemental sets.

**Supplemental sets:**

* Rows (manner):
  * nasal
  * approximant
  * lateral fricative
  * lateral approximant
* Columns (place of articulation):
  * bilabial
  * labiodental
  * dental
  * alveolar,
  * para_alveolar (merged cells for dental, alveolar, and postalveolar),
  * postalveolar
  * retroflex
  * palatal
  * velar
  * uvular
  * epiglottal
  * glottal

Updating a profile by the row and the column of the symbol will yield the
feature profile of the default IPA symbol. Further features can be added to
represent diacritics.

**Examples**:

* consonant profile + nasal row + bilabial = /m/
* consonant profile + nasal row + velar = /ŋ/
* /ŋ/ profile + voiceless = /ŋ̊/
* vowel profile + open + front + unrounded = /a/
* /a/ profile + nasalized = /ã/

Co-articulations, including affricates, are not present as rows. They will
be represented as a sequence of their components.

### Feature distance

The distance values are roughly based on the distance of the symbols on a chart,
adjusted for the misleading structure of a 2 dimensional chart. For example,
the distance between adjacent place of articulation columns are based on how
far apart the articulators are, as long as the voicing value is the same.
Voicing is an independent feature which would be an additional dimension if the
IPA charts were not restricted to 2 dimensions.

[Distance tables by aspect](https://github.com/google-research/nisaba/blob/main/nisaba/scripts/natural_translit/phonology/features/docs/descriptive.md)
