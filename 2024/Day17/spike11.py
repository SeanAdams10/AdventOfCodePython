def change_dict(dict):
    dict[1] = 'one'
    dict[2] = 'two'
    del dict[3]
    dict[4] = 'four'


dict = {1: 'one', 2: 'two', 3: 'three'}
change_dict(dict)
print(dict)

