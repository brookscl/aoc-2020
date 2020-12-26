def stringify(cup_list):
    s = ""
    for c in cup_list:
        s += str(c)
    return s


def part1():
    test_cups = "389125467"
    final_cups = play_long_game(test_cups, 10, 9)
    assert stringify(final_cups) == "92658374"
    final_cups = play_long_game(test_cups, 100, 9)
    assert stringify(final_cups) == "67384529"

    cups = "467528193"
    final_cups = play_long_game(cups, 100, 9)
    print(f"Part 1: {final_cups}")
    assert stringify(final_cups) == "43769582"


MAX_CUP = 1000000


def mod_decrement(i, max_value):
    if i == 1:
        return max_value
    else:
        return i - 1


def find_target(cups, target):
    for i, c in enumerate(cups):
        if c == target:
            return i
    assert False
    return -1


class Node:
    def __init__(self, label: int) -> None:
        self.label = label
        self.next = None

    def __repr__(self):
        return f"Cup number: {self.label}"


def play_long_game(starting_cups, rounds=10000000, max_value=MAX_CUP):
    starting_cups = [int(cup) for cup in starting_cups]
    cup_index = {i: Node(i) for i in range(1, max_value + 1)}

    for i in range(1, max_value):
        cup_index[i].next = cup_index[i + 1]

    cup_index[max_value].next = cup_index[starting_cups[0]]

    for i in range(len(starting_cups)):
        cup_index[starting_cups[i]].next = cup_index[
            starting_cups[(i + 1) % len(starting_cups)]
        ]

    if max_value > len(starting_cups):
        cup_index[starting_cups[-1]].next = cup_index[len(starting_cups) + 1]

    current_cup = cup_index[starting_cups[0]]
    for r in range(rounds):
        if (r % 1000000) == 0:
            print(f"Starting round {r}")

        picked_up = current_cup.next
        current_cup.next = current_cup.next.next.next.next

        target = mod_decrement(current_cup.label, max_value)
        while target in [
            picked_up.label,
            picked_up.next.label,
            picked_up.next.next.label,
        ]:
            target = mod_decrement(target, max_value)

        insert_point = cup_index[target]
        picked_up.next.next.next = insert_point.next
        insert_point.next = picked_up
        current_cup = current_cup.next

    # Do this to support parts 1 AND 2
    return_list = []
    one_spot = cup_index[1].next
    for i in range(8):
        return_list.append(one_spot.label)
        one_spot = one_spot.next
    return return_list


def part2():
    # Let's experiment to look for patterns
    test_cups = "389125467"
    star_cups = play_long_game(test_cups)
    assert star_cups[0] == 934001 and star_cups[1] == 159792

    cups = "467528193"
    final_cups = play_long_game(cups)
    product = final_cups[0] * final_cups[1]
    print(f"Part 2: {product}")
    assert product == 264692662390


part1()
part2()
