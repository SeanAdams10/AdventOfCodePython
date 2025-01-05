import day_17

numbers = [
    202356708354602,
    202425427831338,
    202425427831341,
    202356708354605,
    202356708354607,
    202425427831343
]

data = day_17.get_input_data(2024, 17, sample=0)

for n in numbers:
    registers, program = day_17.read_input(data)
    _, _, _, output = day_17.part_1(n, registers['B'], registers['C'], tuple(program))
    program_s = ','.join([str(p) for p in program])
    print(n)
    print(program_s)
    print(output)
    if output == program_s:
        print('Match Found')

