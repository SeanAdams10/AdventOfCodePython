from itertools import groupby


def most_contiguous_repeats(strings):

    def max_contiguous_repeats(s):
        # Group adjacent characters and find the longest group length
        # return max(len(list(group)) for _, group in groupby(s))
        groups = [len(list(grp)) for _,grp in groupby(s)]
        return sum([x for x in groups if x > 1])

    # Return the string with the highest count of contiguous repeats
    return max(strings, key=max_contiguous_repeats)

# Example usage
strings = ['ababab', 'aaabbb', 'abaabb']
result = most_contiguous_repeats(strings)
print(result)  # Output should be 'aaabbb'