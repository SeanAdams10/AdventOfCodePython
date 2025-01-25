# from itertools import combinations, permutations

# a = set([1,2,3,4,5])

# b = set(permutations(a, 4))
# c = set(combinations(a, 4))

# print('Permutations')
# print(b)
# print('Combinations')
# print(c)



x = set([5,4,3,2,1])
b = set([1,2,3,4])

print(b.intersection(x) == b)
print(b.issubset(x))

