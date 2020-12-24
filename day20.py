import numpy as np
import math


def load_tiles(file_name):
    tile_set = {}
    with open(f"inputs/{file_name}") as f:
        raw_tiles = f.read().strip().split("\n\n")

    for tile in raw_tiles:
        tile_rows = tile.split('\n')
        tile_number = tile_rows[0].split(' ')[1][:4]
        top_row = tile_rows[1]
        bottom_row = tile_rows[10]
        left_row, right_row = '', ''
        for row in tile_rows[1:]:
            left_row += row[0]
            right_row += row[9]

        # 0, 1, 2, 3 positions <-- could use enums
        tile_set[tile_number] = [top_row, right_row, bottom_row, left_row]

    return tile_set


def find_all_matching_rows(search_tile, search_border, tiles):
    matches = []
    for tile_number, tile in tiles.items():
        if search_tile != tile_number:
            for i, border in enumerate(tile):
                if search_border == border:
                    matches.append((tile_number, i, border))

    return matches


# Append the dictionary for each tile with all matching rows in other tiles
def search_for_matching_edges(tiles):
    matches = {}
    for tile_number, tile in tiles.items():
        match_list = {}
        for i, border in enumerate(tile):
            forward_matches = find_all_matching_rows(tile_number, border, tiles)
            backward_matches = find_all_matching_rows(tile_number, border[::-1], tiles)
            match_list[i] = (forward_matches, backward_matches)
        matches[tile_number] = match_list

    return matches


def non_matching_rows(border_match_list):
    return border_match_list[0] == [] and border_match_list[1] == []


def find_tile_positions(tile_matches):
    corners = set()
    outsiders = set()
    insiders = set()
    for num, match_data in tile_matches.items():
        empty_edges = sum(non_matching_rows(b) for b in list(match_data.values()))
        if empty_edges == 2:
            corners.add(num)
        elif empty_edges == 1:
            outsiders.add(num)
        elif empty_edges == 0:
            insiders.add(num)
    return corners, outsiders, insiders


def part1():
    tiles = load_tiles('day20_test.txt')
    tile_matches = search_for_matching_edges(tiles)
    print(tile_matches)
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    corner_product = np.prod([int(i) for i in corners])
    print("Test grid:")
    print("==========")
    print(f"Corners: {corners}")
    print(f"Outsiders: {outsiders}")
    print(f"Insiders: {insiders}")
    assert corner_product == 20899048083289

    tiles = load_tiles('day20.txt')
    tile_matches = search_for_matching_edges(tiles)
    dimension = int(math.sqrt(len(tile_matches)))
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    print("Real grid:")
    print("==========")
    print(f"Corners: {corners}")
    print(f"Outsiders: {outsiders}")
    print(f"Insiders: {insiders}")
    assert len(corners) == 4
    assert len(outsiders) == (dimension - 2) * 4
    assert len(insiders) == (dimension - 2) ** 2
    corner_product = np.prod([int(i) for i in corners])
    print(f"Part 1 corners list: {corners}, product: {corner_product}")
    assert corner_product == 17148689442341


# Part 2
def load_tiles_as_matrices(file_name):
    tile_set = {}
    with open(f"inputs/{file_name}") as f:
        raw_tiles = f.read().strip().split("\n\n")

    for tile in raw_tiles:
        tile_matrix = []
        tile_rows = tile.split('\n')
        tile_number = tile_rows[0].split(' ')[1][:4]
        for row in tile_rows[1:]:
            tile_matrix.append(list(row))
        # 0, 1, 2, 3 positions <-- could use enums
        tile_set[tile_number] = np.array(tile_matrix)

    return tile_set


def find_adjacent_tile(tile, search_set, tile_matches, reverse=False):
    matches = tile_matches[tile]
    for direction in range(4):
        # This is also where we'll find the required rotation and flipping
        # match_list[i] = (forward_matches, backward_matches)
        if reverse:
            search_list = list(reversed(matches[direction][1])) + list(reversed(matches[direction][0]))
        else:
            search_list = matches[direction][0] + matches[direction][1]
        for edge in search_list:
            if edge[0] in search_set:
                # Will need to rotate based on i
                return edge[0]
    return None


