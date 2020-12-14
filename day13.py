from numpy import prod


def load_bus_times(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")
    earliest_departure = int(raw_lines[0])
    bus_list = [int(b) for b in raw_lines[1].split(",") if b != 'x']
    return earliest_departure, bus_list


depart, buses = load_bus_times('day13_test.txt')
wait_times = [(b, (b - depart % b)) for b in buses]
shortest = min(wait_times, key=lambda b: b[1])
print(f"Shortest wait time is {shortest}")
assert (shortest[0] * shortest[1]) == 295

real_depart, real_buses = load_bus_times('day13.txt')
wait_times = [(b, (b - real_depart % b)) for b in real_buses]
shortest = min(wait_times, key=lambda b: b[1])
print(f"Part 1 shortest wait time is {shortest}")
print(f"Part 1 answer: {shortest[0] * shortest[1]}")
assert (shortest[0] * shortest[1]) == 3246


# Part 2
def load_all_bus_times(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")

    bus_list = []
    bus_remainder = []
    for i, b in enumerate(raw_lines[1].split(',')):
        if b != 'x':
            bus_list.append(int(b))
            if i > 0:
                bus_remainder.append(int(b) - i)
            else:
                bus_remainder.append(0)
    return bus_list, bus_remainder


def earliest_consecutive_departure(num, rem):
    k = len(num)
    product = prod(num)
    result = 0

    for n, r in zip(num, rem):
        pp = product // n
        result = result + r * pow(int(pp), -1, n) * pp

    return result % product


test_buses = [17, 13, 19]
remainders = [0, 11, 16]
d = earliest_consecutive_departure(test_buses, remainders)
test_buses, remainders = load_all_bus_times('day13_test.txt')
d = earliest_consecutive_departure(test_buses, remainders)
assert d == 1068781

buses, remainders = load_all_bus_times('day13.txt')
d = earliest_consecutive_departure(buses, remainders)
print(f"Part 2 answer: {d}")
assert d == 1010182346291467
