from time import perf_counter
from collections import namedtuple, defaultdict
from itertools import accumulate 
import re
import math 
from operator import mul
    
Robot = namedtuple("Robot", "px, py, vx, vy")

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
    rules = []
    for line in data:
        matches = re.match(r'p=(\d*),(\d*) v=(-?\d*),(-?\d*)',line)
        rules.append(Robot(*map(int, matches.groups())))
    return rules

def move_robots(robots, width, height, steps):
    final_pos = []
    for robot in robots:
        px = (robot.px + robot.vx * steps) % width
        py =  (robot.py + robot.vy * steps) % height
        final_pos.append(Robot(px, py, robot.vx, robot.vy))
    return final_pos

def render_grid(robots, width, height):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot.py][robot.px] = '#'
    return "\n".join(["".join(row) for row in grid])


def print_grid(robots, width, height):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for robot in robots:
        grid[robot.py][robot.px] = '#'
    for row in grid:
        print(''.join(row))

def print_blocked(blk, width, height):
    grid = [['.' for _ in range(width)] for _ in range(height)]
    for x,y in blk:
        grid[y][x] = '#'
    for row in grid:
        print(''.join(row))

def set_blocked(width, height, buffer):
    blocked = set()
    for x in range(width):
        for y in range(height):
            if x + y <= width // (2+buffer):
                blocked.add((x,y))
            if x >= width - width //(2+buffer) + y:
                blocked.add((x,y))

    return blocked

def main():
    data = get_input_data(2024, 14, sample=0)
    robots = read_input(data)
    width = 101
    height = 103
    # width = 11
    # height = 7
    robots = move_robots(robots, width, height, 100)


    quadrants = defaultdict(int)
    for robot in robots:
        if robot.px < width//2 and robot.py < height//2:
            quadrants[1] += 1
        elif robot.px < width//2 and robot.py >= math.ceil(height/2):
            quadrants[2] += 1
        elif robot.px >= math.ceil(width/2) and robot.py < height//2:
            quadrants[3] += 1
        elif robot.px >= math.ceil(width/2) and robot.py >= math.ceil(height/2):
            quadrants[4] += 1

    print(quadrants)
    print('Part 1:', list(accumulate(quadrants.values(), mul))[-1])


    robots = read_input(data)
    # blocked = set_blocked(width, height,3)
    # print_blocked(blocked, width, height)
    # skip = 11500000

    print(len(robots))
    loop = 0
    while True:
        robots = move_robots(robots, width, height, 1)
        loop += 1
        if loop % 1000 == 0:
            print(loop)
        # if any((robot.px, robot.py) in blocked for robot in robots):
        #     continue
        # else:
        #     print_grid(robots, width, height)
        #     input('check this one')
        if '#'*16 in str(render_grid(robots,width, height)):
            print_grid(robots, width, height)
            print(loop)
            input('check this one')



if __name__ == "__main__":
    main()
