from utils import get_input_data, timing_decorator
from collections import deque
import dataclasses
from time import perf_counter
from copy import deepcopy



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
    (0, 0, 0),
    (2, 0, 2),
    (0, 2, 2),
    (2, 2, 4),
    (3, 3, 6),
    (1, 1, 2),
    (2, 1, 3),
    (4, 0, 4),
    (0, 4, 4),
    (4, 4, 8),
    (6, 6, 12),
    (3, 1, 4),
    (4, 1, 5),
    (8, 0, 8),
    (0, 8, 8),
    (8, 8, 16),
    (12, 12, 24),
    (7, 1, 8),
    (8, 1, 9),
    (16, 0, 16),
    (0, 16, 16),
    (16, 16, 32),
    (24, 24, 48),
    (15, 1, 16),
    (16, 1, 17),
    (32, 0, 32),
    (0, 32, 32),
    (32, 32, 64),
    (48, 48, 96),
    (31, 1, 32),
    (32, 1, 33),
    (64, 0, 64),
    (0, 64, 64),
    (64, 64, 128),
    (96, 96, 192),
    (63, 1, 64),
    (64, 1, 65),
    (128, 0, 128),
    (0, 128, 128),
    (128, 128, 256),
    (192, 192, 384),
    (127, 1, 128),
    (128, 1, 129),
    (256, 0, 256),
    (0, 256, 256),
    (256, 256, 512),
    (384, 384, 768),
    (255, 1, 256),
    (256, 1, 257),
    (512, 0, 512),
    (0, 512, 512),
    (512, 512, 1024),
    (768, 768, 1536),
    (511, 1, 512),
    (512, 1, 513),
    (1024, 0, 1024),
    (0, 1024, 1024),
    (1024, 1024, 2048),
    (1536, 1536, 3072),
    (1023, 1, 1024),
    (1024, 1, 1025),
    (2048, 0, 2048),
    (0, 2048, 2048),
    (2048, 2048, 4096),
    (3072, 3072, 6144),
    (2047, 1, 2048),
    (2048, 1, 2049),
    (4096, 0, 4096),
    (0, 4096, 4096),
    (4096, 4096, 8192),
    (6144, 6144, 12288),
    (4095, 1, 4096),
    (4096, 1, 4097),
    (8192, 0, 8192),
    (0, 8192, 8192),
    (8192, 8192, 16384),
    (12288, 12288, 24576),
    (8191, 1, 8192),
    (8192, 1, 8193),
    (16384, 0, 16384),
    (0, 16384, 16384),
    (16384, 16384, 32768),
    (24576, 24576, 49152),
    (16383, 1, 16384),
    (16384, 1, 16385),
    (32768, 0, 32768),
    (0, 32768, 32768),
    (32768, 32768, 65536),
    (49152, 49152, 98304),
    (32767, 1, 32768),
    (32768, 1, 32769),
    (65536, 0, 65536),
    (0, 65536, 65536),
    (65536, 65536, 131072),
    (98304, 98304, 196608),
    (65535, 1, 65536),
    (65536, 1, 65537),
    (131072, 0, 131072),
    (0, 131072, 131072),
    (131072, 131072, 262144),
    (196608, 196608, 393216),
    (131071, 1, 131072),
    (131072, 1, 131073),
    (262144, 0, 262144),
    (0, 262144, 262144),
    (262144, 262144, 524288),
    (393216, 393216, 786432),
    (262143, 1, 262144),
    (262144, 1, 262145),
    (524288, 0, 524288),
    (0, 524288, 524288),
    (524288, 524288, 1048576),
    (786432, 786432, 1572864),
    (524287, 1, 524288),
    (524288, 1, 524289),
    (1048576, 0, 1048576),
    (0, 1048576, 1048576),
    (1048576, 1048576, 2097152),
    (1572864, 1572864, 3145728),
    (1048575, 1, 1048576),
    (1048576, 1, 1048577),
    (2097152, 0, 2097152),
    (0, 2097152, 2097152),
    (2097152, 2097152, 4194304),
    (3145728, 3145728, 6291456),
    (2097151, 1, 2097152),
    (2097152, 1, 2097153),
    (4194304, 0, 4194304),
    (0, 4194304, 4194304),
    (4194304, 4194304, 8388608),
    (6291456, 6291456, 12582912),
    (4194303, 1, 4194304),
    (4194304, 1, 4194305),
    (8388608, 0, 8388608),
    (0, 8388608, 8388608),
    (8388608, 8388608, 16777216),
    (12582912, 12582912, 25165824),
    (8388607, 1, 8388608),
    (8388608, 1, 8388609),
    (16777216, 0, 16777216),
    (0, 16777216, 16777216),
    (16777216, 16777216, 33554432),
    (25165824, 25165824, 50331648),
    (16777215, 1, 16777216),
    (16777216, 1, 16777217),
    (33554432, 0, 33554432),
    (0, 33554432, 33554432),
    (33554432, 33554432, 67108864),
    (50331648, 50331648, 100663296),
    (33554431, 1, 33554432),
    (33554432, 1, 33554433),
    (67108864, 0, 67108864),
    (0, 67108864, 67108864),
    (67108864, 67108864, 134217728),
    (100663296, 100663296, 201326592),
    (67108863, 1, 67108864),
    (67108864, 1, 67108865),
    (134217728, 0, 134217728),
    (0, 134217728, 134217728),
    (134217728, 134217728, 268435456),
    (201326592, 201326592, 402653184),
    (134217727, 1, 134217728),
    (134217728, 1, 134217729),
    (268435456, 0, 268435456),
    (0, 268435456, 268435456),
    (268435456, 268435456, 536870912),
    (402653184, 402653184, 805306368),
    (268435455, 1, 268435456),
    (268435456, 1, 268435457),
    (536870912, 0, 536870912),
    (0, 536870912, 536870912),
    (536870912, 536870912, 1073741824),
    (805306368, 805306368, 1610612736),
    (536870911, 1, 536870912),
    (536870912, 1, 536870913),
    (1073741824, 0, 1073741824),
    (0, 1073741824, 1073741824),
    (1073741824, 1073741824, 2147483648),
    (1610612736, 1610612736, 3221225472),
    (1073741823, 1, 1073741824),
    (1073741824, 1, 1073741825),
    (2147483648, 0, 2147483648),
    (0, 2147483648, 2147483648),
    (2147483648, 2147483648, 4294967296),
    (3221225472, 3221225472, 6442450944),
    (2147483647, 1, 2147483648),
    (2147483648, 1, 2147483649),
    (4294967296, 0, 4294967296),
    (0, 4294967296, 4294967296),
    (4294967296, 4294967296, 8589934592),
    (6442450944, 6442450944, 12884901888),
    (4294967295, 1, 4294967296),
    (4294967296, 1, 4294967297),
    (8589934592, 0, 8589934592),
    (0, 8589934592, 8589934592),
    (8589934592, 8589934592, 17179869184),
    (12884901888, 12884901888, 25769803776),
    (8589934591, 1, 8589934592),
    (8589934592, 1, 8589934593),
    (17179869184, 0, 17179869184),
    (0, 17179869184, 17179869184),
    (17179869184, 17179869184, 34359738368),
    (25769803776, 25769803776, 51539607552),
    (17179869183, 1, 17179869184),
    (17179869184, 1, 17179869185),
    (34359738368, 0, 34359738368),
    (0, 34359738368, 34359738368),
    (34359738368, 34359738368, 68719476736),
    (51539607552, 51539607552, 103079215104),
    (34359738367, 1, 34359738368),
    (34359738368, 1, 34359738369),
    (68719476736, 0, 68719476736),
    (0, 68719476736, 68719476736),
    (68719476736, 68719476736, 137438953472),
    (103079215104, 103079215104, 206158430208),
    (68719476735, 1, 68719476736),
    (68719476736, 1, 68719476737),
    (137438953472, 0, 137438953472),
    (0, 137438953472, 137438953472),
    (137438953472, 137438953472, 274877906944),
    (206158430208, 206158430208, 412316860416),
    (137438953471, 1, 137438953472),
    (137438953472, 1, 137438953473),
    (274877906944, 0, 274877906944),
    (0, 274877906944, 274877906944),
    (274877906944, 274877906944, 549755813888),
    (412316860416, 412316860416, 824633720832),
    (274877906943, 1, 274877906944),
    (274877906944, 1, 274877906945),
    (549755813888, 0, 549755813888),
    (0, 549755813888, 549755813888),
    (549755813888, 549755813888, 1099511627776),
    (824633720832, 824633720832, 1649267441664),
    (549755813887, 1, 549755813888),
    (549755813888, 1, 549755813889),
    (1099511627776, 0, 1099511627776),
    (0, 1099511627776, 1099511627776),
    (1099511627776, 1099511627776, 2199023255552),
    (1649267441664, 1649267441664, 3298534883328),
    (1099511627775, 1, 1099511627776),
    (1099511627776, 1, 1099511627777),
    (2199023255552, 0, 2199023255552),
    (0, 2199023255552, 2199023255552),
    (2199023255552, 2199023255552, 4398046511104),
    (3298534883328, 3298534883328, 6597069766656),
    (2199023255551, 1, 2199023255552),
    (2199023255552, 1, 2199023255553),
    (4398046511104, 0, 4398046511104),
    (0, 4398046511104, 4398046511104),
    (4398046511104, 4398046511104, 8796093022208),
    (6597069766656, 6597069766656, 13194139533312),
    (4398046511103, 1, 4398046511104),
    (4398046511104, 1, 4398046511105),
    (8796093022208, 0, 8796093022208),
    (0, 8796093022208, 8796093022208),
    (8796093022208, 8796093022208, 17592186044416),
    (13194139533312, 13194139533312, 26388279066624),
    (8796093022207, 1, 8796093022208),
    (8796093022208, 1, 8796093022209),
    (17592186044416, 0, 17592186044416),
    (0, 17592186044416, 17592186044416),
    (17592186044416, 17592186044416, 35184372088832),
    (26388279066624, 26388279066624, 52776558133248),
    (17592186044415, 1, 17592186044416),
    (17592186044416, 1, 17592186044417),
]



