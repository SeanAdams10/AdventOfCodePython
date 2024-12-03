import re

def split_lines_do_dont(input_data: list) -> list:
    input_data = "don't()do()" + input_data
    allparts = []
    parts = input_data.split(r"don't()")
    # print(parts)
    for part in parts:
        # print ("part: ", repr(part))
        new_parts = part.split(r'do()')
        # print("new parts: ", new_parts)
        allparts.extend(new_parts[1:]) #ignore the first part after the do
    
    result = [x for x in allparts if x]  #remove empty strings
    return result

with open("2024/Day03/input.txt") as f:
    data = f.read()

grps = re.findall(r"mul\(\d*,\d*\)", data)

total = 0
for grp in grps:
    # print(str(grp))
    x, y = map(int, grp[4:-1].split(","))
    total += x*y

print(f'Part 1: {total}')

######
# Part 2

total = 0
split_lines = split_lines_do_dont(data)
print ('#' * 20)
print("Split Lines", split_lines)
print ('#' * 20)

for line in split_lines:
    print(line)
    grps = re.findall(r"mul\(\d*,\d*\)", line)
    print(grps)
    for grp in grps:
        print(str(grp))
        x, y = map(int, grp[4:-1].split(","))
        total += x*y
        
print(f'Part 2: {total}')