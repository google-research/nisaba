# Descriptive features

This inventory defines a set of descriptive phonological features that can be used to build phonological profiles based on where a phonological symbol is located on an [IPA chart](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet_chart).

[TOC]

## How to build a feature profile

The ph_class and airstream aspects show which chart the symbol is located on.

* ph_class = vowel: vowel chart (all vowels are pulmonic.)
* ph_class = consonant:
  * airstream = pulmonic: pulmonic consonant chart.
  * airstream = ejective, implosive: non-pulmonic consonant chart.
  * airstream = click: non-pulmonic consonant chart or a separate click chart.

The supplemental sets in the inventory contain the default values for the rows and columns of the consonant charts that represent more than one aspect, such as articulators and airflow, or have another default value for an aspect such as voicing. Rows that are defined only by the manner aspect are not included in the supplemental sets.

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

## Feature distance

The distance values are roughly based on the distance of the symbols on a chart,
adjusted for the misleading structure of a 2 dimensional chart. For example,
the distance between adjacent place of articulation columns are based on how
far apart the articulators are, as long as the voicing value is the same.
Voicing is an independent feature which would be an additional dimension if the
IPA charts were not restricted to 2 dimensions.

### Distance tables by aspect

| ph_class   |   vowel |   consonant |
|------------|---------|-------------|
| vowel      |       0 |           1 |
| consonant  |       1 |           0 |

| airstream   |   pulmonic |   ejective |   implosive |   click |
|-------------|------------|------------|-------------|---------|
| pulmonic    |          0 |          1 |           1 |       1 |
| ejective    |          1 |          0 |           0 |       1 |
| implosive   |          1 |          0 |           0 |       1 |
| click       |          1 |          1 |           1 |       0 |

| manner       |   stop |   fricative |   sibilant |   strident |   non_sibilant |   approximant |   tap |   flap |   trill |
|--------------|--------|-------------|------------|------------|----------------|---------------|-------|--------|---------|
| stop         |      0 |           1 |       1    |       1    |           1    |             2 |   2   |    2   |     2   |
| fricative    |      1 |           0 |       0    |       0    |           0    |             1 |   1   |    1   |     1   |
| sibilant     |      1 |           0 |       0    |       0.25 |           0.5  |             1 |   1   |    1   |     1   |
| strident     |      1 |           0 |       0.25 |       0    |           0.25 |             1 |   1   |    1   |     1   |
| non_sibilant |      1 |           0 |       0.5  |       0.25 |           0    |             1 |   1   |    1   |     1   |
| approximant  |      2 |           1 |       1    |       1    |           1    |             0 |   1   |    1   |     1   |
| tap          |      2 |           1 |       1    |       1    |           1    |             1 |   0   |    0   |     0.5 |
| flap         |      2 |           1 |       1    |       1    |           1    |             1 |   0   |    0   |     0.5 |
| trill        |      2 |           1 |       1    |       1    |           1    |             1 |   0.5 |    0.5 |     0   |

| place        |   labial |   dental |   alveolar |   postalveolar |   palatal |   velar |   uvular |   epiglottal |   glottal |
|--------------|----------|----------|------------|----------------|-----------|---------|----------|--------------|-----------|
| labial       |      0   |      0.5 |        1   |            1.5 |       2   |     2.5 |      3   |          3.5 |       4   |
| dental       |      0.5 |      0   |        0.5 |            1   |       1.5 |     2   |      2.5 |          3   |       3.5 |
| alveolar     |      1   |      0.5 |        0   |            0.5 |       1   |     1.5 |      2   |          2.5 |       3   |
| postalveolar |      1.5 |      1   |        0.5 |            0   |       0.5 |     1   |      1.5 |          2   |       2.5 |
| palatal      |      2   |      1.5 |        1   |            0.5 |       0   |     0.5 |      1   |          1.5 |       2   |
| velar        |      2.5 |      2   |        1.5 |            1   |       0.5 |     0   |      0.5 |          1   |       1.5 |
| uvular       |      3   |      2.5 |        2   |            1.5 |       1   |     0.5 |      0   |          0.5 |       1   |
| epiglottal   |      3.5 |      3   |        2.5 |            2   |       1.5 |     1   |      0.5 |          0   |       0.5 |
| glottal      |      4   |      3.5 |        3   |            2.5 |       2   |     1.5 |      1   |          0.5 |       0   |

