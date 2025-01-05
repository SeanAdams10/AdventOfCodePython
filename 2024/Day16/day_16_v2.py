from time import perf_counter
from collections import namedtuple
from functools import lru_cache

CellVal = namedtuple("CellVal", "r c direction")
Cell = namedtuple("Cell", "r c")

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

    grid={}
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            grid[(r,c)] = cell

    return grid

def print_grid(grid, title):
    print()
    print('-'*20)
    print(title)
    max_r = max([r for r,c in grid.keys()])
    max_c = max([c for r,c in grid.keys()])

    for r in range(max_r+1):
        for c in range(max_c+1):
            if (r,c) in grid.keys():
                print(grid[(r,c)], end='')
        print()

@lru_cache(None)
def expected_cost(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def search(grid):

    def rotate_left(direction):
        return (direction +1) % 4
    
    def rotate_right(direction):
        return (direction - 1) % 4


    def generate_neighbours(cell_value, cost):
        nonlocal goal_cell
        new_cell_dict = {}
        r,c, direction = cell_value
        direction_delta = {0: (r-1,c+0), 1: (r+0,c+1), 2: (r+1,c+0), 3: (r+0,c-1)}
        new_cell = CellVal(*direction_delta[direction],direction)
        new_cell_dict[new_cell] = (cost[0]+1, expected_cost(new_cell, goal_cell),0) #go forward
        new_cell_dict[(r, c,rotate_left(direction))] = (cost[0]+1000, cost[1],0) #rotate left
        new_cell_dict[(r, c,rotate_right(direction))] = (cost[0]+1000, cost[1],0) #rotate right

        new_cell_dict = {
            k: (v1, v2, v1 + v2)
            for k, (v1, v2, _) in new_cell_dict.items()
            if grid.get((k[0], k[1]), '#') != '#' and k not in visited.keys()
        }
        return new_cell_dict

    # def get_closest(open_nodes):
    #     closest = open_nodes.values()[0][2]
    #     closest_cell = open_nodes.keys()[0]
    #     for k,v in visited.items():
    #         if v[2] < closest:
    #             closest = v[2]
    #             closest_cell = k
    #     return closest_cell
    
    def get_closest(open_nodes):
        closest_cell = min(open_nodes, key=lambda k: open_nodes[k][2])
        return closest_cell


    #Main Code for A* search here
    starting_pos = [CellVal(*k,1) for k,v in grid.items() if v == 'S'][0]
    goals = [CellVal(*k,dir) for k,v in grid.items() for dir in (0,1,2,3) if v == 'E' ]
    goal_cell = Cell(goals[0][0], goals[0][1])

    visited = {}
    visited[starting_pos] = (0,expected_cost(starting_pos,goal_cell),0)

    open_nodes = {}
    open_nodes = generate_neighbours(starting_pos, visited[starting_pos])

    while True:
        focus_cell = get_closest(open_nodes)
        new_cells = generate_neighbours(focus_cell, open_nodes[focus_cell])
        visited[focus_cell] = open_nodes[focus_cell]
        del open_nodes[focus_cell]

        open_nodes.update(new_cells)

        # print('Focus cell:', focus_cell)
        # print(f'Visited: {len(visited)} Open: {len(open_nodes)}')
        # print(get_closest(open_nodes), open_nodes[get_closest(open_nodes)])
        # print()

        for goal in goals: #have we hit the goal?
            if (goal) in visited.keys():
                return visited[goal]



def main():
    data = get_input_data(2024, 16, sample=1)
    grid = read_input(data)
    r = search(grid)
    print('Part 1:', r) 


if __name__ == "__main__":
    main()
