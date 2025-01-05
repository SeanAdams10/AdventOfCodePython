combo_operand = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 'registers["A"]',
    5: 'registers["B"]',
    6: 'registers["C"]',
    7: 'X'
}

registers = {'A': 1, 'B': 2, 'C': 3}
A = 16
B = 2
C= 3




commands = {
    0: 'A = int(A / 2**combo_operand[operand])',
# The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. 
# (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
    1: 'B = B ^ operand',
    2: 'B = combo_operand[operand] % 8',
    3: 'if A: ip = operand - 2',
    4: 'B = B ^ C',
    5: 'output.append(combo_operand[operand] % 8)', 
    6: 'B = trunc(A / 2**combo_operand[operand])',
    7: 'C = trunc(A / 2**combo_operand[operand])'
}

operand = 2
A = int(A / 2**combo_operand[operand])

exec(commands[0])
print (A,B,C)





# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

# The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

# The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

# The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

# The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

# The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)



