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
            if forward_matches or backward_matches:
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
        neighbors = len(match_data)
        if neighbors == 2:
            corners.add(num)
        elif neighbors == 3:
            outsiders.add(num)
        elif neighbors == 4:
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


def find_adjacent_tile(tile, search_set, tile_matches):
    matches = tile_matches[tile]
    matching_edges = find_adjacent(matches, search_set)

    return next(iter(matching_edges)) if matching_edges else None


def find_adjacent(matches, search_set):
    matching_edges = set()
    for direction, match in matches.items():
        # This is also where we'll find the required rotation and flipping
        # match_list[i] = (forward_matches, backward_matches)
        search_list = match[0] + match[1]
        for edge in search_list:
            if edge[0] in search_set:
                matching_edges.add(edge[0])
                # Will need to rotate based on i
    return matching_edges


# Should be two consecutive sides matching, and we want the corresponding
# matrix to be aligned along 1,2 direction (east and south) for first upper-left
# corner
def orient_first_corner(corner, tile_matrices, tile_matches):
    matches = tile_matches[corner]
    if (0 in matches) and (1 in matches):
        tile_matrices[corner] = np.rot90(tile_matrices[corner], axes=(1,0))
    elif (2 in matches) and (3 in matches):
        tile_matrices[corner] = np.rot90(tile_matrices[corner])
    elif (0 in matches) and (4 in matches):
        tile_matrices[corner] = np.rot90(tile_matrices[corner])
        tile_matrices[corner] = np.rot90(tile_matrices[corner])
    return


def build_outer_tile_grid(corners, outsiders, tile_matrices, tile_matches):
    shape = int(math.sqrt(len(tile_matrices)))
    grid = {}
    current = next(iter(corners))
    corners.remove(current)
    orient_first_corner(current, tile_matrices, tile_matches)
    x, y = 0, 0
    grid[(x, y)] = (current, tile_matrices[current])
    for j in range(4):
        for k in range(shape - 1):
            if j == 0:
                x += 1
            elif j == 1:
                y += 1
            elif j == 2:
                x -= 1
            else:
                y -= 1
            set_to_search = outsiders
            if k == shape - 2:
                if not corners:
                    break
                set_to_search = corners
            tile = find_adjacent_tile(current, set_to_search, tile_matches)
            if not tile:
                print(f"Failed to find outside tile in {set_to_search}")
                return False
            orient_to_adjacent(tile, current, tile_matrices, tile_matches)
            grid[(x, y)] = (tile, tile_matrices[tile])
            set_to_search.remove(tile)
            current = tile

    return grid


def build_inner_tile_grid(grid, insiders, tile_matrices, tile_matches):
    shape = int(math.sqrt(len(tile_matrices)))
    for y in range(1, shape - 1):
        current = grid[(1, y - 1)][0]
        for x in range(1, shape - 1):
            tile = find_adjacent_tile(current, insiders, tile_matches)
            if not tile:
                print(f"Failed to find inside tile in {insiders}")
                return False
            grid[(x, y)] = (tile, tile_matrices[tile])
            insiders.remove(tile)
            current = grid[(x + 1, y - 1)][0]

    return grid


def print_grid(grid):
    shape = int(math.sqrt(len(grid)))
    for tile_y in range(shape):
        for y in range(10):
            for tile_x in range(shape):
                print(''.join(grid[(tile_x, tile_y)][1][y].tolist()), end=' ')
            print('')
        print('')


def part2():
    tiles = load_tiles('day20_test.txt')
    tile_matches = search_for_matching_edges(tiles)
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    corner_product = np.prod([int(i) for i in corners])
    print(corners)
    assert corner_product == 20899048083289

    tile_matrices = load_tiles_as_matrices('day20_test.txt')
    grid = build_outer_tile_grid(corners, outsiders, tile_matrices, tile_matches)
    grid = build_inner_tile_grid(grid, insiders, tile_matrices, tile_matches)
    print_grid(grid)

    tiles = load_tiles('day20.txt')
    tile_matches = search_for_matching_edges(tiles)
    tile_matrices = load_tiles('day20.txt')
    corners, outsiders, insiders = find_tile_positions(tile_matches)
    grid = build_outer_tile_grid(corners, outsiders, tile_matrices, tile_matches)
    grid = build_inner_tile_grid(grid, insiders, tile_matrices, tile_matches)
    # print_grid(grid)



# part1()
part2()
