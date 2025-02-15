import time
from itertools import permutations, combinations





def return_combos (nodes):
    nodes = sorted(list(nodes))
    for perm in permutations(nodes, 8):
        if perm[0] < perm[1] and perm[2] < perm[3] and perm[4] < perm[5] and perm[6] < perm[7]:
            if perm[0]< perm[2] < perm[4] < perm[6]:
                yield perm

def return_combos_2 (nodes):
    for n in combinations(nodes, 4):
        for a in nodes:
            if a in n: continue
            a_dash = list(n) + [a]
            for b in nodes:
                if b in a_dash: continue
                b_dash = a_dash + [b]
                for c in nodes:
                    if c in b_dash: continue
                    c_dash = b_dash + [c]
                    for d in nodes:
                        if d in c_dash: continue
                        if n[0] < a and n[1] < b and n[2] < c and n[3] < d:
                            yield (n[0], a, n[1], b, n[2], c, n[3], d)


start_time = time.perf_counter()
limit = 18
rc1 = set()
rc3 = set()
for x in return_combos(range(limit)):
    rc1.add(tuple(x))
    rc3.add(tuple([(x[0], x[1]), (x[2], x[3]), (x[4], x[5]), (x[6], x[7])]))
end_time = time.perf_counter()

print(f"Time taken: {end_time - start_time} seconds")
print(len(rc1))
print(len(rc3))



start_time = time.perf_counter()
rc2= set()
for x in return_combos_2(range(limit)):
    rc2.add(tuple(x))
end_time = time.perf_counter()
print(f"Time taken: {end_time - start_time} seconds")
print(len(rc2))

