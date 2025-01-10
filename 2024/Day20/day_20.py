from time import perf_counter
import re
from functools import cache
import sys
from itertools import combinations
from collections import Counter


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
    grid = {}
    for r,d in enumerate(data):
        for c, char in enumerate(d):
            grid[(r,c)] = char
    
    data_t = []
    for c in range(len(data[0])):
        col = ''.join([data[r][c] for r in range(len(data))])
        data_t.append(col)

    data = [d.replace('S', '.').replace('E', '.') for d in data]
    data_t = [d.replace('S', '.').replace('E', '.') for d in data_t]
    return grid, data, data_t

@cache
def manhattan(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_neighbours(current, grid, closed):
    surround = [(0,1), (1,0), (0,-1), (-1,0)]
    r,c = current
    neighbours = [(r+s[0],c+s[1]) for s in surround]
    neighbours = [n for n in neighbours if n in grid and grid[n] == '.' and n not in closed]

    return neighbours   

def find_astar_solution(grid,start, end, yield_flag = False):
    closed = {}
    open = {start: (0, manhattan(start, end), manhattan(start, end), None)}

    while end not in closed:
        current = min(open, key = lambda x: open[x][2])
        yield current
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





def find_matches(data: list, data_t: list) -> list:
    result = []
    for r,d in enumerate(data):
        matches = re.finditer(r'(?=(\.#{1,2}\.))', d)
        for m in matches:
            flip_cell = []
            for c in range(m.start(1)+1, m.end(1)):
                cell = r,c
                flip_cell.append(cell)
            this_match = ((r, m.start(1)), (r, m.end(1)), m.group(1), flip_cell)
            result.append(this_match)

    for c,d in enumerate(data_t):
        matches = re.finditer(r'(?=(\.#{1,2}\.))', d)
        for m in matches:
            flip_cell = []
            for r in range(m.start(1)+1, m.end(1)):
                cell = r,c
                flip_cell.append(cell)
            this_match = ((m.start(1),c), (m.end(1), c), m.group(1), flip_cell)
            flip_cell = []
            result.append(this_match)

    return result


def part_1():
    data = get_input_data(2024, 20, sample=0)
    grid, data, data_t = read_input(data)

    maxr = max([r for r, c in grid.keys()])
    maxc = max([c for r, c in grid.keys()])
    start = [k for k,v in grid.items() if v =='S'][0]
    end = [k for k,v in grid.items() if v =='E'][0]
    grid[end] = '.'
    grid[start] = '.' 

    matches = find_matches(data, data_t)
    for m in matches:
        print(m)


    original_distance,_,_ = find_astar_solution(grid, start, end)
    print(f"Distance to end: {original_distance}")

    distance_saved ={}
    for m in matches:
        grd_temp = grid.copy()
        for r,c in m[3]:
            grd_temp[(r,c)] = '.'

        distance,_,_ = find_astar_solution(grd_temp, start, end)
        saving = original_distance - distance
        if saving in distance_saved:
            distance_saved[saving]+=1
            
        else:
            distance_saved[saving] = 1
        print(f"Distance to end: {distance}, saving: {saving}")

    inscope = [v for k,v in distance_saved.items() if k >= 100]
    total = sum(inscope)
    print(total)


def find_matches_2(moves:list, max: int) -> list:
    options = list(combinations(range(len(moves)), 2))
    print(options)
    original_dist = len(moves)-1
    matches = {}
    for o in options:
        start  = o[0]
        mid = manhattan(moves[o[0]], moves[o[1]])
        end = len(moves) - o[1]
        total = start + mid + end-1
        # print(f'Option: {o}, move 1: {moves[o[0]]}, move 2: {moves[o[1]]}, start: {start}, mid: {mid}, end: {end}, total: {total}')
        if mid <=max and total<original_dist:
            matches[o] = original_dist-total

    return matches


def part_2():
    data = get_input_data(2024, 20, sample=1)
    grid, data, data_t = read_input(data)

    maxr = max([r for r, c in grid.keys()])
    maxc = max([c for r, c in grid.keys()])
    start = [k for k,v in grid.items() if v =='S'][0]
    end = [k for k,v in grid.items() if v =='E'][0]
    grid[end] = '.'
    grid[start] = '.'

    moves = []
    for current in find_astar_solution(grid, start, end):
        moves.append(current)

    options = find_matches_2(moves,2) 
    distances = Counter(options.values())
    for k in sorted(distances):
        print(f'There are {distances[k]} cheats that save {k} picoseconds.')




    # for o in options:
    #     first_part,_,_ = find_astar_solution(grd_temp, start, o[0])
    #     mid_part = manhattan(o[0], 0[1])
    #     end_part,_,_ = find_astar_solution(grd_temp, o[1], end)
    #     total = first_part + mid_part + end_part





if __name__ == "__main__":
    # part_1()
    part_2()


