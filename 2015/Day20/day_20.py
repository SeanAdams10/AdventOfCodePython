from time import perf_counter
from utils import get_input_data, timing_decorator
from math import sqrt, floor
from functools import cache
import itertools


@cache
def prime_factors(n):
    @cache
    def fact(n):
        if n == 1:
            return [1]
        for i in range(2, n+1):
            if n % i == 0:
                new_n = n // i
                return [i] + fact(new_n)
        return []

    result = fact(n)
    return result

@cache
def multcombo(combo):
    result = 1
    for i in combo:
        result *= i
    return result


def part1(target_value):
    value_array = [10] * (target_value//10)

    for i in range(2, target_value//10):
        for index in range(i, target_value//10, i):
            value_array[index] += i*10
        if value_array[i] >= target_value:
            return i
    return -1

def part2(target_value):
    top_val = target_value//10
    value_array = [0] * top_val

    for i in range(1, top_val):
        max_iter = min((i*50) + 1, top_val)
        for index in range(i, max_iter, i):
            value_array[index] += i*11
        if value_array[i] >= target_value:
            return i
    return -1



def main():
    data = get_input_data(2015, 20, sample=0)
    target_value = int(data[0])

    result = part1(target_value)
    print('Part 1:', result)

    result = part2(target_value)
    print('Part 2:', result)

if __name__ == "__main__":
    main()
