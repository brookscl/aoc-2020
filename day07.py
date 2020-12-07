import re


# Part 1
def process_bag_rule_file(file_name):
    rule_list = []
    with open(f"inputs/{file_name}") as f:
        rule_list = f.read().strip().split("\n")
    return rule_list


def build_bag_rules(rule_list):
    bag_rules = {}
    for r in rule_list:
        dependents = {}
        leftright = r.split('s contain ')
        bag = leftright[0]
        right = leftright[1][:-1]
        if right != "no other bags":
            sub_bags = right.split(',')
            for b in sub_bags:
                r = r"^ *(\d) ([\w ].*?)s*$"
                g = re.search(r, b)
                dependents[g.group(2)] = int(g.group(1))
        bag_rules[bag] = dependents
    return bag_rules


def build_contain_set(looking_for, bags, found_set):
    for bag, contains in bags.items():
        if looking_for in contains:
            found_set.add(bag)


def find_eventually_contains_set(looking_for, bags, found_set):
    search_stack = [looking_for]
    while search_stack:
        newly_found = set()
        search_bag = search_stack.pop()
        build_contain_set(search_bag, bags, newly_found)
        if found_set.union(newly_found) != found_set:
            for b in newly_found:
                search_stack.append(b)
                found_set.add(b)


# {bag} contain {n} {bag}(s), etc.
rules = process_bag_rule_file('day07_test.txt')
test_bag_map = build_bag_rules(rules)
bags_that_contain = set()
find_eventually_contains_set('shiny gold bag', test_bag_map, bags_that_contain)

assert len(bags_that_contain) == 4
rules = process_bag_rule_file('day07_input.txt')
bag_map = build_bag_rules(rules)
bags_that_contain = set()
find_eventually_contains_set('shiny gold bag', bag_map, bags_that_contain)
print(f"Part 1 answer: {len(bags_that_contain)}")
assert len(bags_that_contain) == 229


# Part 2
def calculate_bag_count(looking_for, bags):
    total = 0
    contained = bags[looking_for]
    for bag, bag_count in contained.items():
        total += bag_count + bag_count * calculate_bag_count(bag, bags)
    return total


count = calculate_bag_count('shiny gold bag', test_bag_map)
assert count == 32

count = calculate_bag_count('shiny gold bag', bag_map)
print(f"Part 2 answer: {count}")
assert count == 6683
