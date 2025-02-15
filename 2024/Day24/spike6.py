import dataclasses


@dataclasses.dataclass
class Rule:
    op1: str
    op2: str
    operand: str
    result: str



def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    start_vals = {x.split(":")[0].strip(): int(x.split(":")[1].strip())
             for x in data if ":" in x}
    
    rules = []
    for row in data:
        if "->" in row:
            op, res = row.split(' -> ')
            op1, operand, op2 = op.split()
            rules.append(Rule(op1, op2, operand, res))

    return start_vals, rules


# Load data
file_name = 'input.txt'
with open('./2024/Day24/' + file_name) as f:
    data = f.read().splitlines()
start_vals, rules_orig = read_input(data)
# print(start_vals)
# print(rules_orig)

ro = [x.result for x in rules_orig if x.result.startswith('z')]
print(ro)
print('max',max(ro))
print('min',min(ro))


