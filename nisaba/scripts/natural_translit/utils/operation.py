# Copyright 2025 Nisaba Authors.
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

"""Operations."""

from __future__ import annotations

import enum

from nisaba.scripts.natural_translit.utils import inventory
from nisaba.scripts.natural_translit.utils import type_op as ty


class Operation(ty.Thing):
  """An operation that defines the relation between the sides of an alignment.

  Attributes:

  alias: The string that will be used to refer to the operation in an inventory.
    Eg. the voicing operation in a phonological operation inventory can be
    referred to as `phonological.voicing`.
  inventory: The inventory where the operation is first defined.
  index: The index of the operation in the inventory.
  base_cost: The cost of the base operation that will be used to calculate the
    applied cost of an alignment. Higher base cost means the operation will be
    penalised more while calculating an edit distance or a similarity score,
    and the arc weight of the operation will be higher in an FST.
  match: The operation that the partial and unexpected operations will be
    derived from. The default value is the operation itself.
  partial: A partial application of the operation.
  unexpected: An unexpected application of the operation.

  An operation is defined in an inventory, and the corresponding partial
  and unexpected operations will be automatically assigned when the inventory is
  built.

  Example:

  voicing.match: voicing
  voicing.partial: partial_voicing, for when the operation is applied in an
    alignment where at least one side is longer than a single symbol.
  voicing.unexpected: unexpected_voicing, for when the preceding or the
    following context doesn't match the expected context.

  partial_voicing.match: voicing
  partial_voicing.partial: partial_voicing
  partial_voicing.unexpected: unexpected_partial_voicing

  unexpected_voicing.match: voicing
  unexpected_voicing.partial: partial_voicing
  unexpected_voicing.unexpected: unexpected_partial_voicing

  unexpected_partial_voicing.match: voicing
  unexpected_partial_voicing.partial: partial_voicing
  unexpected_partial_voicing.unexpected: unexpected_partial_voicing

  While constructing an FST using a phonological rule
  alignment = Alignment(
      alias='t_voicing',
      left='t',
      right='d',
      preceding=vowel,
      following=vowel,
      operation=voicing
  )
  The operation of a t:d alignment in a substring when the context isn't a
  vowel can be be set with `alignment.operation.partial.unexpected` and the
  source for the partial or unexpected alignment in an aligner output can be
  traced back with `alignment.operation.match`.
  """

  # Tentative penalty for unexpected operations.
  UNEXPECTED_PENALTY = 0.75

  class ReservedIndex(enum.IntEnum):
    """Reserved indices for operation inventories."""

    COMMON = 100
    PHONOLOGICAL = 200
    BRAHMIC = 300

  def __init__(self, alias: str, cost: float):
    super().__init__(alias)
    self.text = alias
    self.inventory = inventory.Inventory.EMPTY
    self.index = 0
    self.base_cost = cost
    self.match = self
    self.partial = self
    self.unexpected = self

  def __str__(self):
    return f'{self.text} ({self.base_cost:.3f})'

  def is_assigned(self) -> bool:
    return not (
        self is Operation.COMMON.unassigned or self is Operation.COMMON.error
    )

  def is_free(self) -> bool:
    return self.base_cost == 0

  def is_cheaper_than(self, operation: Operation) -> bool:
    return self.base_cost < operation.base_cost

  class Inventory(inventory.Inventory):
    """An inventory of operations.

    Attributes:
      prefix: An Operation.ReservedIndex which will be used as the prefix for
        the indices of the operations first defined in this inventory.
      _index_dict: A dictionary of [int, Operation] used for retrieving
        operations in an aligner output.
    """

    def __init__(self, alias: str, *operations: Operation):
      super().__init__(alias, Operation)
      self.prefix = 0
      self._index_dict = {}
      self.add_operations(*operations)

    def index_lookup(self, index: int) -> Operation:
      return self._index_dict.get(index, Operation.COMMON.error)

    def _next_index(self) -> int:
      """Returns the next index for a new Operation.

      Currently the operation of an alignment in an aligner output is retrieved
      from the decimal of the arc weight. In order to make it easier to get the
      correct index, indices that end in 0 are skipped. Eg. If indices that end
      in 0 are allowed in an inventory with prefix 200, the 10th Operation will
      show up as .21 and will have to be reconstructed to 210. It's easier to
      avoid this condition in the first place.
      """
      if not self:
        return self.prefix + 1
      if len(self) == 1:
        return self.prefix + 2
      index = max(self._index_dict.keys()) + 1
      return index if index % 10 else index + 1

    def _make_operation(self, alias: str, cost: float) -> Operation:
      operation = Operation(alias, cost)
      operation.inventory = self
      operation.index = self._next_index()
      if self.add_item(operation):
        self._index_dict[operation.index] = operation
      return operation

    @classmethod
    def from_args(
        cls,
        alias: str,
        prefix: Operation.ReservedIndex,
        *args: tuple[str, float],
    ) -> Operation.Inventory:
      op_inventory = cls(alias)
      op_inventory.prefix = prefix
      for alias, cost in args:
        match = op_inventory._make_operation(alias, cost)
        # Base cost of a partial operation is the same as the match operation.
        # The arc weight is calculated based on the length of the substring.
        partial = op_inventory._make_operation('partial_' + alias, cost)
        # TODO: Dynamically adjust the arc weight of unexpected
        # applications based on context match scores instead of using a
        # constant.
        unexpected = op_inventory._make_operation(
            'unexpected_' + alias, cost + Operation.UNEXPECTED_PENALTY
        )
        unexpected_partial = op_inventory._make_operation(
            'unexpected_partial_' + alias,
            cost + Operation.UNEXPECTED_PENALTY,
        )
        match.partial = partial
        match.unexpected = unexpected
        partial.match = match
        partial.unexpected = unexpected_partial
        unexpected.match = match
        unexpected.partial = unexpected_partial
        unexpected_partial.match = match
      return op_inventory

    def add_operations(self, *operations: Operation) -> None:
      for operation in operations:
        self.add_item(operation)

    def __str__(self):
      return (
          '\n'.join([
              str(operation)
              for operation in self
              if operation.match == operation
          ])
          + '\n'
      )


# Current base costs in the common operation inventory are rough estimations and
# will be updated as necessary.
Operation.COMMON = Operation.Inventory.from_args(
    'common_operations',
    Operation.ReservedIndex.COMMON,
    ('alignable', 0),
    ('boundary', 0.125),
    ('deletion', 1),
    ('error', 100),
    ('identity', 0.1),
    ('insertion', 1),
    ('interchangeable', 0.1),
    ('punctuation', 0.25),
    ('substitution', 1.25),
    ('unassigned', 10),
)
