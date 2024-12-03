import day_03
import pytest



@pytest.mark.parametrize("test_input, expected", [
    ("",[]),
    ("a",['a']),
    ("don't()a",[]),
    ("do()a",['a']),
    ("don't()do()a",['a']),
    ("don't()do()ado()b",['a','b']),
    ("don't()do()adon't()bdo()c",['a','c']),
    ("don't()",[]),
])
def test_split_lines(test_input, expected):
    assert day_03.split_lines_do_dont(test_input) == expected
    
    
    
    