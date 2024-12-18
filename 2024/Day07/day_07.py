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


def read_input(data) -> dict:
    """
    placeholder for the parser needed for this day's puzzle
    """
    result = []
    for row in data:
        total = int(row.split(':')[0])
        remainder = list(map(int, row.split(':')[1].strip().split()))
        result.append((total, remainder))
    return result


def process_rule(target, values, includeConcat=False):
    if len(values) == 1:
        return values[0] == target
    # try multiplication
    testvalues = [values[0]*values[1]] + values[2:]
    if process_rule(target, testvalues, includeConcat):
        return True
    # try addition
    testvalues = [values[0]+values[1]] + values[2:]
    if process_rule(target, testvalues, includeConcat):
        return True
    # try concatenation
    if includeConcat:
        testvalues = [int(str(values[0]) + str(values[1]))] + values[2:]
        if process_rule(target, testvalues, includeConcat):
            return True

    return False


def main():
    data = get_input_data(2024, 7, sample=0)
    parsed = read_input(data)
    print(parsed)

    running_sum = 0
    for total, values in parsed:
        if process_rule(total, values):
            running_sum += total

    print(f'Part 1: {running_sum}')

    running_sum = 0
    for total, values in parsed:
        if process_rule(total, values, True):
            print(f'{total} = {values} is True')
            running_sum += total
        else:
            print(f'{total} = {values} is False')

    print(f'Part 2: {running_sum}')


if __name__ == "__main__":
    main()
