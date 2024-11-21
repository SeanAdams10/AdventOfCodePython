"""Solution for Day 4 of Advent of Code 2015."""
import hashlib


def zero_md5(in_str: str, num_zeros=5) -> int:
    """
    Finds the smallest integer such that when appended to the input string and hashed using MD5,
    the resulting hash starts with a specified number of leading zeros.
    params:
        in_str (str): The input string to which the integer will be appended.
        num_zeros (int, optional): The number of leading zeros required in the hash. Defaults to 5.
    Returns:
        int: The smallest integer that, when appended to the input string, produces an MD5 hash
                with the specified number of leading zeros.
    """
    i = -1
    while True:
        i += 1
        input_bytes = (in_str + str(i)).encode()
        md5 = hashlib.md5(input_bytes)
        if md5.hexdigest()[:num_zeros] == '0' * num_zeros:
            return i


if __name__ == "__main__":
    print(f'Part 1: {zero_md5('bgvyzdsv', 5)}')
    print(f'Part 2: {zero_md5('bgvyzdsv', 6)}')
