

tests = [(10, 65525),
         (0, 65535),
         (65535, 0)]

for test in tests:
    input, expected = test
    print(f'input: {input}, expected: {expected}, actual: {~input & 0xffff}')
    print(f'input: {input}, expected: {
          expected}, actual: {operator.invert(input)}')
    print(f'input: {input}, expected: {expected}, actual: {
          operator.inv(input) & 0xffff}')
