def parse_data(base_data):
    parsed_data = [(line.split()[0],
                    int(line.split()[3]), 
                    int(line.split()[6]),
                    int(line.split()[-2]) ) for line in base_data]

    return parsed_data

def distance_calc (parsed_data, time):
    
    distance_list = []
    for _, speed, fly, rest in parsed_data:
        total = fly + rest
        cycles = time // total
        remainder = time % total
        distance = cycles * fly * speed + min(fly, remainder) * speed
        
        distance_list.append(distance)
    
    return distance_list


def part_2_scoring(parsed_data, time):
    scores = [0] * len(parsed_data) #set up the initial scores
    
    for i in range(time):
        distances = distance_calc(parsed_data, i+1)
        for reindeer, dist in enumerate(distances):
            if dist == max(distances):
                scores[reindeer] +=1
        
    return scores


if __name__ == "__main__":
    with open("Part1Input.txt",'r', encoding='ascii') as f:
        input_data = f.readlines()
    
    pd = parse_data(input_data)
    print('Part 1: ',max(distance_calc(pd, 2503)))
    
    print('Part 2: ', max(part_2_scoring(pd, 2503)))
