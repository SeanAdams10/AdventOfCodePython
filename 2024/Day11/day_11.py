from time import perf_counter
from functools import lru_cache

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
    result = [n for d in data for n in d.split()]
    return result

@lru_cache(maxsize=None)
def move_stones(cells, moves):
    result = []
    for _ in range(moves):
        current_cell = 0
        while current_cell < len(cells):
            if cells[current_cell] == '0':
                cells[current_cell] = '1'
                current_cell += 1
            elif len(cells[current_cell])%2 == 0:
                tmp_cell = cells[current_cell]
                cells[current_cell] = str(int(tmp_cell[:len(tmp_cell)//2]))
                cells.insert(current_cell+1, str(int(tmp_cell[len(tmp_cell)//2:])) )
                current_cell += 2
            else:
                cells[current_cell] = str(int(cells[current_cell])*2024)
                current_cell += 1
        result.append(len(cells))
    
    return result, cells

@lru_cache(maxsize=None)
def move_stones_2(cell, moves):
    if moves == 0:
        return 1
    if cell == '0':
        return move_stones_2('1',moves-1)
    if len(cell)%2 == 0:
        left_part = str(int(cell[:len(cell)//2]))
        right_part = str(int(cell[len(cell)//2:]))
        return move_stones_2(left_part, moves-1) + move_stones_2(right_part, moves-1)
    else:
        return move_stones_2(str(int(cell)*2024), moves-1)

@timing_decorator
def solve_part_1(data,moves):
    result = 0
    for d in data:
        result += move_stones_2(d, moves)
        
    return result
    


def main():
    data = get_input_data(2024, 11, sample=0)
    cells = read_input(data)
    
    result = solve_part_1(cells, 75)
    print(f'Part 1: {result}')

if __name__ == "__main__":
    main()
