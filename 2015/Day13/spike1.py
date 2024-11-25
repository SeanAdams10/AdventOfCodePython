from itertools import permutations
unique_guests = set(["Alice", "Bob", "Carol", "David"])

tables = permutations(unique_guests)
for table in tables:
    print(table)
