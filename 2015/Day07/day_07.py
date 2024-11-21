"""
Day 7: This is the solution for Day 7 of the Advent of Code 2015.
Single class with not much complexity
"""
from typeguard import typechecked


class Wiring:
    """
    Wiring class takes care of the assignment, parsing etc
    """

    def __init__(self) -> None:
        """
        Initialize the wiring
        return: None
        """
        self.wires: dict = {}

    def load_instructions(self, instructions):
        """
        Load the instructions into the wiring
        param: instructions: list: The instructions to load
        return: None
        """
        for instruction in instructions:
            instruction = instruction.strip()
            parts = instruction.split()
            target = parts[-1]
            self.wires[target] = {"instruction": instruction, "value": -1}

    def solve_for_x(self, target) -> int:
        """solves for the target wire"""

        print(f'Solving for {
              target} - instruction: {self.wires[target]["instruction"]}')

        if self.wires[target]["value"] < 0:
            self.run_instruction(self.wires[target]["instruction"])
        return self.wires[target]["value"]

    @typechecked
    def run_instruction(self, instruction):
        """"
        Parse the input instruction.
        param: instruction: str: The instruction to parse
        return: tuple: The parsed instruction
        """
        self.wires = dict(sorted(self.wires.items()))

        parts = instruction.split()
        if "AND" in parts:
            self.and_gate(parts[0], parts[2], parts[4])
        elif "OR" in parts:
            self.or_gate(parts[0], parts[2], parts[4])
        elif "LSHIFT" in parts:
            # p LSHIFT 2 -> q
            self.shift_left(input_wire=parts[0],
                            places=int(parts[2]),
                            target_wire=parts[4])
            # return ("LSHIFT", parts[0], parts[2], parts[4])
        elif "RSHIFT" in parts:
            # p RSHIFT 2 -> q
            self.shift_right(input_wire=parts[0],
                             places=int(parts[2]),
                             target_wire=parts[4])
        elif "NOT" in parts:
            # NOT dq -> dr
            self.not_gate(input_wire=parts[1], target_wire=parts[3])
        else:  # Assign
            if parts[0].isdigit():
                self.assign_literal(target_wire=parts[2],
                                    value=int(parts[0]))
            else:
                self.assign_wire(source_wire=parts[0],
                                 target_wire=parts[2])

    def __str__(self):
        """
        Returns the string representation of the wiring
        """
        result = '\n'.join(
            [f'{key}: {element["value"]}' for key, element in self.wires.items()])

        return result

    @typechecked
    def assign_literal(self, target_wire: str, value: int) -> None:
        """
        Assign the value to the wire
        param: instruction: tuple: The instruction to assign
        return: None
        """
        if value > 65535 or value < 0:
            raise ValueError(f"Value {value} is out of range")

        self.wires[target_wire]["value"] = value

    @typechecked
    def assign_wire(self, source_wire: str, target_wire: str) -> None:
        """
        Assign the value to the wire
        param: instruction: tuple: The instruction to assign
        return: None
        """
        if self.wires[source_wire]["value"] == -1:
            self.solve_for_x(source_wire)

        self.wires[target_wire]["value"] = self.wires[source_wire]["value"]

    @typechecked
    def and_gate(self, x: str, y: str, target: str) -> None:
        """
        Perform an and operation
        param: x: str: The first wire
        param: y: str: The second wire
        param: target: str: The target wire
        return: None
        """

        if x.isdigit():
            xval = int(x)
        else:
            if self.wires[x]["value"] == -1:
                self.solve_for_x(x)
            xval = self.wires[x]["value"]

        if y.isdigit():
            yval = int(y)
        else:
            if self.wires[y]["value"] == -1:
                self.solve_for_x(y)
            yval = self.wires[y]["value"]

        self.wires[target]["value"] = xval & yval

    @typechecked
    def or_gate(self, x: str, y: str, target: str) -> None:
        """
        perform an or operation
        param: x: str: The first wire
        param: y: str: The second wire
        param: target: str: The target wire
        return: None
        """

        if self.wires[x]["value"] == -1:
            self.solve_for_x(x)

        if self.wires[y]["value"] == -1:
            self.solve_for_x(y)

        self.wires[target]["value"] = self.wires[x]["value"] | self.wires[y]["value"]

    @typechecked
    def not_gate(self, input_wire: str, target_wire: str) -> None:
        """
        perform a not operation
        param: target: str: The target wire
        return: None
        """

        if self.wires[input_wire]["value"] == -1:
            self.solve_for_x(input_wire)

        if input_wire.isdigit() or target_wire.isdigit():
            print(f'Bad Input to Not gate {input_wire} {target_wire}')
            raise ValueError("Invalid input")

        # this is a 16 bit number so 2^16 - 1
        self.wires[target_wire]["value"] = self.wires[input_wire]["value"] ^ 65535

    @typechecked
    def shift_left(self, input_wire: str, places: int, target_wire: str) -> None:
        """
        Perform a left shift operation on the input wire and store the result in the target wire.

        Param: input_wire (str): The wire whose value will be shifted.
        Param: places (int): The number of places to shift the value to the left.
        Param: target_wire (str): The wire where the result will be stored.

        Returns:
            None
        """

        if self.wires[input_wire]["value"] == -1:
            self.solve_for_x(input_wire)

        self.wires[target_wire]["value"] = self.wires.get(input_wire, 0)[
            "value"] << places
        # to cap this at 65535
        self.wires[target_wire]["value"] = self.wires[target_wire]["value"] & 65535

    @typechecked
    def shift_right(self, input_wire: str, places: int, target_wire: str) -> None:
        """
        Perform a right shift operation on the input wire and store the result in the target wire.

        Param: input_wire (str): The wire whose value will be shifted.
        Param: places (int): The number of places to shift the value to the left.
        Param: target_wire (str): The wire where the result will be stored.

        Returns:
            None
        """
        if self.wires[input_wire]["value"] == -1:
            self.solve_for_x(input_wire)

        self.wires[target_wire]["value"] = self.wires[input_wire]["value"] >> places


if __name__ == "__main__":
    with open(r"2015/Day07/Part1Input.txt", encoding="ascii") as f:
        lines = f.readlines()

    tst = Wiring()
    tst.load_instructions(lines)

    nodes = ('lw', 'lv', 'a', 'lx', 'e', 'lv', 'lw')
    # for note in nodes:
    #     print(f'{note}: {tst.wires[note]}')
    #     print(f'{note}: {tst.solve_for_x(note)}')
    #     print(f'{note}: {tst.wires[note]}\n')

    print(f'Part 1: {tst.solve_for_x("a")}')
    # for note in nodes:
    #     print(f'{note}: {tst.wires[note]}')

    tst.assign_literal(target_wire='b', value=tst.solve_for_x("a"))
    for key, val in tst.wires.items():
        if key != 'b':
            val["value"] = -1

    print(f'Part 2: {tst.solve_for_x("a")}')
