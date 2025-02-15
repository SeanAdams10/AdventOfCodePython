from typing import Callable
from utils import timing_decorator
import math
import time

from typing import Callable, Tuple, List
import concurrent.futures

def run_test(task: Tuple[int, str, Callable[[int, int], int]]) -> Tuple[int, str, int]:
    """
    Runs one test for a given bit value and test type.

    Args:
        task (Tuple[int, str, Callable[[int, int], int]]): A tuple containing:
            - l (int): The bit index.
            - test_type (str): Which test to run ('t1', 't2', or 't3').
            - test_fun (Callable[[int, int], int]): The function to test.
    
    Returns:
        Tuple[int, str, int]: A tuple containing the bit index, the test type, and the result.
    """
    l, test_type, test_fun = task
    if test_type == 't1':
        result = test_fun(2**l, 0)
    elif test_type == 't2':
        result = test_fun(0, 2**l)
    elif test_type == 't3':
        result = test_fun(2**l, 2**l)
    else:
        raise ValueError("Unknown test type")
    return (l, test_type, result)

@timing_decorator
def test_each_val_parallel(max_bits: int, test_fun: Callable[[int, int], int]) -> Tuple[List[int], List[int]]:
    """
    Tests a function with various bit values, running each individual test in its own process.
    For each bit value `l` in range(max_bits), three tests are performed concurrently:
      - test 1: test_fun(2**l, 0)   [expected result: 2**l]
      - test 2: test_fun(0, 2**l)   [expected result: 2**l]
      - test 3: test_fun(2**l, 2**l)[expected result: 2**(l+1)]
    
    A bit position `l` is marked "good" only if all three tests return the expected results.
    
    Args:
        max_bits (int): The maximum number of bits to test.
        test_fun (Callable[[int, int], int]): A function that takes two integers and returns an integer.
    
    Returns:
        Tuple[List[int], List[int]]: A tuple containing two lists:
            - The first list contains the bit positions that failed one or more tests ("broken").
            - The second list contains the bit positions that passed all tests ("good").
    """
    # Prepare a list of tasks: one for each bit value and each test type.
    tasks = [(l, test_type, test_fun) for l in range(max_bits) for test_type in ('t1', 't2', 't3')]
    
    # Dictionary to store results per bit index.
    results_per_bit = {l: {} for l in range(max_bits)}
    
    # Create a ProcessPoolExecutor with enough workers so each task can run concurrently.
    # with concurrent.futures.ProcessPoolExecutor(max_workers=max_bits * 3) as executor:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit all tasks to the process pool.
        future_to_task = {
            executor.submit(run_test, task): (task[0], task[1])
            for task in tasks
        }
        
        # As each future completes, record its result.
        for future in concurrent.futures.as_completed(future_to_task):
            l, test_type = future_to_task[future]
            try:
                _, t_type, result = future.result()
                results_per_bit[l][t_type] = result
            except Exception:
                # If a test raises an exception, record a value that will cause the test to be marked as failed.
                results_per_bit[l][test_type] = None

    broken = []
    good = []
    
    # For each bit index, check whether all three tests returned the expected values.
    for l in range(max_bits):
        t1 = results_per_bit[l].get('t1')
        t2 = results_per_bit[l].get('t2')
        t3 = results_per_bit[l].get('t3')
        if t1 != 2**l or t2 != 2**l or t3 != 2**(l+1):
            broken.append(l)
        else:
            good.append(l)
    
    return broken, good

@timing_decorator
def test_each_val_simple(max_bits: int, test_fun: Callable[[int, int], int]) -> tuple[list[int], list[int]]:
    """
    Tests a function with various bit values and categorizes the results.

    Args:
        max_bits (int): The maximum number of bits to test.
        test_fun (Callable[[int, int], int]): A function that takes two integers and returns an integer.

    Returns:
        (broken, good): A tuple containing:
            - broken: A list of bit positions where the test failed
            - good: A list of bit positions where the test succeeded
    """
    broken = []
    good = []
    
    for l in range(max_bits):
        t1 = test_fun(2**l, 0)
        t2 = test_fun(0, 2**l)
        t3 = test_fun(2**l, 2**l)
        
        if t1 != 2**l or t2 != 2**l or t3 != 2**(l+1):
            broken.append(l)
        else:
            good.append(l)

    return broken, good


def adder(x: int, y: int)->int:

    end_time = time.perf_counter() + 0.5
    dummy = 10
    while time.perf_counter() < end_time:
        dummy = dummy +1
        dummy = math.sqrt(dummy) * math.sqrt(dummy*0.99)
    return x + y

if __name__ == "__main__":

    broken, good = test_each_val_simple(1, adder)
    broken, good = test_each_val_parallel(1000, adder)
    print(broken)
    print(good)
    
