from utils import get_input_data
from functools import lru_cache
from math import floor
import collections

@lru_cache(maxsize=20000000)
def get_next_key(input_key, step_number):
    # step = step_number % 3
    # match step:
    #     case 0: result = ((input_key * 64) ^ input_key) % 16777216
    #     case 1: result = ((input_key//32) ^ input_key) % 16777216
    #     case 2: result = ((input_key * 2048) ^ input_key) % 16777216
    # return result

    input_key = ((input_key * 64) ^ input_key) % 16777216
    input_key = ((input_key//32) ^ input_key) % 16777216
    input_key = ((input_key * 2048) ^ input_key) % 16777216
    return input_key



def main():
    data = get_input_data(2024, 22, sample=1)
    data = [int(x) for x in data]

    key_list = [[i % 10,] for i in data]


    for i in range (2000):
        for k,d in enumerate(data):
            data[k] = get_next_key(d, i)
            key_list[k].append(data[k] % 10)

    print(f'Part 1: {sum(data)}')



    diff_sets = []
    all_elements_set = set()
    for l in key_list:
        diff = [l[k+1] - l[k] for k in range(len(l)-1)]
        ds = set()
        for k,grp in enumerate(diff):
            ds.add((l[k-3],l[k-2],l[k-1],l[k]))

        all_elements_set =  all_elements_set.union(ds)
        print(len(ds))
        diff_sets.append(ds)

    print('all elements in the set',len(all_elements_set))
    all_elements = [element for grp in diff_sets for element in grp]
    counter = collections.Counter(all_elements)
    print(counter.most_common(5))


    # print(a)
    # print(diff_list)
if __name__ == "__main__":
    main()