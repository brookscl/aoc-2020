from enum import Enum, auto
import numpy


def load_tickets(file_name):
    class TicketStates(Enum):
        RULES = auto()
        YOUR_TICKET = auto()
        NEARBY_TICKETS = auto()

    read_state = TicketStates.RULES
    with open(f"inputs/{file_name}") as f:
        raw_lines = f.read().strip().split("\n")

    rules = {}
    tickets = []
    for line in [line for line in raw_lines if line.strip() != '']:
        if line == 'your ticket:':
            read_state = TicketStates.YOUR_TICKET
            continue
        elif line == 'nearby tickets:':
            read_state = TicketStates.NEARBY_TICKETS
            continue

        if read_state == TicketStates.RULES:
            parts = line.split(': ')
            rule_name = parts[0]
            r1 = parts[1].split(' or ')[0]
            r2 = parts[1].split(' or ')[1]
            r1 = (int(r1.split('-')[0]), int(r1.split('-')[1]))
            r2 = (int(r2.split('-')[0]), int(r2.split('-')[1]))
            rules[rule_name] = (r1, r2)

        if read_state == TicketStates.YOUR_TICKET:
            my_ticket = [int(v) for v in line.split(',')]

        if read_state == TicketStates.NEARBY_TICKETS:
            values = [int(v) for v in line.split(',')]
            tickets.append(values)

    return rules, tickets, my_ticket


def is_valid(value, rules):
    for rule in rules.values():
        if rule[0][0] <= value <= rule[0][1] or rule[1][0] <= value <= rule[1][1]:
            return True
    return False


def error_rate(rules, tickets):
    errors = []
    for ticket in tickets:
        for value in ticket:
            if not is_valid(value, rules):
                errors.append(value)

    return sum(errors)


r, t, m = load_tickets('day16_test.txt')
e = error_rate(r, t)
assert e == 71

r1, t1, m1 = load_tickets('day16.txt')
e1 = error_rate(r1, t1)
print(f"Part 1: {e1}")
assert e1 == 27850


# Part 2
def matching_rules(value, rules):
    match_set = set()
    for rule_name, rule in rules.items():
        if rule[0][0] <= value <= rule[0][1] or rule[1][0] <= value <= rule[1][1]:
            match_set.add(rule_name)
    return match_set


def search_for_rule_positions(rules, tickets):
    errors = []
    field_matches = []
    for i in range(len(tickets[0])):
        field_matches.append(set(rules.keys()))

    for ticket in tickets:
        for i, value in enumerate(ticket):
            matching_rule_set = matching_rules(value, rules)
            if len(matching_rule_set) > 0:
                field_matches[i] = field_matches[i].intersection(matching_rule_set)

    return field_matches


def calculate_departure_values(ticket, field_matches):
    return numpy.product([ticket[v] for k, v in field_matches.items() if 'departure' in k])


def more_fields(field_matches):
    for f in field_matches:
        if len(f) > 0:
            return True
    return False


def collapse_matches(field_matches):
    field_map = {}
    while more_fields(field_matches):
        for i, m in enumerate(field_matches):
            if len(m) == 1:
                field_name = next(iter(m))
                field_map[field_name] = i
                field_matches = [x - {field_name} for x in field_matches]
                break

    return field_map


matches = search_for_rule_positions(r, t)
print(matches)

matches = search_for_rule_positions(r1, t1)


matches = collapse_matches(matches)
for i, m in enumerate(matches):
    print(f"{i}: {m}")
t = calculate_departure_values(m1, matches)
assert t == 491924517533
print(f"Part 2 answer: {t}")
