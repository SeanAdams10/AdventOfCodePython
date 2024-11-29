import re
from itertools import accumulate, product
import operator
from functools import lru_cache


def parse(inputs):
    parsed = []
    ingredients: list = []
    attributes: tuple = ('capacity', 'durability', 'flavor',
                         'texture', 'calories', 'overall')
    for input_line in inputs:
        matches = re.match(
            r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', input_line)
        parsed.append(tuple(int(matches.group(x)) for x in range(2, 7)))
        # parsed.append((int(matches.group(2)), int(matches.group(3)),
        #                int(matches.group(4)), int(matches.group(5)), int(matches.group(6)))
        # parsed[matches.group(1)] = {'capacity': int(matches.group(2)),
        #                             'durability': int(matches.group(3)),
        #                             'flavor': int(matches.group(4)),
        #                             'texture': int(matches.group(5)),
        #                             'calories': int(matches.group(6))}
        ingredients.append(matches.group(1))

    return tuple(parsed), tuple(attributes), tuple(ingredients)


def eval(parsed_input, position):
    """
    evaluates the scores of a particular cookie based on the ingredients and their quantities
    param: parsed_input: tuple: The parsed input from the input file.   format is
        parsed = ((-1, -2, 6, 3, 8),
                (2, 3, -2, -1, 3))
    param: position: tuple: The position of each ingredient in the cookie
        position = (44, 56)
    return: tuple: the scores of the cookie
        scores = (68, 80, 152, 76, 62842880)
    """

    # print('Parsed input', parsed_input)
    # print('Position', position)
    scores = [0 for _ in parsed_input[0]]
    for ingredient in range(len(parsed_input)):
        for attribute in range(len(parsed_input[ingredient])):
            # print(ingredient, attribute,
            #       parsed_input[ingredient][attribute], position[ingredient])
            scores[attribute] += parsed_input[ingredient][attribute] * \
                position[ingredient]
        # print(ingredient, attribute, scores)

    scores = [max(0, score) for score in scores]
    # clean out negative scores

    total_score = list(accumulate(scores[0:-1], operator.mul))[-1]
    scores.append(total_score)
    return tuple(scores)


def generate_neighbours(position, search_depth=1):
    """
    this generates all the neighbours of a given position
    param: position: tuple: the coordinates of this item
        example: (33, 33, 34)
    param: search_depth: int: the depth of the search
    return: list: a list of all the neighbours of this position


    """
    ingredient_cnt = len(position)
    moves = (x for x in range(-search_depth, search_depth + 1))
    # generate all possible moves for each ingredient on a single axis
    # e.g. (-1, 0, 1) for search_depth = 1
    direction_delta = list(product(moves, repeat=ingredient_cnt))
    direction_delta = [delta for delta in direction_delta if sum(
        delta) == 0 and any(delta)]  # remove the 0, 0, 0 move

    # convert the dictionary to a list of tuples to enable zipping
    positions_list = list(position)
    new_position_result = list()

    for delta in direction_delta:

        pos_zip = list(zip(positions_list, delta))
        new_pos = tuple(pos + move_val for pos, move_val in pos_zip)

        if sum(new_pos) == 100:
            if all(0 <= x <= 100 for x in new_pos):
                new_position_result.append(new_pos)

    return sorted(new_position_result)


def find_best_score(parsed_input, search_depth=1):
    best_score = 0
    best_positions = set()
    found_better: bool = True

    # create the starting position, close to the middle of the search space
    pos = []
    for index, ingredient in enumerate(parsed_input):
        if index != len(parsed_input) - 1:
            pos.append(int(100 / len(parsed_input)))
        else:
            pos.append(100 - sum(pos))
        # in other words - if it's the last ingredient, then just assign the remaining value to it
    pos = tuple(pos)
    best_positions.add(pos)
    best_score = eval(parsed_input, pos)[-1]
    print('-'*50)
    print(f'Best Score Starting: {best_score}')
    print(f'Best Positions: {best_positions}')

    while found_better:
        found_better = False
        for best_position in best_positions:
            for new_pos in generate_neighbours(best_position, search_depth):
                # print('new position:', new_pos)
                pos_score = eval(parsed_input, new_pos)[-1]
                if pos_score > best_score:
                    best_score = pos_score
                    best_positions = set()
                    best_positions.add(new_pos)
                    found_better = True
                elif pos_score == best_score:
                    best_positions.add(new_pos)

            if found_better:
                print(f'Best Score: {best_score}')
                print(f'Best Positions: {best_positions}')

    return best_score, best_positions


def find_best_score_p2(parsed_input, search_depth=110):
    best_score = 0
    best_positions = set()
    found_better: bool = True

    # create the starting position, close to the middle of the search space
    pos = []
    for index, ingredient in enumerate(parsed_input):
        if index != len(parsed_input) - 1:
            pos.append(int(100 / len(parsed_input)))
        else:
            pos.append(100 - sum(pos))
        # in other words - if it's the last ingredient, then just assign the remaining value to it
    pos = tuple(pos)
    best_positions.add(pos)
    starting_score = eval(parsed_input, pos)
    if starting_score[-2] != 500:
        best_score = -1
    else:
        best_score = eval(parsed_input, pos)[-1]

    print('-'*50)
    print(f'Best Score Starting: {best_score}')
    print(f'Starting Score: {starting_score}')
    print(f'Best Positions: {best_positions}')

    while found_better:
        found_better = False
        for best_position in best_positions:
            for new_pos in generate_neighbours(best_position, search_depth):
                # print('new position:', new_pos)
                pos_score = eval(parsed_input, new_pos)[-1]
                if pos_score > best_score and eval(parsed_input, new_pos)[-2] == 500:
                    best_score = pos_score
                    best_positions = set()
                    best_positions.add(new_pos)
                    found_better = True
                elif pos_score == best_score:
                    best_positions.add(new_pos)

            if found_better:
                print(f'Best Score: {best_score}')
                print(f'Best Positions: {best_positions}')

    return best_score, best_positions


if __name__ == "__main__":
    inputs = ["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
              "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]
    parsed_input, attributes, ingredients = parse(inputs)
    # position = (50, 50)
    best_score, _ = find_best_score(parsed_input, 22)
    print('Part 1 Sample Answer:', best_score)  # 62842880

    best_score, pos = find_best_score_p2(parsed_input, 110)
    print('Part 2 Sample Answer:', best_score, ' Pos:', pos)  # 62842880

    with open(r"2015/Day15/Part1Input.txt", 'r', encoding="ascii") as f:
        inputs = f.readlines()
    parsed_input, _, _ = parse(inputs)

    best_score, _ = find_best_score_p2(parsed_input, 20)
    print('Part 2 Full Answer:', best_score)  # 15862900

    # best_score, pos = find_best_score_p2(parsed_input, 110)
    # print('Part 2 Full Answer:', best_score, ' Pos:', pos)  # 62842880
