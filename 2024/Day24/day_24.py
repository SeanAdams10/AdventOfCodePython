from time import perf_counter
from utils import get_input_data, timing_decorator
import dataclasses
import re
from collections import defaultdict, deque
from itertools import permutations, combinations


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

def part_1(rules, registers):
    instr_q = deque(rules)
    rotation_count = 0
    while len(instr_q) >0:
        update = instr_q[0]
        if update.op1 not in registers or update.op2 not in registers:
            instr_q.rotate(1)
            rotation_count += 1
            if rotation_count > len(instr_q):
                # print("Infinite loop detected")
                return 0,[]
            continue

        rotation_count = 0
        match update.operand:
            case 'AND':
                registers[update.result] = registers[update.op1] & registers[update.op2]
            case 'OR':
                registers[update.result] = registers[update.op1] | registers[update.op2]
            case 'XOR':
                registers[update.result] = registers[update.op1] ^ registers[update.op2]
            case _:
                print(f"Unknown operation: {update.operand}")

        instr_q.popleft()

    keys = sorted([x for x in registers if x.startswith('z')], reverse=True)
    result = ''.join([str(registers[x]) for x in keys])
    # print(result)
    decimal_result = int(result, 2)
    # print(f"Part 1 result: {decimal_result}")
    return decimal_result, registers

def compare_bits(x_bin:str, y_bin: str)->list:

    max_len = max(len(x_bin), len(y_bin))
    x_bin = x_bin.zfill(max_len)[::-1]
    y_bin = y_bin.zfill(max_len)[::-1]

    diff_bits = []
    for i in range(len(x_bin)):
        if x_bin[i] != y_bin[i]:
            diff_bits.append(i)

    # print(diff_bits[::-1])
    return diff_bits



def test_values(start_values, rules):
    registers = defaultdict(int)
    for reg, val in start_values.items():
        registers[reg] = int(val)

    result, registers = part_1(rules, registers)
    if result ==0:
        return 0, registers, []
        
    x_keys = sorted([x for x in registers if x.startswith('x')], reverse=True)
    x_bin = ''.join([str(registers[x]) for x in x_keys])
    x_dec = int(x_bin, 2)

    y_keys = sorted([x for x in registers if x.startswith('y')], reverse=True)
    y_bin = ''.join([str(registers[x]) for x in y_keys])
    y_dec = int(y_bin, 2)

    z_keys = sorted([x for x in registers if x.startswith('z')], reverse=True)
    z_bin = ''.join([str(registers[x]) for x in z_keys])
    z_dec = int(z_bin, 2)

    # print(f"x: {x_dec}, y: {y_dec}, z: {z_dec} , expected: {x_dec + y_dec}")
    # print(x_bin)
    # print(y_bin)
    # print(f"{x_dec + y_dec:b}")
    # print(f"{z_bin}")

    diff_bits = compare_bits(z_bin, f'{(x_dec + y_dec):b}')
    

    return result, registers, diff_bits
   


def find_nodes(rules_dict, diff_bits, levels):
    nodes = set()
    search_nodes = ['z' + str(i).zfill(2) for i in diff_bits]
    lext_level_search = []
    nodes.update(search_nodes)
    while levels >0:
        levels -=1

        while search_nodes:
            node = search_nodes.pop(0)
            if node in rules_dict:
                nodes.add(node)
                lext_level_search.append(rules_dict[node].op1)
                lext_level_search.append(rules_dict[node].op2)
        search_nodes = lext_level_search.copy()
    return nodes

def return_combos (nodes):
    for n in combinations(nodes, 4):
        for a in nodes:
            if a in n: continue
            a_dash = list(n) + [a]
            for b in nodes:
                if b in a_dash: continue
                b_dash = a_dash + [b]
                for c in nodes:
                    if c in b_dash: continue
                    c_dash = b_dash + [c]
                    for d in nodes:
                        if d in c_dash: continue
                        if n[0] < a and n[1] < b and n[2] < c and n[3] < d:
                            yield (n[0], a, n[1], b, n[2], c, n[3], d)


def swap_rules(rules, a, b):
    rules[a].result = b
    rules[b].result = a
    rules[a], rules[b] = rules[b], rules[a]

    return rules

def compare_numbers(expected:int, actual: int)->list:

    diff_bits = []
    for i in range(47):
        e_bit = (expected >> i) & 1
        a_bit = (actual >> i) & 1
        diff_bits.append(e_bit != a_bit)    

    return diff_bits




