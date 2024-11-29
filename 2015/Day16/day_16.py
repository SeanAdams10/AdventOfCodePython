import re

with open(r'2015/Day16/Part1Input.txt', 'r') as file:
    data = file.readlines()

# Parse the input
aunts = {}
for key, line in enumerate(data):
    matches = re.findall(r'(\w+): (\d+)', line)
    new_data = {}
    for match in matches:
        new_data[match[0]] = match[1]
    aunts[key] = new_data

print(aunts[212])
match_text = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1, }

for key, aunt in aunts.items():
    mismatch = False
    for item, count in aunt.items():
        if match_text[item] != int(count):
            mismatch = True
            break

    if not mismatch:
        print('Part 1:', key+1)
        break

# Part 2
for key, aunt in aunts.items():
    mismatch = False
    for item, count in aunt.items():
        if item in ['cats', 'trees']:
            if match_text[item] >= int(count):
                mismatch = True
                break
        elif item in ['pomeranians', 'goldfish']:
            if match_text[item] <= int(count):
                mismatch = True
                break
        elif match_text[item] != int(count):
            mismatch = True
            break

    if not mismatch:
        print(key, aunt)
        print('Part 2:', key+1)
        break
