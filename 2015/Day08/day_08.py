import dataclasses
# from pydantic import BaseModel, field_validator, ValidationInfo
# import pydantic
from dataclasses import dataclass
import re


@dataclass
class SpecificString():
    original: str
    cleaned: str
    encoded: str
    original_length: int
    cleaned_length: int
    encoded_length: int
     
    def __str__(self)->str:
        return (f'Original: {self.original}, '
            f'Cleaned: {self.cleaned}, '
            f'Original Length: {self.original_length}, '
            f'Cleaned Length: {self.cleaned_length}, '
            f'Encoded: {self.encoded}, '
            f'Encoded Length: {self.encoded_length}')


class StringChecker():
    def __init__(self, string_list: list) -> None:
        self.data = []
        for string in string_list:
            self.data.append(self.clean_one_string(string))

    def clean_one_string(self, string: str) -> SpecificString:
        this_str = SpecificString(original=string, original_length=len(string), cleaned='', cleaned_length=0,encoded='', encoded_length=0)
        new_str = string[1:-1]
        new_str = new_str.replace(r'\"',"~")
        new_str = new_str.replace(r'\\',"~")        
        new_str= re.sub(r'\\x[0-9a-f]{1,2}', '~', new_str)
        this_str.cleaned = new_str
        
        new_str = string.replace('\\', '\\\\')
        new_str = new_str.replace('"', r'\"')
        new_str = f'"{new_str}"'        
        this_str.encoded = new_str
        this_str.encoded_length = len(new_str)                         
        return this_str

    def part_1(self) -> int:
        return sum([x.original_length - x.cleaned_length for x in self.data])

    def part_2(self) -> int:
        return sum([x.encoded_length - x.original_length for x in self.data])


if __name__ == '__main__':
    with open('.\Part1Input.txt') as f:
        data = f.read().splitlines()
    #data = [r'""',r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    test = StringChecker(data)
    
    for x in test.data:
        print(x)
    
    
    
    print('Part1:',test.part_1())
    print('Part2:',test.part_2())
    
    
