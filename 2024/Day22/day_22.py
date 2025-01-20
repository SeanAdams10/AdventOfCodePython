from utils import get_input_data
from functools import lru_cache
from math import floor
import collections

@lru_cache(maxsize=20000000)
def get_next_key(input_key, step_number):
    # step = step_number % 3
    # match step:
    #     case 0: result = ((input_key * 64) ^ input_key) % 16777216
    #     case 1: result = ((input_key//32) ^ input_key) % 16777216
    #     case 2: result = ((input_key * 2048) ^ input_key) % 16777216
    # return result

    input_key = ((input_key * 64) ^ input_key) % 16777216
    input_key = ((input_key//32) ^ input_key) % 16777216
    input_key = ((input_key * 2048) ^ input_key) % 16777216
    return input_key




def find_price_breaks(price_list: list) -> int:

    # first we take the prices from the process and find the differences for this buyer
    # then, for this buyer we look at each 4-step price beak pattern
    # if we've not seen this before, then we store this along with the price at the time
    buyer_price_breaks = []
    all_breaks = set()
    for buyer in price_list:
        curr_price_break = dict()
        diff = [buyer[k+1] - buyer[k] for k in range(len(buyer)-1)]

        for i in range(3, len(diff)):
            pattern = (diff[i-3],diff[i-2],diff[i-1],diff[i])
            if pattern not in curr_price_break:
                curr_price_break[pattern] = buyer[i+1]
                all_breaks.add(pattern)

        buyer_price_breaks.append(curr_price_break)

    # overall_bananas = dict()
    # for buyer in buyer_price_breaks:
    #     for pattern, price in buyer.items():
    #         if pattern not in overall_bananas:
    #             overall_bananas[pattern] = price
    #         else:
    #             overall_bananas[pattern] += price

    # now summarize
    overall_bananas = dict()
    for pattern in all_breaks:
        overall_bananas[pattern] = sum([buyer[pattern] for buyer in buyer_price_breaks if pattern in buyer])

    max_bananas = max(overall_bananas, key= lambda x: overall_bananas[x])

    print(f'Part 2: bananas = {overall_bananas[max_bananas]} and break = {max_bananas}')

    return max_bananas, overall_bananas[max_bananas]


def main():
    data = get_input_data(2024, 22, sample=0)
    data = [int(x) for x in data]

    price_list = [[i % 10,] for i in data]


    for i in range (2000):
        for k,d in enumerate(data):
            data[k] = get_next_key(d, i)
            price_list[k].append(data[k] % 10)

    print(f'Part 1: {sum(data)}')

    break_prices,bananas = find_price_breaks(price_list)





if __name__ == "__main__":
    main()