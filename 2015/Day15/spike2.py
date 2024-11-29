from itertools import accumulate
import operator


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

    print('Parsed input', parsed_input)
    print('Position', position)
    scores = [0 for _ in parsed_input[0]]
    for ingredient in range(len(parsed_input)):
        for attribute in range(len(parsed_input[ingredient])):
            print(ingredient, attribute,
                  parsed_input[ingredient][attribute], position[ingredient])
            scores[attribute] += parsed_input[ingredient][attribute] * \
                position[ingredient]
        print(ingredient, attribute, scores)

    total_score = list(accumulate(scores[0:-1], operator.mul))[-1]
    scores.append(total_score)
    return scores


parsed_input = ((-1, -2, 6, 3, 8),
                (2, 3, -2, -1, 3))
# scores = [0 for _ in parsed_input[0]]
# print(scores)
position = (44, 56)
# for ingredient in range(len(parsed_input)):
#     for attribute in range(len(position)):
#         scores[attribute] += parsed_input[ingredient][attribute] * \
#             position[ingredient]

# print(scores)
# total_score = list(accumulate(scores, operator.mul))[-1]
# scores.append(total_score)
# print(scores)


print(eval(parsed_input, position))
