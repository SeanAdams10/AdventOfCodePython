from utils import get_input_data, timing_decorator
from collections import deque
import dataclasses
from time import perf_counter



test_cases = [
    (19606853692217,19297486219791,38904339912008),
    (0, 0, 0),   # 0 + 0 = 0
    (0, 1, 1),   # 0 + 1 = 1
    (1, 0, 1),   # 1 + 0 = 1
    (1, 1, 2),   # 1 + 1 = 2
    (1, 2, 3),   # 1 + 2 = 3
    (2, 1, 3),   # 2 + 1 = 3
    (2, 2, 4),   # 2 + 2 = 4
    (3, 3, 6),   # 3 + 3 = 6 (double carry over)
    (2**45, 2**45, 2**46),  # Test carry over at bit 45
    (2**46, 2**46, 2**47),  # Test carry over at bit 46
    (2**45 - 1, 1, 2**45),  # Test carry over from bit 0 to bit 45
    (2**46 - 1, 1, 2**46),  # Test carry over from bit 0 to bit 46
    (2**45, 1, 2**45 + 1),  # Test no carry over at bit 45
    (2**46, 1, 2**46 + 1),  # Test no carry over at bit 46
]


@dataclasses.dataclass
class Rule:
    op1: str
    op2: str
    operand: str
    result: str


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    start_vals = {x.split(":")[0].strip(): int(x.split(":")[1].strip())
             for x in data if ":" in x}
    
    rules = []
    for row in data:
        if "->" in row:
            op, res = row.split(' -> ')
            op1, operand, op2 = op.split()
            rules.append(Rule(op1, op2, operand, res))

    return start_vals, rules



def convert_dict_to_int(registers, key) ->int:
    keys = sorted([x for x in registers if x.startswith(key)], reverse=True)
    x = ''.join([str(registers[x]) for x in keys])
    if not x:
        return 0
    return int(x, 2)


def part_1(rules, registers):
    ops = {
        'AND': lambda x, y: x & y,
        'OR': lambda x, y: x | y,
        'XOR': lambda x, y: x ^ y
        }
    
    def recurse_answer(key):
        if key in registers:
            return registers[key]
        rule = rules_dict[key]
        op1 = recurse_answer(rule.op1)
        op2 = recurse_answer(rule.op2)
        registers[key] = ops[rule.operand](op1, op2)
        return registers[key]

        
    rules_dict = {x.result: x for x in rules}
    result = []
    for i in range(46):
        key = f'z{str(i).rjust(2,"0")}'
        result.append(recurse_answer(key))

    binary_string = ''.join(map(str, result[::-1]))
    decimal_result = int(binary_string, 2)

    return decimal_result, result


def get_expected(registers):
    x = convert_dict_to_int(registers, 'x')
    y = convert_dict_to_int(registers, 'y')
    z = x+y

    return x,y,z

def create_registers(bit_count, value, prefix):
    result = dict()
    for i in range(bit_count):
        key = f"{prefix}" + str(i).rjust(2, "0")
        result[key] = (value >> i) & 1
    return result

def test_all_bits(rules):

    z_count = len([x for x in rules if x.result.startswith('z')])
    result = 0
    for t in test_cases:
        x = create_registers(z_count, t[0], 'x')
        y = create_registers(z_count, t[1], 'y')
        assert t[0] + t[1] == t[2]
        registers = {**x, **y}
        actual = part_1(rules, registers.copy())[0]
        this_result = actual ^ t[2]
        if result != this_result:
            result = result | this_result
            print(f'new result found {result}')
            bit_count = bin(this_result).count('1')
            print(f'Bit difference cnt: {bit_count}')

    return result, bit_count

def main():
    data = get_input_data(2024, 24, sample=0)
    start_vals, rules = read_input(data)

    actual = part_1(rules, start_vals.copy())[0]
    print(actual)

    x,y,expected = get_expected(start_vals)
    
    difference = bin(actual ^ expected)
    print (f'({x},{y},{expected})')
    print(f"Expected:   {bin(expected).rjust(48)} = {expected}")
    print(f"Actual:     {bin(actual).rjust(48)} = {actual}")
    print(f"Difference: {difference.rjust(48)} = {int(difference, 2)}")
    print(f'Bit difference cnt: {difference.count("1")}')

    differnece, diff_cnt = test_all_bits(rules)
    print(f'Bit difference cnt after testing: {diff_cnt}')
    





if __name__ == "__main__":
    main()
