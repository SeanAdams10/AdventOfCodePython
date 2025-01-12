from functools import cache
from itertools import product
from aoc_utils import manhattan


class Keypad():

    def __init__(self):
        self.keypad_dict= {
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '0': (3, 1),
            'A': (3, 2),
            }
        self.keypad_dict_r =  {v: k for k, v in self.keypad_dict.items()}
        self.keypad_moves = self.create_keypad_moves()
        

    @cache
    def find_paths(self, start, end)->list:

        grid, grid_r = self.keypad_dict, self.keypad_dict_r

        if start == end:
            return ['A']
        start_cell = grid[start]
        end_cell = grid[end]
        result = []

        moves = {
            '>': (0, 1),
            '<': (0, -1),
            '^': (-1, 0),
            'v': (1, 0),
        }
        current_dist = manhattan(start_cell, end_cell)
        for direction, move in moves.items():
            new_cell = (start_cell[0] + move[0], start_cell[1] + move[1])
            if new_cell not in grid.values():
                continue
            if manhattan(new_cell, end_cell) < current_dist:
                new_start = grid_r[new_cell]
                step = [direction + fs  for fs in self.find_paths(new_start, end)] 
                result.extend(step)
        return result    

    @cache
    def find_shortest(self,start, end)->list:
        candidates = self.find_paths(start, end)
        min_len = min([len(c) for c in candidates])
        shortest = list(filter(lambda x: len(x) == min_len, candidates))
        return shortest

    @cache
    def create_keypad_moves(self)->dict:
        perms = list(product(self.keypad_dict, repeat = 2))

        result = {}
        for p in perms:
            result[p] = self.find_shortest(p[0], p[1])
        return result
    
    
    def translate_keyinput(self, keyinput: str)->list:
        results = ['']
        keyinput = 'A' + keyinput
        for i in range(0, len(keyinput)-1):
            new = product(results, self.find_shortest(keyinput[i], keyinput[i+1]))
            results = [a+b for a,b in new]
            # print(f'From: {keyinput[i]} to: {keyinput[i+1]}',self.find_shortest(keyinput[i], keyinput[i+1]))
        return results

class Dir_Pad(Keypad):


    def __init__(self):
        self.keypad_dict = {
            '^': (0, 1),
            'A': (0, 2),
            '<': (1, 0),
            'v': (1, 1),
            '>': (1, 2)
        }
        self.keypad_dict_r = {v: k for k, v in self.keypad_dict.items()}
        self.keypad_moves = self.create_keypad_moves()


        





if __name__ == "__main__":
    # kp = Keypad()
    # print(kp.keypad_dict)
    # print(kp.keypad_dict_r)
    # print(kp.keypad_moves)

    dp = Dir_Pad()
    print(dp.keypad_dict)
    print(dp.keypad_dict_r)
    print(dp.keypad_moves)