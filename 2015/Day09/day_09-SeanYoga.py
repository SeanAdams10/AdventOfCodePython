from itertools import permutations


class RouteFinder:
    def __init__(self, distance_list):
        self.locations = set()
        self.distances = {}
        for item in distance_list:
            line = item.split(' ')
            # print(line)
            self.locations.add(line[0])
            self.locations.add(line[2])   
            self.distances[(line[0], line[2])] = int(line[4])
            self.distances[(line[2], line[0])] = int(line[4])



with open('Part1Input.txt', 'r', encoding='ascii') as file:
    distance_list = file.readlines()
    
# distance_list = [
#     'London to Dublin = 464',
#     'London to Belfast = 518',
#     'Dublin to Belfast = 141',
# ]

tst = RouteFinder(distance_list)

all_combinations = list(permutations(tst.locations))

answers = set()
for c in all_combinations:
    total_distance = 0
    for i in range(len(c)-1):
        total_distance += tst.distances[(c[i], c[i+1])]
    answers.add(total_distance)

print(f'Part1: {min(answers)}')
print(f'Part2: {max(answers)}')