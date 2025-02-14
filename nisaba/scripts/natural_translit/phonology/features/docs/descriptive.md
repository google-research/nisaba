# Descriptive features distance tables

Distance tables for [descriptive phonological features](https://github.com/google-research/nisaba/blob/main/nisaba/scripts/natural_translit/phonology/features/README.md#descriptive-features).

[TOC]

<!-- AUTO-GENERATED INVENTORY STRING STARTS HERE -->

## Inventory: descriptive

### aspect: ph_class
max_dist: 1.00

| distances   |   vowel |   consonant |
|-------------|---------|-------------|
| vowel       |       0 |           1 |
| consonant   |       1 |           0 |

### aspect: airstream
max_dist: 1.00

| distances   |   pulmonic |   ejective |   implosive |   click |
|-------------|------------|------------|-------------|---------|
| pulmonic    |          0 |          1 |           1 |       1 |
| ejective    |          1 |          0 |           0 |       1 |
| implosive   |          1 |          0 |           0 |       1 |
| click       |          1 |          1 |           1 |       0 |

### aspect: manner
max_dist: 2.00

| distances    |   stop |   fricative |   sibilant |   strident |   non_sibilant |   approximant |   tap |   flap |   trill |
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

### aspect: place
max_dist: 4.00

| distances    |   labial |   dental |   alveolar |   postalveolar |   palatal |   velar |   uvular |   epiglottal |   glottal |
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

### aspect: articulator
max_dist: 0.50

| distances   |   labial |   apical |   laminal |   dorsal |   laryngeal |
|-------------|----------|----------|-----------|----------|-------------|
| labial      |      0   |      0.5 |       0.5 |      0.5 |         0.5 |
| apical      |      0.5 |      0   |       0.5 |      0.5 |         0.5 |
| laminal     |      0.5 |      0.5 |       0   |      0.5 |         0.5 |
| dorsal      |      0.5 |      0.5 |       0.5 |      0   |         0.5 |
| laryngeal   |      0.5 |      0.5 |       0.5 |      0.5 |         0   |

### aspect: height
max_dist: 3.00

| distances   |   close |   near_close |   close_mid |   mid |   open_mid |   near_open |   open |
|-------------|---------|--------------|-------------|-------|------------|-------------|--------|
| close       |     0   |          0.5 |         1   |   1.5 |        2   |         2.5 |    3   |
| near_close  |     0.5 |          0   |         0.5 |   1   |        1.5 |         2   |    2.5 |
| close_mid   |     1   |          0.5 |         0   |   0.5 |        1   |         1.5 |    2   |
| mid         |     1.5 |          1   |         0.5 |   0   |        0.5 |         1   |    1.5 |
| open_mid    |     2   |          1.5 |         1   |   0.5 |        0   |         0.5 |    1   |
| near_open   |     2.5 |          2   |         1.5 |   1   |        0.5 |         0   |    0.5 |
| open        |     3   |          2.5 |         2   |   1.5 |        1   |         0.5 |    0   |

### aspect: backness
max_dist: 2.00

| distances   |   front |   near_front |   central |   near_back |   back |
|-------------|---------|--------------|-----------|-------------|--------|
| front       |     0   |          0.5 |       1   |         1.5 |    2   |
| near_front  |     0.5 |          0   |       0.5 |         1   |    1.5 |
| central     |     1   |          0.5 |       0   |         0.5 |    1   |
| near_back   |     1.5 |          1   |       0.5 |         0   |    0.5 |
| back        |     2   |          1.5 |       1   |         0.5 |    0   |

### aspect: breathiness
max_dist: 1.00

| distances   |   aspirated |   breathy |   murmured |   unaspirated |   none |
|-------------|-------------|-----------|------------|---------------|--------|
| aspirated   |           0 |         0 |          0 |             1 |      1 |
| breathy     |           0 |         0 |          0 |             1 |      1 |
| murmured    |           0 |         0 |          0 |             1 |      1 |
| unaspirated |           1 |         1 |          1 |             0 |      0 |
| none        |           1 |         1 |          1 |             0 |      0 |

### aspect: voicing
max_dist: 1.00

| distances   |   voiced |   voiceless |
|-------------|----------|-------------|
| voiced      |        0 |           1 |
| voiceless   |        1 |           0 |

### aspect: labialization
max_dist: 1.00

| distances   |   labialized |   rounded |   none |   unrounded |
|-------------|--------------|-----------|--------|-------------|
| labialized  |            0 |         0 |      1 |           1 |
| rounded     |            0 |         0 |      1 |           1 |
| none        |            1 |         1 |      0 |           0 |
| unrounded   |            1 |         1 |      0 |           0 |

### aspect: lateralization
max_dist: 1.00

| distances   |   lateral |   none |
|-------------|-----------|--------|
| lateral     |         0 |      1 |
| none        |         1 |      0 |

### aspect: nasalization
max_dist: 1.00

| distances   |   nasalized |   none |
|-------------|-------------|--------|
| nasalized   |           0 |      1 |
| none        |           1 |      0 |

### aspect: palatalization
max_dist: 1.00

| distances   |   light |   heavy |   none |
|-------------|---------|---------|--------|
| light       |     0   |     0.5 |    1   |
| heavy       |     0.5 |     0   |    0.5 |
| none        |     1   |     0.5 |    0   |

### aspect: rhoticization
max_dist: 1.00

| distances   |   rhotic |   none |
|-------------|----------|--------|
| rhotic      |        0 |      1 |
| none        |        1 |      0 |

### aspect: duration
max_dist: 2.00

| distances   |   extra_short |   short |   half_long |   long |   extra_long |
|-------------|---------------|---------|-------------|--------|--------------|
| extra_short |           0   |     0.5 |         1   |    1.5 |          2   |
| short       |           0.5 |     0   |         0.5 |    1   |          1.5 |
| half_long   |           1   |     0.5 |         0   |    0.5 |          1   |
| long        |           1.5 |     1   |         0.5 |    0   |          0.5 |
| extra_long  |           2   |     1.5 |         1   |    0.5 |          0   |

### aspect: syllabicity
max_dist: 1.00

| distances   |   syllabic |   none |
|-------------|------------|--------|
| syllabic    |          0 |      1 |
| none        |          1 |      0 |
