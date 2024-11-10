"""
Present delivery class to solve AOC Day 3
"""


class PresentDelivery:
    """
    Present delivery class to solve AOC Day 3
    """

    def __init__(self, persona_count: int) -> None:
        """Initialise the present delivery object
        :param persona_count: The number of people delivering presents"""
        self.persona_count = persona_count
        self.position: list = []
        for _ in range(persona_count):
            self.position.append((0, 0))
        self.visited: set = set()

    def process_path(self, steps: str):
        """Process the path of steps
        :param steps: The steps to process"""
        # Add the starting position to the visited set
        self.visited.add(tuple(self.position[0]))

        # then work through all the moves
        for direction in steps:
            self.move(direction)
            # Add in the position which is now at the end of the
            # list of positions in self.position
            self.visited.add(tuple(self.position[-1]))

    def move(self, direction: str) -> None:
        """Move the position based on the direction
        This works by each persona being rotated through
        the first slot in self.position

        :param direction: The direction to move in"""

        print(self.position)
        current_pos: list = list(self.position.pop(0))
        print(current_pos)

        if direction == '^':
            current_pos[1] += 1
        elif direction == 'v' or direction == 'V':
            current_pos[1] -= 1
        elif direction == '>':
            current_pos[0] += 1
        elif direction == '<':
            current_pos[0] -= 1

        self.position.append(tuple(current_pos))

    def visited_count(self) -> int:
        """Return the number of houses visited"""
        return len(self.visited)


if __name__ == '__main__':
    pd_single = PresentDelivery(1)
    pd_double = PresentDelivery(2)
    with open(r'.\2015\Day03\Part1Input.txt', 'r', encoding='utf8') as working_data:
        path = working_data.read()
        pd_single.process_path(path)
        pd_double.process_path(path)

    print(f'Part 1 answer is {pd_single.visited_count()}')
    print(f'Part 2 answer is {pd_double.visited_count()}')
