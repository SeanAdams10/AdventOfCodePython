from time import perf_counter
from itertools import combinations, product
from functools import cache
from keypad import Keypad, Dir_Pad
from utils import get_input_data, timing_decorator, shortest_list



kp = Keypad()
dp = Dir_Pad()

#Consolidate into one dictionary
translate = kp.keypad_moves
for k,v in dp.keypad_moves.items():
    translate[k] = v



@cache
def get_min_cost(this_str, level, max_level):
    if level == max_level:
        return len(this_str)

    costs = []
    for k,s in enumerate(this_str):
        from_val = 'A' if k==0 else this_str[k-1]
        to_val = s
        new_str = translate[(from_val, to_val)]
        if isinstance(new_str, str):
            #if there's only a single translation
            potential_cost = get_min_cost(x, level+1, max_level)
        elif isinstance(new_str, list):
            #if there's a list of translation options
            potential_cost = min([get_min_cost(x, level+1, max_level) for x in new_str])
        costs.append(potential_cost)
    
    return sum(costs)

    # for k,v in translate.items():
    #     new_str = this_str + k
    #     if new_str in costs:
    #         continue
    #     costs.append(get_min_cost(new_str, level+1, max_level))
    # return 1 + sum(costs)


# @timing_decorator
def main():
    # Sample part 1
    data = get_input_data(2024, 21, sample=1)
    costs = [get_min_cost(x,0,3) for x in data]
    complexity = [int(v[:3])*costs[k] for k,v in enumerate(data)]
    print(f'Part 1 Sample: {sum(complexity)}')
    assert sum(complexity) == 126384

    # Actual part 1
    data = get_input_data(2024, 21, sample=0)
    costs = [get_min_cost(x,0,3) for x in data]
    complexity = [int(v[:3])*costs[k] for k,v in enumerate(data)]
    print(f'Part 1 Actual: {sum(complexity)}')
    assert sum(complexity) == 248108

    # Actual part 2
    data = get_input_data(2024, 21, sample=0)
    costs = [get_min_cost(x,0,26) for x in data]
    complexity = [int(v[:3])*costs[k] for k,v in enumerate(data)]
    print(f'Part 1 Actual: {sum(complexity)}')
    assert sum(complexity) == 303836969158972











if __name__ == "__main__":
    main()
