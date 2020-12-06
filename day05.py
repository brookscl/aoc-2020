def pass_row(boarding_pass):
    field = boarding_pass[:7].replace('F', '0').replace('B', '1')
    return int(field, 2)


def pass_col(boarding_pass):
    field = boarding_pass[7:].replace('L', '0').replace('R', '1')
    return int(field, 2)


test_pass = 'FBFBBFFRLR'
assert pass_row(test_pass) == 44
assert pass_col(test_pass) == 5

test_pass = 'BFFFBBFRRR'
assert pass_row(test_pass) == 70
assert pass_col(test_pass) == 7


# Part 1
def process_pass_file(file_name):
    pass_list = []
    with open(f"inputs/{file_name}") as f:
        pass_list = f.read().strip().split("\n")
    return pass_list


def seat_id(p):
    return pass_row(p) * 8 + pass_col(p)


def find_highest_seat_id(pass_list):
    return seat_id(max(pass_list, key=lambda p: seat_id(p)))


passes = process_pass_file('day05_input.txt')
highest = find_highest_seat_id(passes)
assert highest == 874
print(f"Part 1 highest seat ID: {highest}")


# Part 2
def build_seat_map(pass_list):
    return sorted([seat_id(p) for p in pass_list])


def find_missing(seat_list):
    return [x for x in range(seat_list[0],
                             seat_list[-1]+1) if x not in seat_list]


sorted_passes = build_seat_map(passes)
missing = find_missing(sorted_passes)[0]
assert missing == 594
print(f"Missing: {missing}")
