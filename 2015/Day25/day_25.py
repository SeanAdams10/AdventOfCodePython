from time import perf_counter
from utils import get_input_data, timing_decorator


def sum_of_n(n):
    return (n * (n + 1)) // 2

def main():
    row_target = 2947
    col_target = 3029
    # row 2947, column 3029.

    solid_rows = sum_of_n(row_target + col_target - 2)
    print(solid_rows)
    target = solid_rows + col_target
    #this gives the number of times to run the calc

    start = 20151125
    for _ in range(target - 1):
        start = (start * 252533) % 33554393

    print(start)

if __name__ == "__main__":
    main()