def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """

    opkey = {'AND': 0, 'OR': 1, 'XOR': 2}

    keys = []
    start_vals = {x.split(":")[0].strip(): int(x.split(":")[1].strip())
             for x in data if ":" in x}

    keys.extend(start_vals.keys())
    start_vals = {keys.index(k):v for k,v in start_vals.items()}

    
    rules = []
    for row in data:
        if "->" in row:
            op, res = row.split(' -> ')
            op1, operand, op2 = op.split()

            if op1 not in keys: keys.append(op1)
            op1_key = keys.index(op1)

            if op2 not in keys: keys.append(op2)
            op2_key = keys.index(op2)

            if res not in keys: keys.append(res)
            res_key = keys.index(res)

            operand_key = opkey[operand]        
            # rules.append((op1, op2, operand, res),)
            rules.append((op1_key, op2_key, operand_key, res_key),)

    return start_vals, rules, keys



def convert_dict_to_int(registers, key) ->int:
    keys = sorted([x for x in registers if x.startswith(key)], reverse=True)
    x = ''.join([str(registers[x]) for x in keys])
    if not x:
        return 0
    return int(x, 2)

def part_1(rules, registers, keys):
    ops = {
        0: lambda x, y: x & y,
        1: lambda x, y: x | y,
        2: lambda x, y: x ^ y
        }
    
    def recurse_answer(key, stack):
        if key in registers:
            return registers[key], True
        rule = rules_dict[key]

        if rule[0] in stack: return -1, False
        op1, success = recurse_answer(rule[0], stack + [key])
        if not success: return -1, False

        if rule[1] in stack: return -1, False        
        op2, success = recurse_answer(rule[1], stack + [key])
        if not success: return -1, False

        registers[key] = ops[rule[2]](op1, op2)
        return registers[key], True
        
    rules_dict = {x[3]: x for x in rules}
    result = []
    for i in range(46):
        key = f'z{str(i).rjust(2,"0")}'
        int_key = keys.index(key)
        val, success = recurse_answer(int_key, list())
        if not success:
            return -1, [], False
        result.append(val)

    binary_string = ''.join(map(str, result[::-1]))
    decimal_result = int(binary_string, 2)

    return decimal_result, result, True


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

def test_all_bits(rules, start=0, end=999999):

    z_count = len([x for x in rules if x[3].startswith('z')])
    result = 0
    bit_count = 0
    is_broken_rule = False
    for t in test_cases[start:end]:
        x = create_registers(z_count, t[0], 'x')
        y = create_registers(z_count, t[1], 'y')
        assert t[0] + t[1] == t[2]
        assert t[0] <= 2**45 
        assert t[1] <= 2**45 
        assert t[1] <= 2**46 

        registers = {**x, **y}
        actual, bit_list = part_1(rules, deepcopy(registers))
        if not bit_list: #if the result is not a valid result, skip
            is_broken_rule = True   
            continue

        this_result = actual ^ t[2]
        if result != this_result:
            if result | this_result > result:
                result = result | this_result
                # print(f'new result found {result}')
                bit_count = bin(result).count('1')
                # print(f'Bit difference cnt: {bit_count}')

    if is_broken_rule:
        return int('1'*46, 2), 46
    return result, bit_count

def swap_rules(rules, key, newkey):
    key_rule = next(rule for rule in rules if rule[3] == key)
    key_rule_id = next(k for k,rule in enumerate(rules) if rule[3] == key)
    newkey_rule = next(rule for rule in rules if rule[3] == newkey)
    newkey_rule_id = next(k for k,rule in enumerate(rules) if rule[3] == newkey)


    rules[key_rule_id] = (key_rule[0], key_rule[1], key_rule[2], newkey_rule[3])
    rules[newkey_rule_id] = (newkey_rule[0], newkey_rule[1], newkey_rule[2], key_rule[3])  

    return rules


def find_candidates(rules, baseline):
    all_keys = [x.result for x in rules]    

    candidates = set()
    counter = 0
    for x in range(len(all_keys)):
        print(f'Outer Loop: {x} :: {all_keys[x]} :: {len(all_keys[x+1:])}')
        for y in range(x+1,len(all_keys)):
            counter += 1
            new_rules = deepcopy(rules)
            new_rules = swap_rules(new_rules, all_keys[x], all_keys[y])
            _, diff_cnt = test_all_bits(new_rules)
            # if diff_cnt == 46: print(f'broken rule',all_keys[x], all_keys[y])
            if diff_cnt < baseline:
                candidates.add((all_keys[x], all_keys[y], diff_cnt))
                print(f'New candidate found: {all_keys[x]} and {all_keys[y]} with {diff_cnt}')

            if counter % 500 == 0 :
                print(f'Counter: {counter}')


    
    return candidates



def phase_2(rules_orig, combinations)-> list:

    counter = 0
    lowest = 22
    for k1 in range(len(combinations)):
        for k2 in range(k1+1, len(combinations)):
            for k3 in range(k2+1, len(combinations)):
                for k4 in range(k3+1, len(combinations)):

                    c1 = combinations[k1]
                    c2 = combinations[k2]
                    c3 = combinations[k3]
                    c4 = combinations[k4]

                    #todo: check that none of the elements of the combination are the same
                    check_dup = set([c1[0],c1[1], c2[0],c2[1], c3[0],c3[1], c4[0],c4[1]])
                    if len(check_dup) < 8:
                        continue

                    counter += 1
                    if counter % 2000 == 0:
                        print(counter,c1,c2,c3,c4)
                        print(counter,k1,k2,k3,k4)

                    rules = deepcopy(rules_orig)
                    rules = swap_rules(rules, c1[0], c1[1])
                    rules = swap_rules(rules, c2[0], c2[1])
                    rules = swap_rules(rules, c3[0], c3[1])
                    rules = swap_rules(rules, c4[0], c4[1])

                    error_cnt = test_all_bits(rules)[1]
                    if error_cnt <= lowest:
                        lowest = error_cnt
                        print(f"Lowest: {lowest}, {c1}, {c2}, {c3}, {c4}")

                    #todo: check if the valid flag is in errors or positive results
                    if error_cnt == 0:
                        print(f"Result found: {c1}, {c2}, {c3}, {c4}")
                        print (f"Result: {error_cnt}")
                        return [c1, c2, c3, c4]
    return [('0','0'),('0','0'),('0','0'),('0','0')]


def main():
    data = get_input_data(2024, 24, sample=0)
    start_vals, rules, keys = read_input(data)

    start_time = perf_counter()
    for i in range(10000):
        actual = part_1(deepcopy(rules), deepcopy(start_vals), keys)[0]
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time} seconds")

    # start_time = perf_counter()
    # for i in range(10000):
    #     actual = part_1_recursion(deepcopy(rules), deepcopy(start_vals))[0]
    # end_time = perf_counter()
    # print(f"Time taken_Recursion: {end_time - start_time} seconds")


    # x,y,expected = get_expected(start_vals)
    
    # difference = bin(actual ^ expected)
    # print (f'({x},{y},{expected})')
    # print(f"Expected:   {bin(expected).rjust(48)} = {expected}")
    # print(f"Actual:     {bin(actual).rjust(48)} = {actual}")
    # print(f"Difference: {difference.rjust(48)} = {int(difference, 2)}")
    # print(f'Bit difference cnt: {difference.count("1")}')

    # print('testing')

    # differnece, diff_cnt = test_all_bits(rules)
    # print(f'Bit difference cnt after testing: {diff_cnt}')
    
    # candidates = find_candidates(rules, diff_cnt)

    # with open('./2024/Day24/candidates.txt','w') as f:
    #     data = f.writelines([f'{x},{y},{z}\n' for x,y,z in candidates])


    # with open('2024/Day24/candidates.txt', 'r') as f:
    #     data = f.read().splitlines()
    #     candidates = [(x.split(',')[0], x.split(',')[1], int(x.split(',')[2])) for x in data]

    # candidates = [(min(x[0], x[1]), max(x[0], x[1]), x[2]) for x in candidates] #order the pairs
    # candidates = list(set(candidates)) #remove duplicates

    # cutoff = int(input("Enter the cutoff value: "))

    # candidates = filter(lambda x: int(x[2]) < cutoff, candidates) #filter out the ones that don't do much
    # candidates = sorted(candidates, key=lambda x: x[2]) #then sort in ascending order - most effective first

    # result = phase_2(rules, candidates)

    # if result:
    #     result = [f'{min(x)},{max(x)}' for x in result]
    #     result = sorted(result, reverse=False)
    #     print(','.join(result))




if __name__ == "__main__":
    main()
