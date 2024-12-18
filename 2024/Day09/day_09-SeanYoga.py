from itertools import groupby

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
    result = []
    for i in range(len(data[0])//2+1):
        result.extend([str(i)]*int(data[0][i*2]))
        if i < len(data[0])//2:
            result.extend(['.']*int(data[0][i*2+1]))

    return result


def main():
    data = get_input_data(2024, 9, sample=1)
    inbound_data = read_input(data)

    # while '.' in inbound_data:
    #     dot = inbound_data.index('.')
    #     inbound_data[dot] = inbound_data[-1]
    #     inbound_data.pop()
    #     # print(inbound_data)
    #     # print('.', end='')

    # total = 0
    # for key, val in enumerate(inbound_data):
    #     total += int(val)*key

    # print(f'Part 1: {total}')

    for key, value in groupby(inbound_data):
        print(key, list(value))


if __name__ == "__main__":
    main()
