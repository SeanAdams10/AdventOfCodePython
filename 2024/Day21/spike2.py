def create_keypad()-> dict:
    keypad_dict = {
    '7': (0, 0),
    '8': (0, 1),
    '9': (0, 2),
    '4': (1, 0),
    '5': (1, 1),
    '6': (1, 2),
    '1': (2, 0),
    '2': (2, 1),
    '3': (2, 2),
    '0': (3, 1),
    'A': (3, 2),
    }

    keypad_dict_r = {v: k for k, v in keypad_dict.items()}
    return keypad_dict, keypad_dict_r

@cache
def find_paths(start, end)->list:

    grid, grid_r = create_keypad()

    if start == end:
        return ['A']
    start_cell = grid[start]
    end_cell = grid[end]
    result = []

    moves = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0),
    }
    current_dist = manhattan(start_cell, end_cell)
    for direction, move in moves.items():
        new_cell = (start_cell[0] + move[0], start_cell[1] + move[1])
        if new_cell not in grid.values():
            continue
        if manhattan(new_cell, end_cell) < current_dist:
            new_start = grid_r[new_cell]
            step = [direction + fs  for fs in find_paths(new_start, end)] 
            result.extend(step)
    return result    

def find_shortest(start, end)->list:
    candidates = find_paths(start, end)
    min_len = min([len(c) for c in candidates])
    shortest = list(filter(lambda x: len(x) == min_len, candidates))
    return shortest



def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

@cache
def create_keypad_moves()->dict:
    grid, _ = create_keypad()

    perms = list(product(grid.keys(), repeat = 2))

    result = {}
    for p in perms:
        result[p] = find_shortest(p[0], p[1])
    return result



result = create_keypad_moves()
print(result)
