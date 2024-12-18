from collections import deque, namedtuple
coord = namedtuple('coord', 'r,c')
import time


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


def read_input(data) -> list:
    """
    Reads the input data and returns the grid, the starting position, and the maximum size of the grid
    :param data: The input data
    :return: The grid as a list of coords (named tuple)
    :return: the starting position as a coord (named tuple)
    :return: maximum size of the grid
    :raises: none
    """
    grid = {coord(r, c): cell for r, row in enumerate(data)
            for c, cell in enumerate(row) if cell == '#'}
    start = [coord(r, c) for r, row in enumerate(data)
             for c, cell in enumerate(row) if cell == '^'][0]
    print(f'start: {start}')
    max_x, max_y = len(data), len(data[0])

    return grid, start, coord(max_x, max_y)


def step(grid, start, max_size):
    """
    steps through the grid, starting at the given position, and rotating at each block.   Returns the set of visited positions, and keeps a full move history to look for circles
    :param grid: The grid with blockers
    :param start: The starting position
    :param max_size: The maximum size of the grid
    :return: The set of visited positions
    :raises ValueError: If we have been here before
    """
    moves = deque([coord(-1, 0), coord(0, 1), coord(1, 0), coord(0, -1)])
    current = coord(start.r, start.c)
    visited = set()
    visited.add(current)
    move_hist = set((current, moves[0]))
    next_pos = coord(current.r + moves[0].r, current.c + moves[0].c)
    # print(current)
    while 0 <= next_pos.r < max_size.r and 0 <= next_pos.c < max_size.c:  # While we are within the grid
        if next_pos in grid:  # we only store blockers in the grid
            moves.rotate(-1)
        else:
            # we have been here before, travelling in the same direction
            if (next_pos, moves[0]) in move_hist:
                raise ValueError('We have been here before')
            current = next_pos
            visited.add(current)
            move_hist.add((current, moves[0]))
        next_pos = coord(current.r + moves[0].r, current.c + moves[0].c)
        # print(current)
    return visited


def find_blockers(grid, start, max_size, visited):
    """
    It checks all the positions which were visited in part 1 to see if adding a block there would cause a circuit
    :param grid: The grid with blockers
    :param start: The starting position
    :param max_size: The maximum size of the grid
    :param visited: The set of visited positions from part 1
    :return: The set of positions which would cause a circuit
    """
    options = visited - set([start])  # don't consider the starting position
    solutions = set()
    for pos in options:
        grd_new = dict(grid)
        grd_new[pos] = '#'

        try:
            _ = step(grd_new, start, max_size)
        except ValueError:
            solutions.add(pos)

    return solutions


def main():
    data = get_input_data(2024, 6, sample=0)
    start_time = time.time()
    
    grid = {}
    start = max_size = coord(0, 0)
    grid, start, max_size = read_input(data)
    visited = step(grid, start, max_size)
    print(f'Part 1: {len(visited)}')
    end_time = time.time()
    duration = end_time-start_time
    print(f'Duration: {duration}')
    
    # blk = find_blockers(grid, start, max_size, visited)
    # print(f'Part 2: {len(blk)}')


if __name__ == "__main__":
    main()
