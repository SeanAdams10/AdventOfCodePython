from time import perf_counter
from itertools import combinations, product
from keypad import Keypad, Dir_Pad

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


def shortest_list(candidates: list) -> list:
    print(f'startign length: {len(candidates)}')
    min_len = min([len(c) for c in candidates])
    shortest = list(filter(lambda x: len(x) == min_len, candidates))
    print(f'endig length: {len(shortest)}')
    return shortest


def main():
    data = get_input_data(2024, 21, sample=1)
    kp = Keypad()
    dp = Dir_Pad()
    answer = {}

    for code in data:
        paths = kp.translate_keyinput(code)
        print(f'Code: {code} length of Path0: {len(paths[0])} count: {len(paths)}')
        paths1 = []
        for p in paths:
            paths1.extend (dp.translate_keyinput(p))
        paths1 = shortest_list(paths1)
        print(f'Code: {code} length of Path1: {len(paths1[0])} count: {len(paths1)}')

        paths2 = []
        for p in paths1[:1]:
            paths2.extend (dp.translate_keyinput(p))
        paths2 = shortest_list(paths2)
        print(f'Code: {code} length of Path2: {len(paths2[0])} count: {len(paths2)}')    

        paths3 = []
        for p in paths2[:1]:
            paths3.extend (dp.translate_keyinput(p))
        paths3 = shortest_list(paths3)
        print(f'Code: {code} length of Path3: {len(paths3[0])} count: {len(paths3)}')    

        answer[code] = len(paths3[0])

    print(answer)
    complexity = [int(k[:3])*v for k,v in answer.items()]
    print(complexity)
    print (sum(complexity))











if __name__ == "__main__":
    main()
