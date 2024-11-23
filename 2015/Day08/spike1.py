import re

new_str = r'\x27 aa \x4'
print(re.sub(r'\\x[0-9]{1,2}', '~', new_str))
print(new_str)

string = '"\\"'
print(string)
new_str = string.replace('\\', '\\\\')
print(new_str)


