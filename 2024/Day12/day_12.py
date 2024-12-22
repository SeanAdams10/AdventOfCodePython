from time import perf_counter
from itertools import product
from collections import defaultdict
from shapely.geometry import Polygon

GroupCount = defaultdict(list)

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

class GridCell():
    def __init__(self, cell, value):
        self.cell = cell
        self.value = value
        self.borders = 4
        self.area = 1
        n_delta = product([cell], [(-1,0), (1,0), (0,1), (0,-1)])
        self.neighbours = [(x[0][0] + x[1][0], x[0][1] + x[1][1]) for x in n_delta]
        self.group = None
        self.group_neighbours = set()

    def clean_offgrid_neighbours(self, grid):
        self.neighbours = [n for n in self.neighbours if n in grid.keys()]

    def __repr__(self):
        return f'{self.cell}: {self.value}'


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    result = dict()
    for r,row_data in enumerate(data):
        for c, cell_data in enumerate(row_data):
            result[(r,c)] = GridCell((r,c), cell_data)
    return result


        

# def clean_offgrid(grid):
#     for grid_c in grid:
#         grid_c.clean_offgrid_neighbours(grid)



def make_groups(grid):

    def recurse_group(inner_grid, cell, group, value):
        if inner_grid[cell.cell].value != value:
            return False
        else:
            inner_grid[cell.cell].group = group
            for c in cell.neighbours:
                new_cell = inner_grid[c]
                if not(new_cell.group):
                    if recurse_group(inner_grid, new_cell, group, value):
                        cell.group_neighbours.add(new_cell.cell)

            return True


    for cell in grid.values():
        if cell.group is None:
            recurse_group(grid, cell, cell.cell, cell.value)


def simplify_poly(poly):
    """
    Returns a new Polygon with consecutive collinear vertices removed.
    """
    # Work on the exterior ring (assuming a single-ring polygon).
    coords = list(poly.exterior.coords)
    
    # We will build a new list of coords that removes collinear points
    new_coords = [coords[0]]
    
    for i in range(1, len(coords) - 1):
        p_prev = coords[i - 1]
        p_curr = coords[i]
        p_next = coords[i + 1]
        
        # Only keep p_curr if it's not collinear
        if not are_collinear(p_prev, p_curr, p_next):
            new_coords.append(p_curr)
    
    # Add the last point (which should be same as the first for a closed ring)
    new_coords.append(coords[-1])
    
    return Polygon(new_coords)




def are_collinear(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y1 - y2) * (x1 - x3) == (y1 - y3) * (x1 - x2)


def do_part_1(grid):
    groups={}

    # Add up the groups
    for cell in grid.values():
        if cell.group in groups.keys():
            groups[cell.group]+=1
        else:
            groups[cell.group] =1
       
    for key,value in groups.items():
        print(grid[key].value, key, value)

    group_count = GroupCount
    for key,grid_cell in grid.items():
        borders = 4
        for n in grid_cell.neighbours:
            if n in grid.keys() and grid[n].value == grid_cell.value:
                borders -=1
        grid_cell.borders = borders
        #print(f'cell {grid_cell.cell}: has {borders} borders')
        group_count[grid_cell.group].append(borders)

    print(group_count)
   
    total_price = 0
    for key, value in group_count.items():
        area = len(value)
        perim = sum(value)
        price = area*perim
        total_price += price
        print(f'A region of {key} plants with price {area} * {perim} = {price}.')

    print(f'Part 1: {total_price}')


def main():
    data = get_input_data(2024, 12, sample=7)
    grid = read_input(data)
    for cell in grid.values():
        cell.clean_offgrid_neighbours(grid)
    
    make_groups(grid)

    do_part_1(grid)
    

if __name__ == "__main__":
    main()
