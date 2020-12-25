def transform(subject, target=None, loop_count=100000000):
    loops = 0
    current = 1
    while loops < loop_count:
        loops += 1
        current = current * subject
        current = current % 20201227
        if target and current == target:
            return loops, current
    return loops, current

def part1():
    card_public_key = 5764801
    door_public_key = 17807724
    initial_subject = 7

    card_loop_size, _ = transform(initial_subject, card_public_key)
    assert card_loop_size == 8
    door_loop_size, _ = transform(initial_subject, door_public_key)
    assert door_loop_size == 11

    _, key1 = transform(door_public_key, None, card_loop_size)
    _, key2 = transform(card_public_key, None, door_loop_size)
    assert key1 == key2 == 14897079

    cpk = 9789649
    dpk = 3647239
    card_loop_size, _ = transform(initial_subject, cpk)
    door_loop_size, _ = transform(initial_subject, dpk)
    _, key1 = transform(dpk, None, card_loop_size)
    _, key2 = transform(cpk, None, door_loop_size)
    print(f"Part 1 keys should be: {key1}, {key2}")


part1()
