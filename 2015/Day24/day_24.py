from time import perf_counter
from utils import get_input_data, timing_decorator
from functools import cache
import math


min_length = float('inf')
visited = set()

def return_combos(unused: tuple, target: int, grp1: tuple, grp2: tuple, grp3: tuple)-> tuple:
    global min_length

    if len(grp1) > min_length:
        return None

    #poor man's memoization
    global visited
    if (grp1, grp2, grp3) in visited:
        return None
    visited.add((grp1, grp2, grp3))

    unused = tuple(sorted(unused, reverse=True))

    final_list = set()
    if not unused:
        if sum(grp1) == target and sum(grp2) == target and sum(grp3) == target:
            if len(grp1) < min_length:
                min_length = len(grp1)
                print(min_length)
            if len(grp1) == min_length:
                print("Found one: ", grp1, grp2, grp3)
                return ((grp1, grp2, grp3),)
    elif sum(grp1) > target or sum(grp2) > target or sum(grp3) > target:
        return None

    result = set()
    for i in unused:
        new_unused = tuple(x for x in unused if x != i)
        new_grp1 = tuple(sorted(grp1 + (i,)))
        new_grp2 = grp2
        new_grp3 = grp3
        if len(new_grp1) <= min_length:
            result = return_combos(new_unused, target, new_grp1, new_grp2, new_grp3)
        if result:
            final_list.update(result)

        new_grp1 = grp1
        new_grp2 = tuple(sorted(grp2 + (i,)))
        new_grp3 = grp3
        result = return_combos(new_unused, target, new_grp1, new_grp2, new_grp3)
        if result:
            final_list.update(result)

        new_grp1 = grp1
        new_grp2 = grp2
        new_grp3 = tuple(sorted(grp3 + (i,)))
        result = return_combos(new_unused, target, new_grp1, new_grp2, new_grp3)
        if result:
            final_list.update(result)
        

    return final_list



def main():
    data = get_input_data(2015, 24, sample=0)
    data = [int(x) for x in data]
    global min_length
    min_length = len(data)//2

    options = return_combos(tuple(data), sum(data)//3, tuple(), tuple(), tuple())
    options_2 = [(g1, g2, g3, len(g1), math.prod(g1)) for g1, g2, g3 in options]

    options_2.sort(key=lambda x: (x[3], x[4]))
    print(options_2[0][4])


if __name__ == "__main__":
    main()
