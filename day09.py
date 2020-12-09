from itertools import combinations


# Part 1
def process_code_file(file_name):
    with open(f"inputs/{file_name}") as f:
        data_list = [int(x) for x in f.read().strip().split("\n")]
    return data_list


def build_valid_sums(number_list, index, preamble):
    all_combinations = combinations(number_list[index:index + preamble], 2)
    sums = set([sum(t) for t in all_combinations])
    return sums


def find_invalid_code(number_list, preamble):
    for i, n in enumerate(number_list[preamble:]):
        valid_numbers = build_valid_sums(number_list, i, preamble)
        if n not in valid_numbers:
            return n
    return -1


numbers = process_code_file('day09_test.txt')
invalid = find_invalid_code(numbers, 5)
assert invalid == 127

real_numbers = process_code_file('day09.txt')
invalid = find_invalid_code(real_numbers, 25)
print(f"Part 1 invalid code: {invalid}")
assert invalid == 69316178


# Part 2
def find_weakness(number_list, desired):
    length = len(number_list)
    for i in range(length):
        for j in range(i + 1, length - i):
            s = sum(number_list[i:j+1])
            if s == desired:
                return min(number_list[i:j+1]) + max(number_list[i:j+1])
            elif s > desired:
                break
    return -1


weakness = find_weakness(numbers, 127)
assert weakness == 62

real_weakness = find_weakness(real_numbers, invalid)
print(f"Part 2 weakness: {real_weakness}")
assert real_weakness == 9351526
