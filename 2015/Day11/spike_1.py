import re


x = re.match(r'.*(.)\1.*(.)\2.*','abcdffaa')
if x:
    print("Yes")
else:
    print("No")

