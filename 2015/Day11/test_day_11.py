import pytest
import day_11
import string



@pytest.mark.parametrize("input, expected", [
    ('aaaaaaaa', 'aaaaaaab'),
    ('aaaaaaaz', 'aaaaaaba'),
    ('aaaaaazz', 'aaaaabaa'),
    ('aaaaazzz', 'aaaabaaa'),
    ('aaaazzzz', 'aaabaaaa'),
    ('aazzzzzz', 'abaaaaaa'),
    ('azaaaaag', 'azaaaaah'),
    ('azaaaaaz', 'azaaaaba'),
    ('zaaaaaaz', 'zaaaaaba'),
])
def test_increment_pass(input, expected):
    assert day_11.increment_password(input) == expected

    
@pytest.mark.parametrize("input, expected", [
    ('hijklmmn', True),
    ('abbceffg', False),
    ('abbcegjk', False),
    ('abcdffaa', True),
    ('ghjaabcc', True)  
])
def test_rule_1(input, expected):
    let = string.ascii_lowercase
    target_letters = [let[i] + let[i+1] + let[i+2] for i in range(len(let)-2)]
    assert day_11.check_rule_1(input, target_letters) == expected
    
@pytest.mark.parametrize("input, expected", [
    ('hijklmmn', False),
    ('abbceffg', True),
    ('abbcegjk', True),
    ('abcdffaa', True),
    ('ghjaabcc', True)
])
def test_rule_2(input, expected):
    assert day_11.check_rule_2(input) == expected
    
@pytest.mark.parametrize("input, expected", [
    ('hijklmmn', False),
    ('abbceffg', True),
    ('abbcegjk', False),
    ('abcdffaa', True),
    ('ghjaabcc', True)
])
def test_rule_3(input, expected):
    assert day_11.check_rule_3(input) == expected
    
@pytest.mark.parametrize("input, expected", [
    ('abcdefgh', 'abcdffaa'),
    ('ghijklmn', 'ghjaabcc'),
    ('hepxcrrq', 'hepxxyzz')
])
def test_next_pass(input, expected):
    let = string.ascii_lowercase
    target_letters = [let[i] + let[i+1] + let[i+2] for i in range(len(let)-2)]

    assert day_11.find_next_pass(target_letters=target_letters, start=input) == expected
    
def test_part_2():
    let = string.ascii_lowercase
    target_letters = [let[i] + let[i+1] + let[i+2] for i in range(len(let)-2)]
    
    start = 'hepxxyzz'
    start = day_11.increment_password(start) 
    assert day_11.find_next_pass(target_letters, start) == 'heqaabcc'


if __name__ == '__main__':
    pytest.main()