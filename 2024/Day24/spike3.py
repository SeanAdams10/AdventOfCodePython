def numbers():
    yield 0
    yield 1
    yield 2


for n in numbers():
    print(n)