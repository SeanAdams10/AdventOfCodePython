"""
Solution for day 8 of 2015 Advent of Code.
"""
from dataclasses import dataclass
import re


@dataclass
class SpecificString():
    """
    this class is used to store the original string, the cleaned string, and the encoded string
    """
    original: str
    cleaned: str
    encoded: str
    original_length: int
    cleaned_length: int
    encoded_length: int

    def __str__(self) -> str:
        return (f'Original: {self.original}, '
                f'Cleaned: {self.cleaned}, '
                f'Original Length: {self.original_length}, '
                f'Cleaned Length: {self.cleaned_length}, '
                f'Encoded: {self.encoded}, '
                f'Encoded Length: {self.encoded_length}')


class StringChecker():
    """
    class to check strings for the 2015 Advent of Code Day 8
    """

    def __init__(self, string_list: list) -> None:
        self.data = []
        for string in string_list:
            self.data.append(self.clean_one_string(string))

    def clean_one_string(self, string: str) -> SpecificString:
        """
        Cleans up a specific string and returns a SpecificString object
        params:
            string: str - the string to clean
        returns:
            SpecificString - the cleaned string
        """
        this_str = SpecificString(original=string, original_length=len(
            string), cleaned='', cleaned_length=0, encoded='', encoded_length=0)
        new_str = string[1:-1]
        new_str = new_str.replace(r'\"', "~")
        new_str = new_str.replace(r'\\', "~")
        new_str = re.sub(r'\\x[0-9a-f]{1,2}', '~', new_str)
        this_str.cleaned = new_str
        this_str.cleaned_length = len(new_str)

        new_str = string.replace('\\', '\\\\')
        new_str = new_str.replace('"', r'\"')
        new_str = f'"{new_str}"'
        this_str.encoded = new_str
        this_str.encoded_length = len(new_str)
        return this_str

    def part_1(self) -> int:
        """
        Returns the part 1 answer
        """
        return sum([x.original_length - x.cleaned_length for x in self.data])

    def part_2(self) -> int:
        """
        Returns the part 2 answer
        """
        return sum([x.encoded_length - x.original_length for x in self.data])


if __name__ == '__main__':
    with open(r'2015\Day08\Part1Input.txt', encoding="ASCII") as f:
        data = f.read().splitlines()
    data = [r'""', r'"abc"', r'"aaa\"aaa"', r'"\x27"']

    test = StringChecker(data)

    for item in test.data:
        print(item)

    print('Part1:', test.part_1())
    print('Part2:', test.part_2())
