# Languages

Feature family tree for the supported
[languages](https://github.com/google-research/nisaba/blob/main/nisaba/scripts/natural_translit/phonology/features/README.md#language).

<!-- AUTO-GENERATED INVENTORY STRING STARTS HERE -->

```dot
graph {
ordering="out"
size = 12
rankdir="LR"
ranksep="1, equally"
style="invis"
node [shape="plain"]
language [label="Language"]
dravidian [label="Dravidian"]
language -- dravidian
subgraph {
kn [label="Kannada"]
dravidian -- kn
te [label="Telugu"]
dravidian -- te
tamil_kota [label="Tamil-Kota"]
dravidian -- tamil_kota
subgraph {
ml [label="Malayalam"]
tamil_kota -- ml
ta [label="Tamil"]
tamil_kota -- ta
}
}
indo_european [label="Indo-European"]
language -- indo_european
subgraph {
indo_aryan [label="Indo-Aryan"]
indo_european -- indo_aryan
subgraph {
bn [label="Bengali"]
indo_aryan -- bn
gu [label="Gujarati"]
indo_aryan -- gu
hi [label="Hindi"]
indo_aryan -- hi
mr [label="Marathi"]
indo_aryan -- mr
pa [label="Panjabi"]
indo_aryan -- pa
}
germanic [label="Germanic"]
indo_european -- germanic
subgraph {
en [label="English"]
germanic -- en
}
}
mixed_family [label="Mixed Family Tags"]
language -- mixed_family
subgraph {
mul [label="Multiple Languages"]
mixed_family -- mul
und [label="Undetermined"]
mixed_family -- und
x_uni [label="Unified Phonology"]
mixed_family -- x_uni
x_psa [label="Pan South Asian"]
mixed_family -- x_psa
}
}
```
