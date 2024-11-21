import re

"""
Solution for Advent of Code Day 05
"""


def is_3_vowels(word):
    """Check if a word has at least 3 vowels"""
    vowels = 'aeiou'
    print((1 for letter in word if letter in vowels))
    # return sum(1 for letter in word if letter in vowels) >= 3
    return len(re.findall(r'[aeiou]', word)) >= 3


def is_double_letter(word):
    """Check if a word has at least one letter that appears twice in a row"""
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return True
    return False


def is_no_banned_strings(word):
    """Check if a word does not contain any of the banned strings"""
    banned_strings = ['ab', 'cd', 'pq', 'xy']
    return not any(banned in word for banned in banned_strings)


def is_nice(word):
    """Check if a word is nice"""
    return is_3_vowels(word) and is_double_letter(word) and is_no_banned_strings(word)


def is_double_pair(word):
    """Check if a word has at least one pair of letters that appear at least twice"""
    if re.search(r'(..).*\1', word):
        return True
    return False


def is_repeat_char(word):
    """Check if a word has at least one pair of letters that appear at least twice"""
    if re.search(r'(.).\1', word):
        return True
    return False


def is_nice_2(word):
    """Check if a word is nice"""
    return is_double_pair(word) and is_repeat_char(word)


if __name__ == '__main__':
    with open(r'2015\Day05\Part1Input.txt', 'r') as file:
        words = file.read().splitlines()
    nice_words = sum(1 for word in words if is_nice(word))
    print(f'Part 1: {nice_words}')

    nice_words_2 = sum(1 for word in words if is_nice_2(word))
    print(f'Part 2: {nice_words_2}')
