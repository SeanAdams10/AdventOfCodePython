combo_operand = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 'registers["A"]-1',
    5: 'registers["B"]',
    6: 'registers["C"]*2',
    7: 'X'
}

combo_operand = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 'A-1',
    5: 'B',
    6: 'C*2',
    7: 'X'
}



registers = {'A': 1, 'B': 2, 'C': 3}
A = 1
B = 2
C= 3

for i in range(7):
    value = combo_operand[i]
    if isinstance(value, str):
        value = eval(value,{"A": registers["A"], "B": registers["B"], "C": registers["C"], "X": 0})
    print(value)


exec('A=-90', {}, registers)
print(registers['A'])
