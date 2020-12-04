import re


def process_passport_file(file_name):
    passport_list = []
    with open(f"inputs/{file_name}") as f:
        read_data = f.read().strip()

    read_data = read_data.replace("\n\n", " | ")
    read_data = read_data.replace("\n", " ")
    raw_list = read_data.split(" | ")
    for p in raw_list:
        passport_list.append(dict(field.split(':') for field in p.split(" ")))
    return passport_list


def valid_passports(passport_list, validator):
    return sum(1 for p in passport_list if validator(p))


def is_valid_fieldset(passport):
    golden_passport = {
        'ecl': None,
        'pid': None,
        'eyr': None,
        'hcl': None,
        'byr': None,
        'iyr': None,
        'hgt': None
    }

    return len(passport.keys() & golden_passport.keys()) == 7


passports = process_passport_file('day04_test.txt')
assert valid_passports(passports, is_valid_fieldset) == 2


passports = process_passport_file('day04_input.txt')
valid = valid_passports(passports, is_valid_fieldset)
print(f"Part 1 valid passports: {valid}")
assert valid == 242


# Part 2
# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.
def is_valid_field(field):
    f, v = field[0], field[1]
    if f == 'byr':
        return 1920 <= int(v) <= 2002
    elif f == 'iyr':
        return 2010 <= int(v) <= 2020
    elif f == 'eyr':
        return 2020 <= int(v) <= 2030
    elif f == 'hgt':
        cm = re.search(r'(\d+)cm', v)
        if cm:
            return 150 <= int(cm.group(1)) <= 193
        inches = re.search(r'(\d+)in', v)
        if inches:
            return 59 <= int(inches.group(1)) <= 76
        return False
    elif f == 'hcl':
        return re.search(r'^#(?:[0-9a-f]{3}){1,2}$', v)
    elif f == 'ecl':
        return v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    elif f == 'pid':
        return re.search(r'^[0-9]{9}$', v)
    return True


def is_fully_valid(passport):
    return is_valid_fieldset(passport) \
           and all(is_valid_field(f) for f in passport.items())


valid = valid_passports(passports, is_fully_valid)
print(f"Part 2 valid passports: {valid}")
assert valid == 186
