"""
Solution for Advent of Code Day 06
This module contains a LightManager class to manage a grid of lights based on commands
from an input file. The commands can turn on, turn off, or toggle the lights within
specified coordinates. The module also includes functionality to count the number of
lights that are on and to ensure that light values do not exceed specified limits.
Classes:
    LightManager: Manages the grid of lights and processes commands to modify the grid.
Functions:
    main: Reads commands from an input file, applies them to the LightManager, and prints
          the results for Part 1 and Part 2 of the puzzle.
"""
import re
import time
from dataclasses import dataclass
import numpy as np


@dataclass
class LightManager:
    """"
    This class is used to manage the lights through the entire solution
    """

    command: str
    first_x: int
    first_y: int
    second_x: int
    second_y: int

    def __init__(self, x_size: int = 1000, y_size: int = 1000, max_value: int = 1):
        if x_size <= 0 or y_size <= 0:
            raise ValueError("Invalid dimensions")
        self.max_value = max_value
        self.lights = np.zeros((x_size, y_size), dtype=int)

    def split_command(self, input_line) -> None:
        """
        This splits the command into the command and the coordinates
        param: input_line: str: The command to be split
        return: None
        """
        # Use regex to extract the command and coordinates
        match = re.match(
            r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)", input_line)

        if match:
            self.command = str(match.group(1))
            self.first_x = int(match.group(2))
            self.first_y = int(match.group(3))
            self.second_x = int(match.group(4))
            self.second_y = int(match.group(5))
        else:
            raise ValueError("No match found")

    def execute_command(self) -> None:
        """
        This takes the command given on the lights and executes it
        return: None
        """
        x1, x2 = self.first_x, self.second_x
        y1, y2 = self.first_y, self.second_y

        if x1 < 0 or x2 >= self.lights.shape[0] or y1 < 0 or y2 >= self.lights.shape[1]:
            raise ValueError("Coordinates out of bounds")

        match self.command:
            case "turn on":
                self.lights[x1:x2+1, y1:y2+1] += 1
            case "turn off":
                self.lights[x1:x2+1, y1:y2+1] -= 1
            case "toggle":
                if self.max_value == 1:
                    self.lights[x1:x2+1, y1:y2 +
                                1] = np.logical_not(self.lights[x1:x2+1, y1:y2+1])
                else:
                    self.lights[x1:x2+1, y1:y2+1] += 2
            case _:
                raise ValueError("Unknown command")

        # ensure that the lights are not negative, and they are not breaking the max value
        self.lights = np.maximum(self.lights, 0)
        if self.max_value == 1:
            self.lights = np.minimum(self.lights, self.max_value)

    def apply_action(self, action: str) -> None:
        """
        This applies the action provided - first splitting it into
        component parts and then executing the command
        """
        self.split_command(action)
        self.execute_command()

    def count_lights(self) -> int:
        """
        this counts the number of lights turned on
        """
        return np.sum(self.lights)


if __name__ == "__main__":
    start_time = time.time()

    light_manager = LightManager(1000, 1000, 1)
    light_manager2 = LightManager(1000, 1000, -1)

    with open(r"./2015/Day06/Part1Input.txt", "r", encoding="ASCII") as file:
        lines = file.readlines()

    for row, line in enumerate(lines):
        if row >= 999:
            break
        light_manager.apply_action(line.strip())
        light_manager2.apply_action(line.strip())

    print(f"Part 1 answer: {light_manager.count_lights()}")
    print(f"Part 2 answer: {light_manager2.count_lights()}")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
