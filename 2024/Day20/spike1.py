import re

data = '#.#.##.#'
matches = re.finditer(r'(?=(\.#{1,2}\.))', data)
for m in matches:
    print(f'Matched {m.group(1)} at positions {m.start(1)}-{m.end(1)}')
