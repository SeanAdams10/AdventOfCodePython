import pytest
import day_15

def test_p2_read():
    data = [
        "#####",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]
    
    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)
    assert max_r ==4
    assert max_c == 10
    assert steps == ['^']
    assert grid[(2,4)] == '@'
    assert grid[(2,5)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'
    assert r == 2
    assert c == 4


def test_p2_move_one_1():
    data = [
        "#####",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]
    
    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    day_15.move_one_p2(grid, set([(r,c),]), '^')
    assert grid[(2,4)] == '@'
    assert grid[(2,5)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'

def test_p2_move_one_2():
    data = [
        "#####",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]
    
    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    day_15.move_one_p2(grid, set([(r,c),]), '>')
    assert grid[(2,5)] == '@'
    assert grid[(2,4)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'

def test_p2_move_one_3():
    data = [
        "#####",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]
    
    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    day_15.move_one_p2(grid, set([(r,c),]), '<')
    assert grid[(2,3)] == '@'
    assert grid[(2,4)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'

def test_p2_move_one_4():
    data = [
        "#####",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]
    
    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    day_15.move_one_p2(grid, set([(r,c),]), 'v')
    assert grid[(2,4)] == '@'
    assert grid[(2,5)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'


def test_p2_move_one_block1():
    data = [
        "#####",
        "#...#",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]

    # input
    # data = [
    #     "##########",
    #     "##......##",
    #     "##..[]..##",
    #     "##..@...##",
    #     "##########",
    #     "",
    #     "^"
    # ]

    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    assert grid[(3,4)] == '@'
    assert grid[(3,5)] == '.'
    assert grid[(2,4)] == '['
    assert grid[(2,5)] == ']'

    # expected
    # data = [
    #     "##########",
    #     "##..[]..##",
    #     "##..@...##",
    #     "##......##",
    #     "##########",
    #     "",
    #     "^"
    # ]

    
    day_15.move_one_p2(grid, set([(r,c),]), '^')
    assert grid[(2,4)] == '@'
    assert grid[(3,4)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'

def test_p2_move_one_block_avoid():
    data = [
        "#####",
        "#...#",
        "#.O.#",
        "#.@.#",
        "#####",
        "",
        "^"
    ]

    grid, steps, r,c, max_r, max_c = day_15.read_input_p2(data)

    assert grid[(3,4)] == '@'
    grid[(3,5)]= '['
    grid[(3,6)]= ']'
    # input
    # data = [
    #     "##########",
    #     "##......##",
    #     "##..[]..##",
    #     "##..@[].##",
    #     "##########",
    #     "",
    #     "^"
    # ]


    # expected
    # data = [
    #     "##########",
    #     "##..[]..##",
    #     "##..@...##",
    #     "##......##",
    #     "##########",
    #     "",
    #     "^"
    # ]

    day_15.move_one_p2(grid, set([(r,c),]), '^')
    assert grid[(2,4)] == '@'
    assert grid[(3,4)] == '.'
    assert grid[(1,4)] == '['
    assert grid[(1,5)] == ']'
    assert grid[(3,5)] == '['
    assert grid[(3,6)] == ']'

def test_p2_move_one_block_cascade1():
    data = [
        "##########",
        "##......##",
        "##.[]...##",
        "##[][]..##",
        "##..@...##",
        "##########"
    ]
    grid, steps, r,c, max_r, max_c = day_15.read_input(data)

    expected = [
        "##########",
        "##.[]...##",
        "##..[]..##",
        "##[]@...##",
        "##......##",
        "##########"
    ]

    day_15.move_one_p2(grid, set([(r,c),]), '^')
    expected_grid, _,_,_,_,_ = day_15.read_input(expected)
    assert grid == expected_grid

def test_p2_move_one_block_cascade2():
    data = [
        "##########",
        "##......##",
        "##.[][].##",
        "##[][]..##",
        "##..@...##",
        "##########"
    ]
    grid, steps, r,c, max_r, max_c = day_15.read_input(data)

    expected = [
        "##########",
        "##.[][].##",
        "##..[]..##",
        "##[]@...##",
        "##......##",
        "##########"
    ]

    day_15.move_one_p2(grid, set([(r,c),]), '^')
    expected_grid, _,_,_,_,_ = day_15.read_input(expected)
    assert grid == expected_grid

