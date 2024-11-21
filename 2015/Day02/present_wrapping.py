"""
this is the  solution for Day 2 of the Advent of Code 2015.
"""


class PresentWrapping:
    """
    This class is used to calculate the amount of wrapping paper
    """

    def __init__(self, length: int, width: int, height: int):
        """
        initialize the present dimensions
        param: length: int: The length of the present
        param: width: int: The width of the present
        param: height: int: The height of the present
        return: class: The present wrapping class
        """
        self.length = length
        self.width = width
        self.height = height

    def calculate_wrapping_paper(self) -> int:
        """
        Calculate the amount of wrapping paper needed for the present
        return: int: The amount of wrapping paper needed
        """
        side1 = self.length * self.width
        side2 = self.width * self.height
        side3 = self.height * self.length
        smallest_side = min(side1, side2, side3)
        return 2 * (side1 + side2 + side3) + smallest_side

    def calculate_ribbon(self):
        """
        calculate the amount of ribbon needed for the present
        essentially the perimeter of the smallest face
        plus the volume of the present

        return: int: The amount of ribbon needed
        """
        features = [self.length, self.width, self.height]
        features.sort()
        ribbon_length = 2 * (features[0] + features[1]) + \
            features[0] * features[1] * features[2]
        return ribbon_length


if __name__ == "__main__":
    with open(r'Part1Input.txt', encoding='utf-8') as f:
        present_dimensions = f.read().splitlines()

    total_wrapping: int = 0
    total_ribbon: int = 0

    print(f'Total Rows: {len(present_dimensions)}')

    for present_details in present_dimensions:
        input_length, input_width, input_height = present_details.split('x')
        present: PresentWrapping = PresentWrapping(
            int(input_length),
            int(input_width),
            int(input_height))
        total_wrapping += present.calculate_wrapping_paper()
        total_ribbon += present.calculate_ribbon()

    print(f'Part 1 answer is {total_wrapping}')
    print(f'Part 2 answer is {total_ribbon}')
