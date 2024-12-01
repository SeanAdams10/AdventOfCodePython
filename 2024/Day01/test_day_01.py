# pylint: disable=missing-docstring
import pytest
import day_01


@pytest.mark.parametrize("test_input, expected", [
    (['1 2', '3 4', '5 6'], ([1, 3, 5], [2, 4, 6])),
    (['2 3', '4 5', '6 7'], ([2, 4, 6], [3, 5, 7])),
    (['3 4', '5 6', '7 8'], ([3, 5, 7], [4, 6, 8])),
])
def test_parse_input(test_input, expected):
    assert day_01.parse_input(test_input) == expected


def test_part1_sample_input():
    list1 = sorted([3, 4, 2, 1, 3, 3])
    list2 = sorted([4, 3, 5, 3, 9, 3])
    assert day_01.part_1(list1, list2) == 11


def test_part1_main():
    with open(r'./2024/Day01/input.txt', 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

    list1, list2 = day_01.parse_input(data)

    part1_answer = day_01.part_2(list1, list2)
    assert part1_answer == 1660292


def test_part2_sample_input():
    list1 = sorted([3, 4, 2, 1, 3, 3])
    list2 = sorted([4, 3, 5, 3, 9, 3])
    assert day_01.part_2(list1, list2) == 31


def test_part2_main():
    with open(r'./2024/Day01/input.txt', 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

    list1, list2 = day_01.parse_input(data)

    part1_answer = day_01.part_2(list1, list2)
    assert part1_answer == 22776016
