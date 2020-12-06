# Part 1
def process_q_file(file_name):
    q_list = []
    with open(f"inputs/{file_name}") as f:
        q_list = f.read().strip().split("\n\n")
    return q_list


def num_yes(q_list):
    return sum(len(set(q.replace("\n", ""))) for q in q_list)


questions = process_q_file("day06_test.txt")
num = num_yes(questions)
print(f"Part 1 test sum: {num}")
assert num == 11


questions = process_q_file("day06_input.txt")
num = num_yes(questions)
print(f"Part 1 actual sum: {num}")
assert num == 6903


# Part 2
def num_all_yes(q_list):
    count = 0
    for q in q_list:
        set_list = [set(r) for r in q.split("\n")]
        count += len(set.intersection(*set_list))
    return count


questions = process_q_file("day06_test.txt")
num = num_all_yes(questions)
print(f"Part 2 test sum: {num}")
assert num == 6

questions = process_q_file("day06_input.txt")
num = num_all_yes(questions)
print(f"Part 2 actual sum: {num}")
assert num == 3493
