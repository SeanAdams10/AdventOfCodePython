import itertools

#start_string = '1'
# iteration_count = 5
start_string = '1321131112'
iteration_count = 50

for i in range(iteration_count):
    groups = itertools.groupby(start_string)
    lst = [str(len(list(group))) + key for key, group in groups] 
    start_string = ''.join(lst)
    
# print(start_string)
print(len(start_string))