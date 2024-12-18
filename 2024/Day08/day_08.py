from itertools import combinations


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
    placeholder for the parser needed for this day's puzzle
    """
    grid = {(row, col): y for row, x in enumerate(data)
            for col, y in enumerate(x)}
    groups = {}
    for key, val in grid.items():
        if val != '.':
            groups[val] = groups.get(val, []) + [key]
    return grid, groups


def get_antinodes(grd, groups, part_2=0):
    antinodes = set()
    for _, val in groups.items():
        combo = combinations(val, 2)
        for c in combo:
            c = sorted(c)
            row_dist = c[1][0] - c[0][0]
            col_dist = c[1][1] - c[0][1]

            i = 1 if part_2 == 0 else 0
            while True:
                point1 = (c[0][0] - row_dist*i, c[0][1] - col_dist*i)
                point2 = (c[1][0] + row_dist*i, c[1][1] + col_dist*i)
                if point1 in grd:
                    antinodes.add(point1)
                if point2 in grd:
                    antinodes.add(point2)
                if not (point1 in grd or point2 in grd):
                    break
                if part_2 == 0:
                    break
                i += 1

    return antinodes


def main():
    data = get_input_data(2024, 8, sample=0)
    grd, groups = read_input(data)

    antinodes = get_antinodes(grd, groups, 0)
    print(f'Part 1: {len(antinodes)}')

    antinodes = get_antinodes(grd, groups, 1)
    print(f'Part 2: {len(antinodes)}')


if __name__ == "__main__":
    main()
