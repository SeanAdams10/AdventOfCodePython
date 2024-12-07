from collections import namedtuple
from itertools import groupby
import re

grid_cell = namedtuple("grid_cell", ['row', 'col', 'val', 'l_diag', 'r_diag'])


def getinput(sample: int = 0) -> list:

    filename = r"./2024/Day04/"
    if sample > 0:
        filename = filename + "Sample" + str(sample) + ".txt"
    else:
        filename = filename + "Input.txt"
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def parse_input(data: list) -> list:
    rows = data
    cols_list = [[x[i] for x in rows] for i in range(len(rows[0]))]
    cols = ["".join(x) for x in cols_list]


def extract_rows_and_cols(data: list) -> tuple:
    rows = data
    cols_list = [[x[i] for x in rows] for i in range(len(rows[0]))]
    cols = ["".join(x) for x in cols_list]
    return rows, cols


def create_cell_list(rows):
    cell_list = []
    for r_id, row in enumerate(rows):
        for c_id, cell in enumerate(row):
            this_cell = grid_cell(r_id, c_id, cell, r_id+c_id, r_id-c_id)
            cell_list.append(this_cell)
    return cell_list


def extract_diagonals(cell_list):
    l_diag_sorted = sorted(cell_list, key=lambda x: (x.l_diag, x.row, x.col))
    l_diag_list = []
    for _, group in groupby(l_diag_sorted, key=lambda x: x.l_diag):
        l_diag_list.append("".join([x.val for x in group]))

    r_diag_sorted = sorted(cell_list, key=lambda x: (x.r_diag, x.col, x.row))
    r_diag_list = []
    for _, group in groupby(r_diag_sorted, key=lambda x: x.r_diag):
        r_diag_list.append("".join([x.val for x in group]))

    return l_diag_list, r_diag_list


if __name__ == "__main__":
    data = getinput(0)
    rows, cols = extract_rows_and_cols(data)
    cell_list = create_cell_list(rows)
    l_diag_list, r_diag_list = extract_diagonals(cell_list)
    all_strings = rows + cols + l_diag_list + r_diag_list

    # get the count by doing a regex match across all rows, cols, and diagonals
    cnt = sum([len(re.findall('XMAS', x)) + len(re.findall('SAMX', x))
               for x in all_strings])
    print(f'Part 1: {cnt}')


# Part 2
patterns = ('MAS', 'SAM')
counter = 0
for r in range(1, len(rows)-1):
    for c in range(1, len(rows[0])-1):
        diag_1 = rows[r-1][c-1] + rows[r][c] + rows[r+1][c+1]
        diag_2 = rows[r-1][c+1] + rows[r][c] + rows[r+1][c-1]
        if diag_1 in patterns and diag_2 in patterns:
            counter += 1

print(f'Part 2: {counter}')
