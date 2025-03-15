from time import perf_counter
from utils import get_input_data, timing_decorator

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    rules = [(x.split("|")[0].strip(), x.split("|")[1].strip())
             for x in data if "|" in x]
    updates = [x.split(",") for x in data if "," in x]

    return rules, updates


def main():
    data = get_input_data(2015, 22, sample=1)
    read_input(data)


if __name__ == "__main__":
    main()
