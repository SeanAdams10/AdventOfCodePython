from time import perf_counter
from utils import get_input_data, timing_decorator
import re

def read_input(data) -> list:
    """
    placeholder for the parser needed for this day's puzzle
    """
    rules = []
    word = ""
    for line in data:
        parts = line.split(" => ")
        if len(parts) == 2:
            rules.append((parts[0], parts[1]))
        elif line.strip() != "":
            word = line.strip()
    return rules, word

def part1(rules, word):
    answers = set()
    for src, dest in rules:
        for match in re.finditer(src, word):
            new_word = word[:match.start()] + dest + word[match.end():]
            answers.add(new_word)
    print("Part 1:",len(answers))

def part_2(rules, word):
    visited = []

    def depth_first(word, steps):
        if word == "e":
            print("Found it!", steps)
            return steps
        if word in visited:
            return None
        visited.append(word)
        for src, dest in rules:
            for match in re.finditer(dest, word):
                new_word = word[:match.start()] + src + word[match.end():]
                depth = depth_first(new_word, steps + 1)
                if depth:
                    return(depth)
        
        return None

    final_depth = depth_first(word, 0)
    print("Part 2:", final_depth)
    

if __name__ == "__main__":
    data = get_input_data(2015, 19, sample=0)
    rules, word = read_input(data)
    part1(rules, word)
    part_2(rules, word)
