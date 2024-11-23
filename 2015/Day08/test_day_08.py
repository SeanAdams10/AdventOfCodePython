import pytest
# from pydantic import ValidationError

from day_08 import SpecificString, StringChecker


# def test_specific_string():
#     test = SpecificString('""', '""', 2, 0)
#     assert test.original == '""'
#     assert test.cleaned == '""'
#     assert test.original_length == 2
#     assert test.cleaned_length == 0


# def test_specific_string_fail1():
#     with pytest.raises(ValidationError):
#         SpecificString(1, '""', 2, 0)


# def test_specific_string_fail2():
#     with pytest.raises(ValidationError):
#         SpecificString('""', 1, 2, 0)


# def test_specific_string_fail3():
#     with pytest.raises(ValidationError):
#         SpecificString('""', '""', 'a', 0)


# def test_specific_string_fail4():
#     with pytest.raises(ValidationError):
#         SpecificString('""', '""', 1, 'a')


# def test_string_checker():
#     test = StringChecker(['""','"abc"', '"aaa\"aaa"', '"\x27"'])
#     assert test.data == ['""','"abc"', '"aaa\"aaa"', '"\x27"']

def test_clean_all_string():
    test = StringChecker(['""','"abc"', '"aaa\"aaa"', '"\x27"'])
    assert test.part_1() == 12


if __name__ == '__main__':
    pytest.main()
