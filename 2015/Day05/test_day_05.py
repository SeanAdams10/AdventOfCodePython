import pytest
# pylint: disable=missing-docstring
import day_05


@pytest.mark.parametrize('word, expected', [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', True),
    ('haegwjzuvuyypxyu', True),
    ('dvszwmarrgswjxmb', False),
])
def test_is_3_vowels(word, expected):
    assert day_05.is_3_vowels(word) == expected


@pytest.mark.parametrize('word, expected', [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', False),
    ('abcdde', True),
    ('aabbccdd', True),
    ('abcde', False),
])
def test_is_double_letter(word, expected):
    assert day_05.is_double_letter(word) == expected


@pytest.mark.parametrize('word, expected', [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', True),
    ('haegwjzuvuyypxyu', False),
    ('dvszwmarrgswjxmb', True),
    ('ccab', False),
    ('aacd', False),
    ('aapq', False),
    ('aaxy', False),
])
def test_is_no_banned_strings(word, expected):
    assert day_05.is_no_banned_strings(word) == expected


@pytest.mark.parametrize('word, expected', [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', False),
    ('haegwjzuvuyypxyu', False),
    ('dvszwmarrgswjxmb', False),
])
def test_is_nice_1(word, expected):
    assert day_05.is_nice(word) == expected


def test_is_nice_2():
    assert day_05.is_nice_2('qjhvhtzxzqqjkmpb') == True
    assert day_05.is_nice_2('xxyxx') == True
    assert day_05.is_repeat_char('uurcxstgmygtbstg') == False
    assert day_05.is_nice_2('uurcxstgmygtbstg') == False
    assert day_05.is_nice_2('ieodomkazucvgmuy') == False
