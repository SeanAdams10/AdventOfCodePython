from itertools import groupby
import time

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


def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    result = []
    for i in range(len(data[0])//2+1):
        result.extend([str(i)]*int(data[0][i*2]))
        if i < len(data[0])//2:
            result.extend(['.']*int(data[0][i*2+1]))
            
    total_len = sum([int(x) for x in data[0]])
    if len(result) != total_len:
        print(f"Error: Length of result {len(result)} does not match total length of data {total_len}")

    return result

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' took {elapsed_time:.6f} seconds to execute.")
        return result
    return wrapper

@timing_decorator
def simple_compress(data):
    inbound_data = list(data)
    start = 1
    end = len(inbound_data)-1
    while start<end:
        if inbound_data[start] != '.':
            start +=1
        elif inbound_data[end] == '.':
            end -=1
        else:
            inbound_data[start] = inbound_data.pop(end)
            start +=1
            end -=1
    return inbound_data

def sum_compress(in_list):
    total = 0
    for key, val in enumerate(in_list):
        if val != '.':
            total += int(val)*key
    return total   


def complex_compress(inbound_data):
    grp = [(x,len(list(y))) for x,y in groupby(inbound_data)]

    source_id= len(grp)-1
    start_id = 1
    while source_id >0 :
        source = grp[source_id]
        if source[0] == '.':
            source_id -=1 
            continue #ignore any that are . - no compression needed

        if grp[start_id][0] != '.' or grp[start_id][1] == 0:
            start_id += 1
            continue #ignore any that are not . or have a length of 0

        found = False
        for x in range(start_id, source_id):
            target = grp[x]
            if target[0] == '.' and target[1]>=source[1]:
                grp[source_id]=('.',source[1])
                grp.insert(x,source)
                grp[x+1]=('.',grp[x+1][1] - source[1])
                found = True
                if grp[-1][0]=='.':
                    grp.pop(-1)
                break
        if not(found):
            source_id -=1
    return grp

def main():
    data = get_input_data(2024, 9, sample=0)
    inbound_data = read_input(data)

    p1_list = simple_compress(inbound_data)
    total = sum_compress(p1_list)
    print(f'Part 1: {total}')
    
    grp = complex_compress(inbound_data)

    #convert this now back to a regular list
    part2_lst=[]
    for x,y in grp:
        part2_lst.extend([x]*y)

    total = sum_compress(part2_lst)
    
    print(f'Part 2: {total}') 






    
    
        

if __name__ == "__main__":
    main()
