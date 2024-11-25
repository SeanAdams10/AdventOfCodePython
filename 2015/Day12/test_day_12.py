import day_12
import pytest


@pytest.mark.parametrize("test_input, expected", [
    ('[1,2,3]',[1,2,3]),
    ('{"a":2,"b":4}',[2,4]),
    ('[[[3]]]',[3]),
    ('{"a":{"b":4},"c":-1}',[4,-1]),
    ('{"a":[-1,1]}',[-1,1]),
    ('[-1,{"a":1}]',[-1,1]),
    ('[]',[]),
    ('{}',[]),
])
def test_day_12_parse(test_input, expected):
    assert day_12.parse_numbers(test_input) == expected

@pytest.mark.parametrize("test_input, expected", [
    ('[1,2,3]',[1,2,3]),
    ('[1,{"c":"red","b":2},3]',[1,3]),
    ('{"d":"red","e":[1,2,3,4],"f":5}',[]),
    ('[1,"red",5]',[1,5]),
])
def test_day_12_parse_part2(test_input, expected):
    assert day_12.parse_numbers(test_input,'red') == expected



def test_part1():
    with open('Part1Input.txt','r', encoding='ascii') as file:
        json_str = file.read()
        assert sum(day_12.parse_numbers(json_str)) == 111754

def test_part2():
    with open('Part1Input.txt','r', encoding='ascii') as file:
        json_str = file.read()
        assert sum(day_12.parse_numbers(json_str,'red')) == 65402



if __name__ == '__main__':
    pytest.main()