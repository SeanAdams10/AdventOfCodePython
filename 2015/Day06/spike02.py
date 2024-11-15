import re

input_string = "turn on 489,959 through 759,964"

def split_command(input_line):
    # Use regex to extract the command and coordinates
    match = re.match(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)", input_string)

    if match:
        command = match.group(1)
        first_x = int(match.group(2))
        first_y = int(match.group(3))
        second_x = int(match.group(4))
        second_y = int(match.group(5))
    else:
        print("No match found")





