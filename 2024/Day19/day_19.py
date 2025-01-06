from time import perf_counter
from functools import cache, lru_cache

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
    towels = [x for x in data if ',' in x]
    towels = (y.strip() for x in towels for y in x.split(','))
    designs = [x for x in data if len(x) > 0 and ',' not in x]


    return tuple(towels), tuple(designs)

@lru_cache(maxsize=100000)
def process_one_design(towels: tuple, design: str, allow_multiple: bool)-> list:
    """
    Processes one design
    :param towels: A tuple of towels
    :param design: A string representing a design
    :return: A list of towels
    """
    if len(design) == 0:
        return 0
    result = 0
    for t in towels:
        if design == t:
            result += 1
        if design[:len(t)]==t:
            sub = process_one_design(towels, design[len(t):], allow_multiple)
            result += sub
    return result


def main():
    data = get_input_data(2024, 19, sample=0)
    towels, designs = read_input(data)
    print(towels)
    print(designs)

    # design_check = [process_one_design(towels, d) for d in designs]
    design_check = []
    for d in designs:
        design_check.append(process_one_design(towels, d, False))
        # print(f'Processed design {d}')
    design_result = [d >0 for d in design_check]
    print(f'Part 1: {sum(design_result)}')

    design_check = []
    for d in designs:
        design_check.append(process_one_design(towels, d, True))
        print(f'Processed design {d} for length {design_check[-1]}')
    design_result = sum(design_check)
    print(f'Part 2: {design_result}')


 
if __name__ == "__main__":
    main()
