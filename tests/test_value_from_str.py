""" integral test"""

import pytest

from parsing import value_from_str

@pytest.mark.parametrize(
    'in_str, out_val',
    [
        ('', 0),
        ('1 234.56 р', 1234.56),
        ('$ 1,000.01', 1000.01)
    ]
)
def test_values_from_strs(in_str: str, out_val: float) -> None:
    """ str to val test"""
    assert value_from_str(in_str) == out_val
