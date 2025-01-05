from time import perf_counter
from collections import namedtuple
from functools import lru_cache
from functools import total_ordering

CellVal = namedtuple("CellVal", "r c direction")


@total_ordering
class Node():
    def __init__(self, cell, cost_g, parent_cell, goal):
        self.r, self.c, self.direction = cell
        self.parent_list = [parent_cell]
        self.cost_g = cost_g
        self.goal = goal
        self.cost_h = self.expected_cost()
        self.cost_total = self.cost_g + self.cost_h

    def key(self):
        return (self.r, self.c, self.direction)

    def __eq__(self, other):
        # Implementation of equality comparison
        return self.r == other.r and self.c == other.c and self.direction == other.direction

    def __lt__(self, other):
        # Implementation of less-than comparison
        return self.cost_total < other.cost_total

    def __repr__(self):
        return (f'cell: ({self.r},{self.c}) dir: {self.direction} '
            f'cost: g={self.cost_g} h={self.cost_h} total={self.cost_total}')

    def __str__(self):
        return (f'cell: ({self.r},{self.c}) dir: {self.direction} '
            f'cost: g={self.cost_g} h={self.cost_h} total={self.cost_total}')

    def generate_neighbours(self, grid):
        new_cell_dict = {}
        r_l = self.__rotate_left()
        r_r = self.__rotate_right()
        m_f = self.__move_forward()

        new_cell_dict[r_l.key()] = r_l
        new_cell_dict[r_r.key()] = r_r
        new_cell_dict[m_f.key()] = m_f

        new_cell_dict = {
            k: v
            for k, v in new_cell_dict.items()
            if grid.get((k[0], k[1]), '#') != '#'
        }
        return new_cell_dict

    def __rotate_left(self):
        result_node = Node((self.r, self.c, (self.direction + 1) %
                           4), self.cost_g + 1000, self, self.goal)
        return result_node

    def __rotate_right(self):
        result_node = Node((self.r, self.c, (self.direction - 1) %
                           4), self.cost_g + 1000, self, self.goal)
        return result_node

    def __move_forward(self):
        direction_delta = {0: (self.r-1, self.c+0), 1: (self.r+0, self.c+1),
                           2: (self.r+1, self.c+0), 3: (self.r+0, self.c-1)}
        result_node = Node(CellVal(
            *direction_delta[self.direction], self.direction), self.cost_g + 1, self, self.goal)
        return result_node
    
    def expected_cost(self):
        return abs(self.r - self.goal[0]) + abs(self.c - self.goal[1])




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
        print(f"Function '{func.__name__}' took {
              elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """

    grid = {}
    for r, row in enumerate(data):
        for c, cell in enumerate(row):
            grid[(r, c)] = cell

    return grid


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



def get_closest(open_nodes):
    closest_cell = min(open_nodes, key=lambda k: open_nodes[k].cost_g)
    # print(f'Closest cell: {open_nodes[closest_cell]}')
    return closest_cell

def update_open_nodes(open_nodes, visited_nodes,  new_nodes):
    for k, v in new_nodes.items():
        #if we've found a cheaper way to a visited node then remove it from visited and add it to open
        if k in visited_nodes.keys():
            if visited_nodes[k].cost_total > v.cost_total:
                open_nodes[k] = v
                del visited_nodes[k]

        #if we've found a cheaper way to an open node then update the open node
        if k in open_nodes.keys():
            if open_nodes[k].cost_total > v.cost_total:
                open_nodes[k] = v
            elif open_nodes[k].cost_total == v.cost_total:
                #if we have the same cost then add the parent list to the open node to allow for similar paths
                open_nodes[k].parent_list.extend(v.parent_list)
        else:
            if k not in visited_nodes.keys() and k not in open_nodes.keys():
                open_nodes[k] = v
    return open_nodes

def search(grid):

    # Main Code for A* search here
    goals = [CellVal(*k, dir) for k, v in grid.items()
             for dir in (0, 1, 2, 3) if v == 'E']
    goal_cell = (goals[0][0], goals[0][1])

    starting_pos = [CellVal(*k, 1) for k, v in grid.items() if v == 'S'][0]
    starting_node = Node(cell = starting_pos, cost_g=0, parent_cell=None, goal = goal_cell)

    visited_nodes = {}
    visited_nodes[starting_pos] = starting_node

    open_nodes = {}
    open_nodes = starting_node.generate_neighbours(grid)

    while True:
        focus_node = get_closest(open_nodes)

        new_nodes = open_nodes[focus_node].generate_neighbours(grid)

        visited_nodes[focus_node] = open_nodes[focus_node]
        del open_nodes[focus_node]

        update_open_nodes(open_nodes, visited_nodes,  new_nodes)

        for goal in goals:  # have we hit the goal?
            if goal in visited_nodes.keys():
                return visited_nodes[goal]


def main():
    data = get_input_data(2024, 16, sample=0)
    grid = read_input(data)
    final_node = search(grid)
    print('Part 1:', final_node.cost_total)

    node_set = set()
    r,c, _ = final_node.key()
    node_set.add((r,c))
    working_list = [final_node]
    while len(working_list) > 0:
        working_node = working_list.pop()
        r,c, _ = working_node.key()
        node_set.add((r,c))
        if len(working_node.parent_list) >1:
            print('2 parents found')
            print(working_node)
        for parent in working_node.parent_list:
            if parent:
                working_list.append(parent)
        


    print('Part 2:', len(node_set))


if __name__ == "__main__":
    main()
