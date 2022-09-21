# Natural Transliteration for Brahmic Scripts

This collection of [OpenGrm Pynini](http://www.opengrm.org/twiki/bin/view/GRM/Pynini) grammars takes the [ISO 15919](https://en.wikipedia.org/wiki/ISO_15919) transliteration of a Brahmic script that is normalized and converted by the [Nisaba Brahmic library](https://github.com/google-research/nisaba/tree/main/nisaba/nisaba/scripts/brahmic/README.md), and converts it to a Latin transliteration based on language specific pronunciation. For example, the natural transliteration of the same ISO string `apa` would be `ap` in Hindi, and `aba` in Malayalam.

The natural transliteration grammars use internal notations that only contain extended ASCII characters for ease of input. All substrings are enclosed in type specific, asymmetrical boundary marks. `< >` donates a [grapheme](#typ-representation-and-grapheme-inventory), `{ }` donates a [phoneme](#txn-representation-and-phoneme-inventory), and `“ ”` donates a [transliteration](#transliteration-strings-and-transliteration-inventory) substring.

## typ representation and grapheme_inventory
`typ` is an internal typable representation for ISO characters. `typ` strings are enclosed in less than and greater than signs.

**Examples**

* `ā` -> `<aa>`
* `ṭ` -> `<tt>`
* `nⸯ` -> `<n_chl>`

[`grapheme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/brahmic/natural_translit/grapheme_inventory.py) is a library that contains the `typ`-ISO mapping and forms the `typ` symbols.

## iso2typ grammar

`iso2typ` grammar rewrites an ISO string as a series of `typ` characters.

**Example**

* `āṭānⸯ` -> `<aa><tt><aa><n_chl>`

## txn representation and phoneme_inventory

`txn` is an internal, high coverage, typable representation for multilingual phoneme inventories. `txn` strings are enclosed in curly brackets.

**Examples**

* `aː` -> `{a_l}`
* `ʈ` -> `{tt}`
* `n̪` -> `{ni}`

Nasality and aspiration are featurised for phoneme inventory parsimony, and are represented as `{nsl}` and `{asp}` respectively.

**Examples**

* `õː` -> `{o_l}{nsl}`
* `ᵐb` -> `{nsl}{b}`
* `bʰ` -> `{b}{asp}`

[`phoneme_inventory`](https://github.com/google-research/nisaba/tree/main/nisaba/scripts/brahmic/natural_translit/phoneme_inventory.py) is a library that contains the `txn`-[IPA](https://www.internationalphoneticassociation.org/content/ipa-chart) mapping and forms the `txn` symbols covering the unified South Asian phoneme inventory presented in [Demirsahin et al. (2018)](https://research.google/pubs/pub47341/).

## typ2txn grammar

`typ2txn` grammar assigns a naive orthography to phonology mapping prior to the phonological operations. The format of an assignment is `(<typ_graphemes>={txn_phonemes})`.

**Example**

* `<aa><tt><aa><n_chl>` -> `(<aa>={a_l})(<tt>={tt})(<aa>={a_l})(<n_chl>={ni})`

## Transliteration strings and transliteration_inventory

Transliteration strings are enclosed in double quotation marks. This allows for keeping track of grapheme-transliteration alignments and disambiguates strings like `'ai'` as `'“ai”'` `'“a”“i”'`.

## phon_ops grammar

`phon_ops` grammar applies the phonological operations on the pronunciation side.

**Example**: Malayalam voicing

* `(<aa>={a_l})(<tt>={tt})(<aa>={a_l})(<n_chl>={ni})` -> `(<aa>={a_l})(<tt>={dd})(<aa>={a_l})(<n_chl>={ni})`

## txn2nat grammar

`txn2nat` grammar outputs three different types of pronunciation informed transliteration.

*PSAF*: Fine grained Pan South Asian representation.

**Example**

* `(<aa>={a_l})(<tt>={dd})(<aa>={a_l})(<n_chl>={ni})` ->

 `(<aa>=“aa”)(<tt>=“d”)(<aa>=“aa”)(<n_chl>=“n”)` ->

   `aadaan`

*PSAC*: Coarse grained Pan South Asian representation.

**Example**

* `(<aa>={a_l})(<tt>={dd})(<aa>={a_l})(<n_chl>={ni})` ->

 `(<aa>=“a”)(<tt>=“d”)(<aa>=“a”)(<n_chl>=“n”)` ->

   `aadaan`

*NAT*: Regional natural transliteration.

**Example**

* `(<aa>={a_l})(<tt>={dd})(<aa>={a_l})(<n_chl>={ni})` ->

 `(<aa>=“aa”)(<tt>=“d”)(<aa>=“a”)(<n_chl>=“n”)` ->

   `aadaan`

## e2e grammars

These are end-to-end grammars for individual languages.

**Example**

* `hi_e2e`: End-to-end grammar for Hindi

* `ml_e2e`: End-to-end grammar for Malayalam

End-to-end grammars compose the relevant fsts from grammars and pass arguments to functions where necessary.

**Example**

* `voicing` is a phon_ops function that takes the preceding and following phonological context as arguments. The ml_e2e grammar passes the arguments `ph.VOWEL, ph.NASAL, ph.APPROXIMANT` for the phonological context, so that voicing happens between vowels, nasals, and approximants.

```
_VOICING = ops.voicing(
    p.union(ph.VOWEL, ph.NASAL, ph.APPROXIMANT).optimize(),  # Preceding context
    p.union(ph.VOWEL, ph.NASAL, ph.APPROXIMANT).optimize(),  # Following context
    following_modifier=ph.ASP)  # Modifiers that don't block the operation, such as aspiration.
```

## util library

This library holds most common constants such as SIGMA_STAR and boundary signs for enclosing different types of strings, as well as basic operations for aligning and assigning strings.

## rewrite_functions library

This library contains common rewrite functions shared across grammars, which modify an alignment dependent on the context.

## Citing

If you use this software in a publication, please cite the accompanying
[paper](http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.718.pdf) from
[LREC 2022](https://lrec2022.lrec-conf.org/en/):

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
  url= {http://www.lrec-conf.org/proceedings/lrec2022/pdf/2022.lrec-1.718.pdf},
}
```
