with open('2024/Day24/candidates.txt', 'r') as f:
    data = f.read().splitlines()
    candidates = [(x.split(',')[0], x.split(',')[1], x.split(',')[2]) for x in data]

candidates = [(min(x[0], x[1]), max(x[0], x[1]), x[2]) for x in candidates]
print(len(candidates))
candidates = list(set(candidates))
print(len(candidates))
candidates = sorted(candidates, key=lambda x: (x[2], x[0], x[1]))

print(candidates)
