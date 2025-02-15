import re
with open('./2024/Day24b/best.txt','r') as f:
    data = f.read().splitlines()

for d in data:
    matches = re.match(r"(\d{3}):\s+\('(\w{3})\', '(\w{3})\', '(\w{3})\', '(\w{3})\', '(\w{3})\', '(\w{3})\', '(\w{3})\', '(\w{3})\'\)",d)
    # if matches:
    #     print(matches.groups())

    result = matches.groups()[0]
    t1 = tuple(sorted([matches.groups()[1], matches.groups()[2]]))
    t2 = tuple(sorted([matches.groups()[3], matches.groups()[4]]))
    t3 = tuple(sorted([matches.groups()[5], matches.groups()[6]]))
    t4 = tuple(sorted([matches.groups()[7], matches.groups()[8]]))
    x = sorted([t1, t2, t3, t4])



    print(f'{result}: {x}')