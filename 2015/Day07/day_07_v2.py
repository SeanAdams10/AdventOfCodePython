import operator
from functools import lru_cache

operations_dict = {"AND": operator.and_, "OR": operator.or_,
                   "LSHIFT": operator.lshift, "RSHIFT": operator.rshift}


def parse_input(data):
    instructions = {}
    for line in data:
        # Split the instruction and the output
        instr, target_wire = line.split(' -> ')
        instructions[target_wire] = instr.split(
            ' ')  # Split the instruction into a list
    return instructions


def outer_solve_for_x(instructions, wire, b=None):

    @lru_cache
    def solve_for_x(wire):
        if wire.isdigit():
            return int(wire)
        if len(instructions[wire]) == 1:  # assign operation
            return solve_for_x(instructions[wire][0])
        elif len(instructions[wire]) == 2:  # NOT operation
            # you have to mask the result to 16 bits because of the quirky way Python handles negative numbers
            return operator.invert(solve_for_x(instructions[wire][1])) & 0xffff
        else:  # binary operation
            operation_function = operations_dict[instructions[wire][1]]
            return operation_function(solve_for_x(instructions[wire][0]),
                                      solve_for_x(instructions[wire][2])) & 0xffff

    if b is not None:
        instructions['b'] = [b]
    return solve_for_x(wire)


with open(r'.\2015\Day07\Part1input.txt', 'r') as f:
    data = f.read().splitlines()

instructions = parse_input(data)
print(f'Part 1: {outer_solve_for_x(instructions, "a")}')
part_1_result = outer_solve_for_x(instructions, "a")

print(f'Part 2: {outer_solve_for_x(instructions, "a", str(part_1_result))}')
