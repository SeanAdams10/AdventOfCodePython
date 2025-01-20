from keypad import Keypad, Dir_Pad
from itertools import product, permutations
from collections import Counter


def main():
    kp = Keypad()
    mv = kp.keypad_moves
    dp = Dir_Pad()
    dv = dp.keypad_moves

    print(mv[('A','0')])
    
    print(mv[('0','2')])
    print(mv[('2','9')])
    print(mv[('9','A')])

    a=['<A']
    b=['^A']
    c=['>^^A', '^>^A', '^^>A']
    d=['vvvA']

    f = product(a,b,c,d)
    print(list(f))  

    f2 = ['A' + ''.join(i) for i in product(a,b,c,d)]    
    print(f2)
    a=f2[0]

    f2Pairs = list(zip(a, a[1:])) #Create an offset pair of the string
    print(list(f2Pairs))

    f2pCounter = dict(Counter(f2Pairs))
    print(f2pCounter)
    print(sum(f2pCounter.values()))

    # ('A', '<'): 1
    print(dv[('A', '<')])

    for k,v in f2pCounter.items():
        print(dv[k])
        # w = 'a' + dv[k]
        # wPairs = list(zip(w, w[1:])) #Create an offset pair of the string
        # wCounter = Counter(wPairs)*v
        # print(dict(wCounter))







    # for k,v in mv.items():

    #     for i in v:
    #         print(f"{k}: {i}")   


    # dp = Dir_Pad()
    # mv = dp.keypad_moves
    # mv_depth = dp.keypad_moves
    # for k,v in mv.items():
    #     for i in v:
    #         print(f"{k}: {i}")   
    # pass


if __name__ == "__main__":
    main()