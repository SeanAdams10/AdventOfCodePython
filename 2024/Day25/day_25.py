from time import perf_counter
from utils import get_input_data, timing_decorator

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """

    device_id = 0
    keys = []

    for r in data:
        if not(r.strip()):
            device_id +=1
            continue
        
        if len(keys) <= device_id:
            keys.append([r])
        else:
            keys[device_id].append(r)
    
    key_2 = []
    for k in keys:
        keylen = len(k[0]) 
        mult = -1 if k[0] == '#'*keylen else 1

        k = k[1:-1]
        key_vals = [mult]
        for i in range(keylen):
            c = len([x[i] for x in k if x[i] == '#'])
            key_vals.append(c)
        key_2.append(key_vals)

    return key_2


def main():
    data = get_input_data(2024, 25, sample=0)
    parsed = read_input(data)

    locks = [x[1:] for x in parsed if x[0] == -1]
    keys = [x[1:] for x in parsed if x[0] == 1]

    match_cnt = 0
    for l in locks:
        for k in keys:
            sums = [a+b for a,b in zip(l,k)]
            all_match = all([x <= 5 for x in sums])
            if all_match:
                match_cnt += 1

    print(f'Matches: {match_cnt}')

if __name__ == "__main__":
    main()
