class PresentWrapping:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def calculate_wrapping_paper(self):
        side1 = self.length * self.width
        side2 = self.width * self.height
        side3 = self.height * self.length
        smallest_side = min(side1, side2, side3)
        return 2 * (side1 + side2 + side3) + smallest_side

    def calculate_ribbon(self):
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

    for present in present_dimensions:
        length, width, height = present.split('x')
        present = PresentWrapping(int(length), int(width), int(height))
        total_wrapping += present.calculate_wrapping_paper()
        total_ribbon += present.calculate_ribbon()

    print(f'Part 1 answer is {total_wrapping}')
    print(f'Part 2 answer is {total_ribbon}')
