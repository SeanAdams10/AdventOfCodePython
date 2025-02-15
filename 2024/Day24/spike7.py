# List of tuples (x, y, z) where z is the sum of x and y
test_cases = [
    (0, 0, 0),   # 0 + 0 = 0
    (0, 1, 1),   # 0 + 1 = 1
    (1, 0, 1),   # 1 + 0 = 1
    (1, 1, 2),   # 1 + 1 = 2
    (1, 2, 3),   # 1 + 2 = 3
    (2, 1, 3),   # 2 + 1 = 3
    (2, 2, 4),   # 2 + 2 = 4
    (3, 3, 6),   # 3 + 3 = 6 (double carry over)
    (2**45, 2**45, 2**46),  # Test carry over at bit 45
    (2**46, 2**46, 2**47),  # Test carry over at bit 46
    (2**45 - 1, 1, 2**45),  # Test carry over from bit 0 to bit 45
    (2**46 - 1, 1, 2**46),  # Test carry over from bit 0 to bit 46
    (2**45, 1, 2**45 + 1),  # Test no carry over at bit 45
    (2**46, 1, 2**46 + 1),  # Test no carry over at bit 46
]

# Adding test cases for bits between 1 and 45
for i in range(1, 45):
    test_cases.append((2**i, 2**i, 2**(i+1)))  # Test carry over at bit i
    test_cases.append((2**i - 1, 1, 2**i))     # Test carry over from bit 0 to bit i
    test_cases.append((2**i, 1, 2**i + 1))     # Test no carry over at bit i

# Print the test cases
for case in test_cases:
    print(case)