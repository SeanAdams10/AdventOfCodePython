from functools import lru_cache
from operator import and_, or_, lshift, rshift


def parse_input(data):
    return_val = {}
    for item in data:
        s = item.split(' -> ')
        target = s[1]
        source = s[0].split()
        return_val[target] = source

    return return_val


def get_value(wires, wire='a', b=None):
    operations = {'AND': and_, 'OR': or_, 'LSHIFT': lshift, 'RSHIFT': rshift}

    @lru_cache
    def aux(wire):
        try:
            return int(wire)
        except ValueError:
            lhs = wires[wire]
        if len(lhs) == 1:  # assign
            return aux(lhs[0])
        if len(lhs) == 2:  # not
            return ~aux(lhs[1]) & 0xffff
        return operations[lhs[1]](aux(lhs[0]), aux(lhs[2]))

    if b is not None:
        wires['b'] = [b]
    return aux(wire)


data = open("2015/Day07/Part1Input.txt").read().splitlines()
wires = parse_input(data)
print(wires)

print(first := get_value(wires))
print(get_value(wires, b=first))
