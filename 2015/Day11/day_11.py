import string
import re



def check_rule_1(password, targets):
    for target in targets:
        if target in password:
            return True
    return False

def check_rule_2(password):
    for c in password:
        if c in ['i', 'o', 'l']:
            return False
    return True

def check_rule_3(password):
    if re.match(r'.*(.)\1.*(.)\2.*',password):
        return True
    return False

def increment_password(password):
    pwd_lst = list(password)
    # print(pwd_lst)
    i  = len(pwd_lst)-1
    while i>=0:
        if pwd_lst[i] == 'z':
            pwd_lst[i] = 'a'
        else:
            pwd_lst[i] = chr(ord(pwd_lst[i]) + 1)
            break
        i -= 1
    password = ''.join(pwd_lst)
    return password

def find_next_pass(target_letters, start):
    i=1
    while True:
        i+=1
        if check_rule_1(start, target_letters) and check_rule_2(start) and check_rule_3(start):
            break
        start = increment_password(start)   

        if i%1000000 == 0:
            print(f'Iteration: {i} Password: {start}')
    return start

if __name__ == '__main__':
    let=string.ascii_lowercase
    target_letters = [let[i] + let[i+1] + let[i+2] for i in range(len(let)-2)]
    print(target_letters)

    start = 'hepxcrrq'
    start = find_next_pass(target_letters, start)
    print(f'Part 1: {start}')


    start = 'hepxxyzz'
    start = increment_password(start)


    start = find_next_pass(target_letters, start)
    print(f'Part 2: {start}')
