import itertools
import numpy as np


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


def build_space_map(starting_grid, dimensions=3):
    grid_rows = starting_grid.strip().split("\n")
    dimension_range = (2 + len(grid_rows[0]), 2 + len(grid_rows), ) + (3,) * (dimensions - 2)
    space_map = np.full(dimension_range, 0, dtype=int)
    for y, row in enumerate(grid_rows):
        for x, state in enumerate(row):
            p = (x + 1, y + 1) + (1,) * (dimensions - 2)
            space_map[p] = 1 if state == '#' else 0

    return space_map


def active_neighbor_count(space_map, point, dimensions=3):
    p = (-1,) * dimensions + (0,) * dimensions + (1,) * dimensions
    home = (0,) * dimensions
    directions = set(list(itertools.permutations(p, dimensions))) - {home}
    count = 0
    for d in directions:
        check_point = tuple(d[i] + point[i] for i in range(dimensions))
        try:
            count += space_map[check_point]
        except IndexError:
            continue
        if count > 3:
            break
    return count


def propagate_cubes(space_map, cycles, dims=3):

    for cycle in range(cycles):
        dimension_range = (2 + space_map.shape[0], 2 + space_map.shape[1],) + (2 + space_map.shape[2],) * (dims - 2)
        new_map = np.full(dimension_range, 0, dtype=int)
        print(f"Growing matrix to {dimension_range}")

        for point, value in np.ndenumerate(space_map):
            offset_point = tuple(x+1 for x in point)
            if value == 1:
                new_map[offset_point] = 1 if 2 <= active_neighbor_count(space_map, point, dims) <= 3 else 0
            else:
                new_map[offset_point] = 1 if active_neighbor_count(space_map, point, dims) == 3 else 0

        space_map = new_map

    return space_map


def cube_count(space_map):
    return np.sum(np.concatenate(space_map))


space = build_space_map(test_grid)
c = cube_count(space)
assert c == 5
final_space = propagate_cubes(space, 6)
c = cube_count(final_space)
assert c == 112

print("Starting real part 1")
real_space = build_space_map(real_grid)
c = cube_count(real_space)
assert c == 36
final_space = propagate_cubes(real_space, 6)
c = cube_count(final_space)
print(f"Part 1 answer: {c}")
assert c == 382


# Part 2 -- will brute force work?
print("Starting part 2")
space = build_space_map(test_grid, 4)
c = cube_count(space)
assert c == 5
final_space = propagate_cubes(space, 6, 4)
c = cube_count(final_space)
assert c == 848

print("Starting real part 2")
real_space = build_space_map(real_grid, 4)
c = cube_count(real_space)
assert c == 36
final_space = propagate_cubes(real_space, 6, 4)
c = cube_count(final_space)
print(f"Part 2 answer: {c}")
