def load_rules(file_name):
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")

    reading_rules = True
    rule_dict = {}
    test_patterns = []
    for line in raw_lines:
        if line.strip() == "":
            reading_rules = False
            continue

        if reading_rules:
            rule_number, rule_list = line.split(": ")
            if '"' in rule_list:
                rule_dict[rule_number] = rule_list[1]
            elif "|" in rule_list:
                left, right = rule_list.split(" | ")
                left = left.split(" ")
                right = right.split(" ")
                rule_dict[rule_number] = [left, right]
            else:
                rule_dict[rule_number] = [rule_list.split(" ")]
        else:
            test_patterns.append(line)

    return rule_dict, test_patterns


def valid_rule(pattern, rule_seq, rule_dict):
    if pattern == '' or rule_seq == []:
        return pattern == '' and rule_seq == []
    r = rule_dict[rule_seq[0]]
    if isinstance(r, str):
        if pattern[0] == r:
            return valid_rule(pattern[1:], rule_seq[1:], rule_dict)
    else:
        return any(valid_rule(pattern, t + rule_seq[1:], rule_dict) for t in r)


def valid(pattern, rule_dict):
    return valid_rule(pattern, ['0'], rule_dict)


def count_matches(rule_dict, test_patterns):
    return sum(1 for p in test_patterns if valid(p, rule_dict))


assert valid("a", {"0": "a"})
assert valid("b", {"0": "b"})
assert not valid("b", {"0": "a"})
assert not valid("ab", {"0": "a"})
assert valid("ab", {"0": [["1", "2"]], "1": "a", "2": "b"})

rules, patterns = load_rules("day19_test1.txt")
print(rules)
m = count_matches(rules, patterns)
assert m == 2

rules, patterns = load_rules("day19_test2.txt")
print(rules)
m = count_matches(rules, patterns)
assert m == 2

rules, patterns = load_rules("day19.txt")

m = count_matches(rules, patterns)
print(f"Part 1 matches: {m}")
assert m == 176


rules, patterns = load_rules("day19.txt")
rules['8'] = (['42'], ['42', '8'])
rules['11'] = (['42', '31'], ['42', '11', '31'])
m = count_matches(rules, patterns)
print(f"Part 2 matches: {m}")
assert m == 352
