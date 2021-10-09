# Mappings common to scripts

These files contain shared parts of the data files for the scripts under `scripts/brahmic/data/script`. Since these are shared parts, they cannot have
the fields `raw` and `uname_prefix` as they are usually script specific.

1.  `consonant.tsv`: Characters with an inherent schwa. The corresponding Latin
sequence does not have schwa. Example: `KA (क) ⇥ k`
