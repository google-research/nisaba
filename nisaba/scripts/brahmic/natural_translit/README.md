# Natural transliteration for Nisaba

## typ representation and iso2typ grammar
`typ` is an internal, typable representation for ISO characters.
<!-- TODO: add full ISO to typ table -->

**Examples**

* ā -> aa
* ṭ -> tt
* nⸯ -> n_chl

`iso2typ` grammar rewrites an ISO strings as a series of typ characters.

**Example**

* āṭānⸯ -> (aa)(tt)(aa)(n_chl)

## txn representation and typ2txn grammar

`txn` is an internal, high coverage, typable representation for multilingual
phoneme inventories.

**Examples**

* aː -> a_l
* ʈ -> tt
* n̪ -> ni

`typ2txn` grammar assigns a naive ortography to phonology mapping. The format is `(<typ_graphemes>=<txn_phonemes>)`.

**Example**

* (aa)(tt)(aa)(n_chl) -> (aa=a_l)(tt=tt)(aa=a_l)(n_chl=ni)

## phon_ops grammar

`phon_ops` grammar applies the phonological operations on the pronunciation side.

**Example**: Malayalam voicing

* (aa=a_l)(tt=tt)(aa=a_l)(n_chl=ni) -> (aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni)

## txn2nat grammar

`txn2nat` grammar outputs three different types of pronunciation informed transliteration.

*PSAF*: Fine grained Pan South Asian representation.

**Example**

* (aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni) -> aadaan

*PSAC*: Coarse grained Pan South Asian representation.

**Example**

* (aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni) -> adan

*NAT*: Regional natural transliteration.

**Example**

* (aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni) -> aadan
