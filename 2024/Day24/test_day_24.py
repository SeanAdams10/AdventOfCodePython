import day_24_v3
# import spike10_recursion_only
import pytest


@pytest.mark.parametrize("in_dict, key,expected", [
    ({'x00':0, 'x01':0, 'x02': 0}, 'x', 0),
    ({'x00':0, 'x01':0, 'x02': 1}, 'x', 4),
    ({'x00':0, 'x01':1, 'x02': 1}, 'x', 6),
    ({'x00':1, 'x01':0, 'x02': 0}, 'x', 1),
    ({'x00':1, 'x02':0, 'x01': 1}, 'x', 3),
    ({'x00':1, 'x02':0, 'x01': 1}, 'y', 0),
    ({'x00':1, 'x02':0, 'z01':1, 'x01': 1}, 'x', 3),
])
def test_convert_dict_to_int(in_dict, key, expected):
    assert day_24_v3.convert_dict_to_int(in_dict, key) == expected


@pytest.mark.parametrize("bitcount, value, prefix, expected", [
    (3, 0, 'x', {'x00':0, 'x01':0, 'x02': 0}),
    (3, 4, 'x', {'x00':0, 'x01':0, 'x02': 1}),
    (3, 6, 'x', {'x00':0, 'x01':1, 'x02': 1}),
    (3, 1, 'x', {'x00':1, 'x01':0, 'x02': 0}),
    (3, 3, 'x', {'x00':1, 'x01':1, 'x02': 0}),
    (3, 0, 'y', {'y00':0, 'y01':0, 'y02': 0}),
    (3, 3, 'y', {'y00':1, 'y01':1, 'y02': 0}),
    (5, 2, 'x',{'x00':0, 'x01':1, 'x02': 0, 'x03': 0, 'x04': 0}),
])
def test_create_registers(bitcount, value, prefix, expected):
    assert day_24_v3.create_registers(bitcount, value, prefix) == expected


@pytest.mark.parametrize("rules, startkey, endkey, result", [
    ([(1,1,1,'a'), (2,2,2,'b')],'a','b',
     [(1,1,1,'b'), (2,2,2,'a')]), 
    ([(1,1,1,'a'), (2,2,2,'b'), (3,3,3,'c')],'a','c',
     [(1,1,1,'c'), (2,2,2,'b'), (3,3,3,'a')]), 

])

def test_swap_rules(rules, startkey, endkey, result):
    day_24_v3.swap_rules(rules, startkey, endkey)
    assert rules == result


def test_part_1_recursion():
    registers = {}
    rules = [('a', 'a', 'AND', 'z00'), ('b', 'b', 'OR', 'a'), ('a', 'a', 'AND', 'b'),]
    decimal_result, result, success =  day_24_v3.part_1(rules, registers)
    assert success == False
    assert decimal_result == -1
    assert result == []




if __name__ == "__main__":
    pytest.main()