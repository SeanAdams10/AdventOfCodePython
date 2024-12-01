"""
Solution for day 1 of the Advent of Code 2024.
"""


from itertools import product


def parse_input(in_data):
    """
    converts the input file into two lists of integers
    params:
    in_data: list of strings
    returns: 
    two lists of integers
    """
    in_data = [(int(x.split()[0]), int(x.split()[1])) for x in in_data]

    # split these tuples into two lists
    lst1, lst2 = zip(*in_data)
    lst1 = sorted(list(lst1))
    lst2 = sorted(list(lst2))
    return lst1, lst2


def part_1(lst1, lst2):
    """
    calculates the sum of the absolute differences between the two lists
    """
    result = sum([abs(x[0] - x[1]) for x in zip(lst1, lst2)])
    return result


def part_2(lst1, lst2):
    """
    calculates the sum of the products of the matching elements in the two lists
    """
    result = sum([x[1] for x in product(lst1, lst2) if x[0] == x[1]])
    return result


if __name__ == '__main__':
    with open(r'./2024/Day01/input.txt', 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

    list1, list2 = parse_input(data)

    part1_answer = part_2(list1, list2)
    print(part1_answer)

    part2_answer = part_2(list1, list2)
    print(part2_answer)
