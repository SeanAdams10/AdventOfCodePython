

points = []
with open('2024/Day17/match_8.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_10.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_12.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_14.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_16.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_18.csv','r') as f:
    points.extend([int(line.strip()) for line in f])
with open('2024/Day17/match_20.csv','r') as f:
    points.extend([int(line.strip()) for line in f])

all_values = list(set(points))
all_values.sort()
differences = list({y - x for x, y in pairwise(all_values)})
differences.sort()
print(differences)

with open('2024/Day17/gaps.csv','w') as f:
    for x in differences:
        f.write(f"{x}\n")
