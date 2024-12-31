from time import perf_counter
import re
from collections import namedtuple
from math import ceil

Row = namedtuple('Row', ['ax', 'ay', 'bx', 'by', 'tx', 'ty'])

def get_input_data(year: int, day: int, sample: int = 0) -> list:
    """
    Reads either the sample or the puzzle input data
    :param year: The year of the puzzle
    :param day: The day of the puzzle
    :param sample: The sample number (0 for puzzle input)
    :return: A list of strings
    """
    root = rf"{year}/Day{str(day).zfill(2)}/"

    if sample == 0:
        file = root + "input.txt"
    else:
        file = root + rf"sample{str(sample)}.txt"
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    if not data:
        raise FileNotFoundError("Input data file is empty")
    return data

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    i=0
    rules = []
    while i+2 < len(data):
        matches = re.match(r'.*X([\+\-]\d*), Y([\+\-]\d*)', data[i])
        if matches:
            ax = int(matches.group(1))
            ay = int(matches.group(2))

        matches = re.match(r'.*X([\+\-]\d*), Y([\+\-]\d*)', data[i+1])
        if matches:
            bx = int(matches.group(1))
            by = int(matches.group(2))

        matches = re.match(r'.*X=(\d*), Y=(\d*)', data[i+2])
        if matches:
            tx = int(matches.group(1))
            ty = int(matches.group(2))

        rules.append(Row(ax, ay, bx, by, tx, ty))
        i+=4
    return rules


def solve_rule(ax, ay, bx, by, tx, ty):
    b = (ay * tx - ax * ty) / (ay*bx - ax * by)
    a = (tx - b * bx) / ax
    cost = 3*a + b
    if int(a) == ceil(a) and int(b) == ceil(b):
        return a, b, cost
    else:
        return 0,0,0

def main():
    data = get_input_data(2024, 13, sample=0)
    rules = read_input(data)
    print(rules)

    sum_a = sum_b = sum_cost = 0
    for rule in rules:
        a, b, cost = solve_rule(
            rule.ax, rule.ay, rule.bx, rule.by, rule.tx, rule.ty
        )
        sum_a += a
        sum_b += b
        sum_cost += cost
    
    print(f"Part 1: Sum a: {sum_a} Sum b: {sum_b} Sum cost: {sum_cost}")

    # Part 2
    sum_a = sum_b = sum_cost = 0
    for rule in rules:
        a, b, cost = solve_rule(
            rule.ax, rule.ay, rule.bx, rule.by, 
            rule.tx + 10000000000000, rule.ty + 10000000000000
        )
        sum_a += a
        sum_b += b
        sum_cost += cost

    print(f"Part 2: Sum a: {sum_a} Sum b: {sum_b} Sum cost: {sum_cost}")
    

if __name__ == "__main__":
    main()
