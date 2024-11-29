import itertools

a = (-1,0,1)
b = itertools.product(a, repeat=1)
c = itertools.product(a, repeat=2)
d = itertools.product(a, repeat=3)

print(list(b))
print (list(c))
print(list(d))

initial = (50, 50)
deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

new_positions = [(initial[0] + delta[0], initial[1] + delta[1]) for delta in deltas]

print(new_positions)
def add_tuples(initial, deltas):
    return [tuple(map(sum, zip(initial, delta))) for delta in deltas]

# Example usage
initial = (50, 50, 50)
deltas = [(-1, -1, -1), (-1, 0, 0), (-1, 1, 1), (0, -1, -1), (0, 0, 0), (0, 1, 1), (1, -1, -1), (1, 0, 0), (1, 1, 1)]

new_positions = add_tuples(initial, deltas)
print(new_positions)


print (list(zip((50,50), (-1, -1))))
print (list(map(sum, zip((50,50), (-1, -1)))))


print(list(zip({"Butterscotch": 44, "Cinnamon": 56}.values(), (-1,-1))))


print(zip((("a",10),("b",20)),(1,2)))
print(list(zip((("a",10),("b",20)),(1,2))))



dictionary = {"a": 10, "b": 10}
list_of_tuples = list(dictionary.items())
print(list_of_tuples)
      