def build_tile_grid(start_corner, corners, outsiders, insiders, tile_matrices, tile_matches, reverse=False):
    shape = int(math.sqrt(len(tile_matrices)))
    grid = {}
    current = start_corner
    # Build top row (ugh)
    x, y = 0, 0
    grid[(x, y)] = (current, tile_matrices[current])
    for x in range(1, shape - 1):
        tile = find_adjacent_tile(current, outsiders, tile_matches, reverse)
        if not tile:
            return False
        grid[(x, y)] = (tile, tile_matrices[tile])
        outsiders.remove(tile)
        current = tile
    corner = find_adjacent_tile(current, corners, tile_matches, reverse)
    grid[(shape - 1, 0)] = (corner, tile_matrices[corner])
    corners.remove(corner)

    # Build middle rows (ugh ugh)
    for y in range(1, shape - 1):
        left_edge = find_adjacent_tile(grid[(0, y-1)][0], outsiders, tile_matches, reverse)
        if not left_edge:
            return False
        grid[(0, y)] = (left_edge, tile_matrices[left_edge])
        outsiders.remove(left_edge)
        current = left_edge
        for x in range(1, shape - 1):
            tile = find_adjacent_tile(current, insiders, tile_matches, reverse)
            if not tile:
                return False
            grid[(x, y)] = (tile, tile_matrices[tile])
            insiders.remove(tile)
            current = tile
        right_edge = find_adjacent_tile(current, outsiders, tile_matches, reverse)
        if not right_edge:
            return False
        grid[(shape - 1, y)] = (right_edge, tile_matrices[right_edge])

    # Finally, build bottom row
    y = shape - 1
    lower_left = find_adjacent_tile(grid[(0, y-1)][0], corners, tile_matches, reverse)
    grid[(0, y)] = (lower_left, tile_matrices[lower_left])
    corners.remove(lower_left)
    current = lower_left
    for x in range(1, shape - 1):
        tile = find_adjacent_tile(current, outsiders, tile_matches, reverse)
        if not tile:
            return False
        grid[(x, y)] = (tile, tile_matrices[tile])
        outsiders.remove(tile)
        current = tile
    corner = find_adjacent_tile(current, corners, tile_matches, reverse)
    grid[(shape - 1, y)] = (corner, tile_matrices[corner])
    corners.remove(corner)

    return grid


def print_grid(grid):
    shape = int(math.sqrt(len(grid)))
    for tile_y in range(shape):
        for y in range(10):
            for tile_x in range(shape):
                print(''.join(grid[(tile_x, tile_y)][1][y].tolist()), end=' ')
            print('')


def part2():
    tiles = load_tiles('day20_test.txt')
    tile_matches = search_for_matching_edges(tiles)
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    corner_product = np.prod([int(i) for i in corners])
    print(corners)
    assert corner_product == 20899048083289
    print('Matching edges for corners:')
    for c in corners:
        print(f"{c}: {tile_matches[c]}")

    tile_matrices = load_tiles_as_matrices('day20_test.txt')
    for c in set(corners):
        grid = build_tile_grid(c, set(corners - {c}), outsiders, insiders, tile_matrices, tile_matches)
        if grid:
            break
    print_grid(grid)

    tiles = load_tiles('day20.txt')
    tile_matches = search_for_matching_edges(tiles)
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    tile_matrices = load_tiles('day20.txt')
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    # try each fucking corner
    for corner in set(corners):
        # try forward search
        print(f"Trying with corner {corner}")
        grid = build_tile_grid(corner, set(corners - {corner}), outsiders, insiders, tile_matrices, tile_matches)
        if not grid:
            print(f"Trying REVERSED with corner {corner}")
            build_tile_grid(corner, set(corners - {corner}), outsiders, insiders, tile_matrices, tile_matches, True)
        if grid:
            break
    if grid:
        print_grid(grid)
    else:
        print("***Could not build grid***")


# part1()
part2()
