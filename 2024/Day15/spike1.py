import day_15

data = [
    "##########",
    "##......##",
    "##.[]...##",
    "##[][]..##",
    "##..@...##",
    "##########"
]

grid, steps, r,c, max_r, max_c = day_15.read_input(data)
print('Original')
day_15.print_grid(grid, max_r, max_c)
expected = [
    "##########",
    "##.[]...##",
    "##..[]..##",
    "##[]@...##",
    "##......##",
    "##########"
]
expected_grid, _,_,_,_,_ = day_15.read_input(expected)

day_15.move_one_p2(grid, set([(r,c),]), '^')
print('New')
day_15.print_grid(grid, max_r, max_c)
print('Expected')
day_15.print_grid(expected_grid, max_r, max_c)