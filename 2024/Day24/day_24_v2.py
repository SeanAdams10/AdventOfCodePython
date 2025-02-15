from utils import get_input_data, timing_decorator
from collections import deque
import dataclasses
from time import perf_counter




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
    if isinstance(rules, list):
        instr_q = deque(rules)
    elif isinstance(rules, dict):
        instr_q = deque(list(rules.values()))

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



def test_bits(bit_count: int, rules: list)->list:
    def create_registers(bit_count_int, value_int, prefix: str)->dict:
        result = dict()
        for i in range(bit_count_int):
            key = f"{prefix}" + str(i).zfill(2)
            result[key] = (value_int >> i) & 1
        return result

    result = []
    for l in range(bit_count):

        test_result = True
        #test case 1 = 1 and 0
        registers = create_registers(bit_count, 2**l, 'x')
        registers.update(create_registers(bit_count, 0, 'y'))
        test_result = test_result and (part_1(rules, registers)[0] == 2**l)

        #test case 2 = 0 and 1
        registers = create_registers(bit_count, 0, 'x')
        registers.update(create_registers(bit_count, 2**l, 'y'))
        test_result = test_result and (part_1(rules, registers)[0] == 2**l)

        #test case 3 = 0 and 0
        registers = create_registers(bit_count, 0, 'x')
        registers.update(create_registers(bit_count, 0, 'y'))
        test_result = test_result and part_1(rules, registers)[0] == 0

        #test case 3 = 1 and 1
        registers = create_registers(bit_count, 2**l, 'x')
        registers.update(create_registers(bit_count, 2**l, 'y'))
        test_result = test_result and part_1(rules, registers)[0] == 2**(l+1)


        result.append(test_result)

    return result

def get_expected_value(registers):
    x_keys = sorted([x for x in registers if x.startswith('x')], reverse=True)
    x_bin = ''.join([str(registers[x]) for x in x_keys])
    x_dec = int(x_bin, 2)

    y_keys = sorted([x for x in registers if x.startswith('y')], reverse=True)
    y_bin = ''.join([str(registers[x]) for x in y_keys])
    y_dec = int(y_bin, 2)

    expected = x_dec + y_dec
    return x_dec,y_dec,expected





def phase1(rules , registers)-> list:

    baseline = test_bits(46, rules)
    baseline_target = sum(baseline)
    print(baseline_target)
    candidates = set()
    counter = 0
    for r1 in rules:
        for r2 in rules:
            if r1 == r2:
                continue

            counter +=1
            if counter % 500 == 0:
                print(counter)
                print(r1.result, r2.result)
            r1.result, r2.result = r2.result, r1.result
            test_results = test_bits(46, rules)
            if sum(test_results) > baseline_target:
                candidates.add((max(r1.result, r2.result), min(r1.result, r2.result), sum(test_results)))
                print(f'Result found: {r1.result}, {r2.result}, {sum(test_results)}')
            r1.result, r2.result = r2.result, r1.result
    
    return candidates

def swap_rules(rules, a, b):
    rules[a].result = b
    rules[b].result = a
    rules[a], rules[b] = rules[b], rules[a]

    return rules


def phase_2(rules_orig, registers_orig, combinations)-> list:
    _,_,expected = get_expected_value(registers_orig)

    rules_orig = {x.result:x for x in rules_orig}

    counter = 0
    for k1 in range(len(combinations)):
        for k2 in range(k1+1, len(combinations)):
            for k3 in range(k2+1, len(combinations)):
                for k4 in range(k3+1, len(combinations)):

                    c1 = combinations[k1]
                    c2 = combinations[k2]
                    c3 = combinations[k3]
                    c4 = combinations[k4]
                    counter += 1
                    if counter % 1000 == 0:
                        print(counter,c1,c2,c3,c4)
                        print(counter,k1,k2,k3,k4)

                    rules = rules_orig.copy()
                    registers = registers_orig.copy()
                    rules = swap_rules(rules, c1[0], c1[1])
                    rules = swap_rules(rules, c2[0], c2[1])
                    rules = swap_rules(rules, c3[0], c3[1])
                    rules = swap_rules(rules, c4[0], c4[1])

                    valid = test_bits(46, rules)
                    if sum(valid) > 44:
                        print(f"Result found: {c1}, {c2}, {c3}, {c4}")
                        print (f"Result: {sum(valid)}")
                        # return [c1, c2, c3, c4]
    return

def compare_numbers(expected:int, actual: int)->list:

    diff_bits = []
    for i in range(47):
        e_bit = (expected >> i) & 1
        a_bit = (actual >> i) & 1
        diff_bits.append(e_bit == a_bit)    

    return diff_bits


def main():
    data = get_input_data(2024, 24, sample=0)
    start_vals, rules = read_input(data)

    x,y,expected = get_expected_value(start_vals)
    actual = part_1(rules, start_vals)[0]
    print(f"Expected: {expected}, Actual: {actual}")
    print(f"Expected (binary): {bin(expected)[2:].zfill(46)}")
    print(f"Actual (binary): {bin(actual)[2:].zfill(46)}")
    print(f"XOR (binary): {bin(expected ^ actual)[2:].zfill(46)}")

    result_vector = test_bits(46,rules)
    result_vector_sum = [k for k,v in enumerate(result_vector) if not v]
    result_vector_2 = compare_numbers(expected, actual)
    result_vector_2_sum = [k for k,v in enumerate(result_vector_2) if not v]

    print(result_vector_sum)
    print(result_vector_2_sum)






    # start_time = perf_counter()
    # for _ in range(1):
    #     decimal_results, registers = part_1(rules, start_vals)
    # end_time = perf_counter()
    # print(f"Part 1: {decimal_results}")
    # print(f"Execution time: {end_time - start_time}")


    


    # candidates = phase1(rules, start_vals)
    # with open('2024/Day24/candidates.txt', 'w') as f:
    #     for c in candidates:
    #         f.write(f"{c[0]} {c[1]}\n")
    # print(candidates)

    # with open('2024/Day24/candidates.txt', 'r') as f:
    #     data = f.read().splitlines()
    #     candidates = [(x.split()[0], x.split()[1]) for x in data]

    # print(candidates)

    # result = phase_2(rules, start_vals, candidates)
    # if result:
    #     result = [f'{min(x)},{max(x)}' for x in result]
    #     result = sorted(result, reverse=False)
    #     print(','.join(result))
    
if __name__ == "__main__":
    main()
