import itertools

moves = (-1,0,1)

deltas = list(itertools.product(moves, repeat=2))
print(deltas)

print(list(itertools.permutations(moves, 2))) 
print(list(itertools.combinations(moves, 2))) 
