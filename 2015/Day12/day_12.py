import json
def parse_numbers(json_doc: str,ignore_str=None)->list:
    numbers = []
    
    json_native = json.loads(json_doc)
    
    def find_numbers(jn):
        if isinstance(jn, int):
            numbers.append(jn)
        elif isinstance(jn, dict):
            if ignore_str in jn.values():
                return
            for value in jn.values():
                find_numbers(value)
        elif isinstance(jn, list):
            for value in jn:
                find_numbers(value)
                
    find_numbers(json_native)
    return numbers


print(parse_numbers('[1,2,3]')) # [1,2,3]

with open('Part1Input.txt','r', encoding='ascii') as file:
    json_str = file.read()
    print(f'Part 1: {sum(parse_numbers(json_str))}') 
    print(f'Part 2: {sum(parse_numbers(json_str,"red"))}') 
    