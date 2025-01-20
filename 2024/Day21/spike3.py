from keypad import Keypad, Dir_Pad
import math
from time import perf_counter

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper

# @timing_decorator
def run_backprop():
    kp = Keypad()
    dp = Dir_Pad()
    cache_factor = 3

    
    for cache_factor in range(1,8):
        initial = kp.keypad_moves
        start_time = perf_counter()
        for layers in range(2):
            print (f"Layer {layers+1} cache_factor: {cache_factor}")
            for k,v in initial.items():
                new_steps = []
                maxlen = math.inf        
                for option in v:
                    cache_size = max(1, len(option)//cache_factor)
                    new_val = dp.translate_keyinput(option, cache_size)
                    min_len = min([len(x) for x in new_val])
                    if min_len < maxlen:
                        maxlen = min_len
                        new_steps = new_val
                    elif min_len == maxlen:
                        new_val = [x for x in new_val if len(x) == min_len]
                        new_steps.extend(new_val)
                initial[k] = new_steps
        end_time = perf_counter()
        # print(initial)
        print(f"Cache Factor: {cache_factor} took {end_time - start_time:.6f} seconds")

    # input("Press Enter to continue...")

run_backprop()

