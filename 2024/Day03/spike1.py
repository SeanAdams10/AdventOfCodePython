import re
input_data  = "xmul(2,4)%&mul[3,7]!@^don't_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
input_data = "don'tdo" + input_data
allparts = []
parts = re.split(r"don't\(\)", input_data)
print(parts)
for part in parts:
    print ("part: ", repr(part))
    new_parts = re.split(r'do\(\)', part)
    print("new parts: ", new_parts)
    allparts.extend(new_parts[1:]) #ignore the first part after the do


print('All parts surviving',allparts)