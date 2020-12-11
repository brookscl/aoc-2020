import collections
from itertools import groupby


def process_jolt_file(file_name):
    with open(f"inputs/{file_name}") as f:
        jolt_list = [int(x) for x in f.read().strip().split("\n")]
    jolt_list.sort()
    jolt_list.insert(0, 0)
    jolt_list.append(max(jolt_list) + 3)
    return jolt_list


def process_distributions(jolt_list):
    diff_list = [j-i for i, j in zip(jolt_list[:-1], jolt_list[1:])]
    return collections.Counter(diff_list)


def calculate_hash(dist_map):
    return dist_map[1] * dist_map[3]


jolts_test1 = process_jolt_file('day10_test1.txt')
jolt_distributions = process_distributions(jolts_test1)
test_answer = calculate_hash(jolt_distributions)
assert test_answer == 35

jolts_test2 = process_jolt_file('day10_test2.txt')
jolt_distributions = process_distributions(jolts_test2)
test_answer = calculate_hash(jolt_distributions)
assert test_answer == 220

real_jolts = process_jolt_file('day10.txt')
jolt_distributions = process_distributions(real_jolts)
real_answer = calculate_hash(jolt_distributions)
print(f"Part 1 answer: {real_answer}")
assert real_answer == 2040


# (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
def count_arrangements_recursive(jolt_list):
    if (len(jolt_list) > 2) and (jolt_list[2] - jolt_list[0]) > 3:
        return count_arrangements_recursive(jolt_list[1:])
    elif (len(jolt_list) > 3) and (jolt_list[3] - jolt_list[0]) > 3:
        return 1 + count_arrangements_recursive(jolt_list[1:]) + \
               count_arrangements_recursive(jolt_list[2:])
    elif len(jolt_list) > 4:
        return 2 + count_arrangements_recursive(jolt_list[1:]) + \
               count_arrangements_recursive(jolt_list[2:]) + \
               count_arrangements_recursive(jolt_list[3:])
    return 0


def count_arrangements_iterative(jolt_list):
    diffs = [jolt_list[n]-jolt_list[n-1] for n in range(1, len(jolt_list))]
    count_runs_of_1 = [sum(1 for _ in group) for x, group in groupby(diffs) if x == 1]
    count_runs_of_1 = [x for x in count_runs_of_1 if x > 1]
    count_runs_of_1.sort()
    counts = [len(list(group)) for key, group in groupby(count_runs_of_1)]
    counts.extend([0, 0, 0])
    return 2**counts[0] * 4**counts[1] * 7**counts[2]


t1 = count_arrangements_recursive(jolts_test1) + 1
t11 = count_arrangements_iterative(jolts_test1)
assert t1 == t11 == 8

t2 = count_arrangements_recursive(jolts_test2) + 1
t22 = count_arrangements_iterative(jolts_test2)
assert t2 == t22 == 19208

t3 = count_arrangements_iterative(real_jolts)
print(f"Part 2 arrangements: {t3}")
assert t3 == 28346956187648
