import pytest
import day_17

# pylint: disable=missing-docstring


@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 1, 'C': 1}, 0, (0, 0), 2, [], {'A': 10, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (0, 1), 2, [], {'A': 5, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (0, 2), 2, [], {'A': 2, 'B': 1, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (0, 3), 2, [], {'A': 3, 'B': 1, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (0, 4), 2, [], {'A': 0, 'B': 1, 'C': 1}),
    ({'A': 30, 'B': 2, 'C': 1}, 0, (0, 5), 2, [], {'A': 7, 'B': 2, 'C': 1}),
    ({'A': 40, 'B': 1, 'C': 4}, 0, (0, 6), 2, [], {'A': 2, 'B': 1, 'C': 4}),
])
def test_run_instruction_adv(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers

    # The adv instruction (opcode 0) performs division. 
    # The numerator is the value in the A register. 
    # The denominator is found by raising 2 to the power of the instruction's combo operand. 
    # (So, an operand of 2 would divide A by 4 (2^2); 
    # an operand of 5 would divide A by 2^B.) 
    # The result of the division operation is truncated to an integer and then written to the A register.


@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 1, 'C': 1}, 0, (1, 0), 2, [], {'A': 10, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 5, 'C': 1}, 0, (1, 1), 2, [], {'A': 10, 'B': 4, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (1, 2), 2, [], {'A': 10, 'B': 3, 'C': 1}),
    # ({'A': 30, 'B': 1, 'C': 1}, 0, (1, 3), 1, [], {'A': 3, 'B': 1, 'C': 1}),
    # ({'A': 30, 'B': 1, 'C': 1}, 0, (1, 4), 1, [], {'A': 0, 'B': 1, 'C': 1}),
    # ({'A': 30, 'B': 2, 'C': 1}, 0, (1, 5), 1, [], {'A': 7, 'B': 2, 'C': 1}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (1, 6), 2, [], {'A': 40, 'B': 8, 'C': 4}),
    ({'A': 40, 'B': 100, 'C': 4}, 0, (1, 7), 2, [], {'A': 40, 'B': 99, 'C': 4}),
])
def test_run_instruction_bxl(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers
# The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.


@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 1, 'C': 1}, 0, (2, 0), 2, [], {'A': 10, 'B': 0, 'C': 1}),
    ({'A': 10, 'B': 5, 'C': 1}, 0, (2, 1), 2, [], {'A': 10, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (2, 2), 2, [], {'A': 10, 'B': 2, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (2, 3), 2, [], {'A': 30, 'B': 3, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (2, 4), 2, [], {'A': 30, 'B': 6, 'C': 1}),
    ({'A': 30, 'B': 12, 'C': 1}, 0, (2, 5), 2, [], {'A': 30, 'B': 4, 'C': 1}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (2, 6), 2, [], {'A': 40, 'B': 4, 'C': 4}),
])
def test_run_instruction_bst(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers

# The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 0, 'B': 1, 'C': 1}, 0, (3, 0), 2, [], {'A': 0, 'B': 1, 'C': 1}),
    ({'A': 0, 'B': 1, 'C': 1}, 10, (3, 0), 12, [], {'A': 0, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 5, (3, 2), 2, [], {'A': 10, 'B': 1, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 5, (3, 0), 0, [], {'A': 10, 'B': 1, 'C': 1}),
])
def test_run_instruction_jnz(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers

@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 5, 'C': 1}, 5, (3, 1), 1, [], {'A': 10, 'B': 1, 'C': 1}),
])
def test_run_instruction_jnz_bad_operand(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    with pytest.raises(AssertionError):
        instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id) 
