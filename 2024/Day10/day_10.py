from time import perf_counter
from itertools import product

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
    grd_values={}
    for r, d in enumerate(data):
        for c,v in enumerate(d):
            if v.isdigit():
                grd_values[(r,c)] = int(v)
            else:
                grd_values[(r,c)] = -1                
    max_r=len(data)-1
    max_c= len(data[0])-1
    
    grd_neighbours = {}
    for x in grd_values:
        combo = product([x], [(-1,0),(+1,0), (0,-1), (0,+1)])
        grd_neighbours[x] = [(current[0] + delta[0], current[1]+ delta[1]) for current, delta in combo]
        grd_neighbours[x] = list(filter(lambda x: 0<=x[0]<=max_r and 0<=x[1]<=max_c, grd_neighbours[x]))

    return grd_values, grd_neighbours


def main():
    data = get_input_data(2024, 10, sample=0)
    grd_values, grd_neighbours = read_input(data)
    print(grd_neighbours)

    trail_heads = [cell for cell, value in grd_values.items() if value == 0]
    result={}
    for t in trail_heads:
        current_edge = set([t])
        for i in range(1,10):
            current_edge = set([n for e in current_edge for n in grd_neighbours[e] if grd_values[n]==i])
        result[t] = len(current_edge)

    print(f'Part 1 {sum(result.values())}')

    trail_heads = [cell for cell, value in grd_values.items() if value == 0]
    result={}
    for t in trail_heads:
        current_path = [[t],]
        for i in range(1,10):
            next = []
            for p in current_path:
                next_nodes = [p + [n] for n in grd_neighbours[p[-1]] if grd_values[n]==i]
                next.extend(next_nodes)
            current_path = next
        result[t] = current_path
    
    result_count = [len(x) for x in result.values()]
    print(f'Part 2 {sum(result_count)}')




if __name__ == "__main__":
    main()
