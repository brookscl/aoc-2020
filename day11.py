import copy


def process_seat_file(file_name):
    with open(f"inputs/{file_name}") as f:
        rows = f.read().strip().split("\n")
    return [list(s) for s in rows]


def count_occupied_adjacents(seat_map, x, y):
    count_of_occupied_seats = 0
    adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]
    for dx, dy in adjacency:
        if 0 <= (x + dx) < len(seat_map[0]) and 0 <= y + dy < len(seat_map):
            if seat_map[y + dy][x + dx] == '#':
                count_of_occupied_seats += 1
    return count_of_occupied_seats


def adjacent_seats_unoccupied(seat_map, x, y):
    return count_occupied_adjacents(seat_map, x, y) == 0


def crowded_seat(seat_map, x, y):
    return count_occupied_adjacents(seat_map, x, y) >= 4


def check_seat(seat_map, x, y, new_map, sit_rule, leave_rule):
    if seat_map[y][x] == 'L':    # Unoccupied
        if sit_rule(seat_map, x, y):
            new_map[y][x] = '#'
            return True
    elif seat_map[y][x] == '#':  # Occupied
        if leave_rule(seat_map, x, y):
            new_map[y][x] = 'L'
            return True
    return False


def process_ferry(seat_map, sit_rule=adjacent_seats_unoccupied, leave_rule=crowded_seat):
    changed = True
    new_map = copy.deepcopy(seat_map)
    while changed:
        changed = False
        for y, row in enumerate(seat_map):
            for x in range(len(row)):
                if check_seat(seat_map, x, y, new_map, sit_rule, leave_rule) and not changed:
                    changed = True
        seat_map = copy.deepcopy(new_map)
    return new_map


def occupied_count(seat_map):
    return sum(s.count('#') for s in seat_map)


# Part 1
seats = process_seat_file('day11_test.txt')
final_seats = process_ferry(seats)
count = occupied_count(final_seats)
assert count == 37

real_seats = process_seat_file('day11.txt')
final_seats = process_ferry(real_seats)
count = occupied_count(final_seats)
assert count == 2386
print(f"Part 1 count: {count}")


# Part 2
def count_occupied_visibles(seat_map, x, y):
    count_of_occupied_seats = 0
    adjacency = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if not (i == j == 0)]
    for dx, dy in adjacency:
        x_pos, y_pos = x, y
        while 0 <= (x_pos + dx) < len(seat_map[0]) and 0 <= y_pos + dy < len(seat_map):
            if seat_map[y_pos + dy][x_pos + dx] == '#':
                count_of_occupied_seats += 1
                break
            elif seat_map[y_pos + dy][x_pos + dx] == 'L':
                break
            x_pos += dx
            y_pos += dy
    return count_of_occupied_seats


def visible_seats_unoccupied(seat_map, x, y):
    return count_occupied_visibles(seat_map, x, y) == 0


def mildly_crowded_seat(seat_map, x, y):
    return count_occupied_visibles(seat_map, x, y) >= 5


final_seats = process_ferry(seats, visible_seats_unoccupied, mildly_crowded_seat)
count = occupied_count(final_seats)
assert count == 26

final_seats = process_ferry(real_seats, visible_seats_unoccupied, mildly_crowded_seat)
count = occupied_count(final_seats)
# assert count == 2386
print(f"Part 2 count: {count}")
