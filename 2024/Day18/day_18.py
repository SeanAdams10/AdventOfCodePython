from time import perf_counter

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

def print_grid(grid, title):
    print()
    print('-'*20)
    print(title)
    max_r = max([r for r, c in grid.keys()])
    max_c = max([c for r, c in grid.keys()])

    for r in range(max_r+1):
        for c in range(max_c+1):
            if (r, c) in grid.keys():
                print(grid[(r, c)], end='')
        print()

def manhattan(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_neighbours(current, grid, closed):
    surround = [(0,1), (1,0), (0,-1), (-1,0)]
    r,c = current
    neighbours = [(r+s[0],c+s[1]) for s in surround]
    neighbours = [n for n in neighbours if n in grid and grid[n] == '.' and n not in closed]

    return neighbours   

def part1(grid,maxr, maxc):
    start = (0,0)
    end = (maxr-1, maxc-1)
    closed = {}
    open = {start: (0, manhattan(start, end), manhattan(start, end), None)}

    while end not in closed:
        current = min(open, key = lambda x: open[x][2])
        neighbours = get_neighbours(current, grid, closed)
        for n in neighbours:
            g = open[current][0] + 1
            h = manhattan(n, end)
            cell_val = (g, h, g+h, current)
            if n in open:
                if open[n][2] > cell_val[2]:
                    open[n] = cell_val
            else:
                open[n] = cell_val
        closed[current] = open[current]
        # grid[current] = 'O' 
        # print_grid(grid, f'Current grid, current: {current}')
        del open[current]
        if not open and end not in closed:
            print('No path found')
            raise ValueError('No path found')   
    
    return closed[end][0], closed, open


def read_input(data, rows, columns, limit) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """

    grid = {(r,c): '.' for r in range(rows) for c in range(columns)}
    for r in data[:limit]:
        cell = tuple(map(int, r.split(',')))
        grid[cell] = '#'
    return grid


def main():
    # data = get_input_data(2024, 18, sample=1)
    # maxr = 7
    # maxc = 7
    # maxiter = 12

    data = get_input_data(2024, 18, sample=0)
    maxr = 71
    maxc = 71
    maxiter = 1024

    grid = read_input(data,maxr,maxc, maxiter)
    print_grid(grid, 'Initial grid')

    distance, closed, open = part1(grid, maxr, maxc)
    print(f'Part 1: {distance}')

    for r in range(maxiter, len(data)):
        try:
            grid = read_input(data,maxr,maxc, r+1)
            distance, closed, open = part1(grid, maxr, maxc)
            print(f'Part 2 success: {r} {distance}') 
        except ValueError:
            print(f'Part 2 no path: {r} data: {data[r]}')
            break






if __name__ == "__main__":
    main()
