"""
Floor Counter for advent of code day 1 2015
"""


class FloorCounter:
    """
    Class to count the floor of a building based on the instructions
    given in the input file. '(' means to go up one floor and ')'
    means to go down one floor. The floor starts at 0.

    """

    def __init__(self):
        self.floor = 0

    def process_instructions(self, instructions: str) -> str:
        """
        Process the elevator instructions and return the floor
        param: instructions: str: The instructions to process
        return: int: The floor the elevator stops at
        """
        self.floor
        for char in instructions:
            if char == '(':
                self.floor += 1
            elif char == ')':
                self.floor -= 1
        return self.floor

    def basement(self, instructions: str) -> int:
        """
        Find the position of the first character that causes the elevator to
        enter the basement (floor -1)
        param: instructions: str: The instructions to process
        return: int: The position of the first character that causes the elevator 
        to enter the basement
        """
        self.floor = 0
        for i, char in enumerate(instructions, 1):
            if char == '(':
                self.floor += 1
            elif char == ')':
                self.floor -= 1
            if self.floor == -1:
                return i
        return None


if __name__ == "__main__":
    fc = FloorCounter()
    with open(r'Part1Input.txt', encoding='utf-8') as f:
        elevator_instructions = f.read()
    print(len(elevator_instructions))
    elevator_instructions = elevator_instructions[:1800]
    print(f'Part 1 answer is {fc.process_instructions(elevator_instructions)}')
    print(f'Part 2 answer is {fc.basement(elevator_instructions)}')
