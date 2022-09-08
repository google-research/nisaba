# Natural Transliteration for Brahmic Scripts

## typ representation and iso2typ grammar
`typ` is an internal, typable representation for ISO characters.

**Examples**

* `ā` -> `aa`
* `ṭ` -> `tt`
* `nⸯ` -> `n_chl`

See [ISO to typ table](#iso-to-typ-mapping) for current symbol coverage.

`iso2typ` grammar rewrites an ISO strings as a series of typ characters.

**Example**

* `āṭānⸯ` -> `(aa)(tt)(aa)(n_chl)`

## txn representation and typ2txn grammar

`txn` is an internal, high coverage, typable representation for multilingual
phoneme inventories.

**Examples**

* `aː` -> `a_l`
* `ʈ` -> `tt`
* `n̪` -> `ni`

Nasality and aspiration are featurised for phoneme inventory parsimony, and are represented as `nsl` and `asp` respectively.

**Examples**

* `õː` -> `o_l,nsl`
* `ᵐb` -> `nsl,b`
* `bʰ` -> `b,asp`

See [IPA to txn table](#ipa-to-txn-mapping) for symbols covering the unified South Asian phoneme inventory presented in [Demirsahin et al. (2018)](https://research.google/pubs/pub47341/).

`typ2txn` grammar assigns a naive ortography to phonology mapping. The format is `(<typ_graphemes>=<txn_phonemes>)`.

**Example**

* `(aa)(tt)(aa)(n_chl)` -> `(aa=a_l)(tt=tt)(aa=a_l)(n_chl=ni)`

## phon_ops grammar

`phon_ops` grammar applies the phonological operations on the pronunciation side.

**Example**: Malayalam voicing

* `(aa=a_l)(tt=tt)(aa=a_l)(n_chl=ni)` -> `(aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni)`

## txn2nat grammar

`txn2nat` grammar outputs three different types of pronunciation informed transliteration.

*PSAF*: Fine grained Pan South Asian representation.

**Example**

* `(aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni)` -> `aadaan`

*PSAC*: Coarse grained Pan South Asian representation.

**Example**

* `(aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni)` -> `adan`

*NAT*: Regional natural transliteration.

**Example**

* `(aa=a_l)(tt=dd)(aa=a_l)(n_chl=ni)` -> `aadan`

## Tables

### ISO to typ mapping

ISO | typ
------ | ------
`’` | `avg`
`+` | `zwj`
`\|` | `zwn`
`ˑ` | `nkt`
`a` | `a`
`ā` | `aa`
`æ` | `ac`
`ai` | `ai`
`au` | `au`
`b` | `b`
`bʰ` | `bh`
`c` | `c`
`cʰ` | `ch`
`d` | `d`
`ḍ` | `dd`
`dʰ` | `dh`
`ḍʰ` | `ddh`
`e` | `e`
`ê` | `ec`
`ē` | `ee`
`f` | `f`
`g` | `g`
`ġ` | `gg`
`gʰ` | `gh`
`h` | `h`
`ḥ` | `vis`
`ḫ` | `upadh`
`ẖ` | `jihva`
`i` | `i`
`ī` | `ii`
`j` | `j`
`jʰ` | `jh`
`k` | `k`
`kʰ` | `kh`
`kⸯ` | `k_chl`
`l` | `l`
`ḷ` | `ll`
`l̥` | `l_vocal`
`l̥̄` | `ll_vocal`
`ḻ` | `lr`
`lⸯ` | `l_chl`
`ḷⸯ` | `ll_chl`
`m` | `m`
`ṁ` | `ans`
`m̐` | `cnd`
`n` | `n`
`ñ` | `ny`
`ṅ` | `ng`
`ṇ` | `nn`
`ṉ` | `na`
`nⸯ` | `n_chl`
`ṇⸯ` | `nn_chl`
`o` | `o`
`ô` | `oc`
`ō` | `oo`
`õm` | `om`
`p` | `p`
`pʰ` | `ph`
`q` | `q`
`r` | `r`
`r̆` | `reye`
`ṛ` | `rd`
`r̥` | `r_vocal`
`r̥̄` | `rr_vocal`
`ṟ` | `rr`
`ṛʰ` | `rdh`
`rⸯ` | `reph`
`ṟⸯ` | `rr_chl`
`s` | `s`
`ś` | `sh`
`ṣ` | `ss`
`t` | `t`
`ṭ` | `tt`
`ṯ` | `ta`
`tʰ` | `th`
`ṭʰ` | `tth`
`u` | `u`
`ū` | `uu`
`v` | `v`
`x` | `x`
`y` | `y`
`ẏ` | `yy`
`z` | `z`

### IPA to txn mapping

IPA | txn
------ | ------
`~ ` | ` nsl`
`ʰ ` | ` asp`
`a ` | ` a`
`aː ` | ` a_l`
`æ ` | ` ae`
`æː ` | ` ae_l`
`e ` | ` e`
`e̯ ` | ` e_g`
`eː ` | ` e_l`
`ə ` | ` @`
`əː ` | ` @_l`
`ɛ ` | ` eh`
`ɛː ` | ` eh_l`
`i ` | ` i`
`i̯ ` | ` i_g`
`iː ` | ` i_l`
`o ` | ` o`
`o̯ ` | ` o_g`
`oː ` | ` o_l`
`ɔ ` | ` oh`
`ɔː ` | ` oh_l`
`u ` | ` u`
`u̯ ` | ` u_g`
`uː ` | ` u_l`
`b ` | ` b`
`d ` | ` d`
`d̪ ` | ` di`
`dz ` | ` dz`
`dʒ ` | ` jh`
`ɖ ` | ` dd`
`f ` | ` f`
`ɡ ` | ` g`
`ɣ ` | ` xa`
`h ` | ` h`
`j ` | ` y`
`k ` | ` k`
`l ` | ` l`
`ɭ ` | ` ll`
`m ` | ` m`
`n ` | ` n`
`n̪ ` | ` ni`
`ɲ ` | ` ny`
`ɳ ` | ` nn`
`ŋ ` | ` ng`
`p ` | ` p`
`q ` | ` q`
`r ` | ` r`
`ɻ ` | ` rru`
`ɽ ` | ` rr`
`ɾ ` | ` rt`
`s ` | ` s`
`ʂ ` | ` ss`
`ʃ ` | ` sh`
`t ` | ` t`
`t̪ ` | ` ti`
`ts ` | ` ts`
`tʃ ` | ` ch`
`ʈ ` | ` tt`
`ʋ ` | ` vu`
`x ` | ` x`
`z ` | ` z`
`ʒ ` | ` zh`

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