def part1():
    file_name = 'input.txt'
    with open('./2024/Day24b/' + file_name) as f:
        data = f.read().splitlines()
    start_vals, rules = read_input(data)

    # # set the initial value
    # registers = defaultdict(int)
    # for reg, val in start_vals.items():
    #     registers[reg] = int(val)

    # result, registers = part_1(rules, registers)

    # match file_name:
    #     case 'input.txt':
    #         assert result == 38869984335432
    #     case 'sample1.txt':
    #         assert result == 4
    #     case 'sample2.txt':
    #         assert result == 2024
    #     case 'sample3.txt':
    #         assert result == 9        
    #     case _:
    #         print("No assertion for this file")

    # print(f'Rule count', len(registers))

def get_expected_value(registers):
    x_keys = sorted([x for x in registers if x.startswith('x')], reverse=True)
    x_bin = ''.join([str(registers[x]) for x in x_keys])
    x_dec = int(x_bin, 2)

    y_keys = sorted([x for x in registers if x.startswith('y')], reverse=True)
    y_bin = ''.join([str(registers[x]) for x in y_keys])
    y_dec = int(y_bin, 2)

    expected = x_dec + y_dec
    return x_dec,y_dec,expected



def test_rules(registers, rules, x_dec,y_dec,expected):
    instr_q = deque(rules)
    rotation_count = 0
    while len(instr_q) >0:
        update = instr_q[0]
        if update.op1 not in registers or update.op2 not in registers:
            instr_q.rotate(1)
            rotation_count += 1
            if rotation_count > len(instr_q):
                # print("Infinite loop detected")
                return -1
            continue

        rotation_count = 0

        match update.operand:
            case 'AND':
                registers[update.result] = registers[update.op1] & registers[update.op2]
            case 'OR':
                registers[update.result] = registers[update.op1] | registers[update.op2]
            case 'XOR':
                registers[update.result] = registers[update.op1] ^ registers[update.op2]
            case _:
                print(f"Unknown operation: {update.operand}")
                raise ValueError

        instr_q.popleft()

    #right now we have the set of registers

    z_keys = sorted([x for x in registers if x.startswith('z')], reverse=True)
    z_bin = ''.join([str(registers[x]) for x in z_keys])
    z_dec = int(z_bin, 2)

    diff_bits = compare_bits(z_bin, f'{(x_dec + y_dec):b}')
    return len(diff_bits), diff_bits


def part_2():
    # Load data
    file_name = 'input.txt'
    with open('./2024/Day24/' + file_name) as f:
        data = f.read().splitlines()
    start_vals, rules_orig = read_input(data)
    registers_orig = set_start_registers(start_vals, rules_orig)
    rules_dict_orig = {x.result:x for x in rules_orig}
    x,y,expected = get_expected_value(registers_orig)
    bit_diff_orig,bit_diff_list_orig = test_rules(registers_orig, rules_orig, x,y,expected)

    actual = part_1(rules_orig, registers_orig)
    diff_list = compare_numbers(expected, expected)


    #find the nodes we need to test
    r = rules_dict_orig.copy()
    nodes = find_nodes(r, bit_diff_list_orig,1)
    # nodes = sorted([x for x in rules_dict_orig if x.startswith('z')], reverse=True)

    min_diff_bits = bit_diff_orig

    print('starting min diff bits:', bit_diff_orig)

    for k,perm in enumerate(return_combos(nodes)):
        rules_dict_copy = rules_dict_orig.copy()
        registers_copy = registers_orig.copy()

        if k % 1000000 == 0:
            print(f'trying permutation:{k} min_diff_bits: {min_diff_bits}')

        for i in range(0,8,2):
            rules_dict_copy = swap_rules(rules_dict_copy, perm[i], perm[i+1])

        rules_copy = [x for x in rules_dict_copy.values()]

        bit_diff,_ = test_rules(registers_copy, rules_copy, x,y,expected)
        if bit_diff == -1:
            #infinite loop
            continue
        if bit_diff < min_diff_bits:
            min_diff_bits = bit_diff
            print(f'{str(min_diff_bits).zfill(3)}: ', perm)
        if bit_diff == 0:
            print('Part 2 result:', perm)
            break






def set_start_registers(start_values, rules):
    registers = defaultdict(int)
    for reg, val in start_values.items():
        registers[reg] = int(val)
    return registers




def main():
    # part_1()
    part_2()









if __name__ == "__main__": 
    main()
