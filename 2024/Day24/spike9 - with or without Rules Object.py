from utils import get_input_data, timing_decorator
from collections import deque
import dataclasses
from time import perf_counter
from copy import deepcopy


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
            rules.append((op1, op2, operand, res),)

    return start_vals, rules


# def convert_dict_to_int(registers, key) ->int:
#     keys = sorted([x for x in registers if x.startswith(key)], reverse=True)
#     x = ''.join([str(registers[x]) for x in keys])
#     if not x:
#         return 0
#     return int(x, 2)

def part_1(rules, registers):
    instr_q = deque()
    if isinstance(rules, list):
        instr_q = deque(rules)
    elif isinstance(rules, dict):
        instr_q = deque(list(rules.values()))

    rotation_count = 0
    while len(instr_q) >0:
        update = instr_q[0]
        if update[0] not in registers or update[1] not in registers:
            instr_q.rotate(1)
            rotation_count += 1
            if rotation_count > len(instr_q):
                # print("Infinite loop detected")
                return 0,[]
            continue

        rotation_count = 0
        match update[2]:
            case 'AND':
                registers[update[3]] = registers[update[0]] & registers[update[1]]
            case 'OR':
                registers[update[3]] = registers[update[0]] | registers[update[1]]
            case 'XOR':
                registers[update[3]] = registers[update[0]] ^ registers[update[1]]
            case _:
                print(f"Unknown operation: {update[2]}")

        instr_q.popleft()

    keys = sorted([x for x in registers if x.startswith('z')], reverse=True)
    result = ''.join([str(registers[x]) for x in keys])
    # print(result)
    decimal_result = int(result, 2)
    # print(f"Part 1 result: {decimal_result}")
    return decimal_result, registers



# def create_registers(bit_count, value, prefix):
#     result = dict()
#     for i in range(bit_count):
#         key = f"{prefix}" + str(i).rjust(2, "0")
#         result[key] = (value >> i) & 1
#     return result

# def test_all_bits(rules, start=0, end=999999):

#     z_count = len([x for x in rules if x.result.startswith('z')])
#     result = 0
#     bit_count = 0
#     is_broken_rule = False
#     for t in test_cases[start:end]:
#         x = create_registers(z_count, t[0], 'x')
#         y = create_registers(z_count, t[1], 'y')
#         assert t[0] + t[1] == t[2]
#         assert t[0] <= 2**45 
#         assert t[1] <= 2**45 
#         assert t[1] <= 2**46 

#         registers = {**x, **y}
#         actual, bit_list = part_1(rules, deepcopy(registers))
#         if not bit_list: #if the result is not a valid result, skip
#             is_broken_rule = True   
#             continue

#         this_result = actual ^ t[2]
#         if result != this_result:
#             if result | this_result > result:
#                 result = result | this_result
#                 # print(f'new result found {result}')
#                 bit_count = bin(result).count('1')
#                 # print(f'Bit difference cnt: {bit_count}')

#     if is_broken_rule:
#         return int('1'*46, 2), 46
#     return result, bit_count

# def swap_rules(rules, key, newkey):
#     key_rule = next(rule for rule in rules if rule.result == key)
#     key_rule_id = next(k for k,rule in enumerate(rules) if rule.result == key)
#     newkey_rule = next(rule for rule in rules if rule.result == newkey)
#     newkey_rule_id = next(k for k,rule in enumerate(rules) if rule.result == newkey)

    
#     key_rule.result, newkey_rule.result = newkey_rule.result, key_rule.result
#     return rules


# def find_candidates(rules, baseline):
#     all_keys = [x.result for x in rules]    

#     candidates = set()
#     counter = 0
#     for x in range(len(all_keys)):
#         print(f'Outer Loop: {x} :: {all_keys[x]} :: {len(all_keys[x+1:])}')
#         for y in range(x+1,len(all_keys)):
#             counter += 1
#             new_rules = deepcopy(rules)
#             new_rules = swap_rules(new_rules, all_keys[x], all_keys[y])
#             _, diff_cnt = test_all_bits(new_rules)
#             # if diff_cnt == 46: print(f'broken rule',all_keys[x], all_keys[y])
#             if diff_cnt < baseline:
#                 candidates.add((all_keys[x], all_keys[y], diff_cnt))
#                 print(f'New candidate found: {all_keys[x]} and {all_keys[y]} with {diff_cnt}')

#             if counter % 500 == 0 :
#                 print(f'Counter: {counter}')


    
#     return candidates



# def phase_2(rules_orig, combinations)-> list:

#     counter = 0
#     lowest = 22
#     for k1 in range(len(combinations)):
#         for k2 in range(k1+1, len(combinations)):
#             for k3 in range(k2+1, len(combinations)):
#                 for k4 in range(k3+1, len(combinations)):

#                     c1 = combinations[k1]
#                     c2 = combinations[k2]
#                     c3 = combinations[k3]
#                     c4 = combinations[k4]

#                     #todo: check that none of the elements of the combination are the same
#                     check_dup = set([c1[0],c1[1], c2[0],c2[1], c3[0],c3[1], c4[0],c4[1]])
#                     if len(check_dup) < 8:
#                         continue

#                     counter += 1
#                     if counter % 2000 == 0:
#                         print(counter,c1,c2,c3,c4)
#                         print(counter,k1,k2,k3,k4)

#                     rules = deepcopy(rules_orig)
#                     rules = swap_rules(rules, c1[0], c1[1])
#                     rules = swap_rules(rules, c2[0], c2[1])
#                     rules = swap_rules(rules, c3[0], c3[1])
#                     rules = swap_rules(rules, c4[0], c4[1])

#                     error_cnt = test_all_bits(rules)[1]
#                     if error_cnt <= lowest:
#                         lowest = error_cnt
#                         print(f"Lowest: {lowest}, {c1}, {c2}, {c3}, {c4}")

#                     #todo: check if the valid flag is in errors or positive results
#                     if error_cnt == 0:
#                         print(f"Result found: {c1}, {c2}, {c3}, {c4}")
#                         print (f"Result: {error_cnt}")
#                         return [c1, c2, c3, c4]
#     return [('0','0'),('0','0'),('0','0'),('0','0')]


def main():
    data = get_input_data(2024, 24, sample=0)
    start_vals, rules = read_input(data)

    start_time = perf_counter()
    for i in range(10000):
        actual = part_1(deepcopy(rules), deepcopy(start_vals))[0]
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
