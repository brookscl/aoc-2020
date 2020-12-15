import copy


def play_game(numbers, rounds):
    generated = copy.deepcopy(numbers)
    for i in range(len(numbers), rounds):
        if (i % 10000) == 0:
            print(f"Iteration {i}")

        new = 0
        prior = generated[i-1]
        try:
            last_occurrence_pos = len(generated) - 2 - generated[len(generated)-2::-1].index(prior)
            new = i - last_occurrence_pos - 1
        except ValueError:
            new = 0
        generated.append(new)
    return generated[-1]


def play_game_smart(numbers, rounds):
    history = {}

    for i, n in enumerate(numbers):
        history[n] = (-1, i)

    prior = numbers[-1]
    for i in range(len(numbers), rounds):
        # if (i % 100000) == 0:
        #     print(f"Iteration {i}")

        new_value = 0
        h = history[prior]
        if h[0] == -1:  # First time
            new_value = 0
        else:
            new_value = i - h[0] - 1

        if new_value in history:
            history[new_value] = (history[new_value][1], i)
        else:
            history[new_value] = (-1, i)
        prior = new_value

    return prior


test1 = "0,3,6"
test1 = [int(i) for i in test1.split(",")]

assert play_game(test1, 4) == 0
assert play_game(test1, 5) == 3
assert play_game(test1, 9) == 4
assert play_game(test1, 2020) == 436

real = [9,3,1,0,8,4]
result = play_game(real, 2020)
print(f"Part 1 result: {result}")
assert result == 371

assert play_game_smart(test1, 4) == 0
assert play_game_smart(test1, 5) == 3
assert play_game_smart(test1, 9) == 4
assert play_game_smart(real, 2020) == 371

result = play_game_smart(real, 30000000)
print(f"Part 2 result: {result}")
assert result == 352
