# Copyright 2024 Nisaba Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Creates FST from unweighted rules with same sigma on lhs and rhs.

Two different relationships between the rules are supported:

1. Ordered partition of unordered set of rules

This behaves as if there is no a priori order between the rules. In the
implementation, the rules are partitioned and ordered into multiple rule-sets
s.t. the following substring relationship is obeyed. The ordering of the
rule-sets are in phonological bleeding order. FSTs from each of these rule-sets
are CDRewritten and then are composed together in order.

1.1 LHS of a rule is substring of LHS of another, as in this example:
    (1) xAy -> C
    (2) A -> B
    As A is a substring of xAy, (1) should be in a rule set strictly before
    the one containing (2).

TODO: Consider additional substring relationships like:
1.2 RHS of a rule is substring of LHS of another, as in this example:
    (1) A -> B
    (2) xBy -> C
    As B is a substring of xBy, (1) should be applied strictly before (2).

1.3 (1) A -> xy
    (2) yz -> B
    As the suffix of the RHS of (1) becomes the prefix of LHS of (2),
    (1) should be applied strictly before (2).

1.4 (1) A -> yz
    (2) xy -> B
    As the prefix of the RHS of (1) becomes the suffix of LHS of (2),
    (1) should be applied strictly before (2).

Adding these relationships are prevented by the pynini timeout issue stemming
from the use of string_map(). Adding these rules can potentially increase the
number of rule-sets and that in turn could have impact the FAR file sizes.
So the FAR file size increases need to be monitored with these updates.

2. Cascading rules

Each rule is applied on the entire text individually one after another.
Obviously the textual order of the rules is important, as these are phonological
rules in feeding order. This is implemented as a sequential composition of
CDRewrites of the FSTs from each rule.
"""

import itertools as it
import os
from typing import Iterable, Iterator, List, NamedTuple

import networkx as nx
import pandas as pd

import pynini
import pathlib
import nisaba.scripts.utils.file as uf
import nisaba.scripts.utils.rewrite as ur

Rule = NamedTuple('Rule', [('lhs', str), ('rhs', str)])
RuleSet = Iterable[Rule]
RuleSets = List[RuleSet]


def rules_from_string_file(file: os.PathLike) -> Iterator[Rule]:
  """Yields string rules from a text resource with unweighted string maps."""
  return rules_from_string_path(uf.AsResourcePath(file))


def rules_from_string_path(file: os.PathLike) -> Iterator[Rule]:
  """Yields string rules from a text file with unweighted string maps."""
  with pathlib.Path(file).open('rt') as f:
    df = pd.read_csv(f, sep='\t', comment='#', escapechar='\\',
                     names=['lhs', 'rhs'], na_filter=False)
    for row in df.itertuples(index=False, name='Rule'):
      if not row.lhs:
        raise ValueError('Rule expects an LHS: {}'.format(row))
      yield row


def _match_lhs_in_lhs(rule_a: Rule, rule_b: Rule) -> bool:
  return rule_a.lhs in rule_b.lhs


def partition_unordered(rules: RuleSet) -> List[RuleSet]:
  """Ordered partition of unordered rules s.t. no substring relation in a set.

  Algorithm: Consider the digraph of rules s.t. two rules have a directed edge
  iff there is a substring relation as defined above. Set of all leafs are
  removed from this digraph and set aside as the first set of the desired
  ordered partition of rules. This removal process is repeated until there are
  no rule-nodes remaining in the graph. These rule sets in the order of their
  creation form the desired ordered partition of rules.

  Args:
    rules: String rules representing a set of rewrites.

  Returns:
    The partition of rules.
  """

  g = nx.DiGraph()
  g.add_nodes_from(rules)
  g.add_edges_from((p1, p2) for p1, p2 in it.product(rules, rules)
                   if p1 != p2 and _match_lhs_in_lhs(p1, p2))
  partition = []
  while g.number_of_nodes() > 0:
    leaves = [node for node in g.nodes if g.out_degree(node) == 0]
    if not leaves:
      raise ValueError('Digraph should be acyclic')
    partition += [leaves]
    g.remove_nodes_from(leaves)
  return partition


def fst_from_rules(rules: RuleSet, sigma: pynini.Fst) -> pynini.Fst:
  """Gets rewrite FST from given rule set representing rewrites.

  Args:
    rules: String rules representing a set of rewrites.
    sigma: Fst to consider the complete alphabet for CDRewrites.

  Returns:
    The Rewrite FST for the specified rule file.
  """

  fsts = [pynini.optimize(pynini.string_map(rule_set))
          for rule_set in partition_unordered(rules)]
  return ur.RewriteAndComposeFsts(fsts, sigma)


def fst_from_rule_file(rule_file: os.PathLike, sigma: pynini.Fst) -> pynini.Fst:
  """Gets rewrite FST from a given rewrite rule file.

  Args:
    rule_file: Path relative to depot for a rule file specifying rewrite rules.
    sigma: Fst to consider the complete alphabet for CDRewrites.

  Returns:
    The Rewrite FST for the specified rule file. If the rule file is missing
    then an FST accepting everything is returned.
  """
  return fst_from_rules(list(rules_from_string_file(rule_file)), sigma)


def _fst_from_cascading_rules(rules: RuleSet, sigma: pynini.Fst) -> pynini.Fst:
  """Gets rewrite FST from given rule set representing rewrites.

  Args:
    rules: String rules representing a set of rewrites.
    sigma: Fst to consider the complete alphabet for CDRewrites.

  Returns:
    The Rewrite FST for the specified rule file.
  """

  fsts = (pynini.cross(rule.lhs, rule.rhs) for rule in rules)
  return ur.RewriteAndComposeFsts(fsts, sigma)


def fst_from_cascading_rule_file(rule_file: os.PathLike,
                                 sigma: pynini.Fst) -> pynini.Fst:
  """Gets rewrite FST from a given rewrite rule file.

  Args:
    rule_file: Path relative to depot for a rule file specifying rewrite rules.
    sigma: Fst to consider the complete alphabet for CDRewrites.

  Returns:
    The Rewrite FST for the specified rule file. If the rule file is missing
    then an exception is thrown.
  """
  return _fst_from_cascading_rules(rules_from_string_file(rule_file), sigma)
