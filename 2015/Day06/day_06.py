import re
import numpy as np
import time

class LightManager:
    def __init__(self, x_size:int=1000, y_size:int=1000, max_value:int=1):
        if x_size <= 0 or y_size <= 0:
            raise ValueError("Invalid dimensions")
        self.command = None
        self.first_x = None
        self.first_y = None
        self.second_x = None
        self.second_y = None
        self.max_value = max_value
        self.lights = np.zeros((x_size, y_size), dtype=int)
        

    def split_command(self, input_line):
        # Use regex to extract the command and coordinates
        match = re.match(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)", input_line)

        if match:
            self.command = match.group(1)
            self.first_x = int(match.group(2))
            self.first_y = int(match.group(3))
            self.second_x = int(match.group(4))
            self.second_y = int(match.group(5))
        else:
            raise ValueError("No match found")
     
    def execute_command(self):
        # print(f"Executing command: {self.command} from ({self.first_x}, {self.first_y}) to ({self.second_x}, {self.second_y})")
        x1,x2 = self.first_x, self.second_x
        y1,y2 = self.first_y, self.second_y
        
        if x1<0 or x2>=self.lights.shape[0] or y1<0 or y2>=self.lights.shape[1]:
            raise ValueError("Coordinates out of bounds")
        
        match self.command:
            case "turn on":
                self.lights[x1:x2+1, y1:y2+1] +=1
            case "turn off":
                self.lights[x1:x2+1, y1:y2+1] -=1
            case "toggle":
                if self.max_value == 1:
                    self.lights[x1:x2+1, y1:y2+1] = np.logical_not(self.lights[x1:x2+1, y1:y2+1])
                else:
                    self.lights[x1:x2+1, y1:y2+1] += 2
            case _:
                raise ValueError("Unknown command")
            

        #ensure that the lights are not negative, and they are not breaking the max value
        self.lights = np.maximum(self.lights, 0)
        if self.max_value == 1:
            self.lights = np.minimum(self.lights, self.max_value)

           
    def apply_action(self, action: str):
        self.split_command(action)
        self.execute_command()
        
    def count_lights(self):
        return np.sum(self.lights)

if __name__ == "__main__":
    start_time = time.time()
    
    light_manager = LightManager(1000, 1000, 1)
    light_manager2 = LightManager(1000, 1000, None)
    
    with open(r"./2015/Day06/Part1Input.txt", "r") as file:
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



