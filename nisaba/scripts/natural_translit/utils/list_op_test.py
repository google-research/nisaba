# Copyright 2023 Nisaba Authors.
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
from nisaba.scripts.natural_translit.utils import list_op as ls

_A_FST = ls.pyn.accep('a')
_B_STR = 'b'
_C_STR = 'c'
_D_INT = 4

_THINGS = [
    ls.ty.Thing.from_value_of(_A_FST),
    ls.ty.Thing.from_value_of(_B_STR),
    ls.ty.Thing.from_value_of(_C_STR),
    ls.ty.Thing.from_value_of(_D_INT),
]


def _concat(a: str, b: str) -> str:
  return a + b


class ListOpTest(absltest.TestCase):

  def assertPynEqual(self, fst1, fst2):
    self.assertTrue(ls.pyn.equal(fst1, fst2))

  def test_star_opt(self):
    self.assertPynEqual(
        ls.star_opt(ls.pyn.union(_A_FST, _B_STR)),
        ls.pyn.union(_A_FST, _B_STR).star.optimize()
    )

  def test_union_opt(self):
    self.assertPynEqual(
        ls.union_opt(_A_FST, _B_STR),
        ls.pyn.union(_A_FST, _B_STR).optimize()
    )

  def test_union_star(self):
    self.assertPynEqual(
        ls.union_star(_A_FST, _B_STR),
        ls.pyn.union(_A_FST, _B_STR).star.optimize()
    )

  def test_apply_foreach(self):
    self.assertEqual(
        ls.apply_foreach(_concat, [
            [_B_STR, _B_STR], [_B_STR, _C_STR], [_C_STR, _B_STR]
        ]),
        [
            _concat(_B_STR, _B_STR),
            _concat(_B_STR, _C_STR),
            _concat(_C_STR, _B_STR)
        ]
    )

  def test_apply_union(self):
    self.assertPynEqual(
        ls.apply_union(_concat, [[_B_STR, _B_STR], [_B_STR, _C_STR]]),
        ls.pyn.union(
            _concat(_B_STR, _B_STR),
            _concat(_B_STR, _C_STR)
        ).optimize()
    )

  def test_apply_union_star(self):
    self.assertPynEqual(
        ls.apply_union_star(_concat, [[_B_STR, _B_STR], [_B_STR, _C_STR]]),
        ls.pyn.union(
            _concat(_B_STR, _B_STR),
            _concat(_B_STR, _C_STR)
        ).star.optimize()
    )

  def test_cross_union(self):
    self.assertPynEqual(
        ls.cross_union([[_A_FST, _B_STR], [_A_FST, _C_STR]]),
        ls.pyn.union(
            ls.pyn.cross(_A_FST, _B_STR),
            ls.pyn.cross(_A_FST, _C_STR)
        ).optimize()
    )

  def test_cross_union_star(self):
    self.assertPynEqual(
        ls.cross_union_star([[_A_FST, _B_STR], [_A_FST, _C_STR]]),
        ls.pyn.union(
            ls.pyn.cross(_A_FST, _B_STR),
            ls.pyn.cross(_A_FST, _C_STR)
        ).star.optimize()
    )

  def test_attr_list(self):
    self.assertEqual(
        ls.attr_list([complex(1, 2), complex(3.5, 4)], 'real'),
        [1.0, 3.5]
    )

  def test_attr_list_wrong_key(self):
    self.assertEmpty(
        ls.attr_list([complex(1, 2), complex(3.5, 4)], 'rea'),
    )

  def test_attr_list_with_type(self):
    self.assertEqual(
        ls.attr_list([complex(1, 2), complex(3.5, 4)], 'real', float),
        [1.0, 3.5]
    )

  def test_attr_list_wrong_type(self):
    self.assertEmpty(
        ls.attr_list([complex(1, 2), complex(3.5, 4)], 'real', int),
    )

  def test_fst_attr_list(self):
    self.assertEqual(
        ls.fst_attr_list(_THINGS, 'value'), [_A_FST, _B_STR, _C_STR]
    )

  def test_fst_attr_list_union(self):
    self.assertPynEqual(
        ls.fst_attr_list_union(_THINGS, 'value'),
        ls.pyn.union(_A_FST, _B_STR, _C_STR).optimize()
    )

  def test_fst_attr_list_union_star(self):
    self.assertPynEqual(
        ls.fst_attr_list_union_star(_THINGS, 'value'),
        ls.pyn.union(_A_FST, _B_STR, _C_STR).star.optimize()
    )

if __name__ == '__main__':
  absltest.main()