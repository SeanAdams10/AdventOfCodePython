# pylint: disable=missing-docstring
import pytest

from day_08 import StringChecker


def test_part1_sample():
    data = [r'""', r'"abc"', r'"aaa\"aaa"', r'"\x27"']
    test = StringChecker(data)

    assert test.part_1() == 12


def test_part2_sample():
    data = [r'""', r'"abc"', r'"aaa\"aaa"', r'"\x27"']
    test = StringChecker(data)

    assert test.part_2() == 19


def test_part1_actual():
    with open(r'2015\Day08\Part1Input.txt', encoding="ASCII") as f:
        data = f.read().splitlines()
    # data = [r'""',r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    test = StringChecker(data)
    assert test.part_1() == 1342


def test_part2_actual():
    with open(r'2015\Day08\Part1Input.txt', encoding="ASCII") as f:
        data = f.read().splitlines()
    # data = [r'""',r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    test = StringChecker(data)
    assert test.part_2() == 2074


if __name__ == '__main__':
    pytest.main()
