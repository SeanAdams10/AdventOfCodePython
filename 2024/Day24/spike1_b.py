with open(f'.\\2024\\Day24\\sample5.txt', 'r') as f:
    lines = f.readlines()

rules = []
for l in lines:
    l = l.strip()
    if ':' in l:
        continue
    if not(l):
        continue
    
    pre, post = l.split(' -> ')
    op1, operand, op2 = pre.split(' ')
    result = post.strip()
    r = (l, op1, operand, op2, result)
    rules.append(r)

# print(rules)

#RemoveKeys
removal = ['z' + str(i).rjust(2, '0') for i in range(9, 48)]
removal.extend(['x' + str(i).rjust(2, '0') for i in range(7, 48)])
removal.extend(['y' + str(i).rjust(2, '0') for i in range(7, 48)])
while True:
    removed = 0
    for r in rules:
        if r[4] in removal or r[1] in removal or r[3] in removal:
            removal.append(r[1])
            removal.append(r[3])
            removal.append(r[4])
            removed += 1
    
    rules = [x for x in rules if x[1] not in removal and x[3] not in removal and x[4] not in removal]
    if removed == 0:
        break

print(rules)

rule_list = sorted(rules, key=lambda x: (x[1], x[3]))
rule_list2 = [f'{min(x[1], x[3])} {x[2]} {max(x[1], x[3])} -> {x[4]}'  for x in rule_list]
rule_list2 = sorted(rule_list2)
print('\n'.join(rule_list2))
