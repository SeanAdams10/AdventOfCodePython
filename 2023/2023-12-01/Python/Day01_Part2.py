import re

r = '1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine'
dctX = {n: i % 9+1 for i, n in enumerate(r.split('|'))}
print(dctX)


def findall(line):
    matches = re.findall(rf'(?=({r}))', line)
    digitMatches = [*map(dctX.get, matches)]
    print('plain map::', str(map(dctX.get, matches)))
    answer = digitMatches[0]*10 + digitMatches[-1]
    return answer


data = open('UserData.txt').read().splitlines()
total = 0
for line in data:
    total += findall(line)

print(total)


print(re.findall(rf'(?=(one|eight))', 'oneight'))
