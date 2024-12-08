def get_input_data(sample: int = 0) -> list:
    if sample == 0:
        file = r"2024/Day05/input.txt"
    else:
        file = r"2024/Day05/sample.txt"
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    return data


def read_input(data) -> list:
    rules = [(x.split("|")[0].strip(), x.split("|")[1].strip())
             for x in data if "|" in x]
    updates = [x.split(",") for x in data if "," in x]

    return rules, updates


def check_errors(rules: list, updates: list) -> list:
    good_updates = []
    bad_updates = []
    for update in updates:
        error = False
        for rule in rules:
            if rule[0] in update and rule[1] in update:
                idx1 = update.index(rule[0])
                idx2 = update.index(rule[1])
                if idx1 > idx2:
                    bad_updates.append((update, rule[0], rule[1]))
                    error = True
                    break
        if not error:
            good_updates.append(update)
    return good_updates, bad_updates


def get_sum_mid(reports: list) -> int:
    sum_mid = 0
    for report in reports:
        length = len(report)
        mid = length // 2
        sum_mid += int(report[mid])
    return sum_mid


def fix_errors(bad_updates: list, rules: list) -> list:
    fixed_updates = []
    while len(bad_updates) > 0:
        for update, bad1, bad2 in bad_updates:
            idx1 = update.index(bad1)
            idx2 = update.index(bad2)
            update[idx1], update[idx2] = update[idx2], update[idx1]
        good, bad_updates = check_errors(rules, [x[0] for x in bad_updates])
        if good:
            fixed_updates.extend(good)
    return fixed_updates


def main():
    data = get_input_data(sample=0)
    rules, updates = read_input(data)
    good, bad = check_errors(rules, updates)
    print(f'Part 1: {get_sum_mid(good)}')

    fixed = fix_errors(bad, rules)
    print(f'Part 2: {get_sum_mid(fixed)}')


if __name__ == "__main__":
    main()
