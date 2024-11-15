import numpy as np

# Create a 1000 element numpy array initialized to zero (False)
bit_array = np.zeros((1000, 1000), dtype=np.bool_)

# Change rows 1-10 to have the value 1 (True)
bit_array[1:11,:] = True

# Change rows 5-15 to the not of what they are now
bit_array[5:16,:] = np.logical_not(bit_array[5:16,:])

# Change all elements in row 1-2; columns 1:10 to the value True
bit_array[1:3, 1:10] = True

print(bit_array)


