from itertools import permutations

def parse_input(happiness_changes):
    happiness_data = {}
    
    for change in happiness_changes:
        change_parts = change.split()
        if change_parts[2] == "gain":
            happiness = int(change_parts[3])
        else:
            happiness = -int(change_parts[3])
        change_parts[-1] = change_parts[-1][:-1] #remove the period at the end
        happiness_data[(change_parts[0], change_parts[-1])] = happiness
    return happiness_data

def unique_guests(happiness_data):
    guests = set()
    
    for key,value in happiness_data.items():
        guests.add(key[0])
        guests.add(key[1])        
    return guests

def measure_combo(happiness_data, this_combo):
    total_happiness = 0
    
    for i in range(len(this_combo)-1):
        total_happiness += happiness_data[(this_combo[i], this_combo[i+1])]
        total_happiness += happiness_data[(this_combo[i+1], this_combo[i])]
    
    total_happiness += happiness_data[(this_combo[0], this_combo[-1])]
    total_happiness += happiness_data[(this_combo[-1], this_combo[0])]
    
    return total_happiness

def find_best_combo(happiness_data):
    best_combo = None
    best_happiness = -9999
    
    unique_guest_set = unique_guests(happiness_data)
    
    tables = permutations(unique_guest_set)
    for table in tables:
        this_happiness = measure_combo(happiness_data, table)
        if this_happiness > best_happiness:
            best_happiness = this_happiness
            best_combo = table
    
    return best_happiness, best_combo



if __name__== "__main__":
    with open("Part1Input.txt",'r',encoding='ascii') as f:
        happiness_changes = f.readlines()
        happiness_details = parse_input(happiness_changes)
        best, table = find_best_combo(happiness_details)
        print('Part 1:', best)

    # Part 2
    guests = unique_guests(happiness_details)
    for guest in guests:
        happiness_details[('Self', guest)] = 0
        happiness_details[(guest, 'Self')] = 0
    
    best, table = find_best_combo(happiness_details)
    print('Part 2:', best)

    