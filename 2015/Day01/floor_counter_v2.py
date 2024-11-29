from itertools import accumulate


data = open("Part1Input.txt", "r", encoding="ascii").readline()


def travel(acc, c):
    return acc + (1 if c == '(' else -1)


floors_visited = list(accumulate(data, travel, initial=0))

print(floors_visited[-1])
print(next(i for i, floor in enumerate(floors_visited) if floor < 0))
