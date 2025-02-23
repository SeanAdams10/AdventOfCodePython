from utils import get_input_data, timing_decorator
from time import perf_counter
from copy import deepcopy
from functools import cache
import pickle




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
    start_vals = {x.split(":")[0].strip(): int(x.split(":")[1].strip())
             for x in data if ":" in x}
    
    rules = []
    for row in data:
        if "->" in row:
            op, res = row.split(' -> ')
            op1, operand, op2 = op.split()
            rules.append((op1.strip(), op2.strip(), operand.strip(), res.strip()),)

    return start_vals, rules



def convert_dict_to_int(registers, key) ->int:
    keys = sorted([x for x in registers if x.startswith(key)], reverse=True)
    x = ''.join([str(registers[x]) for x in keys])
    if not x:
        return 0
    return int(x, 2)

@cache
def part_1(rules: tuple, registers: tuple, largest_z: int):
    assert isinstance(rules, tuple)
    assert isinstance(registers, tuple)
    rules = list(rules)
    registers = dict(registers)
    ops = {
        'AND': lambda x, y: x & y,
        'OR': lambda x, y: x | y,
        'XOR': lambda x, y: x ^ y
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
    for i in range(largest_z+1):
        key = f'z{str(i).rjust(2,"0")}'
        val, success = recurse_answer(key, list())
        if not success:
            return -1
        result.append(val)

    binary_string = ''.join(map(str, result[::-1]))
    decimal_result = int(binary_string, 2)

    return decimal_result



def get_expected(registers):
    x = convert_dict_to_int(registers, 'x')
    y = convert_dict_to_int(registers, 'y')
    z = x+y

    return x,y,z

@cache
def create_registers(bit_count, value, prefix):
    result = dict()
    for i in range(bit_count+1):
        key = f"{prefix}" + str(i).rjust(2, "0")
        result[key] = (value >> i) & 1
    return result

def swap_rules(rules, key, newkey):
    key_rule = next(rule for rule in rules if rule[3] == key)
    key_rule_id = next(k for k,rule in enumerate(rules) if rule[3] == key)
    newkey_rule = next(rule for rule in rules if rule[3] == newkey)
    newkey_rule_id = next(k for k,rule in enumerate(rules) if rule[3] == newkey)


    rules[key_rule_id] = (key_rule[0], key_rule[1], key_rule[2], newkey_rule[3])
    rules[newkey_rule_id] = (newkey_rule[0], newkey_rule[1], newkey_rule[2], key_rule[3])  

    return rules

def find_candidates_one_bit(rules, largest_z, print_padding):
    assert isinstance(rules, tuple)
    rules = list(rules)

    all_keys = [x[3] for x in rules]    

    counter = 0
    for x in range(len(all_keys)):
        print('-'* (print_padding*4), f'Outer Loop: {x} :: {all_keys[x]} :: {len(all_keys[x+1:])}')
        for y in range(x+1,len(all_keys)):
            counter += 1
            new_rules = deepcopy(rules)
            new_rules = swap_rules(new_rules, all_keys[x], all_keys[y])
            lsb, success = find_first_broken(new_rules, largest_z, part_1, print_padding+1) 
            # _, diff_cnt = test_all_bits(new_rules, largest_z)
            if not success:
                continue
            if lsb == -1 or lsb > largest_z: 
                #if there are zero differences, or the difference is after the test bit
                print(' '*(print_padding*4), f'New candidate found: {all_keys[x]} and {all_keys[y]} with lsb = {lsb}')
                candidate = (min(all_keys[x], all_keys[y]), max(all_keys[x], all_keys[y]), lsb)
                yield candidate

            if counter % 2000 == 0 :
                print('-'*(print_padding*4), f'Counter: {counter}')

def get_lsb_index(n): #get the index of the least significant bit
    return (n & -n).bit_length() - 1

def find_first_broken(rules, largest_z, test_function, print_padding):
    """
    Finds the first broken rule in a set of rules by testing against provided test cases.
    Args:
        rules (list): A list of rules to be tested.
        largest_z (int): The largest value of 'z' to be considered in the test cases.
        test_function (function): A function that takes the rules, registers, and largest_z as input and returns the test result.
    Returns:
        tuple: A tuple containing:
            - int: The index of the first broken rule, or -1 if no broken rule is found.
            - bool: A boolean indicating whether the rules are valid (True) or broken (False).
    """

    test_cases.sort(key = lambda x: x[2])
    
    final_test_bits = 0
    for t in test_cases:
        expected = t[2]
        # if expected > 2**largest_z: continue
        x = create_registers(46, t[0], 'x')
        y = create_registers(46, t[1], 'y')
        registers = {**x, **y}
        actual = test_function(tuple(rules), tuple(registers.items()), largest_z)
        if actual == -1: #if the result is not a valid result - this means the rules are broken
            final_test_bits = -1
            break   
        
        this_test = actual ^ expected #get the bit difference between actual & expected
        final_test_bits = final_test_bits | this_test #combine the bit differences

    
    final_test_bits = final_test_bits & (2**(largest_z+1)-1) #mask the bits to only the first 46 bits
    if final_test_bits < 0: #if the rules are broken, return -1
        # print('-'*(print_padding*4), 'FindBroken: Broken Rule Found')
        return -1, False
    if final_test_bits == 0:
        # print('-'*(print_padding*4), 'FindBroken: No broken bits found')
        return -1, True
    # print('-'*(print_padding*4), f'FindBroken: Broken bit {get_lsb_index(final_test_bits)}')
    return get_lsb_index(final_test_bits), True

def test_all_bits(rules, largest_z):

    result = 0
    bit_count = 0
    is_broken_rule = False
    for t in test_cases:
        # if t[2] > 2**largest_z: continue

        x = create_registers(46, t[0], 'x')
        y = create_registers(46, t[1], 'y')

        registers = {**x, **y}
        actual = part_1(tuple(rules), tuple(registers.items()), largest_z)
        if actual < 0: #if the result is not a valid result, skip
            is_broken_rule = True   
            break

        this_result = actual ^ t[2]    #This is an XOR because you want to look for differences
        if result != this_result:
            if result | this_result > result:
                result = result | this_result
                # print(f'new result found {result}')
                bit_count = bin(result).count('1')
                # print(f'Bit difference cnt: {bit_count}')

    if is_broken_rule:
        return int('1'*46, 2), 46
    return result, bit_count


def finder(rules, applied_swaps,max_z, recurse_depth):
    first_bit, success = find_first_broken(rules, max_z, part_1, recurse_depth)
    if not success:
        return -1
    if first_bit < 0: #i.e. success with a -1 meaning no broken rules
        return applied_swaps
    if recurse_depth == 4: # if we have not found a solution after 4 swaps then fail
        return -1
    
    for c in find_candidates_one_bit(tuple(rules), first_bit, recurse_depth):
        new_rules = deepcopy(rules)
        new_rules = swap_rules(new_rules, c[0], c[1])
        result = finder(new_rules, applied_swaps + [c], max_z, recurse_depth+1)
        if result != -1:
            print('-'*(recurse_depth*4),f'Found a solution at depth {recurse_depth}')
            return result
    return -1




def main():
    file_number= int(input("Enter file number: "))
    data = get_input_data(2024, 24, sample=file_number)
    start_vals, rules = read_input(data)
    largest_z = max([x[3] for x in rules if x[3].startswith('z')])
    largest_z_int = int(largest_z[1:])

    a,b = test_all_bits(rules, largest_z_int)
    print(a,b)


    # print(part_1(tuple(rules), tuple(start_vals.items()), largest_z_int))

    print('Now into Find First Broken')
    print(find_first_broken(rules, largest_z_int, part_1, 0))
    # candidates = find_candidates(rules, 1, largest_z_int, 0)
    swaps = finder(rules, [], largest_z_int,0)
    print()
    print('Swaps')
    print(swaps)

    for key, swp in enumerate(swaps):
        print("Swaps: ", key, swp)
        rules = swap_rules(rules, swp[0], swp[1])

    print('-'*50)
    if b==0: print('Validating Success')
    smallest, success = find_first_broken(rules, largest_z_int, part_1, 0)
    print(smallest, success)
    if success and smallest == -1: print('Success')

    swaps = [(x[0], x[1]) for x in swaps]
    swap_flat = [item for sublist in swaps for item in sublist]
    swap_flat = sorted(swap_flat)

    print('Part 2 Answer')
    print(','.join(swap_flat))

if __name__ == "__main__":
    main()
