def load_nav(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")
    nav_list = []
    for line in raw_lines:
        nav_list.append((line[0], int(line[1:])))
    return nav_list


def turn(current_facing, degrees):
    return (current_facing + (degrees // 90)) % 4


def move(x, y, direction, amount):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    x += directions[direction][0] * amount
    y += directions[direction][1] * amount
    return x, y


# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.
def follow_nav(nav_list):
    direction_map = {'E': 0, 'S': 1, 'W': 2, 'N': 3}
    x, y = 0, 0
    direction = 0
    for n in nav_list:
        command, amount = n[0], n[1]
        if command == 'L':
            direction = turn(direction, -amount)
        elif command == 'R':
            direction = turn(direction, amount)
        elif command == 'F':
            (x, y) = move(x, y, direction, amount)
        else:
            (x, y) = move(x, y, direction_map[command], amount)
    return x, y


def manhattan_distance(coord):
    return abs(coord[0]) + abs(coord[1])


instructions = load_nav('day12_test.txt')
final_position = follow_nav(instructions)
assert manhattan_distance((-5, 17)) == 22
assert manhattan_distance(final_position) == 25

real_instructions = load_nav('day12.txt')
final_position = follow_nav(real_instructions)
d = manhattan_distance(final_position)
print(f"Part 1 distance: {d}")
assert d == 445


# Part 2
def rotate_waypoint(waypoint, amount):
    new_x, new_y = waypoint
    sign = amount // abs(amount)
    for _ in range(abs(amount) // 90):
        new_x, new_y = sign * new_y, -sign * new_x
    return new_x, new_y


def move_to_waypoint(x, y, waypoint, amount):
    return x + waypoint[0] * amount, y + waypoint[1] * amount


def move_waypoint(waypoint, direction, amount):
    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    x = waypoint[0] + directions[direction][0] * amount
    y = waypoint[1] + directions[direction][1] * amount
    return x, y


# Action N means to move the waypoint north by the given value.
# Action S means to move the waypoint south by the given value.
# Action E means to move the waypoint east by the given value.
# Action W means to move the waypoint west by the given value.
# Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
# Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
# Action F means to move forward to the waypoint a number of times equal to the given value.
def follow_waypoint(nav_list):
    direction_map = {'E': 0, 'S': 1, 'W': 2, 'N': 3}
    waypoint = (10, 1)
    x, y = 0, 0
    # direction = 0
    for n in nav_list:
        command, amount = n[0], n[1]
        if command == 'L':
            waypoint = rotate_waypoint(waypoint, -amount)
        elif command == 'R':
            waypoint = rotate_waypoint(waypoint, amount)
        elif command == 'F':
            (x, y) = move_to_waypoint(x, y, waypoint, amount)
        else:
            waypoint = move_waypoint(waypoint, direction_map[command], amount)
    return x, y


final_position = follow_waypoint(instructions)
assert manhattan_distance(final_position) == 286

final_position = follow_waypoint(real_instructions)
d = manhattan_distance(final_position)
print(f"Part 2 distance: {d}")
assert d == 42495
