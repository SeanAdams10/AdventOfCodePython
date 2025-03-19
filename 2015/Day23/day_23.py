from time import perf_counter
from utils import get_input_data, timing_decorator

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """

    result = []
    for line in data:
        a,b = line.split(' ',1)
        c=0
        if ',' in b:
            b,c = b.split(',')
        value = (a,b,int(c))

        result.append(value)
    return result





def main():
    data = get_input_data(2015, 23, sample=0)
    rules = read_input(data)

    a,b = calc_registers(rules, 0,0)
    print(f"Part 1: Value of register b is {b}")

    a,b = calc_registers(rules, 1,0)
    print(f"Part 2: Value of register b is {b}")


def calc_registers(rules,a,b):
    instruction_id = 0

    while instruction_id >=0 and instruction_id < len(rules):
        instruction = rules[instruction_id]
        match instruction[0]:
            case 'hlf':
                if instruction[1] == 'a':
                    a //= 2
                elif instruction[1] == 'b':
                    b //= 2
                else:  raise ValueError(f"Invalid register {instruction[1]}")
                instruction_id += 1
            case 'tpl':
                if instruction[1] == 'a':
                    a *= 3
                elif instruction[1] == 'b':
                    b *= 3
                else:  raise ValueError(f"Invalid register {instruction[1]}")
                instruction_id += 1
            case 'inc':
                if instruction[1] == 'a':
                    a += 1
                elif instruction[1] == 'b':
                    b += 1
                else:  raise ValueError(f"Invalid register {instruction[1]}")
                instruction_id += 1
            case 'jmp':
                instruction_id += int(instruction[1])
            case 'jie':
                if instruction[1] == 'a' and a % 2 == 0:
                    instruction_id += instruction[2]
                elif instruction[1] == 'b' and b % 2 == 0:
                    instruction_id += instruction[2]
                else:
                    instruction_id += 1
            case 'jio':
                if instruction[1] == 'a' and a == 1:
                    instruction_id += instruction[2]
                elif instruction[1] == 'b' and b == 1:
                    instruction_id += instruction[2]
                else:
                    instruction_id += 1
            case _:
                raise ValueError(f"Invalid instruction {instruction[0]}")


        # print(f"instruction id: {instruction_id}, a: {a}, b: {b}")
    return a,b

if __name__ == "__main__":
    main()
