import string

alp = "abcdefghijklmnopqrstuvwxyz"
alp2 = string.ascii_lowercase
print(alp2)


def print_rangoli(size):
    n_rows = 2 * size - 1
    for i in range(n_rows):
        letters = alp[abs(size - i - 1): size]
        dashed_letters = "-".join(letters[::-1][:-1]+letters)
        print(dashed_letters)
        print(dashed_letters.center((4*size-3), "-"))


print_rangoli(5)
