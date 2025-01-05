"""This is my first attempt at solving the puzzle for Day 17 of Advent of Code 2024."""

import re
from time import perf_counter
from functools import cache
from itertools import pairwise
import os


def get_input_data(year: int, day: int, sample: int = 0) -> list:
    """
    Reads either the sample or the puzzle input data
    :param year: The year of the puzzle
    :param day: The day of the puzzle
    :param sample: The sample number (0 for puzzle input)
    :return: A list of strings
    """
    root = rf"{year}/Day{str(day).zfill(2)}/"

    if sample == 0:
        file = root + "input.txt"
    else:
        file = root + rf"sample{str(sample)}.txt"
    with open(file, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    if not data:
        raise FileNotFoundError("Input data file is empty")
    return data


def timing_decorator(func):
    """This is a decorator function that times the execution of a function."""
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {
              elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper


def read_input(data) -> list:
    """
    Parser for the input data - unique to each puzzle
    :param data: A list of strings
    :return: A list of strings
    """
    registers = {'A': 0, 'B': 0, 'C': 0}
    program_raw = []
    for line in data:
        if 'Register' in line:
            matches = re.match(r'Register (\w+): (\d+)', line)
            registers[matches.group(1)] = int(matches.group(2))
        if 'Program' in line:
            program_raw = line.split(': ')[1].split(',')

    program = []
    program = [int(x.strip()) for x in program_raw]

    return registers, program


# def read_all_matches(match_sizes):
#     """ This function reads all the matches from the files and returns a list of all the values
#     :param match_sizes: A list of integers indicating the length of the match in the program
#     :return: A list of integers representing the values of A that match the program
#     """
#     if not match_sizes:
#         match_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
#         raise ValueError("Match sizes must be provided")
#     points = []
#     for size in match_sizes:
#         try:
#             with open(f'2024/Day17/match_{size}.csv', 'r', encoding='utf-8') as f:
#                 points.extend([int(line.strip()) for line in f])
#         except FileNotFoundError:
#             open(f'2024/Day17/match_{size}.csv', 'w', encoding='utf-8').close()

#     all_values = list(set(points))
#     all_values.sort()
#     return all_values

def write_all_matches(match_sizes, matches):
    """ This function reads all the matches from the files and returns a list of all the values
    :param match_sizes: A list of integers indicating the length of the match in the program
    :return: A list of integers representing the values of A that match the program
    """
    if not match_sizes:
        match_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
        raise ValueError("Match sizes must be provided")
    for size in match_sizes:
        with open(f'2024/Day17/match_{size}.csv', 'w', encoding='utf-8') as f:
            for line in matches[size]:
                f.write(f"{line}\n")


# def compact(match_sizes):
#     """This function reads the match files and removes duplicates and sorts the values
#     :param match_sizes: A list of integers indicating the length of the match in the program
#     """
#     if not match_sizes:
#         match_sizes = [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]
#         raise ValueError("Match sizes must be provided")
#     points = []
#     for size in match_sizes:
#         points = []
#         try:
#             with open(f'2024/Day17/match_{size}.csv', 'r', encoding='utf-8') as f:
#                 points = [int(line.strip()) for line in f]
#         except FileNotFoundError:
#             open(f'2024/Day17/match_{size}.csv', 'w', encoding='utf-8').close()

#         points = list(set(points))
#         points.sort()

#         with open(f'2024/Day17/match_{size}.csv', 'w', encoding='utf-8') as f:
#             for line in points:
#                 f.write(f"{line}\n")


def update_gap_set(match_sizes, matches, gap_sets):
    """ this function refreshes the gap set for each map size provided
    :param match_sizes: A list of integers indicating the length of the match in the program
    :return: None
    """
    if not match_sizes:
        raise ValueError("Match sizes must be provided")

    for size in match_sizes:
        all_values = list(set(matches[size]))
        all_values.sort()
        differences = list({y - x for x, y in pairwise(all_values)})
        differences.sort()
        gap_sets[size] = set(differences)

    gap_sets[2].add(1) #the gaps for the first match group always has to include 1



# def update_gap_file(gap_sets):
#     """ this function reads all the match files and calculates the gaps between the values
#     :param match_sizes: A list of integers indicating the length of the match in the program
#     :return: None
#     """
#     if not match_sizes:
#         raise ValueError("Match sizes must be provided")

#     all_values = list(set(read_all_matches(match_sizes)))
#     all_values.sort()
#     differences = list({y - x for x, y in pairwise(all_values)})
#     differences.sort()
#     # print(differences)

#     with open('2024/Day17/gaps.csv', 'w', encoding='utf-8') as f:
#         for x in differences:
#             f.write(f"{x}\n")


def read_gaps():
    """This function reads the gaps between the values of A that match the program
    :return: A list of integers representing the gaps between the values of A
    """
    with open('2024/Day17/gaps.csv', 'r', encoding='utf-8') as f:
        gaps = [int(line.strip()) for line in f]
    if not gaps:
        gaps.append(1)
    return gaps


@cache
def run_instruction(instr, operand, a, b, c, instr_id) -> tuple:
    """This function runs the instruction and returns the updated values of a,b,c and 
    the instruction id

    :param instr: The instruction ID
    :param operand: The operand for the instruction
    :param a: The value of register A
    :param b: The value of register B
    :param c: The value of register C
    :param instr_id: The current instruction ID
    :return: A tuple containing the updated values of a,b,c and the instruction id
    """

    co = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: a,
        5: b,
        6: c,
    }  # combo operands

    if instr in [0, 6, 7]:
        assert operand in co
        # Combo operand 7 doesn't exist, so we need to check for it
    if instr in [3]:
        # operand must be even so that we don't confuse operation ID with operand
        assert operand % 2 == 0

    output = []

    match instr:
        case 0:
            a = int(a / (2**co[operand]))
            instr_id += 2
        case 1:
            b = b ^ operand
            instr_id += 2
        case 2:
            b = co[operand] % 8
            instr_id += 2
        case 3:
            if a:
                instr_id = operand
            else:
                instr_id += 2
        case 4:
            b = b ^ c
            instr_id += 2
        case 5:
            output.append(co[operand] % 8)
            instr_id += 2
        case 6:
            b = int(a / (2**co[operand]))
            instr_id += 2
        case 7:
            c = int(a / (2**co[operand]))
            instr_id += 2

    return instr_id, output, a, b, c

@cache
def part_1(a, b, c, program) -> tuple:
    """This function runs the program and returns the output.    This is memoized to speed it up
    :param a: The value of register A
    :param b: The value of register B
    :param c: The value of register C
    :param program: The program to run
    :return: A tuple containing the updated values of a,b,c and the output
    """
    program = list(program)

    instr_id = 0
    output = []
    while instr_id < len(program):
        instr, operand = program[instr_id], program[instr_id + 1]
        instr_id, instr_output, a, b, c = run_instruction(
            instr, operand, a, b, c, instr_id)
        if instr_output:
            output.extend(instr_output)

    output_str = ','.join([str(x) for x in output])
    return a, b, c, output_str


def get_starting_point(match_sizes, matches):
    """where should we start to search for new matches?
    :param match_sizes: A list of integers indicating the length of the match in the program
    :return: An integer representing the starting point
    """
    if not match_sizes:
        raise ValueError("Match sizes must be provided")

    all_values = set(matches[match_sizes[0]])
    if not all_values:
        all_values.add(8**15-1)

    return max(all_values)



def set_work_queue(match_size, min_value, attempted, matches, gaps):
    if not isinstance(match_size, int):
        raise ValueError("Match size must be an integer")

    work_queue = set()

    update_gap_set([match_size], matches, gaps)

    min_value = get_starting_point([match_size], matches)
    # current_matches = set(read_all_matches([match_size]) + [min_value])
    current_matches = matches[match_size]
    current_gaps = gaps[match_size]

    potential_matches = set([match + gap for gap in current_gaps for match in current_matches])
    potential_matches2 = potential_matches.difference(current_matches).difference(attempted[match_size])
    if not potential_matches2:
        potential_matches2.add(min_value)

    work_queue = set(potential_matches2)

    return work_queue, gaps



def Part_2(data, itercount, timeout, attempted,match_sets,gap_sets, iter_no):
    registers, program = read_input(data)
    pr_str = ','.join([str(x) for x in program])
    a_val = 0
    min_value = 0
    match_size_l = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]

    timeout_flag = False
    success = False

    for k,match_size_c in enumerate(match_size_l):
        iteration_start_time = perf_counter()
        work_queue, gap_sets = set_work_queue(match_size_c, min_value, attempted, match_sets, gap_sets)
        print(f'Open : match_size: {match_size_c:2} attempted: {len(attempted[match_size_c]):7} gaps: {len(gap_sets[match_size_c]):5} current_matches: {len(match_sets[match_size_c]):7} work_queue: {len(work_queue):7}')

        while work_queue:
            # Update the work queue
            a_val = min(work_queue)
            work_queue.remove(a_val)
            if a_val in attempted[match_size_c]:
                continue
            if len(work_queue) == 0 and match_size_c == 2:
                work_queue.add(a_val+1)

            work_queue = set(sorted(list(work_queue))[:itercount*10])

            #run the program to check the result
            a, b, c = a_val, registers['B'], registers['C']
            _, _, _, output = part_1(a, b, c, tuple(program))

            if perf_counter() - iteration_start_time > timeout:
                print(f"Timed out after {timeout} seconds")
                timeout_flag = True
                break

            for size in match_size_l[k:]:
                if output[:size] == pr_str[:size]:
                    match_sets[size].add(a_val)
                    work_queue.update([a_val + gap for gap in gap_sets[size]])

            if output == pr_str:
                print(f"Match found: {a_val}")

            attempted[match_size_c].add(a_val)
            if len(match_sets[match_size_c])>=(iter_no+1)*itercount: #we've hit our target
                break

        print(f'Close: match_size: {match_size_c:2} attempted: {len(attempted[match_size_c]):7} gaps: {len(gap_sets[match_size_c]):5} current_matches: {len(match_sets[match_size_c]):7} work_queue: {len(work_queue):7}')

        if timeout_flag:
            break

    if success:
        print(f"Part 2: {a_val}")
        print()

    write_all_matches(match_size_l, match_sets)    



