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

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    grid = {}
    curr_r=curr_r=0
    for r, row in enumerate(data):
        if row=='' or row[0] in ('<','>', '^', 'v') :
            continue
        max_r = r+1
        for c, cell in enumerate(row):
            grid[(r,c)] = cell
            if cell == '@':
                curr_r, curr_c = r,c
     
    steps = [step for move in data for step in move if step in ('<','>', '^', 'v')]

    max_c = len(data[0])
    return grid, steps, curr_r, curr_c, max_r, max_c



def read_input_p2(data) -> list:
    grid = {}
    curr_r=curr_r=0
    for r, row in enumerate(data):
        if row=='' or row[0] in ('<','>', '^', 'v') :
            continue
        max_r = r+1
        for c, cell in enumerate(row):
            sample_value = {
                '#': '##',
                '.': '..',
                'O': '[]',
                '@': '@.'
            }.get(cell, cell)

            grid[(r,c*2)] = sample_value[0]
            grid[(r,c*2+1)] = sample_value[1]


            if cell == '@':
                curr_r, curr_c = r,c*2
     
    steps = [step for move in data for step in move if step in ('<','>', '^', 'v')]

    max_c = len(data[0])*2
    return grid, steps, curr_r, curr_c, max_r, max_c    



def move_one(grid, r,c,direction):
    new_r, new_c = ({'>': (r,c+1), '<': (r,c-1), '^': (r-1,c), 'v': (r+1,c)}).get(direction,(r,c)) 

    if grid[(new_r,new_c)] == '#':
        return r,c
    if grid[(new_r,new_c)] in ('O','[', ']'):
        move_one(grid, new_r, new_c, direction)
    if grid[(new_r,new_c)] == '.':
        grid[(new_r,new_c)], grid[(r,c)] = grid[(r,c)], grid[(new_r,new_c)]    
        return new_r, new_c
    return r,c

def is_box(cell):
    return cell in ('[',']')

def return_box(grid, cell):
    if grid[cell] == '[':
        return (cell[0], cell[1]+1)
    if grid[cell] == ']':
        return (cell[0], cell[1]-1)
    return cell

def move_one_p2(grid, source_cells,direction):
    # quick_print_grid(grid, source_cells, direction,'Current iteration - direction:')


    r_delta, c_delta = ({'>': (0,1), '<': (0,-1), '^': (-1,0), 'v': (1,0)}).get(direction,(0,0)) 
    #pick the delta based on the direction
    target_cells = set([(cell[0]+r_delta, cell[1]+c_delta) for cell in source_cells])

    if any([grid[cell] == '#' for cell in target_cells]): return False 
    if len(source_cells) ==0: return True
    # if all([grid[cell] == '.' for cell in target_cells]):
    #     return True

    new_target_cells = set()
    for cell in target_cells:
        if grid[cell] != '.':
            new_target_cells.add(cell)
        if is_box(grid[cell]):
            if direction in ('^', 'v'): 
                # if the target is a box then we need to extend the check to include other cells
                new_target_cells.add(return_box(grid, cell))

    move_one_p2(grid, new_target_cells, direction) #only recursively process the ones that are non-empty

    success = [grid[cell] == '.' for cell in target_cells.union(new_target_cells)]
    #all of the target cells must be empty - meaning that they moved correctly

    if all(success):
        for cell in source_cells:
            cell2 = (cell[0]+r_delta, cell[1]+c_delta)
            grid[cell], grid[cell2] = grid[cell2], grid[cell]
        
        # quick_print_grid(grid, source_cells, direction,'Unwind Current iteration - direction:')
        return True
    return False

def quick_print_grid(grid, source_cells, direction, title):
    print()
    print('-'*20)
    print(title, direction)
    print('Source:', source_cells)
    max_r = max([r for r,c in grid.keys()])
    max_c = max([c for r,c in grid.keys()])
    print_grid(grid, max_r, max_c)


def print_grid(grid,max_r, max_c):
    for r in range(max_r+1):
        for c in range(max_c+1):
            if (r,c) in grid.keys():
                print(grid[(r,c)], end='')
        print()

def calc_gps(grid):
    max_r = max([r for r,c in grid.keys()])
    max_c = max([c for r,c in grid.keys()])

    gps = 0
    for (r,c),value in grid.items():
        if value == 'O':
            gps += r*100 + c
        if value == '[':
            c2 = max_c - (c+1) 
            # this_gps = r*100 + min(c,c2)
            this_gps = r*100 + c
            gps += this_gps
            # print('Cell:', r,c, 'Left Dist:',c, 'Right Dist:',c2, 'GPS:', this_gps)


            
    return gps

def main():
    data = get_input_data(2024, 15, sample=0)
    grid, steps, r,c, max_r, max_c = read_input(data)

    for step in steps:
        r,c = move_one(grid, r,c,step)
        # print('Step:', step)
        # print_grid(grid, r,c, max_r, max_c)

    gps = calc_gps(grid)
    print('part 1:', gps)

    # Part 2
    grid, steps, r,c, max_r, max_c = read_input_p2(data)
    for step in steps:
        move_one_p2(grid, [(r,c)],step)
        r,c = [cell for cell in grid if grid[cell] == '@'][0]

    gps = calc_gps(grid)
    print('part 2:', gps)




if __name__ == "__main__":
    main()
