from time import perf_counter
from itertools import product
from collections import defaultdict
from shapely.geometry import Polygon
from rtree import index

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
        self.cells = [cell]
        self.value = value
        self.borders = 4
        self.area = 1
        self.poly = Polygon([(cell[0], cell[1]), (cell[0]+1, cell[1]), (cell[0]+1, cell[1]+1), (cell[0], cell[1]+1)])
    
    def __repr__(self):
        return f"GridCell({self.cells}, {self.value})"

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    result = list()
    for r,row_data in enumerate(data):
        for c, cell_data in enumerate(row_data):
            result.append(GridCell((r,c), cell_data))
    return result


def plot_polygons(grid):
    import matplotlib.pyplot as plt

    # Plot the original polygons for reference
    for cell in grid:
        x, y = cell.poly.exterior.xy
        plt.plot(x, y, linestyle='--', label=f'Polygon {cell.value}')
        # Add labels to each polygon
        centroid = cell.poly.centroid
        plt.text(centroid.x, centroid.y, cell.value, fontsize=12, ha='center')

    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Merged Polygon Visualization')
    plt.show()


def make_groups(grid):
    # Build an R-tree spatial index
    spatial_index = index.Index()
    for i, cell in enumerate(grid):
        spatial_index.insert(i, cell.poly.bounds)

    changes_made = True
    while changes_made:
        changes_made = False
        for key, cell in enumerate(grid):
            if not(cell.value): # skip empty cells
                continue
            candidate_indices = list(spatial_index.intersection(cell.poly.bounds))
            result = {i:grid[i] for i in candidate_indices if isinstance(grid[i].poly.union(cell.poly),Polygon) and i!= key and grid[i].value == cell.value}
            for i,r in result.items():
                cell.cells.extend(r.cells)
                cell.poly = cell.poly.union(r.poly)
                cell.area += r.area
                r.value =''
                r.cells = []
                r.Poly = None
                changes_made = True

            if changes_made:
                # rebuild index
                # spatial_index = index.Index()
                # for i, cell in enumerate(grid):
                #     if cell.value:
                #         spatial_index.insert(i, cell.poly.bounds)
                print(f'Number of cells remaining: {len([cell for cell in grid if cell.value])}')                
            


        grid = [cell for cell in grid if cell.value]
        print(f'Number of cells remaining: {len(grid)}')                
        # rebuild index
        spatial_index = index.Index()
        for i, cell in enumerate(grid):
            spatial_index.insert(i, cell.poly.bounds)

    return grid


def are_collinear(p1, p2, p3):
    """
    Returns True if points p1, p2, p3 are collinear using cross product == 0.
    """
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) == (p3[0] - p2[0]) * (p2[1] - p1[1])

def simplify_polygon(poly_list):
    i=-1
    new_poly = list(poly_list[:-1]) #remove the last one since it's a duplicate of the first
    while i < len(new_poly)-1:
        p1 = new_poly[i-1]
        p2 = new_poly[i]
        p3 = new_poly[i+1]
        if are_collinear(p1, p2, p3):
            new_poly.pop(i)
        else:
            i += 1

    new_poly.append(new_poly[0]) #close the circle
    return new_poly

def simplfy_inner_and_outer(poly):
    outer = list(poly.exterior.coords)
    inner = [list(hole.coords) for hole in poly.interiors]
    new_outer = simplify_polygon(outer)
    new_inner = [simplify_polygon(hole) for hole in inner]
    return Polygon(new_outer, new_inner)


def main():
    data = get_input_data(2024, 12, sample=0)
    grid = read_input(data)

    grid = make_groups(grid)
    # plot_polygons(grid)

    part1_total = 0
    part2_total = 0
    for cell in grid:
        cell.poly = simplfy_inner_and_outer(cell.poly)
        area = cell.poly.area
        perimeter = cell.poly.length
        price = area * perimeter
        sides = len(cell.poly.exterior.coords) - 1
        for hole in cell.poly.interiors:
            sides += len(hole.coords) - 1

        p2price = sides * area
        # print(f"Cell {cell.cells} with value '{cell.value}' has area {area} and perimeter {perimeter} and price {price}")
        print(f"Cell {cell.poly} with value '{cell.value}' has area {area} and perimeter {perimeter} and sides {sides} and price {p2price}")
        part1_total += price
        part2_total += p2price
    # do_part_1(grid)

    print(f"Part 1: {part1_total}")
    print(f"Part 2: {part2_total}")
    

if __name__ == "__main__":
    # poly_test = Polygon([(4, 4), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)])
    # coord_list = [(2, 1.333), (2, 2), (0, 2), (0, 0), (2, 0), (2, 1.333)]
    # poly_2 = simplify_polygon(coord_list)
    # poly_test2 = simplfy_inner_and_outer(poly_test)
    # print(repr(poly_2))
    main()


