from blist import blist


def play_game(cups, rounds):
    for r in range(rounds):
        current_cup = cups[0]
        picked_up = cups[1:4]
        cups = cups[0] + cups[4:]
        target = int(current_cup)
        placed = False
        while not placed:
            if target == 1:
                target = 9
            else:
                target -= 1
            if str(target) in cups:
                insert_spot = cups.index(str(target))
                cups = cups[0:insert_spot+1] + picked_up + cups[insert_spot+1:]
                placed = True

        # rotate the cups to put next target at zero position
        cups = cups[1:] + cups[0]

    # now rotate to the 1 spot and eliminate 1
    one_spot = cups.index('1')
    return cups[one_spot + 1:] + cups[0:one_spot]


def stringify(cup_list):
    s = ''
    for c in cup_list:
        s += str(c)
    return s

def part1():
    test_cups = '389125467'
    final_cups = play_long_game(test_cups, 10, 9)
    assert stringify(final_cups) == '92658374'
    final_cups = play_game(test_cups, 100)
    assert stringify(final_cups) == '67384529'

    cups = '467528193'
    final_cups = play_game(cups, 100)
    print(f"Part 1: {final_cups}")
    assert stringify(final_cups) == '43769582'


MAX_CUP = 1000000


def play_long_game(starting_cups, rounds=10000000, max=MAX_CUP):
    cups = blist([i for i in range(1, max + 1)])
    for i, cup in enumerate(starting_cups):
        cups[i] = int(cup)

    for r in range(rounds):
        if (r % 100) == 0:
            print(f"Starting round {r}")

        current_cup = cups[0]
        picked_up = cups[1:4]
        target = current_cup
        placed = False
        insert_spot = -1
        while not placed:
            if target == 1:
                target = MAX_CUP
            else:
                target -= 1
            if target in cups[4:]:
                insert_spot = cups.index(target)
                # cups = blist(cups[0:insert_spot+1] + picked_up + cups[insert_spot+1:])
                placed = True

        # rotate the cups to put next target at zero position
        for cup in reversed(picked_up):
            cups.insert(insert_spot + 1, cup)
        # cups.insert(insert_spot + 1, list(picked_up))
        cups.append(cups[0])
        del cups[0:4]

    # now rotate to the 1 spot and eliminate 1
    one_spot = cups.index(1)
    return cups[one_spot + 1:] + cups[0:one_spot]

    # return cups[one_spot + 1:2]


def part2():
    test_cups = '389125467'
    star_cups = play_long_game(test_cups)
    assert star_cups[0] == 934001 and star_cups[1] == 159792
    # assert final_cups == '92658374'


part1()
part2()
