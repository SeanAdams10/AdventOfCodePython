def read_input(sample: int = 0) -> list:
    if sample == 0:
        file = r"2024/Day05/input.txt"
    elif sample == 1:
        file = r"2024/Day05/sample.txt"
    with open(file) as f:
        data = f.read().splitlines()

    rules = [(x.split("|")[0].strip(), x.split("|")[1].strip())
             for x in data if "|" in x]
    updates = [x.split(",") for x in data if "," in x]

    return rules, updates


if __name__ == "__main__":
    rules, updates = read_input(sample=0)
    print(f"Rules: {rules}")
    print(f"Updates: {updates}")

    rules_set = set([x for x, y in rules] + [y for x, y in rules])
    updates_set = set([item for sublist in updates for item in sublist])

    print(f"Rules Set: {rules_set}")
    print(f"Updates Set: {updates_set}")
    print(f"Missing: {updates_set - rules_set}")
    print(f"Extra: {rules_set - updates_set}")
