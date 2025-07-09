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

from absl.testing import absltest
from nisaba.scripts.natural_translit.utils import lattice as lt


class LatticeTest(absltest.TestCase):

  def test_node(self):
    node = lt.Node('test', 'test_node', 1, 2)
    self.assertEqual(node.alias, 'test')
    self.assertEqual(str(node), 'test_node')
    self.assertEqual(node.x, 1)
    self.assertEqual(node.y, 2)
    self.assertFalse(node.has_state())
    self.assertEqual(node.state_str(), '∅')

  def test_lattice(self):
    lattice = lt.Lattice('test', 6, 4)
    self.assertEqual(lattice.alias, 'test')
    self.assertIs(lattice.fst, lattice.error.fst)
    self.assertEqual(
        lattice.nodes_str(),
        'Lattice: test\n'
        'Nodes:\n'
        'test(0,0)	test(1,0)	test(2,0)	test(3,0)	test(4,0)	test(5,0)\n'
        'test(0,1)	test(1,1)	test(2,1)	test(3,1)	test(4,1)	test(5,1)\n'
        'test(0,2)	test(1,2)	test(2,2)	test(3,2)	test(4,2)	test(5,2)\n'
        'test(0,3)	test(1,3)	test(2,3)	test(3,3)	test(4,3)	test(5,3)\n'
    )
    self.assertEqual(
        lattice.states_str(),
        'Lattice: test\n'
        'States:\n'
        '∅	∅	∅	∅	∅	∅\n'
        '∅	∅	∅	∅	∅	∅\n'
        '∅	∅	∅	∅	∅	∅\n'
        '∅	∅	∅	∅	∅	∅\n'
    )
    self.assertIs(lattice.node(7, 9), lattice.error)
    self.assertIs(lattice.state(7, 9), lattice.error.state)

  def test_states(self):
    lattice = lt.Lattice('test', 4, 3, populate=True)
    self.assertEqual(lattice.error.state_str(), '0')
    self.assertEqual(
        lattice.states_str(),
        'Lattice: test\n'
        'States:\n'
        '1	2	3	4\n'
        '5	6	7	8\n'
        '9	10	11	12\n'
    )
    self.assertEqual(lattice.state_of(lattice.node(1, 2)), 10)


if __name__ == '__main__':
  absltest.main()