# The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 0, 'B': 14, 'C': 6}, 0, (4, 0), 2, [], {'A': 0, 'B': 8, 'C': 6}),
    ({'A': 1, 'B': 14, 'C': 1}, 2, (4, 0), 4, [], {'A': 1, 'B': 15, 'C': 1}),
    ({'A': 1, 'B': 100, 'C': 20}, 4, (4, 2), 6, [], {'A': 1, 'B': 112, 'C': 20}),
])
def test_run_instruction_bxc(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers
    # The bxc instruction (opcode 4) calculates the bitwise XOR of register B 
    # and register C, then stores the result in register B. (For legacy reasons, 
    # this instruction reads an operand but ignores it.)


@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 0), 2, [0], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 1), 2, [1], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 2), 2, [2], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 3), 2, [3], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 4), 2, [0], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 5), 2, [6], {'A': 40, 'B': 14, 'C': 4}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (5, 6), 2, [4], {'A': 40, 'B': 14, 'C': 4}),
])
def test_run_instruction_out(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers
    # The out instruction (opcode 5) calculates the value of its 
    # combo operand modulo 8, then outputs that value. (If a 
    # program outputs multiple values, they are separated by commas.)

@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 1, 'C': 1}, 0, (6, 0), 2, [], {'A': 10, 'B': 10, 'C': 1}),
    ({'A': 10, 'B': 5, 'C': 1}, 0, (6, 1), 2, [], {'A': 10, 'B': 5, 'C': 1}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (6, 2), 2, [], {'A': 10, 'B': 2, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (6, 3), 2, [], {'A': 30, 'B': 3, 'C': 1}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (6, 4), 2, [], {'A': 30, 'B': 0, 'C': 1}),
    ({'A': 30, 'B': 2, 'C': 1}, 0, (6, 5), 2, [], {'A': 30, 'B': 7, 'C': 1}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (6, 6), 2, [], {'A': 40, 'B': 2, 'C': 4}),
])
def test_run_instruction_bdv(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers
    # The bdv instruction (opcode 6) works exactly like the 
    # adv instruction except that the result is stored in the B register. 
    # (The numerator is still read from the A register.)

    # The numerator is the value in the A register. 
    # The denominator is found by raising 2 to the power of the instruction's combo operand. 
    # (So, an operand of 2 would divide A by 4 (2^2); 
    # an operand of 5 would divide A by 2^B.) 
    # The result of the division operation is truncated to an integer and then written to the A register.



@pytest.mark.parametrize("registers, instr_id, instr, expected_instr_id, expected_output, expected_registers", [
    ({'A': 10, 'B': 1, 'C': 1}, 0, (7, 0), 2, [], {'A': 10, 'B': 1, 'C': 10}),
    ({'A': 10, 'B': 5, 'C': 1}, 0, (7, 1), 2, [], {'A': 10, 'B': 5, 'C': 5}),
    ({'A': 10, 'B': 1, 'C': 1}, 0, (7, 2), 2, [], {'A': 10, 'B': 1, 'C': 2}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (7, 3), 2, [], {'A': 30, 'B': 1, 'C': 3}),
    ({'A': 30, 'B': 1, 'C': 1}, 0, (7, 4), 2, [], {'A': 30, 'B': 1, 'C': 0}),
    ({'A': 30, 'B': 2, 'C': 1}, 0, (7, 5), 2, [], {'A': 30, 'B': 2, 'C': 7}),
    ({'A': 40, 'B': 14, 'C': 4}, 0, (7, 6), 2, [], {'A': 40, 'B': 14, 'C': 2}),
])
def test_run_instruction_cdv(registers, instr_id, instr, expected_instr_id, expected_output, expected_registers):
    instr_id, output = day_17.run_instruction(instr[0], instr[1], registers, instr_id)
    assert instr_id == expected_instr_id
    assert output == expected_output
    assert registers == expected_registers
    # The bdv instruction (opcode 6) works exactly like the 
    # adv instruction except that the result is stored in the B register. 
    # (The numerator is still read from the A register.)

    # The numerator is the value in the A register. 
    # The denominator is found by raising 2 to the power of the instruction's combo operand. 
    # (So, an operand of 2 would divide A by 4 (2^2); 
    # an operand of 5 would divide A by 2^B.) 
    # The result of the division operation is truncated to an integer and then written to the A register.




@pytest.mark.parametrize("registers, program, expected_registers, expected_output", [
    ({"A": 0, "B": 0, "C": 9}, [2, 6], {"A": 0, "B": 1, "C": 9}, ''),
    ({"A": 10, "B": 0, "C": 9}, [5, 0, 5, 1, 5, 4], {"A": 10, "B": 0, "C": 9}, '0,1,2'),
    ({"A": 2024, "B": 0, "C": 9}, [0, 1, 5, 4, 3, 0], {"A": 0, "B": 0, "C": 9}, '4,2,5,6,7,7,7,7,3,1,0'),
    ({"A": 0, "B": 29, "C":0}, [1, 7], {"A":0, "B": 26, "C":0}, ''),
    ({"A": 0, "B": 2024, "C": 43690}, [4, 0], {"A": 0, "B": 44354, "C": 43690}, ''),
    ({"A": 729, "B": 0, "C": 0}, [0, 1, 5, 4, 3, 0], {"A": 0, "B": 0, "C": 0}, '4,6,3,5,6,3,5,2,1,0')
])

def test_part1(registers, program, expected_registers, expected_output):
    # Here you would call the function that you are testing
    # For example:
    # output = your_function(registers, program)

    instr_id, output = day_17.part_1(registers, program)
    assert output == expected_output
    assert registers == expected_registers


