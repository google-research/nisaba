This directory contains the unidirectional romanization mappings for Manipuri
written in Bengali script. The romanizer is unidirectional because it performs a
many-to-one mapping.

The romanized output has to match the inverse of the native Meetei Mayek
romanizer in Nisaba so that both FSTs compose to form Bengali to Meetei Mayek
transliterator.

Note, the mappings in this directory are *not* compiled into the main Nisaba
transducers, they are designed to be used by custom transducer pipeline
implementing Bengali to Meetei Mayek transliteration.

This implementation is based on the following sources:

1.  Kishorjit NongmeikapamNingombam Herojit SinghSonia ThoudamSivaji
    Bandyopadhyay (2011): "Manipuri Transliteration from Bengali Script to
    Meitei Mayek: A Rule Based Approach", *Proceedings of International
    Conference on Information Systems for Indian Languages (ICISIL)*, pp.
    195-198,
    [DOI: 10.1007/978-3-642-19403-0_31](https://link.springer.com/chapter/10.1007/978-3-642-19403-0_31).
1.  Thoudam Doren Singh (2012): ["Bidirectional Bengali Script and Meetei Mayek
    Transliteration of Web Based Manipuri News
    Corpus"](https://aclanthology.org/W12-5016), *Proceedings of the 3rd
    Workshop on South and Southeast Asian Natural Language Processing*, pp.
    181–190.
1.  K. Kabi Khanganba, Girish Nath Jha (2014): ["Challenges in Indian Language
    Transliteration: a case of Devanagari, Bangla and
    Manipuri"](http://www.lrec-conf.org/proceedings/lrec2014/workshops/LREC2014Workshop-WILDRE%20Proceedings.pdf),
    *Proceedings of WILDRE2 - 2nd Workshop on Indian Language Data: Resources
    and Evaluation*, pp. 77-83.
1.  Leihaorambam Sarbajit Singh, Kabita Thaoroijam, Pradip Kumar Das (2007):
    ["Bengali Script and Meiteiron Spelling"](http://www.languageinindia.com/june2007/meiteiphoneme.pdf)
