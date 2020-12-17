from collections import namedtuple
import itertools
import numpy as np

Point = namedtuple('Point', 'x y z')

test_grid = """.#.
..#
###"""

real_grid = """##...#.#
####.#.#
#...####
..#.#.#.
####.#..
#.#.#..#
.####.##
..#...##"""

MATRIX_SIZE = 30
MATRIX_OFFSET = 15


def build_space_map(starting_grid):
    grid_rows = starting_grid.strip().split("\n")
    space_map = np.zeros((MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE))
    z = MATRIX_OFFSET
    for y, row in enumerate(grid_rows):
        for x, state in enumerate(row):
            p = Point(x + MATRIX_OFFSET, y + MATRIX_OFFSET, z)
            space_map[p.x, p.y, p.z] = 1 if state == '#' else 0

    return space_map


def active_neighbor_count(space_map, point):
    directions = set(list(itertools.permutations([-1, -1, -1, 0, 0, 0, 1, 1, 1], 3))) - {(0, 0, 0)}
    count = 0
    for d in directions:
        count += space_map[point.x + d[0], point.y + d[1], point.z + d[2]]
    return count


def propagate_cubes(space_map, cycles):

    for cycle in range(cycles):
        new_map = np.zeros((MATRIX_SIZE, MATRIX_SIZE, MATRIX_SIZE))
        for x in range(1, MATRIX_SIZE - 1):
            for y in range(1, MATRIX_SIZE - 1):
                for z in range(1, MATRIX_SIZE - 1):
                    if space_map[x, y, z] == 1:
                        new_map[x, y, z] = 1 if 2 <= active_neighbor_count(space_map, Point(x, y, z)) <= 3 else 0
                    else:
                        new_map[x, y, z] = 1 if active_neighbor_count(space_map, Point(x, y, z)) == 3 else 0

        space_map = new_map

    return space_map


def cube_count(space_map):
    return np.sum(np.concatenate(space_map))


space = build_space_map(test_grid)
c = cube_count(space)
assert c == 5
# final_space = propagate_cubes(space, 6)
# c = cube_count(final_space)
# assert c == 112


real_space = build_space_map(real_grid)
c = cube_count(real_space)
assert c == 36
final_space = propagate_cubes(real_space, 6)
c = cube_count(final_space)
print(f"Part 1 answer: {c}")
assert c == 382


# Part 2 -- will brute force work?
