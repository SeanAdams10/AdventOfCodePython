x = [
    ( ('a','b',10), ('a','b',15), 10),
    ( ('a','b',10), ('a','b',15), 20),
]

with open('./2024/Day24/candidates_2_pair.txt','w') as f:
    for a,b,c in x:
        f.writelines(f'{a}:{b}:{c}\n')
