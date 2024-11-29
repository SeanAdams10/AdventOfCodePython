from itertools import combinations, permutations

with open(r'2015/Day17/Part1Input.txt', 'r') as file:
    data = file.read().splitlines()
print(data)


# sample_containers = (20, 15, 10, 5, 5)
sample_containers = tuple(map(int, data))

all_combos = []
for i in range(len(sample_containers)):
    all_combos.extend(combinations(sample_containers, i+1))

# print(all_combos)


final_set = [x for x in all_combos if sum(x) == 150]
print(final_set)
print(f'Part 1: {len(final_set)}')

min_len = min([len(x) for x in final_set])
final_set_2 = [x for x in final_set if len(x) == min_len]
print('Part 2:', len(final_set_2))
