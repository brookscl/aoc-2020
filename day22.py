from collections import deque


def build_hand(card_list):
    return deque([int(c) for c in card_list])


def load_hands(file_name):
    with open(f"inputs/{file_name}") as f:
        hands = f.read().strip().split("\n\n")

    p1 = build_hand(hands[0].split("\n")[1:])
    p2 = build_hand(hands[1].split("\n")[1:])
    return p1, p2


def play_the_game(p1, p2):
    while p1 and p2:
        p1_card = p1.popleft()
        p2_card = p2.popleft()
        if p1_card > p2_card:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    return p1 if p1 else p2


def calculate_final_score(final_hand):
    final_hand.reverse()
    return sum([(i+1) * c for i, c in enumerate(final_hand)])


def part1():
    p1, p2 = load_hands('day22_test.txt')
    final_hand = play_the_game(p1, p2)
    score = calculate_final_score(final_hand)
    assert score == 306

    p1, p2 = load_hands('day22.txt')
    final_hand = play_the_game(p1, p2)
    score = calculate_final_score(final_hand)
    print(f"Part 1 score: {score}")
    assert score == 32489


def play_the_recursive_game(p1, p2):
    played_hands = set()
    while p1 and p2:
        hand_hash = f"p1: {list(p1)}, p2: {list(p2)}"
        if hand_hash in played_hands:
            return p1, True

        played_hands.add(hand_hash)
        p1_card = p1.popleft()
        p2_card = p2.popleft()
        if p1_card <= len(p1) and p2_card <= len(p2):
            sub_p1 = deque(list(p1)[:p1_card])
            sub_p2 = deque(list(p2)[:p2_card])
            hand, p1_wins = play_the_recursive_game(sub_p1, sub_p2)
        else:
            p1_wins = p1_card > p2_card

        if p1_wins:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])

    if p1:
        return p1, True
    else:
        return p2, False


def part2():
    p1, p2 = load_hands('day22_test.txt')
    final_hand, p1_wins = play_the_recursive_game(p1, p2)
    score = calculate_final_score(final_hand)
    assert score == 291

    # Infinite test
    p1 = deque([43, 19])
    p2 = deque([2, 29, 14])
    final_hand, p1_wins = play_the_recursive_game(p1, p2)
    score = calculate_final_score(final_hand)

    p1, p2 = load_hands('day22.txt')
    final_hand, p1_wins = play_the_recursive_game(p1, p2)
    score = calculate_final_score(final_hand)
    print(f"Part 2 score: {score}")


part1()
part2()
