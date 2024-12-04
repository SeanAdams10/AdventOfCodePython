import re


def split_lines_do_dont(input_data: list) -> list:
    input_data = "don't()do()" + input_data
    allparts = []
    parts = input_data.split(r"don't()")
    for part in parts:
        new_parts = part.split(r'do()')
        allparts.extend(new_parts[1:])  # ignore the first part after the do

    result = [x for x in allparts if x]  # remove empty strings
    return result


def do_mult(split_lines):
    total = 0
    for line in split_lines:
        grps = re.findall(r"mul\(\d*,\d*\)", line)
        for grp in grps:
            x, y = map(int, grp[4:-1].split(","))
            total += x*y

    return total


with open("2024/Day03/input.txt") as f:
    data = f.read()

######
# Part 1

part_1_data = [data]
print(f'Part 1: {do_mult(part_1_data)}')

######
# Part 2

split_lines = split_lines_do_dont(data)
print(f'Part 2: {do_mult(split_lines)}')