| articulator   |   labial |   apical |   laminal |   dorsal |   laryngeal |
|---------------|----------|----------|-----------|----------|-------------|
| labial        |      0   |      0.5 |       0.5 |      0.5 |         0.5 |
| apical        |      0.5 |      0   |       0.5 |      0.5 |         0.5 |
| laminal       |      0.5 |      0.5 |       0   |      0.5 |         0.5 |
| dorsal        |      0.5 |      0.5 |       0.5 |      0   |         0.5 |
| laryngeal     |      0.5 |      0.5 |       0.5 |      0.5 |         0   |

| height     |   close |   near_close |   close_mid |   mid |   open_mid |   near_open |   open |
|------------|---------|--------------|-------------|-------|------------|-------------|--------|
| close      |     0   |          0.5 |         1   |   1.5 |        2   |         2.5 |    3   |
| near_close |     0.5 |          0   |         0.5 |   1   |        1.5 |         2   |    2.5 |
| close_mid  |     1   |          0.5 |         0   |   0.5 |        1   |         1.5 |    2   |
| mid        |     1.5 |          1   |         0.5 |   0   |        0.5 |         1   |    1.5 |
| open_mid   |     2   |          1.5 |         1   |   0.5 |        0   |         0.5 |    1   |
| near_open  |     2.5 |          2   |         1.5 |   1   |        0.5 |         0   |    0.5 |
| open       |     3   |          2.5 |         2   |   1.5 |        1   |         0.5 |    0   |

| backness   |   front |   near_front |   central |   near_back |   back |
|------------|---------|--------------|-----------|-------------|--------|
| front      |     0   |          0.5 |       1   |         1.5 |    2   |
| near_front |     0.5 |          0   |       0.5 |         1   |    1.5 |
| central    |     1   |          0.5 |       0   |         0.5 |    1   |
| near_back  |     1.5 |          1   |       0.5 |         0   |    0.5 |
| back       |     2   |          1.5 |       1   |         0.5 |    0   |

| breathiness   |   aspirated |   breathy |   murmured |   unaspirated |   none |
|---------------|-------------|-----------|------------|---------------|--------|
| aspirated     |           0 |         0 |          0 |             1 |      1 |
| breathy       |           0 |         0 |          0 |             1 |      1 |
| murmured      |           0 |         0 |          0 |             1 |      1 |
| unaspirated   |           1 |         1 |          1 |             0 |      0 |
| none          |           1 |         1 |          1 |             0 |      0 |

| voicing   |   voiced |   voiceless |
|-----------|----------|-------------|
| voiced    |        0 |           1 |
| voiceless |        1 |           0 |

| labialization   |   labialized |   rounded |   none |   unrounded |
|-----------------|--------------|-----------|--------|-------------|
| labialized      |            0 |         0 |      1 |           1 |
| rounded         |            0 |         0 |      1 |           1 |
| none            |            1 |         1 |      0 |           0 |
| unrounded       |            1 |         1 |      0 |           0 |

| lateralization   |   lateral |   none |
|------------------|-----------|--------|
| lateral          |         0 |      1 |
| none             |         1 |      0 |

| nasalization   |   nasalized |   none |
|----------------|-------------|--------|
| nasalized      |           0 |      1 |
| none           |           1 |      0 |

| palatalization   |   light |   heavy |   none |
|------------------|---------|---------|--------|
| light            |     0   |     0.5 |    1   |
| heavy            |     0.5 |     0   |    0.5 |
| none             |     1   |     0.5 |    0   |

| rhoticization   |   rhotic |   none |
|-----------------|----------|--------|
| rhotic          |        0 |      1 |
| none            |        1 |      0 |

| duration    |   extra_short |   short |   half_long |   long |   extra_long |
|-------------|---------------|---------|-------------|--------|--------------|
| extra_short |           0   |     0.5 |         1   |    1.5 |          2   |
| short       |           0.5 |     0   |         0.5 |    1   |          1.5 |
| half_long   |           1   |     0.5 |         0   |    0.5 |          1   |
| long        |           1.5 |     1   |         0.5 |    0   |          0.5 |
| extra_long  |           2   |     1.5 |         1   |    0.5 |          0   |

| syllabicity   |   syllabic |   none |
|---------------|------------|--------|
| syllabic      |          0 |      1 |
| none          |          1 |      0 |
