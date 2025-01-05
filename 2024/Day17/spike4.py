from functools import cache
import itertools
import math

@cache
def div_check(x,depth):
    if depth == 1:
        return int(x/8)
    else:
        return int(div_check(x, depth-1)/8)

depth_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
def valid_number(x, depth):
    global depth_list
    # checks = list(range(1,depth+1))
    checks = list(map(lambda d: div_check(x, d), depth_list))
    if checks[-1]==0 and all([x!=0 for x in checks[:-1]]):
        return True
    else:
        return False
    
def valid_a_value(min_val=0, target_depth=16):
    min_val = max(min_val, 8**(target_depth-1)-1)
    #I've confirmed that the first valid value is at 8**(target_depth-1)-1

    max_val = 8**(target_depth+2)

    for i in itertools.count(min_val):
        valid = valid_number(i, target_depth)
        if valid:
            yield i

def find_min_max():
    target_depth = 16
    min_val = 8**(target_depth-1)-5
    max_val = 8**(target_depth-1)-1
    test_Val = min_val

    for _ in range(10):
        test_Val = min_val + int((max_val - min_val)/2)
        print(min_val, test_Val, max_val, abs(max_val - min_val))
        if valid_number(test_Val, target_depth):
            max_val = test_Val
            print('Valid', test_Val, math.log(test_Val, 8))
        else:
            min_val = test_Val
            print('Invalid', test_Val, math.log(test_Val, 8))
        if max_val <= min_val:
            break

if __name__ == "__main__":
    found = 0
    with open('2024/Day17/valid_values.csv','w') as f:
    
        for a in valid_a_value(min_val=8**14, target_depth=16):
            found += 1
            f.write(f"{a}\n")
            if found>100000:
                break




