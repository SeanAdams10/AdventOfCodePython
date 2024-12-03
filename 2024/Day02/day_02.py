with open('2024/Day02/input.txt') as f:
    data = f.read().splitlines()


def check_safety_single(report: list) -> bool:
    """ checks a single report for safety
    """
    flags_asc: list = [report[i+1] <= report[i]-1 and report[i+1]
                       >= report[i]-3 for i in range(len(report)-1)]
    flags_desc: list = [report[i+1] >= report[i]+1 and report[i+1]
                        <= report[i]+3 for i in range(len(report)-1)]

    return all(flags_asc) or all(flags_desc)




def safety_check(in_data: list, tolerance: int = 0) -> list:
    """ checks a list of reports for safety - if tolerance > 0 then it knocks out one number at a time
    """
    safety: list = []
    for x in in_data:
        line: str = [int(n) for n in x.split()]
        valid: bool = check_safety_single(line)
        print(valid)
        if tolerance == 1:
            for i in range(len(line)):
                tmp_ln: list = line[:i] + line[i+1:]
                valid = valid or check_safety_single(tmp_ln)

        safety.append(valid)
    return safety


safety = safety_check(data)
print(f' Part 1: {sum(safety)}')

safety = safety_check(data, 1)
print(f' Part 2: {sum(safety)}')
