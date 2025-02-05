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

"""Lattice class for building aligner FSTs."""

import pynini as pyn
from nisaba.scripts.natural_translit.utils import log_op as log
from nisaba.scripts.natural_translit.utils import type_op as ty


class Node(ty.Thing):
  """A node in a Lattice that holds an FST state.

  Attributes:
    x: The x-coordinate of the node on a Lattice
    y: The y-coordinate of the node on a Lattice.
    fst: The FST that the state of the node belongs to.
    state: The label of the  FST state this node holds as int, or ty.UNASSIGNED.

  The default coordinates of a Node that is not initiated by a lattice, such as
    a free-standing Node that holds the error state of an FST, are (-1, -1).

  Multiple nodes can be assigned the same state, so that the same state can be
    accessed by different coordinates on intersecting lattices.
  """

  def __init__(
      self,
      alias: str,
      text: str = '',
      x: int = -1,
      y: int = -1,
      fst: pyn.Fst = pyn.Fst(),
  ):
    super().__init__(alias, text)
    self.x = x
    self.y = y
    self.fst = fst
    self.state = ty.UNASSIGNED

  def __str__(self):
    return self.text

  def has_state(self) -> bool:
    return isinstance(self.state, int)

  def state_str(self) -> str:
    if self.has_state():
      return str(self.state)
    else:
      return '∅'


class Lattice(ty.Thing):
  """A 2 dimensional lattice for accessing FST states by x and y coordinates.

  Attributes:
    fst: The FST associated with the lattice.
    width: The width of the lattice.
    height: The height of the lattice.
    nodes: A list of lists of nodes.
    error: The node that will hold the error state of the FST.
  """

  def __init__(
      self,
      alias: str,
      width: int,
      height: int,
      fst: pyn.Fst = pyn.Fst(),
      error: Node = Node('error'),
      populate: bool = False,
  ):
    super().__init__(alias)
    self.text = alias
    self.fst = fst
    self.width = width
    self.height = height
    self._nodes = [
        [self._new_node(x, y) for x in range(self.width)]
        for y in range(self.height)
    ]
    self.error = error
    if error.fst is not self.fst:
      error.fst = self.fst
    if not self.error.has_state():
      self.error.state = self.fst.add_state()
    if populate:
      for row in self._nodes:
        for node in row:
          node.state = self.fst.add_state()

  def __str__(self):
    return self.text

  def _str_nodes(self, state_str: bool) -> str:
    """Returns a string representation of either the nodes or the states.

    Args:
      state_str: If True, nodes are represented as the int value in the FST they
      belong to. If the node has no state ID, it's represented as ∅. If False,
      nodes are represented as the alias of the lattice they belong to and their
      coordinates on the lattice.

    Returns:
      A string representation of the nodes in the lattice.
    """
    return '\n'.join(
        '\t'.join(
            node.state_str() if state_str else node.text for node in row
        )
        for row in self._nodes
    )

  def nodes_str(self) -> str:
    return (
        f'Lattice: {self.alias}\nNodes:\n{self._str_nodes(state_str=False)}\n'
    )

  def states_str(self) -> str:
    return (
        f'Lattice: {self.alias}\nStates:\n{self._str_nodes(state_str=True)}\n'
    )

  def _new_node(self, x: int, y: int, populate: bool = False) -> Node:
    """Makes a new node at the given coordinates."""
    alias = '%s_node_%d_%d' % (self.alias, x, y)
    text = '%s(%d,%d)' % (self.text, x, y)
    node = Node(alias, text, x, y, self.fst)
    if populate:
      node.state = self.fst.add_state()
    return node

  def node(self, x: int, y: int) -> Node:
    """Returns the Node at (x, y).

    If x or y are out of bounds, returns the error node.

    Args:
      x: The x-coordinate of the node.
      y: The y-coordinate of the node.

    Returns:
      Node.
    """
    if x in range(self.width) and y in range(self.height):
      return self._nodes[y][x]
    return self.error

  def state(self, x: int, y: int) -> int:
    """Returns the state of the Node at (x, y).

    If the Node has no state, adds a state to the FST and assigns it to the
    node. If x or y are out of bounds, returns the state of the error node.

    Args:
      x: The x-coordinate of the node.
      y: The y-coordinate of the node.

    Returns:
      The label of the state of the node at (x, y) as int.
    """
    node = self.node(x, y)
    if not node.has_state():
      node.state = self.fst.add_state()
    if isinstance(node.state, int):
      return log.dbg_return(node.state)
    else:
      return log.dbg_return(hash(node), 'unassigned state')

  def state_of(self, node: Node) -> int:
    """Returns the state of a Node. Adds a new state if needed."""
    return self.state(node.x, node.y)
