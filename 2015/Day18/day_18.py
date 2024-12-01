from itertools import product
from numpy import array


class LightGrid:
    def __init__(self, in_data):
        result = {}
        self.rows = len(in_data)
        self.cols = len(in_data[0])

        for row, line in enumerate(in_data):
            for column, char in enumerate(line):
                neighbours = sorted(self._create_neighbours(
                    (len(in_data), len(line)), (row, column)))
                result[(row, column)] = (char == '#', *neighbours)

        self.working = result

    def _create_neighbours(self, grid, pos):
        xmax, ymax = grid
        moves = (-1, 0, 1)
        deltas = list(product(moves, repeat=2))
        deltas.remove((0, 0))  # Remove the non-move
        a = list(zip([pos] * 8, deltas))
        b = [(dx[0] + dy[0], dx[1] + dy[1]) for dx, dy in a]
        c = [(x1, y1) for x1, y1 in b if 0 <= x1 <
             xmax and 0 <= y1 < ymax]

        return c

    def __repr__(self):
        # Create the initial grid
        result = []
        for i in range(self.rows):
            result.append(['.'] * self.cols)

        # Then correct the values
        for key, value in self.working.items():
            row, col = key
            if value[0]:
                result[int(row)][int(col)] = '#'

        # And turn them into a string
        almost = []
        for row in result:
            almost.append(''.join(row))
        return '\n'.join(almost)

    def _make_one_cell_move(self, row, col):
        value, *neighbours = self.working[(row, col)]
        n_value = []
        for n in neighbours:
            n_value.append(self.working[n][0])

        # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
        # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
        if value:
            v_new = sum(n_value) in (2, 3)
        else:
            v_new = sum(n_value) == 3

        return (row, col), (v_new, *neighbours)

    def make_one_move(self):
        new_working = {}
        for key in self.working:
            row, col = key
            new_key, new_value = self._make_one_cell_move(row, col)
            new_working[new_key] = new_value

        self.working = new_working

    def set_corners(self):
        corners = [(0, 0), (0, self.cols-1), (self.rows-1, 0),
                   (self.rows-1, self.cols-1)]
        for corner in corners:
            _, *neighbours = self.working[corner]
            self.working[corner] = (True, *neighbours)

    def count_lights(self):
        new_list = [value[0] for value in self.working.values()]
        return sum(new_list)


def part_1():
    with open('2015/Day18/Part1Input.txt', 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

    grid = LightGrid(data)

    for _ in range(100):
        grid.make_one_move()
    print(f'Part 1 lights on: {grid.count_lights()}')
    del grid


def part_2():
    # with open('2015/Day18/Part1Sample.txt', 'r', encoding='utf-8') as f:
    #     data = f.read().splitlines()

    with open('2015/Day18/Part1Input.txt', 'r', encoding='utf-8') as f:
        data = f.read().splitlines()

    grid = LightGrid(data)
    grid.set_corners()

    for _ in range(100):
        grid.make_one_move()
        grid.set_corners()
    print(f'lights on P2: {grid.count_lights()}')


if __name__ == '__main__':
    part_1()
    part_2()
