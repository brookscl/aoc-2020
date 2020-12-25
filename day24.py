import collections
import math


Point = collections.namedtuple("Point", ["x", "y"])
_Hex = collections.namedtuple("Hex", ["q", "r", "s"])


def Hex(q, r, s):
    assert not (round(q + r + s) != 0), "q + r + s must be 0"
    return _Hex(q, r, s)


def hex_add(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]


def hex_direction(direction):
    return hex_directions[direction]


def hex_neighbor(h, direction):
    return hex_add(h, hex_direction(direction))


direction_map = {
    'ne': 0,
    'e': 1,
    'se': 2,
    'sw': 3,
    'w': 4,
    'nw': 5,
}


def load_tile_flips(file_name):
    with open(f"inputs/{file_name}") as f:
        flips = f.read().strip().split("\n")

    return flips


def process_flip(directions):
    h = Hex(0, 0, 0)
    while directions:
        if directions[:2] in direction_map:
            h = hex_neighbor(h, direction_map[directions[:2]])
            directions = directions[2:]
        else:
            h = hex_neighbor(h, direction_map[directions[:1]])
            directions = directions[1:]
    return h


def process_hex_flips(flips):
    hexes = set()
    for f in flips:
        destination = process_flip(f)
        if destination in hexes:
            hexes.remove(destination)
        else:
            hexes.add(destination)
    return hexes


def black_hexes(hexes):
    return len(hexes)


def part1():
    flips = load_tile_flips('day24_test.txt')
    hexes = process_hex_flips(flips)

    total_black = black_hexes(hexes)
    assert total_black == 10

    flips = load_tile_flips('day24.txt')
    hexes = process_hex_flips(flips)
    total_black = black_hexes(hexes)
    print(f"Part 1 total blacks: {total_black}")
    assert total_black == 469


def neighbors(tile):
    return [hex_neighbor(tile, d) for d in direction_map.values()]


def count_adjacent_blacks(tile, hexes):
    return sum(1 for n in neighbors(tile) if n in hexes)


# Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
def should_be_black(tile, hexes):
    c = count_adjacent_blacks(tile, hexes)
    if tile in hexes and (1 <= c <= 2):
        return True
    elif tile not in hexes and c == 2:
        return True
    else:
        return False


def process_generations(hexes, generations):
    for g in range(generations):
        new_pattern = set()
        checked_hexes = set()
        # we should be OK just looking at neighbors of all of our black hexes!
        for h in hexes:
            for n in [h] + neighbors(h):
                if n not in checked_hexes:
                    checked_hexes.add(n)
                    if should_be_black(n, hexes):
                        new_pattern.add(n)

        hexes = new_pattern

    return hexes


def part2():
    flips = load_tile_flips('day24_test.txt')
    hexes = process_hex_flips(flips)
    final_hexes = process_generations(hexes, 100)
    total_black = black_hexes(final_hexes)
    assert total_black == 2208

    flips = load_tile_flips('day24.txt')
    hexes = process_hex_flips(flips)
    final_hexes = process_generations(hexes, 100)
    total_black = black_hexes(final_hexes)
    print(f"Part 2 total blacks: {total_black}")
    assert total_black == 4353


part1()
part2()
