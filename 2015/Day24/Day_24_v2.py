from utils import get_input_data, timing_decorator
import itertools
import math

def part_1():
    data = get_input_data(2015, 24, sample=0)
    data = [int(x) for x in data]

    target_val = sum(data)//3

    min_length = len(data)
    min_quant = float('inf')

    for i in range(2,(len(data)//3)+1):
        combos = itertools.combinations(data, i)
        for combo in combos:
            if sum(combo) == target_val:
                if len(combo) < min_length:
                    min_length = len(combo)
                    min_quant = math.prod(combo)
                    print(f'Min length: {min_length}, Min Quant: {min_quant}')
                if len(combo) == min_length and math.prod(combo) < min_quant:
                    min_quant = math.prod(combo)
                    print(f'Min length: {min_length}, Min Quant: {min_quant}')

def part_2():
    data = get_input_data(2015, 24, sample=0)
    data = [int(x) for x in data]

    target_val = sum(data)//4

    min_length = len(data)
    min_quant = float('inf')

    for i in range(2,(len(data)//3)+1):
        combos = itertools.combinations(data, i)
        for combo in combos:
            if sum(combo) == target_val:
                if len(combo) < min_length:
                    min_length = len(combo)
                    min_quant = math.prod(combo)
                    print(f'Min length: {min_length}, Min Quant: {min_quant}')
                if len(combo) == min_length and math.prod(combo) < min_quant:
                    min_quant = math.prod(combo)
                    print(f'Min length: {min_length}, Min Quant: {min_quant}')                







if __name__ == "__main__":
    part_1()
    part_2()