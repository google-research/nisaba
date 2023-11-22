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

"""Shortcuts for detailed logs.

Since all calls to absl/logging is made from this file, the log messages
include the name and location of the caller of the logging function as prefix.

Examples:
type_op.py/is_none: returns False, detail: int_0
type_op.py/is_nothing: returns True, detail: Nothing_Unassigned
type_op.py/is_equal: type mismatch between Fst_a and Phon_a
type_op.py/enforce_list: from:dict_{'a': 5}
type_op.py/enforce_list: returns [5]
"""
