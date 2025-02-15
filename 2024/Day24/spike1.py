import re
from collections import deque

ins_q = deque()
ins_q.append("1")
ins_q.append("2")

print(ins_q[0])
print(ins_q)
v = ins_q.popleft()
print(ins_q)
