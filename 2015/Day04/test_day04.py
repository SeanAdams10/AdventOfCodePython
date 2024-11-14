# pylint: disable=missing-docstring
import day_04
import pytest


@pytest.mark.parametrize("input_string, expected_output", [
    ('abcdef', 609043),
    ('pqrstuv', 1048970)
])
def test_zero_md5(input_string, expected_output):
    assert day_04.zero_md5(input_string, 5) == expected_output