def summarize_results(iter_no, match_sets, gap_sets):
    """This function summarizes the results of the matches"""
    match_sizes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22,
                   24, 26, 28, 30, 32]

    summary_file = '2024/Day17/summary.csv'
    if not os.path.exists(summary_file):
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('iter_no,match_size,match_count,min_match,max_match,gap_count,min_gap,max_gap\n')

    with open('2024/Day17/summary.csv', 'a', encoding='utf-8') as f:
        for k,m in enumerate(match_sizes):
            # print(f"Summarizing Match size: {m}")
            all_values = match_sets[m]
            update_gap_set(match_sizes[k:k+1], match_sets, gap_sets)
            this_gap_set = gap_sets[m]

            min_value = min(all_values) if all_values else 0
            max_value = max(all_values) if all_values else 0
            min_gap = min(this_gap_set) if this_gap_set else 0
            max_gap = max(this_gap_set) if this_gap_set else 0
            f.write(f'{iter_no}, {m}, {len(all_values)}, {min_value}, {max_value}, {len(this_gap_set)}, {min_gap}, {max_gap}\n')


def clean_all_files():
    """This function deletes any csv file beginning with match, along with gaps.csv and summary.csv in the folder 2024/Day17/"""
    folder = '2024/Day17/'
    for file_name in os.listdir(folder):
        if file_name.startswith('match') and file_name.endswith('.csv'):
            os.remove(os.path.join(folder, file_name))
    if os.path.exists(os.path.join(folder, 'gaps.csv')):
        os.remove(os.path.join(folder, 'gaps.csv'))
    if os.path.exists(os.path.join(folder, 'summary.csv')):
        os.remove(os.path.join(folder, 'summary.csv'))

def initialize_matches():
    match_sizes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22,
                   24, 26, 28, 30, 32]
    attempted = {x: set() for x in match_sizes}
    matches = {x: set() for x in match_sizes}
    gaps = {x: set() for x in match_sizes}
    return match_sizes,attempted,matches,gaps


def main():
    """This is the main function that runs the program."""

    data = get_input_data(2024, 17, sample=0)
    registers, program = read_input(data)
    _, _, _, output = part_1(
        registers['A'], registers['B'], registers['C'], tuple(program))
    print(f"Part 1: {output}")

    clean_all_files()
    batch_size = 2000
    total_target = 100000
    time_limit = 240
    iter_count = total_target // batch_size

    match_sizes, attempted, matches, gaps = initialize_matches()

    for i in range(iter_count):
        print('*'*20)
        print(f'iteration {i}')
        print('*'*20)
        Part_2(data, batch_size,time_limit, attempted, matches, gaps, i)
        summarize_results(i, matches, gaps)
        write_all_matches(match_sizes, matches)



if __name__ == "__main__":
    main()
