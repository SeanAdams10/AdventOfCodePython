import pytest
import day_15


def test_parse():
    inputs = ["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
              "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]
    expected = ((-1, -2, 6, 3, 8),
                (2, 3, -2, -1, 3))
    attributes = ('capacity', 'durability', 'flavor',
                  'texture', 'calories', 'overall')
    ingredients = ('Butterscotch', 'Cinnamon')

    e, a, i = day_15.parse(inputs)
    assert e == expected
    assert a == attributes
    assert i == ingredients


@pytest.mark.parametrize("position, scores", [
    ((44, 56), (68, 80, 152, 76, 520, 62842880)),
    ((100, 0), (0, 0, 600, 300, 800, 0))
])
def test_eval(position, scores):
    parsed_input = ((-1, -2, 6, 3, 8), (2, 3, -2, -1, 3))
    assert day_15.eval(parsed_input, position) == scores


@pytest.mark.parametrize("position, search_depth, expected", [
    ((33, 33, 34), 1,
        [(32, 33, 35),
         (32, 34, 34),
         (33, 32, 35),
         (33, 34, 33),
         (34, 32, 34),
         (34, 33, 33)]),
    ((50, 50), 0,
        []),
    ((50, 50), 1,
        [(49, 51),
         (51, 49)]),
    ((50, 50), 2,
        [(48, 52),
         (49, 51),
         (51, 49),
         (52, 48)]),
    ((50, 50), 3,
        [(47, 53),
         (48, 52),
         (49, 51),
         (51, 49),
         (52, 48),
         (53, 47)]),
    ((50, 50), 4,
        [(49, 51),
         (51, 49),
         (48, 52),
         (52, 48),
         (47, 53),
         (53, 47),
         (46, 54),
         (54, 46)]),
    ((50, 50), 5,
        [(49, 51),
         (51, 49),
         (48, 52),
         (52, 48),
         (47, 53),
         (53, 47),
         (46, 54),
         (54, 46),
         (45, 55),
         (55, 45)]),
    ((50, 50), 22,
        [(28, 72),
         (29, 71),
         (30, 70),
         (31, 69),
         (32, 68),
         (33, 67),
         (34, 66),
         (35, 65),
         (36, 64),
         (37, 63),
         (38, 62),
         (39, 61),
         (40, 60),
         (41, 59),
         (42, 58),
         (43, 57),
         (44, 56),
         (45, 55),
         (46, 54),
         (47, 53),
         (48, 52),
         (49, 51),
         (51, 49),
         (52, 48),
         (53, 47),
         (54, 46),
         (55, 45),
         (56, 44),
         (57, 43),
         (58, 42),
         (59, 41),
         (60, 40),
         (61, 39),
         (62, 38),
         (63, 37),
         (64, 36),
         (65, 35),
         (66, 34),
         (67, 33),
         (68, 32),
         (69, 31),
         (70, 30),
         (71, 29),
         (72, 28),
         ]),
])
def test_generate_neighbours(position, search_depth, expected):
    assert day_15.generate_neighbours(
        position, search_depth) == sorted(expected)


@ pytest.mark.parametrize("search_depth, expected", [
    (1, 62842880),
    (2, 62842880),
    (10, 62842880),
    (20, 62842880),
    (21, 62842880),
    (22, 62842880),
    (25, 62842880),
    (27, 62842880),
    (30, 62842880),
    (40, 62842880),
    (100, 62842880),
])
def test_part1_sample(search_depth, expected):
    inputs = ["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
              "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]
    parsed, _, _ = day_15.parse(inputs)
    score, position = day_15.find_best_score(parsed, search_depth=search_depth)
    assert score == expected
    pos_expected = {(44, 56), }
    assert position == pos_expected


def test_part1_full():
    with open(r'2015/Day15/Part1Input.txt') as f:
        inputs = f.readlines()
    parsed, _, _ = day_15.parse(inputs)
    expected = 18965440
    score, _ = day_15.find_best_score(parsed)
    assert score == expected


def test_part2_sample():
    inputs = ["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
              "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]
    parsed, _, _ = day_15.parse(inputs)
    score, position = day_15.find_best_score_p2(parsed, 110)
    assert score == 57600000
    pos_expected = {(40, 60), }
    assert position == pos_expected


def test_part2_full():
    with open(r'2015/Day15/Part1Input.txt') as f:
        inputs = f.readlines()
    parsed, _, _ = day_15.parse(inputs)
    expected = 15862900
    score, _ = day_15.find_best_score_p2(parsed, 20)
    assert score == expected


if __name__ == "__main__":
    pytest.main()
